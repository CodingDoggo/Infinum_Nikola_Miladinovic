from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from backend.models import ChatRequest, ChatResponse, Conversation as ConversationSchema, Message as MessageSchema, ConversationCreate
from backend.services import get_ai_response
from backend.database import Conversation, Message, get_db

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(request: Request, db: Session = Depends(get_db)):
    ip_address = request.client.host
    if not ip_address:
        raise HTTPException(status_code=400, detail="Unable to determine client IP address")

    orm_conversations = db.query(Conversation).filter(Conversation.ip_address == ip_address).order_by(Conversation.updated_at.desc()).all()
    return [ConversationSchema.from_orm(conv) for conv in orm_conversations]

@router.post("/conversations", response_model=ConversationSchema)
def create_conversation(conversation: ConversationCreate, request: Request, db: Session = Depends(get_db)):
    ip_address = request.client.host
    db_conversation = Conversation(**conversation.dict(), ip_address=ip_address)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return ConversationSchema.from_orm(db_conversation)

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageSchema])
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return [MessageSchema.from_orm(msg) for msg in messages]

@router.post("/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest, request: Request, db: Session = Depends(get_db)):
    try:
        ip_address = request.client.host
        response_text, conversation_id = get_ai_response(db, ip_address, request_data.question, request_data.conversation_id)
        return ChatResponse(answer=response_text, conversation_id=conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "healthy"}
