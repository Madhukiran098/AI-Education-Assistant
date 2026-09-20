from typing import Dict, Type

from tools.base_tool import BaseTool
from tools.calculation_tool import CalculationTool
from tools.communication_tool import CommunicationTool
from tools.data_retrieval_tool import DataRetrievalTool
from tools.data_validation_tool import DataValidationTool
from tools.report_generation_tool import ReportGenerationTool
from tools.study_planner_tool import StudyPlannerTool
from tools.web_search_tool import WebSearchTool
from tools.email_tool import EmailTool
from tools.calendar_tool import CalendarTool


class ToolRegistry:

    def __init__(self):
        self.tools: Dict[str, Type[BaseTool]] = {}
        self._register_tools()

    def _register_tools(self):

        self.register("calculation", CalculationTool)
        self.register("communication", CommunicationTool)
        self.register("data_retrieval", DataRetrievalTool)
        self.register("data_validation", DataValidationTool)
        self.register("report_generation", ReportGenerationTool)
        self.register("study_planner", StudyPlannerTool)
        self.register("web_search", WebSearchTool)

        # Milestone 2 - Additional Action Tools
        self.register("email", EmailTool)
        self.register("calendar", CalendarTool)

    def register(
        self,
        name: str,
        tool_class: Type[BaseTool]
    ):
        self.tools[name] = tool_class

    def get_tool(self, name: str) -> BaseTool:

        if name not in self.tools:
            raise ValueError(
                f"Tool '{name}' not found in registry. "
                f"Available tools: {list(self.tools.keys())}"
            )

        return self.tools[name]()

    def get_all_tools(self) -> Dict[str, Type[BaseTool]]:
        return self.tools.copy()

    def get_enabled_tools(self) -> Dict[str, BaseTool]:

        enabled_tools = {}

        for name, tool_class in self.tools.items():

            tool = tool_class()

            if tool.enabled:
                enabled_tools[name] = tool

        return enabled_tools

    def list_tools(self) -> list:
        return list(self.tools.keys())

    def get_tool_info(self, name: str) -> dict:

        if name not in self.tools:
            raise ValueError(
                f"Tool '{name}' not found in registry"
            )

        tool_instance = self.tools[name]()

        return {
            "name": name,
            "description": tool_instance.description,
            "category": tool_instance.category
        }

    def get_tools_by_category(
        self,
        category: str
    ) -> Dict[str, Type[BaseTool]]:

        result = {}

        for name, tool_class in self.tools.items():

            tool_instance = tool_class()

            if tool_instance.category == category:
                result[name] = tool_class

        return result


_registry = None


def get_registry() -> ToolRegistry:

    global _registry

    if _registry is None:
        _registry = ToolRegistry()

    return _registry