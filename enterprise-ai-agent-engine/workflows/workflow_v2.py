"""
Tool-Integrated Workflow - Workflow with tool execution support
"""

from agents.planner_agent import PlannerAgent
from agents.research_agent_v2 import ToolAwareResearchAgent
from agents.analysis_agent_v2 import AnalysisAgentV2
from agents.decision_agent import DecisionAgent
from tools.tool_executor import ToolExecutor
from tools.tool_selector import ToolSelector
from tools.tool_factory import get_tool_registry
from typing import Dict, Any
from agents.response_generator import HumanReadableResponseGenerator
from agents.response_generator import HumanReadableResponseGenerator


class ToolIntegratedWorkflow:
    """Workflow that incorporates tool usage throughout the pipeline"""

    def __init__(self):
        # Tool infrastructure (initialize first)
        self.tool_registry = get_tool_registry()
        self.tool_executor = ToolExecutor(self.tool_registry)
        self.tool_selector = ToolSelector(self.tool_registry)
        
        # Agents with tool integration
        self.planner = PlannerAgent()
        self.researcher = ToolAwareResearchAgent()
        self.analyzer = AnalysisAgentV2(self.tool_registry)
        self.decision_maker = DecisionAgent()
        self.response_generator = HumanReadableResponseGenerator()

        self.execution_trace = []

    def run(self, user_request: str) -> Dict[str, Any]:
        """Execute workflow with tool integration"""

        print("\n===== AI AGENT WORKFLOW WITH TOOL INTEGRATION =====")

        self.execution_trace = []

        # Step 1: Planning
        print("\n[STEP 1] PLANNER AGENT")
        plan = self.planner.create_plan(user_request)
        print(plan)

        self.execution_trace.append({
            "step": "Planning",
            "agent": "Planner",
            "status": "completed"
        })

        # Step 2: Research
        print("\n[STEP 2] RESEARCH AGENT WITH TOOLS")
        research_result = self.researcher.research(user_request)
        print(
            f"Research completed using tools: "
            f"{research_result.get('tools_used', [])}"
        )

        self.execution_trace.append({
            "step": "Research",
            "agent": "Researcher",
            "tools_used": research_result.get("tools_used", []),
            "execution_time": research_result.get("execution_time"),
            "status": "completed"
        })

        # Step 3: Intelligent Tool Selection and Execution
        print("\n[STEP 3] INTELLIGENT TOOL SELECTION AND EXECUTION")

        tool_selection = self.tool_selector.select_tool(user_request)

        tool_execution_result = None

        if tool_selection.get("success"):
            selected_tool = tool_selection.get("tool_name")
            parameters = tool_selection.get("parameters", {})

            print(f"âœ“ Selected tool: {selected_tool}")
            print(f"  Confidence: {tool_selection.get('confidence')}")
            print(f"  Reasoning: {tool_selection.get('reasoning')}")
            print(f"  Parameters: {parameters}")

            # Execute selected tool
            tool_execution_result = self.tool_executor.execute_tool(
                selected_tool,
                **parameters
            )

            if tool_execution_result.success:
                print(
                    f"âœ“ Tool executed successfully: "
                    f"{selected_tool}"
                )
                print(
                    f"  Execution time: "
                    f"{tool_execution_result.execution_time:.4f}s"
                )
            else:
                print(
                    f"âœ— Tool execution failed: "
                    f"{tool_execution_result.error}"
                )

        else:
            print(
                f"âš  Tool selection failed: "
                f"{tool_selection.get('error')}"
            )

        self.execution_trace.append({
            "step": "Tool Selection and Execution",
            "selected_tool": tool_selection.get("tool_name"),
            "confidence": tool_selection.get("confidence"),
            "parameters": tool_selection.get("parameters", {}),
            "execution_success": (
                tool_execution_result.success
                if tool_execution_result
                else False
            ),
            "status": "completed"
        })

        # Step 4: Analysis
        print("\n[STEP 4] ANALYSIS AGENT WITH TOOLS")
        analysis_result = self.analyzer.analyze(research_result)

        print(
            f"Analysis completed using tools: "
            f"{analysis_result.get('tools_used', [])}"
        )

        self.execution_trace.append({
            "step": "Analysis",
            "agent": "Analyzer",
            "tools_used": analysis_result.get("tools_used", []),
            "status": "completed"
        })

        # Step 5: Report Generation
        print("\n[STEP 5] REPORT GENERATION WITH TOOLS")

        report_result = self.tool_executor.execute_tool(
            "report_generation",
            report_type="executive",
            title="Agent Execution Report",
            data={
                "planning": plan,
                "research": research_result.get(
                    "information", ""
                )[:200],
                "analysis": analysis_result.get(
                    "analysis", ""
                )[:200]
            }
        )

        if report_result.success:
            print("âœ“ Report generated successfully")
        else:
            print(
                f"âœ— Report generation failed: "
                f"{report_result.error}"
            )

        self.execution_trace.append({
            "step": "Reporting",
            "tool": "report_generation",
            "status": "completed"
        })

        # Step 6: Decision
        print("\n[STEP 6] DECISION AGENT")

        decision_result = self.decision_maker.make_decision(
            analysis_result
        )

        print(
            decision_result["decision"][:200]
        )

        self.execution_trace.append({
            "step": "Decision",
            "agent": "Decision Maker",
            "status": "completed"
        })

        # Step 7: Communication
        print("\n[STEP 7] COMMUNICATION (Optional)")

        comm_result = self.tool_executor.execute_tool(
            "communication",
            message_type="notification",
            recipient="admin@company.com",
            subject="Workflow Execution Complete",
            message=(
                f"Workflow completed successfully. "
                f"{len(self.execution_trace)} steps executed."
            ),
            priority="normal"
        )

        if comm_result.success:
            print("âœ“ Notification sent")
        else:
            print(
                f"âœ— Communication failed: "
                f"{comm_result.error}"
            )

        # Generate final human-readable answer
        selected_tool_name = tool_selection.get("tool_name")
        tool_result_data = (
            tool_execution_result.dict()
            if tool_execution_result
            else {}
        )

        human_readable_answer = self.response_generator.generate(
            request=user_request,
            selected_tool=selected_tool_name,
            tool_result=tool_result_data
        )

        # Compile final results
        result = {
            "success": True,
            "answer": human_readable_answer,
            "request": user_request,
            "plan": plan,
            "research": research_result,
            "selected_tool": tool_selection.get("tool_name"),
            "tool_selection": tool_selection,
            "tool_execution": (
                tool_execution_result.dict()
                if tool_execution_result
                else None
            ),
            "analysis": analysis_result,
            "report": (
                report_result.data
                if report_result.success
                else None
            ),
            "decision": decision_result,
            "execution_trace": self.execution_trace,
            "tool_statistics": (
                self.tool_executor.get_tool_statistics()
            )
        }

        # Include study plan directly when StudyPlannerTool was used
        if (
            tool_execution_result
            and tool_execution_result.success
            and selected_tool == "study_planner"
        ):
            result["study_plan"] = tool_execution_result.data

        return result

    def get_available_tools(self) -> list:
        """Get list of available tools"""
        return self.tool_registry.list_tools()

    def execute_tool_directly(
        self,
        tool_name: str,
        **parameters
    ) -> Dict[str, Any]:
        """Execute a tool directly"""
        return self.tool_executor.execute_tool(
            tool_name,
            **parameters
        ).dict()

    def get_execution_history(self) -> list:
        """Get tool execution history"""
        return self.tool_executor.get_execution_history()


if __name__ == "__main__":
    workflow = ToolIntegratedWorkflow()

    result = workflow.run(
        "How can AI improve business decision making?"
    )

    print("\n===== EXECUTION SUMMARY =====")
    print(f"Request: {result['request']}")
    print(
        f"Steps Executed: "
        f"{len(result['execution_trace'])}"
    )
    print(
        f"Tools Used: "
        f"{result.get('tool_statistics')}"
    )

