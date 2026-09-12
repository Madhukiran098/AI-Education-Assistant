"""
Enhanced FastAPI - AI Education & Career Guidance Assistant
Milestone 2: Tool Integration & Intelligent Action Execution
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from workflows.workflow_v2 import ToolIntegratedWorkflow


# =========================
# Request Models
# =========================

class AgentRequest(BaseModel):
    request: str


class ToolExecutionRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] = {}


# =========================
# FastAPI Application
# =========================

app = FastAPI(
    title="AI Education & Career Guidance Assistant",
    description=(
        "Multi-agent AI assistant with intelligent tool integration "
        "for education and career guidance"
    ),
    version="2.0.0"
)


# =========================
# CORS Configuration
# =========================

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


# =========================
# Create Workflow
# =========================

workflow = ToolIntegratedWorkflow()


# =========================
# Root Endpoint
# =========================

@app.get("/")
def root():
    return {
        "message": "AI Education & Career Guidance Assistant API is running",
        "version": "2.0.0",
        "features": [
            "multi-agent-orchestration",
            "tool-integration",
            "intelligent-tool-selection",
            "tool-execution",
            "decision-support"
        ]
    }


# =========================
# Run Complete Workflow
# =========================

@app.post("/run")
def run_agent(data: AgentRequest):
    try:
        result = workflow.run(data.request)

        return {
            "success": True,
            "request": data.request,

            "plan": result.get("plan"),

            "research": {
                "topic": result["research"].get("topic"),
                "tools_used": result["research"].get("tools_used", []),
                "execution_time": result["research"].get("execution_time")
            },

            "tool_selection": result.get("tool_selection"),

            "tool_execution": result.get("tool_execution"),

            "study_plan": result.get("study_plan"),

            "analysis": {
                "topic": result["analysis"].get("topic"),
                "tools_used": result["analysis"].get("tools_used", [])
            },

            "report": result.get("report"),

            "decision": result.get("decision"),

            "execution_summary": {
                "total_steps": len(result.get("execution_trace", [])),
                "execution_trace": result.get("execution_trace", []),
                "tool_statistics": result.get("tool_statistics", {})
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {str(e)}"
        )


# =========================
# List Available Tools
# =========================

@app.get("/tools")
def list_tools():
    try:
        registry = workflow.tool_registry
        tools = []

        for name in registry.list_tools():
            info = registry.get_tool_info(name)

            tools.append({
                "name": name,
                "description": info.get("description"),
                "category": (
                    info.get("category").value
                    if hasattr(info.get("category"), "value")
                    else str(info.get("category"))
                )
            })

        return {
            "success": True,
            "total_tools": len(tools),
            "tools": tools
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to list tools: {str(e)}"
        )


# =========================
# Get Specific Tool
# =========================

@app.get("/tools/{tool_name}")
def get_tool_info(tool_name: str):
    try:
        registry = workflow.tool_registry

        if tool_name not in registry.list_tools():
            raise HTTPException(
                status_code=404,
                detail=f"Tool '{tool_name}' not found"
            )

        info = registry.get_tool_info(tool_name)

        return {
            "success": True,
            "tool": {
                "name": tool_name,
                "description": info.get("description"),
                "category": (
                    info.get("category").value
                    if hasattr(info.get("category"), "value")
                    else str(info.get("category"))
                )
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to get tool information: {str(e)}"
        )


# =========================
# Direct Tool Execution
# =========================

@app.post("/tools/execute")
def execute_tool(request: ToolExecutionRequest):
    try:
        result = workflow.execute_tool_directly(
            request.tool_name,
            **request.parameters
        )

        return {
            "success": result.get("success"),
            "tool_name": request.tool_name,
            "execution_time": result.get("execution_time"),
            "data": result.get("data"),
            "error": result.get("error")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Tool execution failed: {str(e)}"
        )


# =========================
# Execution History
# =========================

@app.get("/history")
def get_execution_history(limit: Optional[int] = 50):

    history = workflow.get_execution_history()

    if limit is not None and limit > 0:
        history = history[-limit:]

    return {
        "success": True,
        "total_executions": len(history),
        "history": history
    }


# =========================
# Tool Statistics
# =========================

@app.get("/statistics")
def get_statistics():

    stats = workflow.tool_executor.get_tool_statistics()

    return {
        "success": True,
        "statistics": stats
    }


# =========================
# Calculation Tool
# =========================

@app.post("/tools/calculate")
def calculate(
    operation: str,
    values: List[float]
):

    result = workflow.execute_tool_directly(
        "calculation",
        operation=operation,
        values=values
    )

    return {
        "success": result.get("success"),
        "tool_name": "calculation",
        "operation": operation,
        "data": result.get("data"),
        "error": result.get("error")
    }


# =========================
# Data Validation Tool
# =========================

@app.post("/tools/validate")
def validate_data(
    data: str,
    validation_type: str
):

    result = workflow.execute_tool_directly(
        "data_validation",
        data=data,
        validation_type=validation_type
    )

    return {
        "success": result.get("success"),
        "tool_name": "data_validation",
        "validation_type": validation_type,
        "data": result.get("data"),
        "error": result.get("error")
    }


# =========================
# Report Generation Tool
# =========================

@app.post("/tools/report")
def generate_report(
    title: str,
    report_type: str = "summary"
):

    result = workflow.execute_tool_directly(
        "report_generation",
        title=title,
        report_type=report_type,
        data={
            "source": "AI Education & Career Guidance Assistant"
        }
    )

    return {
        "success": result.get("success"),
        "tool_name": "report_generation",
        "report_type": report_type,
        "data": result.get("data"),
        "error": result.get("error")
    }


# =========================
# Global HTTP Exception
# =========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):

    return {
        "success": False,
        "error": exc.detail
    }