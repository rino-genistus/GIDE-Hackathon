import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import DOCS_DIR, INDEX_DIR, FRONTEND_DIR
from ingest import build_index
from retriever import retrieve, index_exists
from generator import generate_answer, ollama_status

app = FastAPI(title="DocQA — Air-Gapped Document Q&A")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer:  str
    sources: list[str]
    chunks:  list[dict]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/status")
def get_status():
    files = []
    if os.path.exists(DOCS_DIR):
        files = [
            f for f in os.listdir(DOCS_DIR)
            if os.path.isfile(os.path.join(DOCS_DIR, f))
        ]
    ollama = ollama_status()
    return {
        "index_built":     index_exists(),
        "model_available": ollama["available"],
        "ollama_model":    ollama["model"],
        "docs_count":      len(files),
        "docs":            files,
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed = {".pdf", ".md", ".txt", ".docx"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported type '{ext}'. Allowed: {', '.join(allowed)}"
        )
    dest = os.path.join(DOCS_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "ok", "filename": file.filename}


@app.post("/ingest")
def ingest_documents():
    result = build_index(DOCS_DIR, INDEX_DIR)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/query", response_model=QueryResponse)
def query_documents(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if not index_exists():
        raise HTTPException(
            status_code=400,
            detail="Index not built yet — upload documents and click Index first."
        )

    chunks = retrieve(req.question)
    if not chunks:
        return QueryResponse(answer="No relevant content found.", sources=[], chunks=[])

    answer  = generate_answer(req.question, chunks)
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    return QueryResponse(answer=answer, sources=sources, chunks=chunks)


# ── Frontend — mount LAST ─────────────────────────────────────────────────────

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "Place index.html in the frontend/ directory."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)