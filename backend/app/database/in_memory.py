"""
CampusMind AI - In-Memory & JSON Data Repository
Guarantees full system functionality even without MongoDB.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"

# In-memory stores
MEM_USERS: List[Dict[str, Any]] = []
MEM_CHATS: List[Dict[str, Any]] = []
MEM_MESSAGES: List[Dict[str, Any]] = []


def _load_json(filename: str) -> List[Dict[str, Any]]:
    file_path = DATA_DIR / filename
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Store] Error reading {filename}: {e}")
    return []


def init_in_memory_store():
    """Initializes in-memory stores from JSON files."""
    global MEM_USERS
    users = _load_json("students.json")
    MEM_USERS = users


# User helpers
def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    for u in MEM_USERS:
        if u.get("email", "").lower() == email.lower():
            return u
    return None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    for u in MEM_USERS:
        if u.get("id") == user_id:
            return u
    return None


def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    MEM_USERS.append(user_data)
    return user_data


# Chat history helpers
def save_chat_message(user_id: str, role: str, content: str, tool_used: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    import datetime
    msg = {
        "id": f"msg_{len(MEM_MESSAGES) + 1}",
        "user_id": user_id,
        "role": role,
        "content": content,
        "tool_used": tool_used,
        "metadata": metadata or {},
        "timestamp": datetime.datetime.now().isoformat()
    }
    MEM_MESSAGES.append(msg)
    return msg


def get_chat_history(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    user_msgs = [m for m in MEM_MESSAGES if m.get("user_id") == user_id]
    return user_msgs[-limit:]


# Direct campus data getters (used by REST routes or fallbacks)
def get_all_timetable() -> List[Dict[str, Any]]:
    return _load_json("timetable.json")


def get_all_notices() -> List[Dict[str, Any]]:
    return _load_json("notices.json")


def get_all_placements() -> List[Dict[str, Any]]:
    return _load_json("placements.json")


def get_all_notes() -> List[Dict[str, Any]]:
    return _load_json("notes.json")


# Auto-initialize
init_in_memory_store()
