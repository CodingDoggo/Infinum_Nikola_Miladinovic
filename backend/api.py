from fastapi import APIRouter, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.services import get_ai_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response_text = get_ai_response(request.question)
        return ChatResponse(answer=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
