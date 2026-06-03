import os
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR  = os.path.dirname(BASE_DIR)
 
DOCS_DIR     = os.path.join(ROOT_DIR, "data", "docs")
INDEX_DIR    = os.path.join(ROOT_DIR, "data", "index")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
 
# Chunking
CHUNK_SIZE    = 1000  # characters
CHUNK_OVERLAP = 200
 
# Retrieval
TOP_K = 3
 
# Embedding (local, no internet needed after first download)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
 
# Ollama — local LLM server (localhost only, fully offline)
OLLAMA_URL   = "http://localhost:11434"
OLLAMA_MODEL = "granite4.1:3b"   # change to whichever model you pulled
 
# Ensure directories exist
for d in [DOCS_DIR, INDEX_DIR]:
    os.makedirs(d, exist_ok=True)