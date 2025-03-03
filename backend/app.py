from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, List, Optional, Any

# Load environment variables
load_dotenv()

app = FastAPI(title="Personal LLM Hub")

# CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for API requests/responses
class ChatRequest(BaseModel):
    chatbot_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Load chatbot configurations
def load_chatbots() -> List[Dict[str, Any]]:
    config_path = Path(__file__).parent.parent / "config" / "chatbots.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading chatbot configurations: {e}")
        return []

# Routes
@app.get("/")
async def read_root():
    return {"status": "API is running"}

@app.get("/chatbots")
async def get_chatbots():
    """Return list of available chatbots"""
    chatbots = load_chatbots()
    # Remove system prompts for frontend display
    safe_chatbots = []
    for bot in chatbots:
        safe_bot = bot.copy()
        if "system_prompt" in safe_bot:
            del safe_bot["system_prompt"]
        safe_chatbots.append(safe_bot)
    return safe_chatbots

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return the response"""
    try:
        # Get chatbot configuration
        chatbots = load_chatbots()
        chatbot = next((bot for bot in chatbots if bot["id"] == request.chatbot_id), None)
        
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        
        # Import the appropriate provider module
        if chatbot["provider"] == "anthropic":
            from llm_providers.anthropic import get_response
        elif chatbot["provider"] == "openai":
            from llm_providers.openai import get_response
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {chatbot['provider']}")
        
        # Generate response
        response = get_response(
            message=request.message,
            system_prompt=chatbot["system_prompt"],
            model=chatbot["model"],
            parameters=chatbot.get("parameters", {})
        )
        
        # In a real implementation, you would store the conversation
        conversation_id = request.conversation_id or "new_conversation_id"
        
        return {
            "response": response,
            "conversation_id": conversation_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)