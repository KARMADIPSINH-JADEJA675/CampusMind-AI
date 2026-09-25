"""
CampusMind AI - Official MCP Client Module
Implements the Model Context Protocol (MCP) Client layer.
Discovers tools, executes MCP tool calls, and returns structured data to the LLM.
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Path setup to import mcp-server
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MCP_SERVER_DIR = BASE_DIR / "mcp-server"
if str(MCP_SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_SERVER_DIR))

# Import the actual MCP Server instance
from server import mcp as campus_mcp_server


class CampusMCPClient:
    """
    MCP Client that maintains communication with the CampusMind MCP Server.
    Provides tool discovery and tool execution adhering to the Model Context Protocol.
    """
    def __init__(self):
        self.server = campus_mcp_server
        self._cached_tools: Optional[List[Dict[str, Any]]] = None

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        Query the MCP Server for all registered MCP tools and their schemas.
        Adheres to MCP tools/list protocol specification.
        """
        try:
            tools = await self.server.list_tools()
            tool_definitions = []
            for t in tools:
                tool_definitions.append({
                    "name": t.name,
                    "description": t.description,
                    "parameters": getattr(t, "parameters", {}) or getattr(t, "inputSchema", {})
                })
            self._cached_tools = tool_definitions
            return tool_definitions
        except Exception as e:
            print(f"[MCP Client] Error listing tools: {e}")
            # Fallback tool signatures
            return [
                {
                    "name": "get_timetable",
                    "description": "Fetch class timetable schedule for university students.",
                    "parameters": {"type": "object", "properties": {"student_id": {"type": "string"}, "day": {"type": "string"}}}
                },
                {
                    "name": "get_notices",
                    "description": "Fetch official university notices and announcements.",
                    "parameters": {"type": "object", "properties": {"category": {"type": "string"}, "limit": {"type": "integer"}}}
                },
                {
                    "name": "get_placements",
                    "description": "Fetch active and upcoming campus placement opportunities.",
                    "parameters": {"type": "object", "properties": {"company": {"type": "string"}, "role": {"type": "string"}, "department": {"type": "string"}}}
                },
                {
                    "name": "search_notes",
                    "description": "Search university academic study notes.",
                    "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "subject": {"type": "string"}}}
                },
                {
                    "name": "generate_quiz",
                    "description": "Generate an academic multiple-choice quiz.",
                    "parameters": {"type": "object", "properties": {"subject": {"type": "string"}, "topic": {"type": "string"}, "number_of_questions": {"type": "integer"}}}
                }
            ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[Any, float]:
        """
        Execute an MCP tool call on the MCP Server.
        Measures execution latency in milliseconds.

        Returns:
            Tuple of (parsed_result_data, execution_time_ms)
        """
        start_time = time.perf_counter()
        print(f"[MCP Client] Sending call to MCP Server -> Tool: '{tool_name}' Args: {arguments}")
        
        try:
            mcp_result = await self.server.call_tool(tool_name, arguments)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Extract content from MCP Result
            data = None
            if hasattr(mcp_result, "structured_content") and mcp_result.structured_content:
                data = mcp_result.structured_content.get("result", mcp_result.structured_content)
            elif hasattr(mcp_result, "content") and mcp_result.content:
                # Content is a list of TextContent objects
                content_item = mcp_result.content[0]
                text_payload = getattr(content_item, "text", str(content_item))
                try:
                    data = json.loads(text_payload)
                except Exception:
                    data = text_payload
            else:
                data = mcp_result
                
            print(f"[MCP Client] MCP Tool '{tool_name}' returned successfully in {elapsed_ms}ms")
            return data, elapsed_ms
            
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            print(f"[MCP Client] Error executing MCP tool '{tool_name}': {e}")
            raise e


# Global singleton instance
_mcp_client = None

def get_mcp_client() -> CampusMCPClient:
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = CampusMCPClient()
    return _mcp_client
