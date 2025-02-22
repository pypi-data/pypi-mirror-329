#!/usr/bin/env python

import os
from pathlib import Path

# Package root directory
PACKAGE_ROOT = Path(__file__).resolve().parents[1]

# Data directories
DATA_DIR = PACKAGE_ROOT / 'flucleave/data'
TRAIN_DIR = DATA_DIR / 'train'
TEST_DIR = DATA_DIR / 'test'

MODEL_DIR = PACKAGE_ROOT / 'flucleave/model'


# Model Architecture Parameters
# ---------------------------
# Size of input sequence window
AA_WINDOW_SIZE = 6  # Number of amino acids to analyze

# Training Parameters
# -----------------
BATCH_SIZE = 32     # Number of samples per training batch
EPOCHS = 150        # Maximum number of training epochs
LEARNING_RATE = 0.0005  # Initial learning rate
PATIENCE = 15       # Number of epochs to wait before early stopping

# Early Stopping Parameters
# -----------------------
MIN_DELTA = 0.001         # Minimum change to qualify as an improvement
RESTORE_BEST_WEIGHTS = True  # Restore model to best weights after stopping

# Validation Monitoring
MONITOR_METRIC = 'val_loss'  # Metric to monitor for early stopping
MONITOR_MODE = 'min'         # Whether to minimize or maximize the metric

# Model Layer Parameters
# --------------------
CNN_FILTERS = 64    # Number of pattern detectors in Conv1D layer
EMBEDDING_DIM = 32  # Size of amino acid embedding vectors
DROPOUT_RATE = 0.3  # Fraction of neurons to drop during training

# Default paths
DEFAULT_MODEL = MODEL_DIR / 'best_model.h5'
TRAINING_CSV = TRAIN_DIR / 'training_data.csv'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging