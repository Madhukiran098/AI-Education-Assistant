# Milestones 1-5: Execution Status

## M1-M5 Application Map

- M1 foundational agent page and M2 Tools Hub are in the combined Streamlit app at `http://localhost:8503`.
- The M1 page displays four foundational agents: Planner, Research, Analysis, and Decision. M3 adds the Business Coordinator to its separate five-agent LangGraph workflow.
- M2's Tools Hub lists nine registered tools. Five tools are currently active and four remain inactive/planned.
- M3 Career Guidance runs separately at `http://localhost:8501`; M4 College Admin runs at `http://localhost:8502`; the FastAPI service runs at `http://localhost:8002`.
- M2 and M3 are decoupled. M3 does not import M2 requests. Its student identity/profile fields currently use demo defaults rather than a live authenticated M1 session handoff.
- M3 Research reads the same SQLite college catalog managed by the M4 admin dashboard.

## Final Verification: 2026-10-03

The live M3 API and Streamlit application were verified using the request `Best career options after MPC with 85% marks`.

- `POST /career/run` returned `success: true` and `workflow_status: free_payment_required` for an isolated final-verification student identity.
- At the initial verification, `POST /tools/execute` returned the original three catalog entries (CBIT Hyderabad, JNTU Hyderabad, OU Hyderabad). The catalog was subsequently extended with MGIT Hyderabad CSE; the current seeded catalog has four entries.
- The Decision Agent response included the top MPC career recommendations, those same college records, entrance examinations, and the four-year roadmap.
- The Decision Agent response was checked for the previous mock employee names; none were present.
- The browser M3 flow was exercised with a fresh variant of the request because the exact query already exists in this local student's purchase history and reopens the saved purchase rather than running a new transaction.
- The combined M1/M2 Streamlit app was running at `http://localhost:8503`, the M3 student app at `http://localhost:8501`, the admin dashboard at `http://localhost:8502`, and the API at `http://localhost:8002`.

### Alex CSE Follow-up

The request `My name is Alex, I scored 85 percent in Intermediate MPC from Hyderabad. I am interested in CSE. Please generate my personalized career roadmap with best colleges including MGIT Hyderabad, skills to learn, and placement details.` was run through the Research, Analysis, and Decision agents. The output addressed Alex by name, recommended CSE-specific software, data, and cloud/cybersecurity paths, listed CSE skills and a four-year roadmap, and included MGIT Hyderabad CSE and JNTU Hyderabad CSE from SQLite. The current catalog values shown for MGIT (Rs. 120,000 fees and 82% placement) are the values stored in the admin database; they are not independently verified institutional statistics.

The browser demo continued through **Buy Personalized Roadmap - Rs. 150**, **Generate Now - Rs. 150**, payment-success confirmation, and **View My Roadmap**. This is a simulated academic-project purchase, not a real payment.

### Screenshots

Screenshots were captured from the live local Streamlit pages:

![Career Guidance Page v2.0 with the MPC request](evidence_career_guidance.png)

![M1 foundational agent framework](evidence_m1_agent_foundation.png)

![M2 Tools Hub and current active/premium access state](evidence_m2_tools_hub.png)

![Data Retrieval with college rows and Decision Agent roadmap](evidence_data_retrieval_roadmap.png)

![College Admin Dashboard analytics](evidence_college_admin_dashboard.png)

![College Catalog CRUD management view](evidence_college_catalog_crud.png)

## Milestone 3: Agent Coordination and Memory

### Implemented
- Business Coordinator validates student and institution context before handing work to the Planner.
- Planner, Research, Analysis, Decision, Business Access, and Memory Save nodes are coordinated by the LangGraph workflow in `workflows/workflow_v3.py`.
- Agent-to-agent handoffs and per-agent timings are kept in the workflow state and message log.
- Short-term working memory is carried in the workflow state for one request.
- SQLite stores career history, previous queries, student profiles, and purchased answers.
- ChromaDB stores and retrieves prior roadmap context; an LRU research cache avoids repeated research work.
- The College Admin catalog is SQLite-backed and feeds college records into Research Agent results.
- Student and administrator Streamlit interfaces use the same project data directory.

### Validation
Run from this directory:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_agents.py tests\test_college_admin_dashboard.py -q
```

## Milestone 4: Workflow API, Monitoring, and Deployment

### Implemented
- `POST /career/run` exposes the M3 LangGraph workflow through FastAPI. Example body:

```json
{
  "student_request": "Best career after MPC with 85% marks",
  "student_id": "STU029",
  "college_id": "COL002",
  "m1_score": 85
}
```

- `GET /health` is the API liveness endpoint.
- `GET /monitoring/summary` reports aggregate workflow event counts and average/p95 duration; it does not return student request text.
- The existing college admin Streamlit dashboard displays student, business, communications, and college catalog information.
- A performance smoke test checks SQLite-backed college research completes within a generous local threshold. This is a regression smoke test, not a load or capacity test.
- Docker and Compose files package the API, M3 student UI, and college admin UI with a persistent data volume.

### Local Run
From this directory, with Docker Desktop installed and running:

```powershell
docker compose up --build
```

- M3 student UI: `http://localhost:8501`
- College admin dashboard: `http://localhost:8502`
- Combined M1/M2 UI: `http://localhost:8503`
- API: `http://localhost:8002`
- API documentation: `http://localhost:8002/docs`
- Health: `http://localhost:8002/health`
- Monitoring summary: `http://localhost:8002/monitoring/summary`

Stop the containers with `docker compose down`. Keep the named `app-data` volume to retain SQLite and ChromaDB state. Removing that volume deletes local persistent data.

Without Docker, the existing Streamlit and API entry points can be run directly from this directory:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8002
.\.venv\Scripts\python.exe -m streamlit run m3_student_app.py --server.port 8501
.\.venv\Scripts\python.exe -m streamlit run college_dashboard.py --server.port 8502
```

Run the focused API, workflow, and performance checks with:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_m3_api.py tests\test_performance_smoke.py tests\test_agents.py tests\test_college_admin_dashboard.py -q
```

## Deployment Readiness and Remaining Work

The Compose setup is a reproducible local/container deployment target. It is not evidence that the service has been deployed to a cloud account. Cloud rollout still requires a selected provider, account credentials, a managed persistent relational database and vector store, TLS and domain configuration, secrets management, backups, and an authentication/authorization policy.

Docker verification for this submission was not executable in the available environment: the Docker CLI/daemon is not installed. The Compose YAML was parsed successfully, but that does not substitute for an image build or container health check. Run `docker compose up --build` on a machine with Docker Desktop installed and running before container acceptance.

Do not expose the current API or demo payment workflow directly to the public internet. The current college subscription/payment verification and sample student identities are demonstration logic. Before production, add identity and tenant authorization, payment-provider verification, request rate limits, durable managed storage, and load testing with an agreed latency/concurrency target. Local SQLite and file-backed ChromaDB should not be shared by horizontally scaled replicas.

## Performance Follow-up

`tests/test_performance_smoke.py` protects the local catalog research path from severe regressions. Before cloud acceptance, run a load test against the deployed environment, set explicit p95 latency and concurrency objectives, and compare CPU, memory, database latency, and workflow traces under expected peak load.
