from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from typing import List, Dict, Optional
import json

app = FastAPI(title="Adaptive Prompt Optimizer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load tool analysis data
try:
    with open("tool_analysis.json", "r") as f:
        TOOL_DATA = json.load(f)
except FileNotFoundError:
    TOOL_DATA = {}

# Configure Gemini API
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
    
genai.configure(api_key=GEMINI_API_KEY)

# Models
class OptimizationRequest(BaseModel):
    base_prompt: str
    target_tool: str
    additional_context: Optional[str] = None

class OptimizationResponse(BaseModel):
    original_prompt: str
    optimized_prompt: str
    explanation: str
    tool: str

# Routes
@app.get("/")
def read_root():
    return {"message": "Adaptive Prompt Optimizer API"}

@app.get("/tools")
def get_available_tools():
    """Return list of supported tools and their capabilities"""
    return {"tools": list(TOOL_DATA.keys())}

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_prompt(request: OptimizationRequest):
    """Optimize a prompt for a specific tool using Gemini"""
    
    if request.target_tool not in TOOL_DATA:
        raise HTTPException(status_code=404, detail=f"Tool '{request.target_tool}' not supported")
    
    tool_info = TOOL_DATA[request.target_tool]
    
    # Create prompt for Gemini
    gemini_prompt = f"""
    You are an expert prompt engineer specializing in optimizing prompts for AI coding tools.
    
    TOOL INFORMATION:
    Tool: {request.target_tool}
    Capabilities: {tool_info.get('capabilities', [])}
    Best practices: {tool_info.get('best_practices', [])}
    Limitations: {tool_info.get('limitations', [])}
    
    ORIGINAL PROMPT:
    {request.base_prompt}
    
    ADDITIONAL CONTEXT (if provided):
    {request.additional_context or 'None provided'}
    
    Please optimize this prompt specifically for {request.target_tool}, considering its unique capabilities and limitations.
    
    Return your response in the following JSON format:
    {{
        "optimized_prompt": "The optimized prompt text",
        "explanation": "Detailed explanation of changes made and why they improve effectiveness for this specific tool"
    }}
    """
    
    try:
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            # If no API key is provided, use mock responses for demonstration
            print("Using mock response as no valid API key was provided")
            
            # Generate a mock optimized prompt based on the tool
            if request.target_tool == "GitHub Copilot":
                optimized_prompt = f"// Generate a function that {request.base_prompt}\n// Use TypeScript with proper error handling"
                explanation = """
                1. Added code comment format with '// ' prefix which Copilot responds well to
                2. Specified the programming language (TypeScript) to get more precise results
                3. Requested proper error handling which leverages Copilot's code quality capabilities
                4. Structured as a function request to utilize Copilot's strength in function generation
                """
            elif request.target_tool == "Cursor":
                optimized_prompt = f"I need to {request.base_prompt}. Please explain your approach step by step and show the code implementation."
                explanation = """
                1. Added a request for step-by-step explanation which Cursor excels at providing
                2. Asked for both explanation and implementation to leverage Cursor's conversational abilities
                3. Used a clear problem statement format that Cursor responds well to
                4. Structured the prompt to encourage detailed responses which is Cursor's strength
                """
            else:
                # Generic optimization for other tools
                optimized_prompt = f"Create a well-documented implementation that {request.base_prompt}. Include comments explaining the approach and any important considerations."
                explanation = """
                1. Added request for documentation which improves code quality
                2. Asked for comments explaining the approach to get better reasoning
                3. Requested consideration of important factors to get more comprehensive results
                4. Structured as a clear implementation task with specific requirements
                """
            
            return {
                "original_prompt": request.base_prompt,
                "optimized_prompt": optimized_prompt,
                "explanation": explanation,
                "tool": request.target_tool
            }
        
        # Use the actual Gemini API if a valid key is provided
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(gemini_prompt)
        
        # Parse JSON response
        result = json.loads(response.text)
        
        return {
            "original_prompt": request.base_prompt,
            "optimized_prompt": result["optimized_prompt"],
            "explanation": result["explanation"],
            "tool": request.target_tool
        }
    except Exception as e:
        print(f"Error optimizing prompt: {str(e)}")
        # Fallback response in case of error
        return {
            "original_prompt": request.base_prompt,
            "optimized_prompt": f"Optimized for {request.target_tool}: {request.base_prompt}",
            "explanation": "The optimization service encountered an error. This is a fallback response.",
            "tool": request.target_tool
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 