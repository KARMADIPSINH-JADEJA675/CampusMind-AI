"""
CampusMind AI - Campus Data & Tools Routes
Exposes timetable, notices, placements, quiz, and direct MCP tool metadata inspection.
"""

from fastapi import APIRouter, Query, Depends
from typing import Optional
from typing import Optional, List, Dict, Any
from app.schemas.campus import QuizRequest
from app.services.mcp_client import get_mcp_client
from app.database.in_memory import get_all_timetable, get_all_notices, get_all_placements, get_all_notes
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api", tags=["Campus Data & MCP"])


@router.get("/timetable")
async def timetable_endpoint(
    day: Optional[str] = Query(None, description="Day of week"),
    current_user: dict = Depends(get_current_user)
):
    student_id = current_user.get("id", "std_001")
    mcp_client = get_mcp_client()
    data, elapsed = await mcp_client.call_tool("get_timetable", {"student_id": student_id, "day": day})
    return {"timetable": data, "count": len(data), "execution_ms": elapsed}


@router.get("/notices")
async def notices_endpoint(
    category: Optional[str] = Query(None, description="Category filter"),
    limit: int = Query(10, ge=1, le=50)
):
    mcp_client = get_mcp_client()
    data, elapsed = await mcp_client.call_tool("get_notices", {"category": category, "limit": limit})
    return {"notices": data, "count": len(data), "execution_ms": elapsed}


@router.get("/placements")
async def placements_endpoint(
    company: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    department: Optional[str] = Query(None)
):
    mcp_client = get_mcp_client()
    data, elapsed = await mcp_client.call_tool("get_placements", {"company": company, "role": role, "department": department})
    return {"placements": data, "count": len(data), "execution_ms": elapsed}


@router.post("/quiz")
async def quiz_endpoint(payload: QuizRequest):
    mcp_client = get_mcp_client()
    data, elapsed = await mcp_client.call_tool("generate_quiz", {
        "subject": payload.subject,
        "topic": payload.topic,
        "number_of_questions": payload.number_of_questions
    })
    return {"quiz": data, "count": len(data), "execution_ms": elapsed}


@router.get("/notes")
async def notes_endpoint(
    query: Optional[str] = Query("", description="Keyword search query"),
    subject: Optional[str] = Query(None, description="Subject filter")
):
    mcp_client = get_mcp_client()
    data, elapsed = await mcp_client.call_tool("search_notes", {"query": query or "", "subject": subject})
    return {"notes": data, "count": len(data), "execution_ms": elapsed}


@router.get("/mcp/tools")
async def mcp_tools_endpoint():
    """Returns active MCP tools metadata dynamically discovered from the MCP Server."""
    mcp_client = get_mcp_client()
    tools = await mcp_client.list_tools()
    return {
        "server": "CampusMind-MCP-Server",
        "protocol": "Model Context Protocol (v2.x)",
        "total_tools": len(tools),
        "tools": tools
    }
