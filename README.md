# AI Education Assistant – Multi-Agent Learning & Decision Engine

> A multi-agent AI education assistant that uses specialized agents for learning planning, research, analysis, and personalized recommendations.

### Architecture
User Topic -> [Research Agent] -> [Planning Agent] -> [Analysis Agent] -> [Final Decision Agent] -> Dashboard

### Key Features
- 4 Specialized AI Agents using Ollama llama3.2
- Real-time Execution Trace
- Final Decision with actionable roadmap
- FastAPI backend + Swagger Docs
- React + Vite modern dashboard

### Tech Stack
Backend: FastAPI, Ollama, Python
Frontend: React, TypeScript, Vite, Tailwind
Model: llama3.2

### How to Run
Backend:
cd enterprise-ai-agent-engine
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000

Frontend:
cd frontend
npm install
npm run dev

### API Endpoints
GET / - Health check
POST /run_agent - {"topic": "AI in Education"}

### Unit Test Plan
1. Health Endpoint - GET /
2. Research Agent - 5 points
3. Planning Agent - plan
4. Analysis Agent - analysis
5. Final Decision - final output

### Author
Madhukiran098 - AI Assistance Project
