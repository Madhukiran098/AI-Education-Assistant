from fastapi import FastAPI
from pydantic import BaseModel

from workflows.workflow import AgentWorkflow

app = FastAPI(title="Enterprise AI Agent Engine")


class TaskRequest(BaseModel):
    task: str


workflow = AgentWorkflow()


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Agent Engine API is running"
    }


@app.post("/run")
def run_agent(request: TaskRequest):

    result = workflow.run(request.task)

    return {
        "task": request.task,
        "plan": result["plan"],
        "research": result["research"],
        "analysis": result["analysis"],
        "decision": result["decision"]
    }