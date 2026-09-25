"""
CampusMind AI - RAG Ingestion Module
Handles loading documents (TXT, MD, PDF), text chunking, embedding generation,
and storing vector indexes.
"""

import os
import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def extract_text_from_file(file_path: Path) -> str:
    """Extract plain text from TXT, MD, or PDF files."""
    ext = file_path.suffix.lower()
    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".pdf":
        if not PYPDF_AVAILABLE:
            return ""
        text = ""
        try:
            reader = PdfReader(str(file_path))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            print(f"[RAG] Error reading PDF {file_path.name}: {e}")
        return text
    return ""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks by words/sentences."""
    words = text.split()
    if not words:
        return []
    
    chunks = []
    start = 0
    step = max(1, chunk_size - overlap)
    
    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        if len(chunk.strip()) > 30:  # skip trivial chunks
            chunks.append(chunk.strip())
        start += step
        
    return chunks


def tokenize(text: str) -> List[str]:
    """Simple alphanumeric tokenizer."""
    return re.findall(r"\b[a-zA-Z0-9_]{2,}\b", text.lower())


def compute_tf_idf_vectors(chunks: List[str]) -> tuple[List[Dict[str, float]], List[str]]:
    """
    Compute standalone normalized TF-IDF vectors for documents.
    Provides offline, deterministic vector embeddings without external API reliance.
    """
    tokenized_chunks = [tokenize(c) for c in chunks]
    doc_count = len(chunks)
    
    # Vocabulary & Document Frequency (DF)
    df = {}
    for doc_tokens in tokenized_chunks:
        unique_tokens = set(doc_tokens)
        for token in unique_tokens:
            df[token] = df.get(token, 0) + 1
            
    vocab = sorted(list(df.keys()))
    
    # IDF dictionary
    idf = {term: math.log((1 + doc_count) / (1 + count)) + 1.0 for term, count in df.items()}
    
    vectors = []
    for doc_tokens in tokenized_chunks:
        tf = {}
        for token in doc_tokens:
            tf[token] = tf.get(token, 0) + 1
            
        vector = {}
        norm_sq = 0.0
        for term, freq in tf.items():
            val = freq * idf.get(term, 1.0)
            vector[term] = val
            norm_sq += val * val
            
        # L2 Normalize
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        normalized_vector = {k: v / norm for k, v in vector.items()}
        vectors.append(normalized_vector)
        
    return vectors, vocab


def ingest_documents(
    docs_dir: str = None,
    store_dir: str = None
) -> Dict[str, Any]:
    """Ingest all documents in docs_dir and build vector index in store_dir."""
    base_dir = Path(__file__).resolve().parent
    if docs_dir is None:
        docs_dir = base_dir / "documents"
    else:
        docs_dir = Path(docs_dir)
        
    if store_dir is None:
        store_dir = base_dir / "vector_store"
    else:
        store_dir = Path(store_dir)
        
    store_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect files
    supported_exts = [".txt", ".md", ".pdf"]
    doc_records = []
    
    for file_path in docs_dir.glob("*.*"):
        if file_path.suffix.lower() in supported_exts:
            content = extract_text_from_file(file_path)
            if content:
                chunks = chunk_text(content)
                for idx, chunk in enumerate(chunks):
                    doc_records.append({
                        "id": f"{file_path.stem}_{idx}",
                        "source": file_path.name,
                        "chunk_index": idx,
                        "text": chunk
                    })
                    
    # Also ingest notes from data/notes.json as part of academic RAG knowledge
    data_notes_file = base_dir.parent / "data" / "notes.json"
    if data_notes_file.exists():
        try:
            with open(data_notes_file, "r", encoding="utf-8") as f:
                notes_data = json.load(f)
                for note in notes_data:
                    doc_records.append({
                        "id": note.get("id", f"note_{len(doc_records)}"),
                        "source": f"Academic Notes: {note.get('subject')} - {note.get('topic')}",
                        "chunk_index": 0,
                        "text": f"{note.get('title')}\nSubject: {note.get('subject')}\nTopic: {note.get('topic')}\n{note.get('content')}"
                    })
        except Exception as e:
            print(f"[RAG] Warning reading notes.json: {e}")

    if not doc_records:
        print("[RAG] No document chunks found to index.")
        return {"status": "empty", "chunks_indexed": 0}

    chunk_texts = [d["text"] for d in doc_records]
    vectors, vocab = compute_tf_idf_vectors(chunk_texts)
    
    for idx, vec in enumerate(vectors):
        doc_records[idx]["vector"] = vec

    index_payload = {
        "metadata": {
            "total_documents": len(list(docs_dir.glob("*.*"))),
            "total_chunks": len(doc_records),
            "vocab_size": len(vocab)
        },
        "documents": doc_records
    }
    
    index_file = store_dir / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_payload, f, indent=2)
        
    print(f"[RAG] Ingestion completed. Indexed {len(doc_records)} chunks into {index_file}")
    return {"status": "success", "chunks_indexed": len(doc_records), "index_path": str(index_file)}


if __name__ == "__main__":
    ingest_documents()
