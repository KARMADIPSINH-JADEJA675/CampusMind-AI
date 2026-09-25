"""
MCP Tool: get_placements
Fetches campus placement opportunities, company details, roles, eligibility criteria, and deadlines.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any


def load_placements_data() -> List[Dict[str, Any]]:
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "placements.json"
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_placements(
    company: Optional[str] = None,
    role: Optional[str] = None,
    department: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get active and upcoming campus placement drives and job openings.

    Args:
        company: Filter by company name (e.g. 'Microsoft', 'Google', 'Amazon').
        role: Filter by role or job title.
        department: Filter by target department or engineering branch.

    Returns:
        List of matching placement opportunities.
    """
    records = load_placements_data()
    
    filtered = records
    if company:
        comp_lower = company.strip().lower()
        filtered = [r for r in filtered if comp_lower in r.get("company", "").lower()]
        
    if role:
        role_lower = role.strip().lower()
        filtered = [r for r in filtered if role_lower in r.get("role", "").lower()]
        
    if department:
        dept_lower = department.strip().lower()
        filtered = [r for r in filtered if dept_lower in r.get("department", "").lower() or "all" in r.get("department", "").lower()]

    results = []
    for item in filtered:
        results.append({
            "id": item.get("id"),
            "company": item.get("company"),
            "role": item.get("role"),
            "ctc": item.get("ctc"),
            "eligibility": item.get("eligibility"),
            "location": item.get("location"),
            "deadline": item.get("deadline"),
            "status": item.get("status", "Open"),
            "rounds": item.get("rounds"),
            "skills": item.get("skills", [])
        })
        
    return results
