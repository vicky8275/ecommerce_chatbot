from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chatbot import ChatBot
from database import seed_database
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting E-Commerce Chatbot...")
    seed_database()
    print("✓ Chatbot ready!")
    yield
    # Shutdown (if needed)
    pass

app = FastAPI(title="E-Commerce Chatbot API", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = ChatBot()

class ChatMessage(BaseModel):
    message: str
    context: dict = None

class ChatResponse(BaseModel):
    response: str
    needs_escalation: bool

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Serve the chat interface"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()



@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message"""
    try:
        result = chatbot.process_message(message.message, message.context)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
