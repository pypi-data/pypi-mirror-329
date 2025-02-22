# FluCleave

Deep learning prediction of influenza virus pathogenicity from HA cleavage sites for H5 and H7 variants.

## Features

-   Analyzes H5 and H7 hemagglutinin (HA) cleavage site sequences
-   Predicts high/low pathogenicity using deep learning
-   Handles both DNA and protein sequences
-   Command-line interface for easy use
-   Trained on curated dataset of known pathogenic sequences

## Installation

```bash
pip install flucleave
```

## Usage

Predict pathogenicity from FASTA file:

```bash
flucleave predict --fasta sequences.fasta --output-dir results/ --prefix sample_name
```

Train new model (optional):

```bash
flucleave train --training-csv data.csv
```

## Training Data

This model was trained on data curated from 2 sources:

-   [Offlu Influenza A Cleavage Sites Document for H5 and H7](https://www.offlu.org/wp-content/uploads/2022/01/Influenza-A-Cleavage-Sites-Final-04-01-2022.pdf)
-   GISAID query of all [LPAI HA sequences](./flucleave/data/train/LPAI_HA_GISAID_20240221.fasta.gz) with complete cleavage sites (as of 2025-02-21)

## Data Format

Input FASTA should contain HA protein sequences in either amino acid or DNA format.

## License

FluCleave is licensed under the [MIT License](LICENSE).
