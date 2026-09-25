"""
CampusMind AI - RAG Retrieval Module
Retrieves relevant context passages given a student's query using cosine similarity.
"""

import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any


def tokenize(text: str) -> List[str]:
    """Simple alphanumeric tokenizer."""
    return re.findall(r"\b[a-zA-Z0-9_]{2,}\b", text.lower())


def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """Compute dot product of two L2-normalized sparse vectors."""
    score = 0.0
    # Iterate over shorter dictionary for efficiency
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    for term, val_a in vec_a.items():
        if term in vec_b:
            score += val_a * vec_b[term]
    return score


class RAGRetriever:
    def __init__(self, index_path: str = None):
        if index_path is None:
            base_dir = Path(__file__).resolve().parent
            self.index_path = base_dir / "vector_store" / "index.json"
        else:
            self.index_path = Path(index_path)
            
        self.index_data = None
        self._load_index()

    def _load_index(self):
        if self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    self.index_data = json.load(f)
            except Exception as e:
                print(f"[RAG] Failed to load index: {e}")
                self.index_data = None
        else:
            self.index_data = None

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve the top_k most relevant chunks matching the student query."""
        if not self.index_data or "documents" not in self.index_data:
            # Try to build index if missing
            from rag.ingestion import ingest_documents
            ingest_documents()
            self._load_index()
            if not self.index_data:
                return []

        tokens = tokenize(query)
        if not tokens:
            return []

        # Build normalized query vector
        q_tf = {}
        for t in tokens:
            q_tf[t] = q_tf.get(t, 0) + 1
        q_norm_sq = sum(v * v for v in q_tf.values())
        q_norm = math.sqrt(q_norm_sq) if q_norm_sq > 0 else 1.0
        q_vec = {k: v / q_norm for k, v in q_tf.items()}

        results = []
        for doc in self.index_data.get("documents", []):
            d_vec = doc.get("vector", {})
            sim = cosine_similarity(q_vec, d_vec)
            
            # Boost score if query exact words appear in text
            lower_text = doc["text"].lower()
            keyword_matches = sum(1 for t in tokens if t in lower_text)
            boosted_score = sim + (keyword_matches * 0.05)
            
            if boosted_score > 0.01:
                results.append({
                    "id": doc.get("id"),
                    "source": doc.get("source"),
                    "chunk_index": doc.get("chunk_index"),
                    "text": doc.get("text"),
                    "score": round(boosted_score, 4)
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


# Global instance helper
_retriever_instance = None

def get_retriever() -> RAGRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = RAGRetriever()
    return _retriever_instance

def retrieve_context(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    return get_retriever().retrieve(query, top_k)


if __name__ == "__main__":
    test_q = "Explain normalization in DBMS"
    print(f"Testing retrieval for: '{test_q}'")
    hits = retrieve_context(test_q)
    for h in hits:
        print(f"[{h['score']}] ({h['source']}): {h['text'][:120]}...\n")
