from typing import List, Dict, Any
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

def recommend_agents(agents: List[Dict[str, Any]], task_description: str, 
                    complexity: str = None, task_type: str = None) -> List[Dict[str, Any]]:

    
    if not GEMINI_API_KEY:
        return fallback_recommend_agents(agents, task_description, complexity, task_type)
    

    prompt = create_gemini_prompt(agents, task_description, complexity, task_type)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        recommendations = parse_gemini_response(response.text, agents)
        print('recommendations', recommendations)
        return recommendations
    except Exception as e:
        print(f"Error using Gemini API: {e}")

        return fallback_recommend_agents(agents, task_description, complexity, task_type)

def create_gemini_prompt(agents: List[Dict[str, Any]], task_description: str, 
                        complexity: str = None, task_type: str = None) -> str:
    agents_info = ""
    for i, agent in enumerate(agents, 1):
        agents_info += f"Agent {i}: {agent['name']}\n"
        agents_info += f"Description: {agent['description']}\n"
        agents_info += f"Strengths: {', '.join(agent['strengths'])}\n"
        agents_info += f"Best for: {', '.join(agent['best_for'])}\n"
        agents_info += f"Integration: {', '.join(agent['integration'])}\n"
        agents_info += f"Learning curve: {agent['learning_curve']}\n"
        agents_info += f"Cost: {agent['cost']}\n\n"
    
    # Build the prompt
    prompt = f"""
    You are an expert system that recommends the most suitable AI coding agents for specific programming tasks.
    
    Here is information about available AI coding agents:
    
    {agents_info}
    
    Task description: {task_description}
    """
    
    if complexity:
        prompt += f"\nTask complexity: {complexity}"
    
    if task_type:
        prompt += f"\nTask type: {task_type}"
    
    prompt += """
    
    Based on the task description and the information about the AI coding agents, recommend the top 3 most suitable agents for this task.
    
    For each recommendation, provide:
    1. The agent name
    2. A score between 0 and 1 indicating how well the agent matches the task (higher is better)
    3. A list of 2-3 specific reasons why this agent is recommended for this task
    
    Format your response as follows:
    
    RECOMMENDATION 1:
    Agent: [agent name]
    Score: [score between 0 and 1]
    Reasons:
    - [reason 1]
    - [reason 2]
    - [reason 3]
    
    RECOMMENDATION 2:
    Agent: [agent name]
    Score: [score between 0 and 1]
    Reasons:
    - [reason 1]
    - [reason 2]
    - [reason 3]
    
    RECOMMENDATION 3:
    Agent: [agent name]
    Score: [score between 0 and 1]
    Reasons:
    - [reason 1]
    - [reason 2]
    - [reason 3]
    """
    
    return prompt

def parse_gemini_response(response_text: str, agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    recommendations = []

    sections = response_text.split("RECOMMENDATION")
    for section in sections[1:4]: 
        try:
            lines = section.strip().split("\n")
            agent_line = next((line for line in lines if line.strip().startswith("Agent:")), "")
            agent_name = agent_line.split(":", 1)[1].strip() if agent_line else ""
            agent_data = next((agent for agent in agents if agent['name'].lower() == agent_name.lower()), None)
            if not agent_data:
                continue

            score_line = next((line for line in lines if line.strip().startswith("Score:")), "")
            try:
                score = float(score_line.split(":", 1)[1].strip()) if score_line else 0.5
                score = min(max(score, 0), 1)  
            except:
                score = 0.5

            reasons = []
            reason_section_started = False
            for line in lines:
                if "Reasons:" in line:
                    reason_section_started = True
                    continue
                if reason_section_started and line.strip().startswith("-"):
                    reasons.append(line.strip()[1:].strip())
            
            recommendations.append({
                "agent": agent_data,
                "score": score,
                "justification": reasons if reasons else ["Recommended by AI analysis."]
            })
            
        except Exception as e:
            print(f"Error parsing recommendation: {e}")
            continue

    if len(recommendations) < 3:
        remaining = fallback_recommend_agents(agents, "", None, None)
        for rec in remaining[:3-len(recommendations)]:
            if not any(r['agent']['name'] == rec['agent']['name'] for r in recommendations):
                recommendations.append(rec)
    
    return recommendations[:3] 

def fallback_recommend_agents(agents: List[Dict[str, Any]], task_description: str, 
                             complexity: str = None, task_type: str = None) -> List[Dict[str, Any]]:
    """Simple fallback recommendation method when Gemini API is not available"""
    import random
    shuffled_agents = random.sample(agents, len(agents))
    
    recommendations = []
    for agent in shuffled_agents[:3]:
        score = random.uniform(0.7, 0.95)  
        justification = [
            f"Good match for your task requirements.",
            f"Integrates with {', '.join(agent.get('integration', [])[:2])}."
        ]
        
        if agent.get('best_for'):
            justification.append(f"Particularly good for {agent.get('best_for')[0]}.")
        
        recommendations.append({
            "agent": agent,
            "score": score,
            "justification": justification
        })
    
    return recommendations 