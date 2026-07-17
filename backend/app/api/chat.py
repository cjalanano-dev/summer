from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from app.services.assistant_service import get_assistant

router = APIRouter(prefix="/chat", tags=["Chat"])


class MessageModel(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[MessageModel]
    model: Optional[str] = None


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
        try:
            # We call the generator from assistant which yields (chunk_type, text)
            generator = assistant.chat(prompt, model=request.model)
            for chunk_type, text in generator:
                if chunk_type == "content":
                    yield f"data: {json.dumps({'content': text})}\n\n"
                elif chunk_type == "thinking":
                    # Optionally handle backend thinking messages, wrap in <think> tags for the frontend parser
                    yield f"data: {json.dumps({'content': f'<think>{text}</think>'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
