#!/usr/bin/env python

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
import numpy as np
import tensorflow as tf
from Bio.Seq import Seq
from .predict import predict_pathogenicity
from .utils import load_sequences, find_cleavage_site

@pytest.fixture
def sample_fasta():
    """Create a temporary FASTA file with test sequences."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.fasta') as f:
        f.write(">seq1 HPAI\n")
        f.write("MNTQILVFALVAIIPTNADKICLGHHAVAN\n")
        f.write(">seq2 LPAI\n")
        f.write("MEKFILFALIVVLPSQADGLCIGYHANNST\n")
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def mock_model():
    """Create a mock TensorFlow model."""
    model = Mock()
    model.predict.return_value = np.array([[0.8], [0.2]])
    return model

def test_load_sequences(sample_fasta):
    """Test loading sequences from FASTA file."""
    sequences = load_sequences(sample_fasta)
    assert len(sequences) > 0
    assert all(isinstance(seq_id, str) and isinstance(seq, str) 
              for seq_id, seq in sequences)

def test_find_cleavage_site():
    """Test cleavage site detection."""
    # Test protein sequence
    protein = "PEPTIDEGLFGAIAPEPTIDE"
    window, pos = find_cleavage_site(protein)
    assert window is not None
    assert len(window) == 6
    
    # Test DNA sequence
    dna = "CCGGAGCCGCTGTTCGGCGCCATCGCGCCG"
    window, pos = find_cleavage_site(dna)
    assert window is not None
    assert len(window) == 6

@patch('tensorflow.keras.models.load_model')
def test_predict_pathogenicity(mock_load_model, sample_fasta, mock_model, tmp_path):
    """Test full prediction pipeline."""
    mock_load_model.return_value = mock_model
    
    # Run predictions
    results = predict_pathogenicity(sample_fasta, str(tmp_path))
    
    # Check results
    assert len(results) == 2  # Two sequences from sample data
    assert all(isinstance(r, dict) for r in results)
    assert all(k in r for r in results 
              for k in ['sequence_id', 'prediction', 'confidence', 'score'])
    
    # Check output file
    output_files = list(tmp_path.glob('*_flucleave_out.csv'))
    assert len(output_files) == 1
    assert output_files[0].is_file()

def test_invalid_input():
    """Test handling of invalid inputs."""
    with pytest.raises(FileNotFoundError):
        predict_pathogenicity('nonexistent.fasta', 'output')

def test_empty_fasta(tmp_path):
    """Test handling of empty FASTA file."""
    # Create empty FASTA
    empty_fasta = tmp_path / "empty.fasta"
    empty_fasta.touch()
    
    results = predict_pathogenicity(str(empty_fasta), str(tmp_path))
    assert len(results) == 0

def test_malformed_sequence(tmp_path):
    """Test handling of malformed sequences."""
    # Create FASTA with invalid sequence
    bad_fasta = tmp_path / "bad.fasta"
    with open(bad_fasta, 'w') as f:
        f.write(">bad_seq\n")
        f.write("INVALID123SEQUENCE\n")
    
    results = predict_pathogenicity(str(bad_fasta), str(tmp_path))
    assert len(results) == 0

if __name__ == '__main__':
    pytest.main([__file__])
