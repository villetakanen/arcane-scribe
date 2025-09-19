import pathlib
from typing import List, Dict, Any, Optional, Tuple

from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient


class QueryEngine:
    """Handles query embedding and similarity search against ChromaDB."""

    def __init__(self, db_dir: pathlib.Path, embedding_model: str = "BAAI/bge-small-en-v1.5") -> None:
        self.db_dir = db_dir
        self.embedder = SentenceTransformer(embedding_model)
        self.client = PersistentClient(path=str(db_dir))
        self.collection = self.client.get_or_create_collection("rpg_rules")

    def embed_query(self, question: str) -> List[float]:
        return self.embedder.encode(question).tolist()

    def search(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        q_emb = self.embed_query(question)
        res = self.collection.query(query_embeddings=[q_emb], n_results=k, include=["documents", "metadatas", "distances"]) 
        hits: List[Dict[str, Any]] = []
        if res and res.get("documents"):
            docs = res["documents"][0]
            metas = res["metadatas"][0]
            dists = (res.get("distances") or [[None]])[0]
            for doc, meta, dist in zip(docs, metas, dists):
                hits.append({
                    "document": doc,
                    "metadata": meta,
                    "distance": dist,
                })
        return hits
