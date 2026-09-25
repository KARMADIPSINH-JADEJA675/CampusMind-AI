"""
MCP Tool: search_notes
Performs semantic and keyword search across university study materials, lecture summaries, and textbook notes.
Integrates with the RAG retrieval pipeline for grounded academic context.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any


def load_notes_data() -> List[Dict[str, Any]]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "notes.json"
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def search_notes(query: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search academic study notes by topic, keyword, or query.

    Args:
        query: Search term or academic question (e.g. 'normalization', 'TCP handshake', 'virtual memory').
        subject: Optional subject filter (e.g. 'DBMS', 'Computer Networks', 'Artificial Intelligence', 'Operating Systems').

    Returns:
        List of matching notes with subject, topic, summary, and excerpt content.
    """
    records = load_notes_data()
    q_tokens = [t.lower() for t in query.split() if len(t) > 2]
    
    scored_notes = []
    for item in records:
        # Subject filter
        if subject and subject.lower() not in item.get("subject", "").lower():
            continue
            
        score = 0
        search_blob = f"{item.get('title', '')} {item.get('topic', '')} {item.get('summary', '')} {' '.join(item.get('tags', []))} {item.get('content', '')}".lower()
        
        # Token match scoring
        for token in q_tokens:
            if token in item.get("topic", "").lower():
                score += 5
            if token in item.get("title", "").lower():
                score += 4
            if token in item.get("tags", []):
                score += 3
            if token in item.get("summary", "").lower():
                score += 2
            if token in item.get("content", "").lower():
                score += 1
                
        if score > 0 or not q_tokens:
            scored_notes.append({
                "score": score,
                "id": item.get("id"),
                "subject": item.get("subject"),
                "topic": item.get("topic"),
                "title": item.get("title"),
                "summary": item.get("summary"),
                "content": item.get("content"),
                "tags": item.get("tags", [])
            })

    scored_notes.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top 3 most relevant notes
    top_results = []
    for n in scored_notes[:3]:
        n.pop("score", None)
        top_results.append(n)
        
    # If no exact note found, return top 3 notes of the subject if specified or general
    if not top_results and records:
        for item in records[:3]:
            top_results.append({
                "id": item.get("id"),
                "subject": item.get("subject"),
                "topic": item.get("topic"),
                "title": item.get("title"),
                "summary": item.get("summary"),
                "content": item.get("content")[:300] + "...",
                "tags": item.get("tags", [])
            })
            
    return top_results
