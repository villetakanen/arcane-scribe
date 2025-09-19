import pathlib
from typing import Optional

import click

from .query import QueryEngine
from .prompt import build_prompt
from .llm import LlamaRunner


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("question", type=str)
@click.option("--db-dir", type=click.Path(file_okay=False, path_type=pathlib.Path), default=pathlib.Path("chromadb"), show_default=True, help="Directory for ChromaDB persistence")
@click.option("--model-path", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path), required=True, help="Path to Gemma GGUF model")
@click.option("--embedding-model", default="BAAI/bge-small-en-v1.5", show_default=True)
@click.option("--k", type=int, default=5, show_default=True, help="Number of context chunks to retrieve")
@click.option("--max-tokens", type=int, default=512, show_default=True)
@click.option("--temperature", type=float, default=0.2, show_default=True)
@click.option("--top-p", type=float, default=0.9, show_default=True)
@click.option("--n-ctx", type=int, default=4096, show_default=True)
@click.option("--n-gpu-layers", type=int, default=0, show_default=True)
def main(
    question: str,
    db_dir: pathlib.Path,
    model_path: pathlib.Path,
    embedding_model: str,
    k: int,
    max_tokens: int,
    temperature: float,
    top_p: float,
    n_ctx: int,
    n_gpu_layers: int,
) -> None:
    """Ask a QUESTION against the indexed knowledge base."""
    # Retrieve context
    engine = QueryEngine(db_dir=db_dir, embedding_model=embedding_model)
    hits = engine.search(question, k=k)

    if not hits:
        click.echo("[arcane-scribe] No context found. Have you indexed PDFs yet?", err=True)
        raise click.Abort()

    # Build prompt
    prompt = build_prompt(question, hits)

    # Run model
    runner = LlamaRunner(model_path=str(model_path), n_ctx=n_ctx, n_gpu_layers=n_gpu_layers)
    answer = runner.generate(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p)

    # Print
    click.echo("\n=== Answer ===\n")
    click.echo(answer)

    click.echo("\n=== Sources ===\n")
    for i, hit in enumerate(hits, 1):
        meta = hit.get("metadata", {})
        click.echo(f"[{i}] {meta.get('source_file','?')} p.{meta.get('page_number','?')}")


if __name__ == "__main__":
    main()

