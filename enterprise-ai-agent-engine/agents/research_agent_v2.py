from typing import Dict, Any
from agents.research_agent import ResearchAgent


class ToolAwareResearchAgent(ResearchAgent):

    def __init__(self):
        super().__init__()

    def research(self, task: str, tools: Any = None) -> Dict[str, Any]:
        result = super().research(task)

        if isinstance(result, dict):
            result["tools_used"] = tools if tools else []

        return result
