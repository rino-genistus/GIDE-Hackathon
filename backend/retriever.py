import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

from config import INDEX_DIR, TOP_K, EMBEDDING_MODEL

os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

# Load the embedding model once at module level
print(f"Loading embedding model: {EMBEDDING_MODEL}")
_embed_model = SentenceTransformer(EMBEDDING_MODEL)
print("Embedding model ready.")


def _load_index(index_dir: str = INDEX_DIR) -> tuple | None:
    """
    Load the FAISS index and chunk metadata from disk.
    Returns (index, chunks, sources) or None if index doesn't exist.
    """
    index_path  = os.path.join(index_dir, "index.faiss")
    chunks_path = os.path.join(index_dir, "chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return None

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        data = pickle.load(f)

    return index, data["chunks"], data["sources"]


def retrieve(query: str, top_k: int = TOP_K, index_dir: str = INDEX_DIR) -> list[dict]:
    """
    Embed the query and return the top_k most relevant chunks.
    Each result: {"chunk": str, "source": str, "score": float}
    Returns empty list if index not built yet.
    """
    loaded = _load_index(index_dir)
    if loaded is None:
        return []

    index, chunks, sources = loaded

    query_vec = _embed_model.encode([query], convert_to_numpy=True).astype(np.float32)
    distances, indices = index.search(query_vec, min(top_k, len(chunks)))

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "chunk":  chunks[idx],
            "source": sources[idx],
            "score":  float(dist), 
        })

    return results


def index_exists(index_dir: str = INDEX_DIR) -> bool:
    """Check whether a built index exists on disk."""
    return (
        os.path.exists(os.path.join(index_dir, "index.faiss")) and
        os.path.exists(os.path.join(index_dir, "chunks.pkl"))
    )