"""
CampusMind AI - Chat & AI Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Student question or query")
    student_id: Optional[str] = "std_001"
    session_id: Optional[str] = "default"


class MCPToolExecutionMetadata(BaseModel):
    tool_name: str
    tool_arguments: Dict[str, Any]
    status: str = "success"
    execution_time_ms: float
    raw_result: Optional[Any] = None


class ChatResponse(BaseModel):
    reply: str
    mcp_tool_used: Optional[str] = None
    mcp_metadata: Optional[MCPToolExecutionMetadata] = None
    mode: str = "DEMO_MODE"  # 'OPENAI_LIVE' or 'DEMO_MODE'
    timestamp: str
