# CampusMind AI - MCP Server

Official Model Context Protocol (MCP) Server for CampusMind AI built with the Python MCP SDK (`mcp` 2.x `MCPServer`).

## Architecture & Flow
```
FastAPI Backend (MCP Client)
           │
           │ (MCP Protocol - Stdio or SSE)
           ▼
 CampusMind MCP Server (server.py)
           │
 ┌─────────┼──────────┬──────────┬──────────┐
 │         │          │          │          │
 ▼         ▼          ▼          ▼          ▼
get_      get_       get_       search_    generate_
timetable notices    placements notes      quiz
```

## Available Tools

| Tool Name | Parameters | Purpose |
|---|---|---|
| `get_timetable` | `student_id` (str), `day` (optional str) | Returns student class schedule, timings, rooms, and professors |
| `get_notices` | `category` (optional str), `limit` (optional int) | Returns official university notices, exams, and circulars |
| `get_placements` | `company` (optional str), `role` (optional str), `department` (optional str) | Returns campus placement drives, CTC, eligibility, and deadlines |
| `search_notes` | `query` (str), `subject` (optional str) | Performs semantic search across academic lecture notes |
| `generate_quiz` | `subject` (str), `topic` (optional str), `number_of_questions` (optional int) | Generates interactive multiple-choice practice questions |

## Starting the Server
Standard Stdio mode:
```bash
python server.py --transport stdio
```

SSE (Server-Sent Events HTTP) mode:
```bash
python server.py --transport sse --port 8001
```
