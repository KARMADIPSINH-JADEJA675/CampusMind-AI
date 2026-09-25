"""
CampusMind AI - RAG Service Wrapper
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from rag.retrieval import retrieve_context
from rag.ingestion import ingest_documents

RAG_DOCS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "rag" / "documents"


def search_documents(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Retrieve semantically relevant chunks for a student query."""
    return retrieve_context(query, top_k=top_k)


def save_and_ingest_document(filename: str, content_bytes: bytes) -> Dict[str, Any]:
    """Save uploaded document and trigger incremental RAG ingestion."""
    RAG_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    target_file = RAG_DOCS_DIR / filename
    with open(target_file, "wb") as f:
        f.write(content_bytes)
        
    # Re-ingest
    res = ingest_documents()
    return {
        "status": "success",
        "filename": filename,
        "chunks_indexed": res.get("chunks_indexed", 0)
    }
