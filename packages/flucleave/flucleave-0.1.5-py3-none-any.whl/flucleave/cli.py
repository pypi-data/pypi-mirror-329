#!/usr/bin/env python3
"""Command line interface for FluCleave predictions."""

import click
import logging
import sys
from pathlib import Path
from typing import NoReturn

from flucleave import __version__
from .predict import predict_pathogenicity
from .train import train_model

logger = logging.getLogger(__name__)

def setup_logging(debug: bool = False) -> None:
    """Configure logging with appropriate level and format."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

@click.group()
@click.version_option(version=__version__, prog_name='FluCleave')
@click.option('--debug', is_flag=True, help='Enable debug logging')
def cli(debug: bool):
    """FluCleave: Predict influenza virus pathogenicity from HA cleavage sites."""
    setup_logging(debug)

@cli.command()
@click.option('--fasta', required=True, type=click.Path(exists=True),
              help='Input FASTA file containing HA sequences')
@click.option('--output-dir', default='.', type=click.Path(),
              help='Output directory for results (default: current directory)')
@click.option('--prefix', help='Prefix for output CSV file')
def predict(fasta: str, output_dir: str, prefix: str):
    """Predict pathogenicity of HA cleavage sites for H5 and H7 variants."""
    try:
        results = predict_pathogenicity(fasta, output_dir, prefix)
        if not results:
            click.echo(click.style("No valid predictions generated", fg='red'))
            sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"Error during prediction: {e}", fg='red'))
        sys.exit(1)

@cli.command()
@click.option('--training-csv', type=click.Path(exists=True),
              help='CSV file with cleavage sites and labels (uses default if not specified)')
@click.option('--model-output', type=click.Path(),
              help='Output path for trained model (uses default if not specified)')
@click.option('--force', is_flag=True, help='Force overwrite existing model files')
def train(training_csv: str, model_output: str, force: bool):
    """Train new pathogenicity prediction model."""
    try:
        click.echo(click.style("Starting model training...", fg='green'))
        train_model(training_csv, model_output, force=force)
        click.echo(click.style("Model training completed!", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Error during training: {e}", fg='red'))
        sys.exit(1)

def main():
    """Entry point for the CLI application."""
    try:
        cli()
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'))
        sys.exit(1)

if __name__ == '__main__':
    main()