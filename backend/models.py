from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str = "New Conversation"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    ip_address: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

# Removed User schemas

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[int] = None
    # Removed user_id

class ChatResponse(BaseModel):
    answer: str
    conversation_id: int
