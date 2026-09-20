import time
from typing import Dict, Any, List

from .base_tool import ToolResult
from .tool_registry import ToolRegistry


class ToolExecutor:

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.execution_history: List[Dict[str, Any]] = []

    def execute_tool(self, tool_name: str, **parameters) -> ToolResult:
        start_time = time.time()

        try:
            tool = self.tool_registry.get_tool(tool_name)

            is_valid, validation_error = tool.validate_parameters(**parameters)

            if not is_valid:
                result = ToolResult(
                    success=False,
                    error=validation_error,
                    tool_name=tool_name
                )
            else:
                result = tool.execute(**parameters)

            result.execution_time = time.time() - start_time

            self.execution_history.append({
                "tool_name": tool_name,
                "parameters": parameters,
                "success": result.success,
                "execution_time": result.execution_time
            })

            return result

        except Exception as e:
            result = ToolResult(
                success=False,
                error=str(e),
                tool_name=tool_name,
                execution_time=time.time() - start_time
            )

            self.execution_history.append({
                "tool_name": tool_name,
                "parameters": parameters,
                "success": False,
                "error": str(e),
                "execution_time": result.execution_time
            })

            return result

    def get_execution_history(self) -> List[Dict[str, Any]]:
        return self.execution_history

    def get_tool_statistics(self) -> Dict[str, Any]:
        total = len(self.execution_history)
        successful = sum(
            1 for item in self.execution_history
            if item.get("success")
        )

        return {
            "total_executions": total,
            "successful_executions": successful,
            "failed_executions": total - successful,
            "success_rate": (
                successful / total * 100
                if total > 0
                else 0
            )
        }
