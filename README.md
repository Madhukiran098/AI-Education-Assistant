# AI Agent Coordination & Decision Engine

> A multi-agent AI education and career guidance platform for intelligent decision support, tool integration, personalized career guidance, memory management, workflow automation, and college analytics.

## Project Overview

The platform uses four specialized agents: Planner, Research, Analysis, and Decision. It provides student education and career support together with college administration and business analytics.

## Milestones

### M1 - Student Platform and Agent Foundation
- Existing Streamlit student application with login, student profile, and AI Assistant experience.
- Foundational Planner, Research, Analysis, and Decision agents.
- Student chat and related guidance flows remain part of the existing project.

### M2 - Tool Integration and Intelligent Execution
- FastAPI backend and workflow-based request handling.
- Tool registry and selection logic for study planning, data retrieval, and calculations.
- Automated tests for API behavior, request validation, tool selection, and workflow execution.

#### Current Student Chatbot Tool Registry

The current registry registers these three tools:

| Tool key | Purpose |
|---|---|
| `data_retrieval` | Retrieve relevant data |
| `study_planner` | Support study-plan requests |
| `calculation` | Handle calculation requests |

Other tool classes are imported in the registry module but are not registered by its current `_register_tools()` method. Registration does not by itself guarantee that every tool is enabled.

### M3 - Career Guidance and Memory
- Career-guidance workflow with planning, research, analysis, and decision stages.
- Career roadmap generation and retrieval of previous guidance where supported by the existing implementation.
- SQLite-backed student and career data, with ChromaDB-backed context retrieval where configured.
- The Rs. 150 roadmap purchase is a simulated academic-project payment flow, not a verified real payment.

### M4 - College Administration, Analytics, and Monitoring
- College administration and catalogue management through the existing admin components.
- SQLite-backed catalogue access shared with career research.
- Workflow monitoring and API health endpoints.
- Existing project tests include college administration, API, and performance smoke coverage.

### Current Integration Notes
- The intended student experience is the combined chatbot in `website/app.py`.
- Supporting API, workflow, and legacy Streamlit entry points remain in the repository; their presence does not mean they have all been merged or removed.
- Keep `college_admin.db` and `student_data.db` separate. Do not seed, overwrite, or reset existing catalogue or student records during documentation or UI integration work.
- Local verification is not proof of production or cloud deployment.

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

- **Combined student interface:** `website/app.py` - the intended single-chatbot student experience.
- **Supporting backend API:** `http://127.0.0.1:8002` when the FastAPI service is running.
- **Legacy/supporting Streamlit entry points:** M3 student and college administration apps remain in the repository. Their presence does not mean they are all part of the active combined interface.
- Local ports depend on which entry point is launched; do not assume every app is running simultaneously.

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

**Latest local test run: 18 passed, 2 dependency deprecation warnings.**

Run:

```powershell
python -m pytest tests\ -q
```

## Project Structure

```text
AI-Education-Assistant/
  website/
    app.py
    shared_database.py
  enterprise-ai-agent-engine/
    agents/
    api/
    tools/
    workflows/
    tests/
    streamlit_app.py
    m3_student_app.py
    college_admin_dashboard.py
    memory_store.py
    career_rag_memory.py
    requirements.txt
    Dockerfile
    docker-compose.yml
  requirements.txt
  README.md
```

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

