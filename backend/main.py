from fastapi import FastAPI, HTTPException
from backend.api import router as chat_router

app = FastAPI(title="Infinum Legal Advisor Chatbot")

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Legal Advisor API is running"}
