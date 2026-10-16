# AI Agent Coordination & Decision Engine

> A multi-agent AI education and career guidance platform for intelligent decision support, tool integration, personalized career guidance, memory management, workflow automation, and college analytics.

## Project Overview

The platform uses four specialized agents: Planner, Research, Analysis, and Decision. It provides student education and career support together with college administration and business analytics.

## Official Project Scope

**Project title:** AI Agent Coordination & Decision Engine

**Aim:** Develop coordinated specialized AI agents for enterprise workflows, information retrieval, analysis, decision support, task execution and response generation using LLMs, orchestration frameworks, memory and tool integrations.

**Expected outcomes:** Multi-Agent Coordination Framework; Intelligent Decision Support; Tool & System Integration; Shared Knowledge & Memory Management; Workflow Automation Platform; Enterprise API Layer.

### Milestone 1 — Agent Environment Setup & Foundation Development
Establish the development environment, LLM and orchestration foundations, agent architecture, prompting and workflows. Implement and test foundational agents and their interactions.

### Milestone 2 — Tool Integration & Intelligent Action Execution
Integrate tools, APIs, databases and external knowledge sources. Support tool selection and execution, monitoring, validation and error handling.

### Milestone 3 — Agent Coordination & Memory Management
Coordinate Planning, Research, Analysis and Decision agents, including agent communication and short-term, long-term and shared memory capabilities where implemented.

### Milestone 4 — Workflow Automation, Decision Intelligence, Enterprise API, Dashboard & Deployment
Orchestrate workflows and automated execution, generate recommendations and responses, provide supported REST API and dashboard functionality, and address logging, deployment, scalability and performance monitoring.

**Official schedule:** Weeks 1–2: Milestone 1; Weeks 3–4: Milestone 2; Weeks 5–6: Milestone 3; Weeks 7–8: Milestone 4 (deployment). This schedule does not imply that unfinished features or cloud deployment are complete.

## Implemented Application Features by Official Milestone

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

- PROJECT_USAGE_GUIDE.md
- EVALUATION_REPORT.md
- MILESTONE_3_4.md
- SUBMISSION_CHECKLIST.md
- M1_M2_M3_CONNECTION.md

Evidence screenshots are included for the completed milestones.

## Project Objective

The objective of the AI Education & Career Guidance Assistant is to help students understand their skills, explore suitable education and career paths, compare college options, and plan their learning journey through an AI-assisted interface.

## Student Experience: One Chatbot

The intended student experience brings education and career assistance together in one chatbot. The Planner, Research, Analysis, and Decision agents coordinate behind the scenes; students receive a consolidated response instead of needing to interact with each agent separately.

### Student Flow

1. **Login and profile creation** — collect the student's name and email and save the profile persistently before proceeding.
2. **Ask a question** — the student asks about studies, skills, careers, exams, or colleges.
3. **Understand the request** — the backend routes the request to the appropriate workflow.
4. **Research and analysis** — the agents process relevant information, assess the student's requirements, and prepare recommendations.
5. **Display guidance** — the chatbot presents a consolidated answer with suitable options and explanations.
6. **Personalised roadmap** — eligible students can use the demonstration purchase flow to access the personalised roadmap.
7. **Save and revisit** — supported profile, history, and roadmap features use persistent storage.
8. **Administration and analytics** — authorised administrators manage college catalogue records and review available statistics.

### Request Routing

| Request type | Backend route |
| --- | --- |
| Study planning and study-tool requests | `POST /tools/run-selected` |
| Career guidance requests | `POST /career/run` |
| Other general requests | `POST /run` |

These routes describe the intended routing contract. Verify the active endpoint implementation before treating every route as integrated into the chatbot.

## Milestone Progression

- **M1 — Foundation:** core agents, student interface, and FastAPI foundation.
- **M2 — Tool integration:** request routing, tool selection, execution, and consolidated responses.
- **M3 — Personalised career guidance:** career research, recommendations, memory, and roadmap generation.
- **M4 — Administration and analytics:** college catalogue management, student/business statistics, monitoring, and reporting.

The milestone progression describes how the project evolves toward the integrated experience. Existing standalone pages or workflows should be identified as such until their integration is verified.

## Data and Payment Notes

- Keep `college_admin.db` and `student_data.db` separate; do not overwrite existing college catalogue or student records when documenting or testing the project.
- College fees, placement figures, and other catalogue values are stored data and should not be presented as independently verified facts unless separately confirmed.
- The ₹150 roadmap purchase is a simulated academic-project payment flow, not a verified real payment.
- Distinguish implemented and tested features from planned or pending integration.

## Author
**Madhukiran098**

AI Agent Coordination & Decision Engine
