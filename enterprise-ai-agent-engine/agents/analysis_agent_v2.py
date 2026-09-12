"""
Analysis Agent v2 - Enhanced analysis with tool integration
"""

from typing import Dict, Any
import time

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from prompts.prompts import ANALYSIS_PROMPT
from tools.tool_registry import ToolRegistry
from tools.tool_selector import ToolSelector
from tools.tool_executor import ToolExecutor


class AnalysisAgentV2:
    """Enhanced Analysis Agent with tool integration support"""

    def __init__(self, tool_registry: ToolRegistry = None):
        self.name = "Analysis Agent v2"

        self.prompt = PromptTemplate(
            template=ANALYSIS_PROMPT,
            input_variables=["research_information"]
        )

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

        # Tool integration
        self.tool_registry = tool_registry

        if self.tool_registry:
            self.tool_selector = ToolSelector(self.tool_registry)
            self.tool_executor = ToolExecutor(self.tool_registry)
        else:
            self.tool_selector = None
            self.tool_executor = None

        self.execution_history = []

    def analyze(
        self,
        research_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform analysis with tool support.

        Args:
            research_result: Research data to analyze

        Returns:
            Analysis result with tool execution metadata
        """

        start_time = time.time()

        try:
            research_information = research_result.get(
                "information",
                ""
            )

            topic = research_result.get(
                "topic",
                "Unknown"
            )

            # -------------------------------------------------
            # Step 1: LLM-based analysis
            # -------------------------------------------------

            print(
                f"\n[Analysis Agent] Analyzing: {topic}"
            )

            formatted_prompt = self.prompt.format(
                research_information=research_information
            )

            response = self.llm.invoke(
                formatted_prompt
            )

            analysis_content = response.content

            # -------------------------------------------------
            # Step 2: Intelligent tool selection
            # -------------------------------------------------

            tools_used = []
            tool_selection = None
            tool_execution_result = None

            if self.tool_selector and self.tool_executor:

                print("\n[Analysis Tool Selection]")

                tool_selection = (
                    self.tool_selector.select_tool(
                        f"Provide deeper analysis and calculate "
                        f"relevant insights for: {topic}"
                    )
                )

                if tool_selection.get("success"):

                    selected_tool = (
                        tool_selection.get("tool_name")
                    )

                    parameters = (
                        tool_selection.get(
                            "parameters",
                            {}
                        )
                    )

                    print(
                        f"Selected tool: {selected_tool}"
                    )

                    print(
                        f"Confidence: "
                        f"{tool_selection.get('confidence')}"
                    )

                    print(
                        f"Reasoning: "
                        f"{tool_selection.get('reasoning')}"
                    )

                    print(
                        f"Parameters from selector: "
                        f"{parameters}"
                    )

                    # -------------------------------------------------
                    # Step 3: Prepare safe parameters
                    # -------------------------------------------------

                    tool_parameters = parameters.copy()

                    # CalculationTool
                    if selected_tool == "calculation":

                        if "operation" not in tool_parameters:
                            tool_parameters["operation"] = "average"

                        if "values" not in tool_parameters:
                            tool_parameters["values"] = [1, 2, 3]

                    # DataValidationTool
                    elif selected_tool == "data_validation":

                        if "data" not in tool_parameters:
                            tool_parameters["data"] = topic

                        if "validation_type" not in tool_parameters:
                            tool_parameters[
                                "validation_type"
                            ] = "text"

                    # DataRetrievalTool
                    elif selected_tool == "data_retrieval":

                        if "source" not in tool_parameters:
                            tool_parameters[
                                "source"
                            ] = "database"

                        if "query" not in tool_parameters:
                            tool_parameters[
                                "query"
                            ] = topic

                    # WebSearchTool
                    elif selected_tool == "web_search":

                        if "query" not in tool_parameters:
                            tool_parameters[
                                "query"
                            ] = topic

                    print(
                        f"Final tool parameters: "
                        f"{tool_parameters}"
                    )

                    # -------------------------------------------------
                    # Step 4: Execute selected tool
                    # -------------------------------------------------

                    print(
                        f"\n[Analysis Tool Execution] "
                        f"Executing {selected_tool}"
                    )

                    tool_execution_result = (
                        self.tool_executor.execute_tool(
                            selected_tool,
                            **tool_parameters
                        )
                    )

                    if tool_execution_result.success:

                        print(
                            "Tool execution successful"
                        )

                        tools_used.append(
                            selected_tool
                        )

                    else:

                        print(
                            f"Tool execution failed: "
                            f"{tool_execution_result.error}"
                        )

                else:

                    print(
                        f"Tool selection failed: "
                        f"{tool_selection.get('error')}"
                    )

            # -------------------------------------------------
            # Step 5: Build result
            # -------------------------------------------------

            execution_time = (
                time.time() - start_time
            )

            result = {
                "topic": topic,
                "analysis": analysis_content,
                "tools_used": tools_used,
                "tool_selection": tool_selection,
                "tool_execution": (
                    tool_execution_result.dict()
                    if tool_execution_result
                    else None
                ),
                "execution_time": execution_time,
                "depth_level": (
                    "enhanced"
                    if tools_used
                    else "standard"
                )
            }

            # -------------------------------------------------
            # Step 6: Execution history
            # -------------------------------------------------

            self.execution_history.append({
                "timestamp": time.time(),
                "topic": topic,
                "tools_used": tools_used,
                "execution_time": execution_time
            })

            return result

        except Exception as e:

            return {
                "topic": research_result.get(
                    "topic",
                    "Unknown"
                ),
                "analysis": (
                    f"Error during analysis: {str(e)}"
                ),
                "tools_used": [],
                "tool_selection": None,
                "tool_execution": None,
                "execution_time": (
                    time.time() - start_time
                ),
                "depth_level": "error",
                "error": str(e)
            }

    def get_execution_history(self) -> list:
        """Get execution history"""

        return self.execution_history

    def clear_history(self):
        """Clear execution history"""

        self.execution_history = []


# -------------------------------------------------------------
# Backward compatibility
# -------------------------------------------------------------

class AnalysisAgent:
    """Analysis Agent (backward compatible)"""

    def __init__(self):
        self.agent_v2 = AnalysisAgentV2()
        self.name = "Analysis Agent"

    def analyze(self, research_result):
        """Legacy interface"""

        result = self.agent_v2.analyze(
            research_result
        )

        return {
            "topic": result["topic"],
            "analysis": result["analysis"]
        }


# -------------------------------------------------------------
# Direct test
# -------------------------------------------------------------

if __name__ == "__main__":

    from tools.tool_factory import get_tool_registry

    registry = get_tool_registry()

    agent = AnalysisAgentV2(
        tool_registry=registry
    )

    research_result = {
        "topic": "AI in business decision making",
        "information": """
        AI can improve business decision making through
        predictive analytics, automation, pattern recognition,
        and data analysis.
        """
    }

    result = agent.analyze(
        research_result
    )

    print(
        "\n===== ANALYSIS AGENT V2 ====="
    )

    print(
        f"Topic: {result['topic']}"
    )

    print(
        f"\nAnalysis:\n{result['analysis']}"
    )

    print(
        f"\nTools Used: "
        f"{result['tools_used']}"
    )

    print(
        f"\nTool Execution: "
        f"{result['tool_execution']}"
    )

    print(
        f"\nExecution Time: "
        f"{result['execution_time']:.4f}s"
    )

    print(
        f"Depth Level: "
        f"{result['depth_level']}"
    )