"""
MCP Tool: get_timetable
Fetches class timetable schedule for university students.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any


def load_timetable_data() -> List[Dict[str, Any]]:
    """Load timetable data from data/timetable.json."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "timetable.json"

    if not data_path.exists():
        return []

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def get_timetable(
    student_id: str = "std_001",
    day: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get timetable for a student.

    If timetable records contain student_id, only that student's
    records are returned.

    If records do not contain student_id, all matching timetable
    records are returned rather than incorrectly guessing which
    parallel/group entry belongs to the student.
    """

    records = load_timetable_data()

    if not records:
        return []

    # ---------------------------------------------------------
    # 1. Student filtering
    # ---------------------------------------------------------
    records_have_student_ids = any(
        r.get("student_id") for r in records
    )

    if records_have_student_ids:
        filtered = [
            r for r in records
            if r.get("student_id") == student_id
        ]
    else:
        # Current timetable.json does not contain student_id.
        # Therefore, do not make up a student-specific mapping.
        filtered = records.copy()

    # ---------------------------------------------------------
    # 2. Day filtering
    # ---------------------------------------------------------
    if day:
        day_clean = day.strip().lower()

        filtered = [
            r for r in filtered
            if str(r.get("day", "")).strip().lower() == day_clean
        ]

    # ---------------------------------------------------------
    # 3. Format response
    # ---------------------------------------------------------
    results = []

    for item in filtered:
        results.append({
            "id": item.get("id"),
            "subject": item.get("subject"),
            "code": item.get("code"),
            "day": item.get("day"),
            "time": item.get("time"),
            "room": item.get("room"),
            "teacher": item.get("teacher"),
            "type": item.get("type", "Lecture")
        })

    return results