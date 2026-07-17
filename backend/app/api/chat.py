from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio

from app.services.assistant_service import get_assistant

router = APIRouter(prefix="/chat", tags=["Chat"])


class MessageModel(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[MessageModel]


@router.post("")
def chat(request: ChatRequest):
    """
    Exposes streaming chat using Server-Sent Events (SSE).
    """
    assistant = get_assistant()

    # Reconstruct history inside Summer's conversation buffer if needed.
    # We clear and reload the history so the memory manager & workspace injection matches.
    assistant.conversation.clear()
    
    # Load all previous messages except the very last one (which is the new prompt)
    for msg in request.messages[:-1]:
        assistant.conversation.add_message(msg.role, msg.content)
        
    prompt = request.messages[-1].content

    def event_generator():
        # Get response generator from Summer.chat
        try:
            # We call the generator from assistant
            generator = assistant.chat(prompt)
            for chunk in generator:
                # Send the clean chunk to the browser
                yield f"data: {json.dumps({'content': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
