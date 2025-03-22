import openai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from backend.config import config
from backend.database import Conversation, Message
from typing import List, Tuple

load_dotenv()

openai.api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Please set it in the environment or config.")

def get_conversation_history(db: Session, conversation_id: int) -> List[dict]:
    """Get the conversation history for a specific conversation."""
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    
    # Format messages for API consumption
    history = []
    
    # Always add system message at the beginning
    system_msg = {
        "role": "system", 
        "content": "You are an expert legal advisor providing general legal guidance. "
                   "Do not provide personal legal representation or definitive legal conclusions."
    }
    history.append(system_msg)
    
    # Add conversation history (excluding system messages that might be in DB)
    for msg in messages:
        if msg.role in ["user", "assistant"]:
            history.append({"role": msg.role, "content": msg.content})
    
    return history

def get_or_create_conversation(db: Session, ip_address: str, conversation_id: int = None) -> Conversation:
    """Get existing conversation by id or create a new one if conversation_id is not provided."""
    if conversation_id:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.ip_address == ip_address).first()
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found for IP {ip_address}")
        return conversation
    else:
        # Create a new conversation
        conversation = Conversation(ip_address=ip_address)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

def get_ai_response(db: Session, ip_address: str, question: str, conversation_id: int = None) -> Tuple[str, int]:
    """Get AI response and update conversation history."""
    try:
        # Get or create conversation using IP address
        conversation = get_or_create_conversation(db, ip_address, conversation_id)
        
        # Get conversation history (already includes system message)
        message_history = get_conversation_history(db, conversation.id)
        
        # Add the new user question to the history for the API call
        message_history.append({"role": "user", "content": question})
        
        # Save user message to database
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=question
        )
        db.add(user_message)
        db.commit()
        client = openai.OpenAI()

        # Get AI response using OpenAI ChatCompletion
        response = client.chat.completions.create(  
            model="gpt-3.5-turbo", 
            messages=message_history
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Save AI response to database
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        db.add(assistant_message)
        
        # Update conversation title for new conversations (use first user message)
        if len(message_history) <= 3:  # Only system + first user message
            title = question[:50] + "..." if len(question) > 50 else question
            conversation.title = title
            
        db.commit()
        
        return ai_response, conversation.id
    except openai.OpenAIError as e:
        error_message = f"An error occurred while fetching the response: {str(e)}"
        return error_message, conversation_id if conversation_id else -1
