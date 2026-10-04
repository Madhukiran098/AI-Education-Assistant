# AI Agent Coordination & Decision Engine

> A multi-agent AI education and career guidance platform for intelligent decision support, tool integration, personalized career guidance, memory management, workflow automation, and college analytics.

## Project Overview

The platform uses four specialized agents: Planner, Research, Analysis, and Decision. It provides student education and career support together with college administration and business analytics.

## Milestones

### M1 – Agent Environment Setup & Foundation Development
- Multi-agent architecture
- Planner, Research, Analysis and Decision agents
- Streamlit dashboard
- FastAPI backend foundation

### M2 – Tool Integration & Intelligent Action Execution

The platform contains **9 registered tools: 5 active and 4 inactive/planned**.

| Tool | Status |
|---|---|
| Communication | Active |
| Data Retrieval | Active |
| Data Validation | Active |
| Report Generation | Active |
| Study Planner | Active |
| Calculation | Inactive / Planned |
| Web Search | Inactive / Planned |
| Email | Inactive / Planned |
| Calendar | Inactive / Planned |

### M3 – Agent Coordination & Memory Management
- Personalized career guidance
- Career research and analysis
- Preview recommendations
- Personalized roadmap generation
- Student memory
- Purchase verification and access control
- ₹150 personalized roadmap purchase

### M4 – Workflow Automation & Decision Intelligence
- College Admin Dashboard
- Student statistics
- Free vs paid student analysis
- Conversion and revenue analysis
- Response-time and failure-rate monitoring
- College catalog management
- Career trends and communication logs
- ₹5,000/year college subscription model

## Backend API

FastAPI: http://127.0.0.1:8002

Main endpoints:
- GET /health
- POST /run
- GET /tools
- POST /tools/execute
- GET /history
- GET /statistics

## Applications

- M1/M2 Student Platform: http://localhost:8503
- M3 Student Career Guidance: http://localhost:8501
- M4 College Admin Dashboard: http://localhost:8502

## Technology Stack

- Backend: FastAPI
- Frontend: Streamlit
- Language: Python
- Testing: Pytest
- API: REST
- Memory: Local persistent storage / vector memory
- Deployment: Docker

## Testing

Automated tests cover agents, APIs, tools, request validation, M3 workflows, college administration, performance, and selected tool APIs.

**Latest validation: 18 passed, 2 warnings.**

Run:

`powershell
python -m pytest tests\ -q
`

## Project Structure

`	ext
enterprise-ai-agent-engine/
├── agents/
├── api/
├── tools/
├── workflows/
├── tests/
├── streamlit_app.py
├── m3_student_app.py
├── college_admin_dashboard.py
├── memory_store.py
├── career_rag_memory.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
`

## Documentation

- DEMO_STEPS.md
- EVALUATION_REPORT.md
- MILESTONE_3_4.md
- SUBMISSION_CHECKLIST.md
- M1_M2_M3_CONNECTION.md

Evidence screenshots are included for the completed milestones.

## Author

**Madhukiran098**

AI Agent Coordination & Decision Engine
