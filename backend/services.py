from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session
from backend.config import config
from backend.database import Conversation, Message
from typing import Tuple, List
from datetime import datetime

def get_or_create_conversation(db: Session, ip_address: str, conversation_id: int = None) -> Conversation:
    """Get existing conversation by ID or create a new one."""
    if conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id, Conversation.ip_address == ip_address
        ).first()
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found for IP {ip_address}")
        return conversation
    else:
        conversation = Conversation(ip_address=ip_address)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

def get_conversation_history(db: Session, conversation_id: int) -> List[dict]:
    """Retrieve conversation history from database."""
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    return messages

def get_ai_response(db: Session, ip_address: str, question: str, conversation_id: int = None) -> Tuple[str, int]:
    """Use LangChain to get AI response and track conversation history."""
    try:

        conversation = get_or_create_conversation(db, ip_address, conversation_id)

        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.4, # I want the AI to be clear and professional
            openai_api_key=config.OPENAI_API_KEY
        )
        
        messages = get_conversation_history(db, conversation.id)
        
        user_message = Message(conversation_id=conversation.id, role="user", content=question)
        db.add(user_message)
        
        if len(messages) == 0:
            title = question[:50] + "..." if len(question) > 50 else question
            conversation.title = title
        
        conversation.updated_at = datetime.utcnow()
        db.commit()

        chat_history = ""
        db_messages = get_conversation_history(db, conversation.id)
        for msg in db_messages:
            role = "User" if msg.role == "user" else "Assistant"
            chat_history += f"{role}: {msg.content}\n"
        
        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template="""
            You are an expert legal advisor providing general legal guidance.  
            Your responses should be clear, professional, and informative.  
            - You may explain legal principles, procedures, and general best practices.  
            - You **must not** provide personal legal representation, draft legal documents, or offer definitive legal conclusions.  
            - Always encourage users to consult a qualified attorney for case-specific advice.  

            Chat history:  
            {chat_history}  

            User: {input}  
            Assistant:  
            """
        )
        
        conversation_chain = LLMChain(
            llm=llm,
            prompt=prompt
        )
        
        response = conversation_chain.invoke({"input": question, "chat_history": chat_history})
        response_text = response['text'].strip()
        
        assistant_message = Message(conversation_id=conversation.id, role="assistant", content=response_text)
        db.add(assistant_message)
        
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        return response_text, conversation.id

    except Exception as e:
        db.rollback() 
        raise e 