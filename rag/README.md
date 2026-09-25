# CampusMind AI - RAG (Retrieval-Augmented Generation)

## Architecture Overview
The RAG module enables CampusMind AI to ground student answers in verifiable university study materials and syllabi, eliminating LLM hallucinations.

```
Document (PDF / TXT / MD)
        ↓
Text Extraction & Cleaning (pypdf)
        ↓
Recursive Chunking (500 words, 100 word overlap)
        ↓
Vector Indexing & Sparse L2-Normalized Vectors
        ↓
Local Vector Store (vector_store/index.json)
        ↓
Cosine Similarity Ranking & Query Expansion
        ↓
Retrieved Top-K Context Sent to LLM System Prompt
```

## Running Ingestion
To index or re-index documents:
```bash
python rag/ingestion.py
```
This automatically processes all files in `rag/documents/` as well as the notes in `data/notes.json`.
