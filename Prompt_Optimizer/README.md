# Adaptive Prompt Optimizer

A tool that optimizes prompts for specific AI coding tools using Gemini LLM.

## Features

- Optimize prompts for 6+ AI coding tools (GitHub Copilot, Cursor, Replit, CodeWhisperer, etc.)
- Tool-specific optimization strategies
- Web interface for prompt input/output
- Detailed explanations of optimizations made

## Tech Stack

- **Frontend**: React with Material-UI
- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini 1.5 Pro

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- Google Gemini API key

### Backend Setup

1. Install Python dependencies:
   ```
   pip install fastapi uvicorn google-generativeai pydantic
   ```

2. Set your Gemini API key:
   ```
   export GEMINI_API_KEY="your-api-key"
   ```

3. Run the FastAPI server:
   ```
   python app.py
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

## Usage

1. Enter your base prompt in the input field
2. Select the target AI coding tool
3. Add any additional context (optional)
4. Click "Optimize Prompt"
5. View the optimized prompt and explanation

## Project Structure

- `app.py`: FastAPI backend server
- `optimizers/`: Tool-specific optimization modules
- `tool_analysis.json`: Tool capabilities and best practices
- `src/`: React frontend code

## License

MIT 