"""
CampusMind AI - Database Connection Manager
Attempts connection to MongoDB if configured and available;
seamlessly falls back to JSON / In-Memory store if MongoDB is offline.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

MONGODB_URI = os.getenv("MONGODB_URI", "")
_mongo_client = None
_db = None
_is_connected = False


def get_database():
    """Returns MongoDB database instance if connected, otherwise None."""
    global _mongo_client, _db, _is_connected
    if _db is not None:
        return _db
        
    if not MONGODB_URI:
        print("[Database] MONGODB_URI not provided. Operating in JSON/In-Memory fallback mode.")
        _is_connected = False
        return None

    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=1500)
        # Ping the server
        _mongo_client.admin.command('ping')
        _db = _mongo_client.get_default_database("campusmind_ai")
        _is_connected = True
        print("[Database] Successfully connected to MongoDB!")
        return _db
    except Exception as e:
        print(f"[Database] MongoDB unavailable ({e}). Using JSON/In-Memory fallback mode.")
        _is_connected = False
        _db = None
        return None


def is_mongodb_active() -> bool:
    return _is_connected
