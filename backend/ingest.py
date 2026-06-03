import os
import pickle
import numpy as np
import pymupdf
from sentence_transformers import SentenceTransformer
import faiss

from config import (
    DOCS_DIR, INDEX_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP,
    EMBEDDING_MODEL
)

# ── Text extraction ────────────────────────────────────────────────────────────

def extract_text(filepath: str) -> str | None:
    """Extract raw text from a file. Returns None for unsupported types."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        try:
            doc = pymupdf.open(filepath)
            return "\n".join(page.get_text() for page in doc)
        except Exception as e:
            print(f"  [warn] Could not read PDF {filepath}: {e}")
            return None

    elif ext in (".md", ".txt"):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"  [warn] Could not read {filepath}: {e}")
            return None

    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError:
            print("  [warn] python-docx not installed — skipping .docx files")
            return None
        except Exception as e:
            print(f"  [warn] Could not read DOCX {filepath}: {e}")
            return None

    else:
        return None  # unsupported type, skip silently


# ── Recursive chunker ─────────────────────────────────────────────────────────

def recursive_chunk(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """
    Split text into overlapping chunks using a priority-ordered separator list.
    Tries to split on paragraphs first, then lines, then sentences, then words.
    Falls back to characters only as a last resort.
    """
    separators = ["\n\n", "\n", ". ", " ", ""]

    def _split(text: str, seps: list[str]) -> list[str]:
        if not text.strip():
            return []

        sep = seps[0]
        remaining = seps[1:]

        # Split on current separator
        parts = text.split(sep) if sep else list(text)

        chunks: list[str] = []
        current = ""

        for part in parts:
            candidate = (current + sep + part) if current else part

            if len(candidate) <= chunk_size:
                current = candidate
            else:
                # Save what we have
                if current.strip():
                    chunks.append(current.strip())

                # If this part alone is still too big and we have finer seps, recurse
                if len(part) > chunk_size and remaining:
                    sub = _split(part, remaining)
                    if sub:
                        chunks.extend(sub[:-1])
                        current = sub[-1]
                    else:
                        current = part
                else:
                    current = part

        if current.strip():
            chunks.append(current.strip())

        return chunks

    raw = _split(text, separators)

    # Apply overlap: prepend the tail of the previous chunk
    result: list[str] = []
    for i, chunk in enumerate(raw):
        if i > 0 and overlap > 0 and raw[i - 1]:
            tail = raw[i - 1][-overlap:]
            chunk = tail + " " + chunk
        result.append(chunk.strip())

    return [c for c in result if c]


# ── Index builder ─────────────────────────────────────────────────────────────

def build_index(docs_dir: str = DOCS_DIR, index_dir: str = INDEX_DIR) -> dict:
    """
    Load all supported documents from docs_dir, chunk them, embed with
    sentence-transformers, build a FAISS index, and save to index_dir.
    Returns a summary dict.
    """
    os.makedirs(index_dir, exist_ok=True)

    # Collect all files
    files = [
        f for f in os.listdir(docs_dir)
        if os.path.isfile(os.path.join(docs_dir, f))
    ]

    if not files:
        return {"status": "error", "message": f"No files found in {docs_dir}"}

    print(f"Found {len(files)} file(s) in {docs_dir}")

    all_chunks: list[str] = []
    all_sources: list[str] = []

    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        print(f"  Processing: {filename}")

        text = extract_text(filepath)
        if text is None:
            print(f"  Skipped (unsupported or unreadable)")
            continue

        chunks = recursive_chunk(text)
        print(f"  → {len(chunks)} chunks")

        all_chunks.extend(chunks)
        all_sources.extend([filename] * len(chunks))

    if not all_chunks:
        return {"status": "error", "message": "No text could be extracted from any document"}

    print(f"\nEmbedding {len(all_chunks)} chunks with {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))

    # Save index and metadata
    faiss.write_index(index, os.path.join(index_dir, "index.faiss"))
    with open(os.path.join(index_dir, "chunks.pkl"), "wb") as f:
        pickle.dump({"chunks": all_chunks, "sources": all_sources}, f)

    summary = {
        "status": "ok",
        "files_processed": len(set(all_sources)),
        "total_chunks": len(all_chunks),
    }
    print(f"\nDone. {summary}")
    return summary


# ── Standalone runner ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = build_index()
    print(result)