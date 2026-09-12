"""
Tool-Aware Research Agent - Research agent with tool integration
"""

from typing import Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from tools.tool_selector import ToolSelector
from tools.tool_executor import ToolExecutor
from tools.tool_factory import get_tool_registry


class ToolAwareResearchAgent:
    """Research agent that can select and use tools"""

    def __init__(self):
        self.name = "Tool-Aware Research Agent"

        # Initialize tool infrastructure
        self.tool_registry = get_tool_registry()
        self.tool_selector = ToolSelector(self.tool_registry)
        self.tool_executor = ToolExecutor(self.tool_registry)

        # LLM for research synthesis
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.3
        )

        self.research_prompt = PromptTemplate(
            template="""Based on the following information gathered, provide a comprehensive research summary:

Topic: {topic}
Gathered Information: {gathered_info}

Provide:
1. Key findings
2. Relevant data points
3. Insights and patterns
4. Sources and reliability assessment

Research Summary:""",
            input_variables=["topic", "gathered_info"]
        )

    def research(self, topic: str) -> Dict[str, Any]:
        """
        Conduct research with tool assistance.

        Args:
            topic: Research topic

        Returns:
            Research results with tool usage
        """

        print(f"\n[Research Agent] Starting research on: {topic}")

        # ---------------------------------------------------------
        # Step 1: Intelligent tool selection
        # ---------------------------------------------------------
        print("\n[Tool Selection]")

        tool_selection = self.tool_selector.select_tool(
            f"Find information and data about {topic}"
        )

        if not tool_selection.get("success"):
            print(
                f"Tool selection failed: "
                f"{tool_selection.get('error')}"
            )

            return {
                "topic": topic,
                "information": f"Could not complete research on {topic}",
                "tools_used": [],
                "tool_results": None,
                "execution_time": 0
            }

        selected_tool = tool_selection.get("tool_name")
        parameters = tool_selection.get("parameters", {})

        print(f"Selected tool: {selected_tool}")
        print(f"Confidence: {tool_selection.get('confidence')}")
        print(f"Reasoning: {tool_selection.get('reasoning')}")
        print(f"Parameters from selector: {parameters}")

        # ---------------------------------------------------------
        # Step 2: Prepare parameters according to selected tool
        # ---------------------------------------------------------

        if selected_tool == "web_search":
            # WebSearchTool requires query
            tool_parameters = {
                "query": parameters.get("query", topic),
                "search_type": parameters.get("search_type", "web"),
                "limit": parameters.get("limit", 10),
                "language": parameters.get("language", "en")
            }

        elif selected_tool == "data_retrieval":
            # DataRetrievalTool requires source and query
            tool_parameters = {
                "source": parameters.get("source", "database"),
                "query": parameters.get("query", topic),
                "filters": parameters.get("filters", {}),
                "limit": parameters.get("limit", 100)
            }

        else:
            # Generic fallback for other tools
            tool_parameters = parameters.copy()

            if not tool_parameters:
                tool_parameters["query"] = topic

        print(f"Final tool parameters: {tool_parameters}")

        # ---------------------------------------------------------
        # Step 3: Execute selected tool
        # ---------------------------------------------------------
        print(f"\n[Tool Execution] Executing {selected_tool}")

        tool_result = self.tool_executor.execute_tool(
            selected_tool,
            **tool_parameters
        )

        if not tool_result.success:
            print(
                f"Tool execution failed: "
                f"{tool_result.error}"
            )

            gathered_info = (
                f"Error gathering information: "
                f"{tool_result.error}"
            )

        else:
            print("Tool execution successful")

            gathered_info = str(tool_result.data)

        # ---------------------------------------------------------
        # Step 4: Research synthesis using LLM
        # ---------------------------------------------------------
        print("\n[Research Synthesis]")

        formatted_prompt = self.research_prompt.format(
            topic=topic,
            gathered_info=gathered_info
        )

        response = self.llm.invoke(formatted_prompt)

        return {
            "topic": topic,
            "information": response.content,
            "tools_used": [selected_tool],
            "tool_selection": tool_selection,
            "tool_results": (
                tool_result.data
                if tool_result.success
                else None
            ),
            "execution_time": tool_result.execution_time,
            "tool_execution_success": tool_result.success
        }


if __name__ == "__main__":

    agent = ToolAwareResearchAgent()

    result = agent.research(
        "machine learning applications in business"
    )

    print("\n===== TOOL-AWARE RESEARCH AGENT =====")
    print(f"Topic: {result['topic']}")
    print(f"Tools Used: {result['tools_used']}")
    print(
        f"\nTool Execution Success: "
        f"{result['tool_execution_success']}"
    )
    print(f"\nResearch:\n{result['information']}")