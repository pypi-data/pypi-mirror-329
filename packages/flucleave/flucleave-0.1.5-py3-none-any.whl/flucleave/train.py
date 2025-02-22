#!/usr/bin/env python

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from pathlib import Path
from typing import Tuple, Dict, Any
from .model import build_model
from .config import *
from .utils import encode_sequences

def load_data(training_csv: str) -> Tuple[np.ndarray, np.ndarray]:
    """Load and prepare training data from CSV.
    
    Args:
        training_csv: Path to CSV containing cleavage sites and labels
        
    Returns:
        tuple: (sequences, labels) where:
            sequences: Array of 6-AA cleavage site windows
            labels: Binary labels (0=LP, 1=HP)
    """
    # Load training data
    data = pd.read_csv(training_csv)
    
    # Extract features and labels
    sequences = data['cleavage_site'].values
    labels = data['label'].values
    
    print(f"Loaded {len(sequences)} sequences for training")
    return sequences, labels

def calculate_class_weights(labels: np.ndarray) -> Dict[int, float]:
    """Calculate balanced class weights for uneven datasets.
    
    Args:
        labels: Binary label array (0=LP, 1=HP)
        
    Returns:
        dict: Class weights {0: weight_lp, 1: weight_hp}
    """
    hp_count = np.sum(labels)
    lp_count = len(labels) - hp_count
    total = hp_count + lp_count
    
    return {
        0: total / (2 * lp_count),  # Weight for LP class
        1: total / (2 * hp_count)   # Weight for HP class
    }

def train_model(training_csv: str = None, model_output: str = None, force: bool = False) -> Dict[str, Any]:
    """Train CNN model for cleavage site pathogenicity prediction."""
    if not training_csv:
        training_csv = str(TRAINING_CSV)  # Convert Path to string
    if not model_output:
        model_output = str(Path(MODEL_DIR) / 'final_model.h5')  # Convert Path to string

    """Train CNN model for cleavage site pathogenicity prediction.
    
    Steps:
    1. Load and prepare sequence data
    2. Calculate balanced class weights
    3. Split into train/validation sets
    4. Build and train CNN model
    5. Save trained model and logs
    
    Args:
        training_csv: Path to training data CSV
        model_output: Path to save trained model
        
    Returns:
        dict: Training history
    """
    # Clean up old model files
    model_dir = Path(MODEL_DIR)
    existing_files = list(model_dir.glob('*.h5')) + list(model_dir.glob('*.csv'))

    if existing_files and not force:
        print("\nFound existing model files:")
        for file in existing_files:
            print(f"- {file.name}")
        print("\nUse --force to overwrite existing files")
        sys.exit(1)
            
    # Delete files if forced
    if existing_files and force:
        for file in existing_files:
            file.unlink()
            print(f"Deleted: {file.name}")

    # Load and prepare data
    sequences, labels = load_data(training_csv)
    sequences_encoded = encode_sequences(sequences)
    
    # Calculate balanced class weights
    class_weights = calculate_class_weights(labels)
    print(f"Class weights: LP={class_weights[0]:.2f}, HP={class_weights[1]:.2f}")

    # Split into train/validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        sequences_encoded, labels,
        test_size=0.2,          # 80% train, 20% validation
        random_state=42,        # For reproducibility
        stratify=labels         # Maintain class distribution
    )

    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    # Build model
    model = build_model()

    # Setup training callbacks with enhanced early stopping
    callbacks = [
        # Early stopping with more sophisticated monitoring
        tf.keras.callbacks.EarlyStopping(
            monitor=MONITOR_METRIC,
            mode=MONITOR_MODE,
            patience=PATIENCE,
            min_delta=MIN_DELTA,
            restore_best_weights=RESTORE_BEST_WEIGHTS,
            verbose=1
        ),
        # Model checkpoint aligned with early stopping
        tf.keras.callbacks.ModelCheckpoint(
            str(model_dir / 'best_model.h5'),
            monitor=MONITOR_METRIC,
            mode=MONITOR_MODE,
            save_best_only=True,
            verbose=1
        ),
        # Training history logger
        tf.keras.callbacks.CSVLogger(
            str(model_dir / 'training_log.csv')
        ),
        # Adaptive learning rate reduction
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor=MONITOR_METRIC,
            mode=MONITOR_MODE,
            factor=0.5,
            patience=PATIENCE // 2,  # More aggressive than early stopping
            min_delta=MIN_DELTA,
            min_lr=1e-6,
            verbose=1
        ),
        # Custom callback to monitor overfitting
        OverfittingMonitor(
            threshold=0.1,  # Maximum allowed gap between train and val metrics
            patience=5      # Number of epochs to wait before warning
        )
    ]

    # Add channel dimension for CNN if needed
    if len(X_train.shape) < 3:
        X_train = np.expand_dims(X_train, axis=-1)
        X_val = np.expand_dims(X_val, axis=-1)

    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        class_weight=class_weights,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    # Save final model state
    model.save(str(Path(model_output)))  # Convert Path to string

    return history.history

class OverfittingMonitor(tf.keras.callbacks.Callback):
    """Custom callback to monitor and warn about overfitting."""
    
    def __init__(self, threshold: float = 0.1, patience: int = 5):
        super().__init__()
        self.threshold = threshold
        self.patience = patience
        self.overfitting_count = 0
        
    def on_epoch_end(self, epoch: int, logs: Dict[str, float] = None):
        if logs is None:
            return
            
        # Calculate gap between training and validation metrics
        acc_gap = abs(logs.get('accuracy', 0) - logs.get('val_accuracy', 0))
        loss_gap = abs(logs.get('loss', 0) - logs.get('val_loss', 0))
        
        if acc_gap > self.threshold or loss_gap > self.threshold:
            self.overfitting_count += 1
            if self.overfitting_count >= self.patience:
                print(f'\nWarning: Potential overfitting detected (epoch {epoch})')
                print(f'Training-validation gaps: accuracy={acc_gap:.3f}, loss={loss_gap:.3f}')
        else:
            self.overfitting_count = 0

if __name__ == "__main__":
    history = train_model(
        training_csv=TRAINING_CSV,
        model_output=os.path.join(MODEL_DIR, 'final_model.h5')
    )
    
    print("\nTraining completed!")
    print(f"Final training accuracy: {history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history['val_accuracy'][-1]:.4f}")