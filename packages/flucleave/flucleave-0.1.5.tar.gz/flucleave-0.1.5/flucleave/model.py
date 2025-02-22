#!/usr/bin/env python

import tensorflow as tf
from tensorflow.keras.layers import (
    Input, Conv1D, Dense, Dropout, Embedding, BatchNormalization
)
from tensorflow.keras.models import Model
from typing import Union
from .config import *


def build_model() -> tf.keras.Model:
    """Builds and compiles a CNN model for analyzing amino acid cleavage sites.
    
    The model performs the following analysis steps:
    1. Takes a sequence of 6 amino acids as input
    2. Converts each amino acid into a learned vector representation
    3. Analyzes pairs of amino acids for local patterns
    4. Captures the strongest patterns across the sequence
    5. Makes a binary classification (HPAI vs LPAI)
    
    Architecture Details:
        - Input: 6 amino acids (encoded as integers 0-20)
        - Embedding: Converts each AA to {EMBEDDING_DIM}-dimensional vector
        - Conv1D: Analyzes pairs of AAs with 64 different pattern detectors
        - Global Pooling: Captures strongest pattern activations
        - Dense: Final classification layers
    
    Returns:
        tf.keras.Model: Compiled model ready for training
        
    Model Params:
        Input shape: (None, 6) - Batch of 6-AA sequences
        Output shape: (None, 1) - Binary classification (0=LPAI, 1=HPAI)
    """
    # Input layer - accepts sequence of 6 amino acids
    # Each AA is encoded as integer 0-20 (20 standard AAs + padding)
    inputs = Input(shape=(AA_WINDOW_SIZE,))

    # Embedding layer - learns vector representation for each amino acid
    # Vector captures chemical/physical properties through training
    # L1 regularization prevents overspecialization
    x = Embedding(
        input_dim=21,  # 20 AAs + padding token
        output_dim=EMBEDDING_DIM,
        activity_regularizer=tf.keras.regularizers.l1(0.005)
    )(inputs)

    # CNN layer - analyzes local patterns in AA pairs
    # Kernel size 2 means it looks at adjacent AAs:
    # [P1-P2], [P2-P3], [P3-P4], [P4-P5], [P5-P6]
    # 64 filters learn different pattern types (hydrophobic, charged, etc)
    x = Conv1D(
        filters=64,
        kernel_size=2,
        activation='relu',
        padding='same',
        kernel_regularizer=tf.keras.regularizers.l2(0.001)
    )(x)

    # Global max pooling - captures strongest pattern activations
    # For each filter, keeps the highest activation across positions
    # Shows where the most important patterns were found
    x = tf.reduce_max(x, axis=1)

    # Dense layer - combines pattern information
    # Reduces 64 pattern detections to 16 higher-level features
    x = Dense(
        units=16,
        activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(0.001)
    )(x)
    x = Dropout(DROPOUT_RATE)(x)

    # Output layer - final pathogenicity prediction
    # Sigmoid activation for binary classification
    outputs = Dense(units=1, activation='sigmoid')(x)

    # Construct and compile model
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='binary_crossentropy',
        metrics=[
            'accuracy',
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )

    return model