"""
CampusMind AI - AI Service & LLM Tool Calling Orchestrator
Coordinates User Intent -> Tool Decision -> MCP Client Tool Call -> Response Generation.
Supports both OpenAI Live API and deterministic Demo Mode fallback.
"""

import os
import re
import json
import datetime
from typing import Dict, Any, Optional, Tuple, List
from app.services.mcp_client import get_mcp_client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
DEMO_MODE_ENV = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")


def detect_tool_intent(query: str) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Intelligent intent analyzer that maps queries to corresponding MCP tools and arguments.
    """
    q_lower = query.lower()

    # 1. Timetable Intent
    # "What is my next class?", "timetable", "schedule", "class today", "lecture"
    if any(k in q_lower for k in ["class", "timetable", "schedule", "lecture", "period", "lab today", "next class"]):
        day = None
        for d in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]:
            if d in q_lower:
                day = d.capitalize()
                break
        return "get_timetable", {"student_id": "std_001", "day": day or "Monday"}

    # 2. Notices Intent
    # "Show today's notices", "announcements", "circulars", "exams notice", "event updates"
    if any(k in q_lower for k in ["notice", "announcement", "circular", "exam schedule", "notification", "updates"]):
        cat = None
        if "exam" in q_lower:
            cat = "Examination"
        elif "placement" in q_lower or "job" in q_lower:
            cat = "Placement"
        elif "event" in q_lower or "hackathon" in q_lower:
            cat = "Events"
        elif "sport" in q_lower:
            cat = "Sports"
        return "get_notices", {"category": cat, "limit": 5}

    # 3. Placements Intent
    # "Which companies are available for placement?", "hiring", "jobs", "placements", "ctc", "salary"
    if any(k in q_lower for k in ["placement", "company", "companies", "hiring", "recruit", "sde", "job", "internship", "package", "ctc"]):
        company = None
        for comp in ["microsoft", "google", "amazon", "infosys", "tcs", "deloitte", "zomato", "capgemini", "oracle"]:
            if comp in q_lower:
                company = comp.capitalize()
                break
        return "get_placements", {"company": company, "role": None, "department": None}

    # 4. Quiz Generation Intent
    # "Generate 5 DBMS MCQs", "quiz on networking", "test me on AI", "questions"
    if any(k in q_lower for k in ["quiz", "mcq", "mcqs", "questions", "test me", "generate practice"]):
        subject = "DBMS"
        if any(s in q_lower for s in ["network", "networks", "tcp", "osi"]):
            subject = "Computer Networks"
        elif any(s in q_lower for s in ["ai", "artificial intelligence", "rag", "mcp", "genai", "transformer"]):
            subject = "Artificial Intelligence"
        elif "dbms" in q_lower or "database" in q_lower or "sql" in q_lower:
            subject = "DBMS"
            
        # extract number if present
        match = re.search(r"\b(\d+)\b", q_lower)
        num = int(match.group(1)) if match else 5
        return "generate_quiz", {"subject": subject, "topic": None, "number_of_questions": num}

    # 5. Study Notes / RAG Intent
    # "Explain DBMS normalization", "what is 2PL", "OSI model", "notes on transformer"
    if any(k in q_lower for k in ["notes", "explain", "normalization", "what is", "acid", "handshake", "dns", "virtual memory", "paging", "rag", "transformer", "b-tree", "2pl"]):
        subject = None
        if "dbms" in q_lower or "normalization" in q_lower or "acid" in q_lower or "b-tree" in q_lower:
            subject = "DBMS"
        elif "network" in q_lower or "tcp" in q_lower or "osi" in q_lower or "dns" in q_lower:
            subject = "Computer Networks"
        elif "ai" in q_lower or "rag" in q_lower or "transformer" in q_lower or "mcp" in q_lower:
            subject = "Artificial Intelligence"
        return "search_notes", {"query": query, "subject": subject}

    # No specific MCP tool strictly required; general conversational query
    return None, {}


def generate_synthesized_demo_response(query: str, tool_name: Optional[str], tool_data: Any) -> str:
    """
    Synthesize natural, informative university assistant responses based on MCP tool data.
    """
    if not tool_name:
        return (
            f"Hello! I am **CampusMind AI**, your university intelligent assistant.\n\n"
            f"I am connected to the campus **Model Context Protocol (MCP) Server** with 5 active tools. "
            f"You can ask me questions like:\n"
            f"- *'What is my next class?'*\n"
            f"- *'Show today's notices.'*\n"
            f"- *'Which companies are available for placement?'*\n"
            f"- *'Explain DBMS normalization from my notes.'*\n"
            f"- *'Generate 5 DBMS MCQs.'*"
        )

    # 1. Timetable Response
    if tool_name == "get_timetable":
        if isinstance(tool_data, list) and len(tool_data) > 0:
            first_class = tool_data[0]
            # Exact format requested in university requirements:
            # "Your next class is DBMS at 10:00 AM in Room A-204."
            resp = (
                f"Your next class is **{first_class['subject']}** at **{first_class['time'].split(' - ')[0]}** "
                f"in **{first_class['room']}**.\n\n"
                f"**Today's Schedule Summary:**\n"
            )
            for idx, c in enumerate(tool_data, 1):
                resp += f"{idx}. **{c['subject']}** ({c['type']})\n"
                resp += f"   • Time: `{c['time']}`\n"
                resp += f"   • Room: {c['room']} | Instructor: {c['teacher']}\n"
            return resp.strip()
        else:
            return "You have no scheduled classes for this day. Enjoy your free study session!"

    # 2. Notices Response
    if tool_name == "get_notices":
        if isinstance(tool_data, list) and len(tool_data) > 0:
            resp = "Here are the latest official university notices retrieved from the administration portal:\n\n"
            for n in tool_data:
                priority_badge = "🔴 [HIGH]" if n.get("priority") == "High" else "🔵 [UPDATE]"
                resp += f"### {priority_badge} {n['title']}\n"
                resp += f"**Category:** {n.get('category')} | **Date:** {n.get('date')} | **From:** {n.get('author')}\n\n"
                resp += f"{n.get('description')}\n\n---\n"
            return resp.strip()
        return "No notices currently matching your criteria."

    # 3. Placements Response
    if tool_name == "get_placements":
        if isinstance(tool_data, list) and len(tool_data) > 0:
            resp = "Here are the current campus placement opportunities and active recruitment drives:\n\n"
            for p in tool_data:
                resp += f"### 🏢 {p['company']} — {p['role']}\n"
                resp += f"- **Package (CTC):** `{p.get('ctc')}`\n"
                resp += f"- **Eligibility:** {p.get('eligibility')}\n"
                resp += f"- **Location:** {p.get('location')} | **Deadline:** `{p.get('deadline')}`\n"
                if p.get("skills"):
                    resp += f"- **Required Skills:** {', '.join(p['skills'])}\n"
                resp += "\n"
            return resp.strip()
        return "No placement drives found matching that company or role."

    # 4. Notes Response
    if tool_name == "search_notes":
        if isinstance(tool_data, list) and len(tool_data) > 0:
            note = tool_data[0]
            resp = f"## 📚 Study Notes: {note.get('title')}\n"
            resp += f"**Subject:** {note.get('subject')} | **Topic:** {note.get('topic')}\n\n"
            resp += f"**Summary:**\n{note.get('summary')}\n\n"
            resp += f"**Detailed Explanation:**\n{note.get('content')}\n"
            return resp.strip()
        return "I could not find specific notes matching that topic in the local academic repository."

    # 5. Quiz Response
    if tool_name == "generate_quiz":
        if isinstance(tool_data, list) and len(tool_data) > 0:
            resp = f"Here is your interactive practice quiz on **{tool_data[0].get('subject', 'DBMS')}**:\n\n"
            for idx, q in enumerate(tool_data, 1):
                resp += f"**Q{idx}. {q['question']}**\n"
                for opt in q["options"]:
                    resp += f"- **({opt['key']})** {opt['text']}\n"
                resp += f"\n> **Correct Answer:** Option {q['correct_answer']}\n"
                resp += f"> **Explanation:** {q['explanation']}\n\n"
            return resp.strip()
        return "Unable to generate quiz questions for the selected subject."

    return str(tool_data)


async def execute_openai_flow(query: str, student_id: str) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
    """
    Attempts OpenAI Live API execution with real function calling / MCP integration.
    Returns None if OPENAI_API_KEY is unset or call fails.
    """
    if not OPENAI_API_KEY or DEMO_MODE_ENV:
        return None

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        mcp_client = get_mcp_client()
        mcp_tools = await mcp_client.list_tools()

        # Format tools for OpenAI
        openai_tools = []
        for t in mcp_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t.get("parameters", {"type": "object", "properties": {}})
                }
            })

        system_prompt = (
            "You are CampusMind AI, an intelligent university assistant. "
            "You have access to official university tools via the Model Context Protocol (MCP). "
            "Always use the available tools to lookup timetable, notices, placements, study notes, or generate quizzes. "
            "Never make up schedules or examination notices."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments or "{}")
            
            # Execute tool through MCP Client
            tool_res, elapsed_ms = await mcp_client.call_tool(fn_name, fn_args)
            
            # Append tool result and request final answer
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_res)
            })

            second_resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            final_reply = second_resp.choices[0].message.content
            metadata = {
                "tool_name": fn_name,
                "tool_arguments": fn_args,
                "execution_time_ms": elapsed_ms,
                "raw_result": tool_res
            }
            return final_reply, fn_name, metadata
        else:
            return msg.content, None, None

    except Exception as e:
        print(f"[AI Service] OpenAI API error ({e}). Seamlessly falling back to Demo Mode.")
        return None


async def process_chat_message(query: str, student_id: str = "std_001") -> Dict[str, Any]:
    """
    Main entry point for AI chat.
    1. Try live OpenAI with MCP tool execution if API key is active.
    2. Fall back cleanly to deterministic MCP Tool Call + grounded synthesis in Demo Mode.
    """
    start_time = datetime.datetime.now()

    # Try Live OpenAI if configured
    openai_result = await execute_openai_flow(query, student_id)
    if openai_result:
        reply, tool_name, metadata = openai_result
        return {
            "reply": reply,
            "mcp_tool_used": tool_name,
            "mcp_metadata": metadata,
            "mode": "OPENAI_LIVE",
            "timestamp": start_time.isoformat()
        }

    # Demo Mode Flow:
    # 1. Determine tool required
    tool_name, tool_args = detect_tool_intent(query)
    metadata = None
    tool_data = None

    if tool_name:
        mcp_client = get_mcp_client()
        tool_data, elapsed_ms = await mcp_client.call_tool(tool_name, tool_args)
        metadata = {
            "tool_name": tool_name,
            "tool_arguments": tool_args,
            "status": "success",
            "execution_time_ms": elapsed_ms,
            "raw_result": tool_data
        }

    # 2. Synthesize natural answer grounded in the tool data
    reply = generate_synthesized_demo_response(query, tool_name, tool_data)

    return {
        "reply": reply,
        "mcp_tool_used": tool_name,
        "mcp_metadata": metadata,
        "mode": "DEMO_MODE",
        "timestamp": start_time.isoformat()
    }
