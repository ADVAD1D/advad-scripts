from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="ADVAD Mock AI Server")

# Data model simulating what ADVAD1D sends
class ChatRequest(BaseModel):
    message: str
    player_data: dict = {}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"Message received from game: {request.message}")
    
    # Mock responses for testing
    mock_responses = [
        "Pilot, I detect a thermal anomaly! Watch out for those asteroids.",
        "That enemy ship's shield is strong. Use your Dash!",
        "Your reflexes are acceptable, but you can improve your time.",
        "Systems online. Proceeding to the next combat phase."
    ]
    
    return {
        "response": random.choice(mock_responses),
        "status": "success",
        "mocked": True
    }

@app.get("/")
async def root():
    return {"message": "ADVAD Mock Server Online. Use /api/chat to interact."}

# USAGE INSTRUCTIONS:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run: uvicorn server:app --reload --port 10000
# 3. In Godot, point your API service to http://127.0.0.1:10000
