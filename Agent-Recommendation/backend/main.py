from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List, Dict, Any
import os
from engine import recommend_agents
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Coding Agent Recommendation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load agent data
def load_agents():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data", "agents.json")
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading agent data: {e}")
        return []

# Data models
class TaskRequest(BaseModel):
    description: str
    complexity: str = None  # Optional: "low", "medium", "high"
    task_type: str = None   # Optional: "web", "data", "mobile", etc.

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to AI Coding Agent Recommendation API"}

@app.get("/agents")
def get_all_agents():
    agents = load_agents()
    return {"agents": agents}

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(task: TaskRequest):
    agents = load_agents()
    if not agents:
        raise HTTPException(status_code=500, detail="Failed to load agent data")
    
    recommendations = recommend_agents(
        agents=agents,
        task_description=task.description,
        complexity=task.complexity,
        task_type=task.task_type
    )
    
    return {"recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 