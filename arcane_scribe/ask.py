import pathlib
from typing import Optional

import click


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("question", type=str)
@click.option("--db-dir", type=click.Path(file_okay=False, path_type=pathlib.Path), default=pathlib.Path("chromadb"), show_default=True, help="Directory for ChromaDB persistence")
@click.option("--model-path", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path), help="Path to Gemma GGUF model")
@click.option("--max-tokens", type=int, default=512, show_default=True)
def main(question: str, db_dir: pathlib.Path, model_path: Optional[pathlib.Path], max_tokens: int) -> None:
    """Ask a QUESTION against the indexed knowledge base.

    This is a skeleton; implementation will be added in Week 2 tasks.
    """
    click.echo(f"[arcane-scribe] Question: {question}")
    click.echo(f"[arcane-scribe] Using DB dir: {db_dir}")
    if model_path:
        click.echo(f"[arcane-scribe] Model: {model_path}")
    click.echo(f"[arcane-scribe] TODO: retrieve context and generate answer (max_tokens={max_tokens}).")


if __name__ == "__main__":
    main()

