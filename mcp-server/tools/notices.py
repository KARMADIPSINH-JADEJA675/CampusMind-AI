"""
MCP Tool: get_notices
Fetches official university announcements, examination updates, and event notices.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any


def load_notices_data() -> List[Dict[str, Any]]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "notices.json"
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_notices(category: Optional[str] = None, limit: Optional[int] = 5) -> List[Dict[str, Any]]:
    """
    Get official university notices, optionally filtered by category.

    Args:
        category: Filter by category (e.g. 'Examination', 'Placement', 'Academic', 'Events', 'Sports').
        limit: Maximum number of notices to return (default: 5).

    Returns:
        List of notices with title, date, description, category, author, and priority.
    """
    records = load_notices_data()
    
    if category and category.lower() != "all":
        cat_lower = category.strip().lower()
        records = [r for r in records if r.get("category", "").lower() == cat_lower]
        
    # Sort by date descending
    records.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    if limit and limit > 0:
        records = records[:limit]
        
    results = []
    for item in records:
        results.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "date": item.get("date"),
            "category": item.get("category"),
            "author": item.get("author"),
            "priority": item.get("priority", "Medium"),
            "description": item.get("description")
        })
        
    return results
