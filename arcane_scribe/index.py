import pathlib
import logging
from typing import Optional

import click

from .ingest import PDFProcessor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("pdf_dir", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("--db-dir", type=click.Path(file_okay=False, path_type=pathlib.Path), default=pathlib.Path("chromadb"), show_default=True, help="Directory for ChromaDB persistence")
@click.option("--reset", is_flag=True, help="Reset the database before indexing")
@click.option("--embedding-model", default="BAAI/bge-small-en-v1.5", show_default=True, help="Sentence transformer model for embeddings")
def main(pdf_dir: pathlib.Path, db_dir: pathlib.Path, reset: bool, embedding_model: str) -> None:
    """Index all PDFs in PDF_DIR into a local vector store."""
    click.echo(f"[arcane-scribe] Indexing PDFs from: {pdf_dir}")
    click.echo(f"[arcane-scribe] Using DB dir: {db_dir}")
    click.echo(f"[arcane-scribe] Using embedding model: {embedding_model}")
    
    try:
        # Initialize processor
        processor = PDFProcessor(db_dir, embedding_model)
        
        # Process all PDFs
        total_chunks = processor.process_directory(pdf_dir, reset)
        
        # Show results
        click.echo(f"[arcane-scribe] Successfully indexed {total_chunks} chunks")
        
        # Show collection stats
        stats = processor.get_collection_stats()
        click.echo(f"[arcane-scribe] Collection stats: {stats}")
        
    except Exception as e:
        click.echo(f"[arcane-scribe] Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()

