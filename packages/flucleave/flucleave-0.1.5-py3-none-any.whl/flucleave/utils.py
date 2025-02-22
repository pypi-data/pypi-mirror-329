#!/usr/bin/env python

from Bio import SeqIO
from Bio.Seq import Seq
from tensorflow.keras.preprocessing.sequence import pad_sequences
from typing import List, Tuple, Optional, Dict
from .config import AA_WINDOW_SIZE

def load_sequences(fasta_file: str) -> List[Tuple[str, str]]:
    """Load sequences from FASTA file and extract cleavage sites.
    
    Processes each sequence to find the cleavage site motif and extracts
    the 6 amino acids preceding it. Handles both DNA and protein sequences.
    
    Args:
        fasta_file: Path to input FASTA file
        
    Returns:
        List of tuples containing (sequence_id, cleavage_site_window)
    """
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        cleavage_site, _ = find_cleavage_site(str(record.seq))
        if cleavage_site:
            sequences.append((record.id, cleavage_site))
    return sequences

def is_dna_sequence(sequence: str) -> bool:
    """Check if a sequence contains only DNA bases.
    
    Args:
        sequence: Input sequence string
        
    Returns:
        True if sequence contains only ATCG, False otherwise
    """
    dna_bases = set('ATCG')
    return all(base.upper() in dna_bases for base in sequence)

def find_cleavage_site(sequence: str) -> Tuple[Optional[str], Optional[int]]:
    """Extract the window of amino acids before a cleavage site motif.
    
    Searches for known cleavage site motifs (GLFGA, GIFGAIA) and extracts
    the preceding 6 amino acids. Handles both DNA and protein sequences.
    
    Args:
        sequence: Input sequence (DNA or protein)
        
    Returns:
        Tuple of (window sequence, position) or (None, None) if not found
    """
    # Known cleavage site motifs
    MOTIFS = ['GLFGA', 'GIFGAIA']
    TRANSLATION_TABLE = 1  # Standard genetic code

    def extract_window(protein: str) -> Tuple[Optional[str], int]:
        """Find motif and extract fixed window of preceding amino acids.
        
        Args:
            protein: Protein sequence to search
            
        Returns:
            Tuple of (window sequence, position) or (None, -1) if not found
        """
        for motif in MOTIFS:
            if motif in protein:
                motif_pos = protein.index(motif)
                if motif_pos >= AA_WINDOW_SIZE:
                    window = protein[motif_pos-AA_WINDOW_SIZE:motif_pos]
                    return window, motif_pos
        return None, -1

    # Handle DNA sequence by translating all reading frames
    if is_dna_sequence(sequence):
        seq_record = Seq(sequence)
        for frame in range(3):
            length = 3 * ((len(seq_record) - frame) // 3)
            protein = str(seq_record[frame:frame + length].translate(TRANSLATION_TABLE))
            window, pos = extract_window(protein)
            if window and len(window) == AA_WINDOW_SIZE:
                return window, pos
    
    # Handle protein sequence directly
    else:
        window, pos = extract_window(sequence)
        if window and len(window) == AA_WINDOW_SIZE:
            return window, pos

    return None, None

def encode_sequences(sequences: List[str], max_length: int = AA_WINDOW_SIZE) -> List[List[int]]:
    """Encode amino acid sequences for model input.
    
    Converts amino acid sequences to integer encodings and pads to fixed length.
    
    Args:
        sequences: List of amino acid sequences
        max_length: Length to pad sequences to (default: AA_WINDOW_SIZE)
        
    Returns:
        List of integer-encoded and padded sequences
    """
    # Define amino acid vocabulary (20 AAs + padding token)
    aa_vocab: Dict[str, int] = {aa: idx for idx, aa in enumerate('ACDEFGHIKLMNPQRSTVWY-')}
    
    # Encode sequences
    encoded = []
    for seq in sequences:
        seq_encoded = [aa_vocab.get(aa.upper(), 20) for aa in seq]
        encoded.append(seq_encoded)
    
    return pad_sequences(encoded, maxlen=max_length)