#!/usr/bin/env python

"""
Convert cleavage site data from JSON to CSV format.

This script processes a JSON file containing HA cleavage site sequences
and their pathogenicity labels (HP=High Pathogenic, LP=Low Pathogenic).
It extracts the relevant sequences and labels, removes duplicates,
and saves the data in a CSV format suitable for model training.
"""

import json
import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Any


def convert_json_to_csv() -> None:
    """Convert cleavage site JSON data to training CSV format.
    
    Process steps:
    1. Load JSON data containing cleavage sites
    2. Extract sequences before cleavage site
    3. Parse pathogenicity labels (HP=1, LP=0)
    4. Remove duplicate sequences
    5. Save as CSV for model training
    """
    # Setup paths using pathlib
    current_dir = Path(__file__).parent
    json_path = current_dir / '../data/train/cleavage_sites.json'
    save_path = current_dir / '../data/train/training_data.csv'

    # Read JSON data
    with open(json_path, 'r') as f:
        cleavage_sites = json.load(f)

    # Initialize lists for data collection
    seq_before_stop: List[str] = []
    labels: List[int] = []

    # Process each entry in the JSON data
    for table in cleavage_sites:
        for entry in cleavage_sites[table]:
            for seq in entry['cleavage_sites']:
                # Split sequence at cleavage site
                before_site = seq.split('/')[0]
                
                # Check pathogenicity information
                if 'variant' in entry:
                    label = _get_pathogenicity_label(entry['variant'])
                elif 'phenotype' in entry:
                    label = _get_pathogenicity_label(entry['phenotype'])
                else:
                    continue
                
                # Add to dataset if valid label found
                if label is not None:
                    seq_before_stop.append(before_site)
                    labels.append(label)

    # Create and clean DataFrame
    df = pd.DataFrame({
        'cleavage_site': seq_before_stop,
        'label': labels
    })
    df = df.drop_duplicates()

    # Save processed data
    save_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Created CSV with {len(df)} unique sequences")


def _get_pathogenicity_label(info: str) -> Optional[int]:
    """Determine pathogenicity label from variant/phenotype info.
    
    Args:
        info: String containing HP/LP pathogenicity information
        
    Returns:
        0 for LP (low pathogenic)
        1 for HP (high pathogenic)
        None if ambiguous or invalid
    """
    if 'LP' in info and not 'HP' in info:
        return 0
    elif 'HP' in info and not 'LP' in info:
        return 1
    elif 'LP' in info and 'HP' in info:
        return None  # Skip ambiguous cases
    else:
        return 1  # Default to HP if not specified


if __name__ == "__main__":
    convert_json_to_csv()