"""
CampusMind AI - Official Model Context Protocol (MCP) Server
Implements standard MCP tools using the Python MCP SDK (mcp 2.x MCPServer).
Exposes tools for Timetable, Notices, Placements, Study Notes, and Quiz Generation.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR / "mcp-server") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "mcp-server"))

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        raise RuntimeError("MCP SDK not installed. Please run: pip install mcp")

from tools.timetable import get_timetable as fn_get_timetable
from tools.notices import get_notices as fn_get_notices
from tools.placements import get_placements as fn_get_placements
from tools.notes import search_notes as fn_search_notes
from tools.quiz import generate_quiz as fn_generate_quiz

# Initialize the MCP Server
mcp = MCPServer(
    name="CampusMind-MCP-Server",
    description="University Assistant MCP Server providing real-time campus data, academic notes, and quiz generation"
)


# Tool 1: get_timetable
@mcp.tool(
    name="get_timetable",
    description="Fetch class timetable schedule for university students by student_id and optional day."
)
def get_timetable(student_id: str = "std_001", day: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get the class timetable for a student.

    Args:
        student_id: The ID of the student (default: "std_001").
        day: Day of the week (e.g. 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday').
    """
    return fn_get_timetable(student_id=student_id, day=day)


# Tool 2: get_notices
@mcp.tool(
    name="get_notices",
    description="Fetch official university announcements, examination schedules, and event notices."
)
def get_notices(category: Optional[str] = None, limit: Optional[int] = 5) -> List[Dict[str, Any]]:
    """
    Get official university notices.

    Args:
        category: Filter by category ('Examination', 'Placement', 'Academic', 'Events', 'Sports', 'General').
        limit: Maximum number of notices to return (default: 5).
    """
    return fn_get_notices(category=category, limit=limit)


# Tool 3: get_placements
@mcp.tool(
    name="get_placements",
    description="Fetch active campus placement drives, company requirements, packages, eligibility, and deadlines."
)
def get_placements(
    company: Optional[str] = None,
    role: Optional[str] = None,
    department: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get active and upcoming campus placement opportunities.

    Args:
        company: Filter by company name (e.g. 'Microsoft', 'Google', 'Amazon', 'Infosys').
        role: Filter by job title or role.
        department: Filter by target department.
    """
    return fn_get_placements(company=company, role=role, department=department)


# Tool 4: search_notes
@mcp.tool(
    name="search_notes",
    description="Search university academic study notes, textbook explanations, and module summaries."
)
def search_notes(query: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search academic study notes.

    Args:
        query: Academic topic or query (e.g. 'normalization', 'TCP handshake', 'virtual memory', 'RAG').
        subject: Optional subject name ('DBMS', 'Computer Networks', 'Artificial Intelligence', 'Operating Systems').
    """
    return fn_search_notes(query=query, subject=subject)


# Tool 5: generate_quiz
@mcp.tool(
    name="generate_quiz",
    description="Generate multiple-choice practice quiz questions with options, correct answer, and explanation."
)
def generate_quiz(
    subject: str = "DBMS",
    topic: Optional[str] = None,
    number_of_questions: Optional[int] = 5
) -> List[Dict[str, Any]]:
    """
    Generate an academic multiple-choice quiz.

    Args:
        subject: Subject for the quiz ('DBMS', 'Computer Networks', 'Artificial Intelligence').
        topic: Specific topic or sub-module.
        number_of_questions: Number of questions (1 to 10).
    """
    return fn_generate_quiz(subject=subject, topic=topic, number_of_questions=number_of_questions)


def main():
    parser = argparse.ArgumentParser(description="CampusMind AI MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol (stdio or sse). Default: stdio"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="Port for SSE transport. Default: 8001"
    )
    args = parser.parse_args()

    print(f"[CampusMind MCP Server] Starting with transport={args.transport} ...", file=sys.stderr)
    if args.transport == "sse":
        # Run SSE server
        mcp.run(transport="sse", port=args.port)
    else:
        # Run standard stdio server
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
