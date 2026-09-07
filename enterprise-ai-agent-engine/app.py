from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from workflows.workflow import AgentWorkflow


app = FastAPI(
    title="AI Agent Coordination & Decision Engine",
    description="Multi-agent AI decision support system",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRequest(BaseModel):
    request: str


workflow = AgentWorkflow()


@app.get("/")
def root():
    return {
        "message": "AI Agent Coordination & Decision Engine API is running"
    }


@app.post("/run")
def run_agent(data: AgentRequest):

    result = workflow.run(data.request)

    return {
        "request": data.request,
        "plan": result["plan"],
        "research": result["research"]["information"],
        "analysis": result["analysis"]["analysis"],
        "decision": result["decision"]["decision"]
    }