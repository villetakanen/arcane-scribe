import pathlib
from typing import Optional

import click


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("pdf_dir", type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path))
@click.option("--db-dir", type=click.Path(file_okay=False, path_type=pathlib.Path), default=pathlib.Path("chromadb"), show_default=True, help="Directory for ChromaDB persistence")
@click.option("--reset", is_flag=True, help="Reset the database before indexing")
def main(pdf_dir: pathlib.Path, db_dir: pathlib.Path, reset: bool) -> None:
    """Index all PDFs in PDF_DIR into a local vector store.

    This is a skeleton; implementation will be added in Week 1 tasks.
    """
    click.echo(f"[arcane-scribe] Indexing PDFs from: {pdf_dir}")
    click.echo(f"[arcane-scribe] Using DB dir: {db_dir}")
    if reset:
        click.echo("[arcane-scribe] Resetting database...")
    click.echo("[arcane-scribe] TODO: implement ingestion, chunking, embeddings, and storage.")


if __name__ == "__main__":
    main()

