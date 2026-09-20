# AI Education Assistant – Multi-Agent Learning & Decision Engine

> A multi-agent AI education assistant that uses specialized agents for learning planning, research, analysis, and personalized recommendations.

### Architecture
User Topic -> [Research Agent] -> [Planning Agent] -> [Analysis Agent] -> [Final Decision Agent] -> Dashboard

### Key Features
- 4 Specialized AI Agents using Ollama llama3.2
- Real-time Execution Trace
- Final Decision with actionable roadmap
- FastAPI backend + Swagger Docs
  

### Tech Stack
Backend: FastAPI, Ollama, Python
Frontend: Streamlit
Model: llama3.2
Testing: Pytest
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
## Milestone 2 – Tool Integration & Intelligent Action Execution

Milestone 2 extends the AI Education & Career Guidance Assistant from a multi-agent decision-support platform into a tool-enabled AI assistance system.

### M2 Capabilities

* Intelligent tool selection based on user intent
* Automated tool execution
* Human-readable AI responses
* Education and career support
* Local Ollama AI processing
* FastAPI backend integration
* Streamlit user interface

### 9 Integrated Tools

1. **Calculation** – Performs mathematical calculations.
2. **Communication** – Creates clear communication messages.
3. **Data Retrieval** – Retrieves configured information.
4. **Data Validation** – Validates user-provided information.
5. **Report Generation** – Generates structured reports.
6. **Study Planner** – Creates personalized study plans.
7. **Web Search** – Processes research and information requests.
8. **Email** – Prepares email communication.
9. **Calendar** – Checks and manages meeting requests.

### M2 Processing Flow

```text
User Request
     ↓
Planner Agent
     ↓
Research Agent
     ↓
Analysis Agent
     ↓
Decision Agent
     ↓
Tool Selection
     ↓
Tool Execution
     ↓
Human-Readable Response
     ↓
Streamlit Dashboard
```

### M2 Example Requests

* `Calculate 25% of 800.`
* `Create a 5-day study plan for learning Python.`
* `How can AI help students choose the right career?`
* `Generate a report on the importance of AI in education.`
* `Check whether this email address is valid.`
* `Prepare an email to my mentor requesting a project review.`
* `Check whether a project meeting is available tomorrow at 4 PM.`

### M2 Technology Stack

```text
Backend: FastAPI, Python
Frontend: Streamlit
AI Engine: Ollama
Model: llama3.2
Testing: Pytest
```

### Unit Test Plan
1. Health Endpoint - GET /
2. Research Agent - 5 points
3. Planning Agent - plan
4. Analysis Agent - analysis
5. Final Decision - final output

### Author
Madhukiran098 - AI Assistance Project
