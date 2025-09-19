from typing import List, Dict


SYSTEM_INSTRUCTIONS = (
    "You are Arcane Scribe, a rules assistant. Answer ONLY from the provided context. "
    "If the answer is not in the context, say you don't know. Provide citations with "
    "source filename and page number for each statement when possible. Be concise."
)


def build_prompt(question: str, contexts: List[Dict]) -> str:
    """Build a prompt including system instructions and context snippets.

    Each context dict should have keys: 'document' and 'metadata' containing
    'source_file' and 'page_number'.
    """
    header = SYSTEM_INSTRUCTIONS + "\n\n"
    ctx_lines: List[str] = ["Context:"]
    for i, hit in enumerate(contexts, 1):
        meta = hit.get("metadata", {})
        src = meta.get("source_file", "unknown")
        page = meta.get("page_number", "?")
        snippet = hit.get("document", "").strip().replace("\n", " ")
        ctx_lines.append(f"[{i}] {src} p.{page}: {snippet}")
    ctx_block = "\n".join(ctx_lines)

    q_block = f"\n\nQuestion: {question}\n\nAnswer (cite sources like [1], [2]):\n"
    return header + ctx_block + q_block
