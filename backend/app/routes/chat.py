"""
CampusMind AI - Chat & AI Assistant Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import process_chat_message
from app.database.in_memory import save_chat_message, get_chat_history
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/chat", tags=["AI Chat"])


@router.post("", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("id", "std_001")
    query = payload.message.strip()
    
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )

    # Save user message to history
    save_chat_message(user_id=user_id, role="user", content=query)

    # Process query through AI Service (MCP Client -> MCP Server -> Tools -> LLM/Demo)
    ai_result = await process_chat_message(query=query, student_id=user_id)

    # Save assistant reply to history
    save_chat_message(
        user_id=user_id,
        role="assistant",
        content=ai_result["reply"],
        tool_used=ai_result.get("mcp_tool_used"),
        metadata=ai_result.get("mcp_metadata")
    )

    return ai_result


@router.get("/history")
async def chat_history_endpoint(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("id", "std_001")
    history = get_chat_history(user_id=user_id, limit=50)
    return {"history": history, "user_id": user_id}
