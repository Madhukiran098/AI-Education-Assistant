from typing import Any, Dict

from langsmith import traceable

from workflows.workflow_v3 import m3_workflow


@traceable(name="M3-Career-Workflow")
def run_m3_workflow(state: Dict[str, Any]):
    return m3_workflow.invoke(state)
