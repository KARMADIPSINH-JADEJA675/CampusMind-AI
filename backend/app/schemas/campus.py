"""
CampusMind AI - Campus Entity Schemas
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class QuizRequest(BaseModel):
    subject: str = "DBMS"
    topic: Optional[str] = None
    number_of_questions: Optional[int] = 5


class DocumentSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
