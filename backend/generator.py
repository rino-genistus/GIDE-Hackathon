import requests
from config import OLLAMA_URL, OLLAMA_MODEL

# ── Check Ollama at startup ───────────────────────────────────────────────────

MODEL_AVAILABLE = False

def _check_ollama() -> bool:
    global MODEL_AVAILABLE
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            # Match on base model name (e.g. "llama3.2" matches "llama3.2:latest")
            base = OLLAMA_MODEL.split(":")[0]
            MODEL_AVAILABLE = any(base in m for m in models)
            if MODEL_AVAILABLE:
                print(f"[generator] Ollama ready — model: {OLLAMA_MODEL}")
            else:
                print(f"[generator] Model '{OLLAMA_MODEL}' not found in Ollama.")
                print(f"[generator] Available: {models}")
                print(f"[generator] Run: ollama pull {OLLAMA_MODEL}")
        return MODEL_AVAILABLE
    except requests.exceptions.ConnectionError:
        print("[generator] Ollama not running. Start it with: ollama serve")
        return False
    except Exception as e:
        print(f"[generator] Ollama check failed: {e}")
        return False

_check_ollama()


# ── Answer generation ─────────────────────────────────────────────────────────

def generate_answer(question: str, context_chunks: list[dict]) -> str:
    """
    Generate an answer using Ollama (local LLM, no internet).
    Falls back to raw retrieved context if Ollama isn't available.
    """
    if not context_chunks:
        return "No relevant content found in the indexed documents."

    # Build context block with source attribution
    context_parts = []
    for i, item in enumerate(context_chunks, 1):
        context_parts.append(
            f"[Source {i} — {item['source']}]\n{item['chunk']}"
        )
    context_text = "\n\n".join(context_parts)

    # Graceful fallback if Ollama isn't up
    if not MODEL_AVAILABLE:
        return (
            "⚠️  Ollama not available — showing raw retrieved context:\n\n"
            + context_text
        )

    system_prompt = (
        "You are a precise document assistant. Answer questions using ONLY the "
        "provided context. Always state which source document your answer comes "
        "from. If the context doesn't contain enough information to answer, say "
        "so clearly — never invent information."
    )

    user_prompt = (
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        f"Answer (with source citations):"
    )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,   # low = factual, consistent
                    "num_predict": 512,
                },
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "⚠️  Generation timed out. Try a shorter question or smaller model.\n\nRaw context:\n" + context_text
    except Exception as e:
        return f"⚠️  Generation error: {e}\n\nRaw context:\n{context_text}"


def ollama_status() -> dict:
    """Return Ollama availability info for the /status endpoint."""
    return {
        "available": MODEL_AVAILABLE,
        "model":     OLLAMA_MODEL,
        "url":       OLLAMA_URL,
    }