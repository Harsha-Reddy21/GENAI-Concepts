# AI Coding Agent Recommendation System

A web application that recommends the best AI coding agents for a given task based on the task description, complexity, and requirements. Powered by Google Gemini LLM.

## Features

- Natural language task description input
- Analysis of task type, complexity, and requirements
- Recommendation of top 3 coding agents with justification
- Support for multiple AI coding agents (Copilot, Cursor, Replit, CodeWhisperer, etc.)
- Powered by Google's Gemini LLM for intelligent recommendations

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini LLM
- **Data**: JSON files for agent information

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   You can obtain a Gemini API key from the [Google AI Studio](https://ai.google.dev/).

6. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

The frontend will be available at http://localhost:3000

## Usage

1. Enter a description of your coding task in the text area
2. Optionally select the complexity and task type
3. Click "Get Recommendations"
4. View the top 3 recommended AI coding agents with explanations

## Example Tasks

- "Build a responsive e-commerce website with product catalog and shopping cart"
- "Create a machine learning model to predict customer churn"
- "Develop a mobile app for tracking fitness activities" 