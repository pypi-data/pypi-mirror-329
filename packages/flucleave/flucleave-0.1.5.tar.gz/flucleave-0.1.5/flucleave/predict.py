#!/usr/bin/env python

import argparse
import os
import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import List, Dict, Any
from .utils import load_sequences, encode_sequences
from .config import *
import csv


def predict_pathogenicity(fasta_file: str, output_dir: str, prefix: str = None) -> List[Dict[str, Any]]:
    """Predict pathogenicity of HA cleavage sites from sequences."""
    # Validate input file
    if not os.path.exists(fasta_file):
        raise FileNotFoundError(f"Input FASTA file not found: {fasta_file}")
    
    if os.path.getsize(fasta_file) == 0:
        print(f"Warning: Empty FASTA file: {fasta_file}")
        return []
        
    # Setup output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load and extract cleavage site windows
    try:
        sequences = load_sequences(fasta_file)
    except Exception as e:
        print(f"Error loading sequences: {e}")
        return []

    if not sequences:
        print(f"No valid cleavage sites found in {fasta_file}")
        return []

    # Split sequence tuples into separate lists
    seq_data = [seq for _, seq in sequences]
    seq_ids = [id for id, _ in sequences]

    # Load model and make predictions
    try:
        X = encode_sequences(seq_data)
        
        model_path = os.path.join(MODEL_DIR, 'best_model.h5')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        model = tf.keras.models.load_model(model_path)
        predictions = model.predict(X)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return []

    # Format results
    results = []
    for seq_id, pred in zip(seq_ids, predictions):
        try:
            label = "HIGH PATHOGENICITY" if pred[0] > 0.5 else "LOW PATHOGENICITY"
            confidence = pred[0] if pred[0] > 0.5 else 1 - pred[0]
            
            result = {
                'filename': Path(fasta_file).name,
                'sequence_id': seq_id,
                'prediction': label,
                'confidence': float(confidence),
                'score': float(pred[0])
            }
            results.append(result)
            
            print(f"\nFasta: {result['filename']}")
            print(f"Sequence: {result['sequence_id']}")
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Raw Score: {result['score']:.2f}")
        except Exception as e:
            print(f"Error processing prediction for {seq_id}: {e}")
            continue

    # Write results to CSV file
    if results:
        try:
            if not prefix:
                out_path = Path(output_dir) / "flucleave_out.csv"
            else:
                out_path = Path(output_dir) / f"{prefix}_flucleave_out.csv"
            with open(out_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            print(f"\nResults written to: {out_path}")
        except Exception as e:
            print(f"Error writing CSV: {e}")

    return results


def main() -> None:
    """Command-line interface for pathogenicity prediction.
    
    Accepts a FASTA file input and optional output path for results CSV.
    Example usage:
        python -m flucleave predict input.fasta --output results.csv
    """
    parser = argparse.ArgumentParser(
        description='''
        Predict HA cleavage site pathogenicity.
        Uses a deep learning model trained on known pathogenic/non-pathogenic sequences
        to predict the pathogenicity of new HA cleavage sites.
        '''.strip()
    )
    parser.add_argument('fasta_file', 
                       help='Input FASTA file containing HA sequences')
    parser.add_argument('--output', 
                       default='predictions.csv',
                       help='Output CSV file path (default: predictions.csv)')
    
    args = parser.parse_args()
    predict_pathogenicity(args.fasta_file, args.output)


if __name__ == "__main__":
    main()