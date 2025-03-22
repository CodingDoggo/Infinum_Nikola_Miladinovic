from fastapi import FastAPI
from backend.api import router as chat_router
from backend.database import create_tables

app = FastAPI(title="Infinum Legal Advisor Chatbot")

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Legal Advisor API is running"}
