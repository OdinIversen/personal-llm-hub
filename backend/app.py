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
    provider_id: str
    instruction_id: str
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Load configurations
def load_providers() -> List[Dict[str, Any]]:
    config_path = Path(__file__).parent.parent / "config" / "providers.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading provider configurations: {e}")
        return []

def load_instructions() -> List[Dict[str, Any]]:
    config_path = Path(__file__).parent.parent / "config" / "instructions.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading instruction configurations: {e}")
        return []

# Routes
@app.get("/api")
async def read_root():
    return {"status": "API is running"}

@app.get("/api/providers")
async def get_providers():
    """Return list of available LLM providers"""
    return load_providers()

@app.get("/api/instructions")
async def get_instructions():
    """Return list of available instruction sets"""
    return load_instructions()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return the response"""
    try:
        # Get provider configuration
        providers = load_providers()
        provider = next((p for p in providers if p["id"] == request.provider_id), None)
        
        if not provider:
            raise HTTPException(status_code=404, detail="Provider not found")
        
        # Get instruction set
        instructions = load_instructions()
        instruction = next((i for i in instructions if i["id"] == request.instruction_id), None)
        
        if not instruction:
            raise HTTPException(status_code=404, detail="Instruction set not found")
        
        # Merge parameters (instruction parameters override provider defaults)
        parameters = provider.get("default_parameters", {}).copy()
        if instruction.get("parameters"):
            parameters.update(instruction.get("parameters"))
        
        # Import the appropriate provider module
        if provider["provider"] == "anthropic":
            from llm_providers.anthropic import get_response
        elif provider["provider"] == "openai":
            from llm_providers.openai import get_response
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider['provider']}")
        
        # Generate response
        response = get_response(
            message=request.message,
            system_prompt=instruction["system_prompt"],
            model=provider["model"],
            parameters=parameters
        )
        
        # In a real implementation, you would store the conversation
        conversation_id = request.conversation_id or "new_conversation_id"
        
        return {
            "response": response,
            "conversation_id": conversation_id
        }
    
    except Exception as e:
        print(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for frontend - do this before the API routes for proper order
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)