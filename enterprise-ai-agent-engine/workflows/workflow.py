from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent
from tools.study_planner_tool import StudyPlannerTool


class AgentWorkflow:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.analyzer = AnalysisAgent()
        self.decision_maker = DecisionAgent()
        self.study_planner = StudyPlannerTool()

    def run(self, user_request):

        print("\n===== AI AGENT WORKFLOW =====")

        # 1. Planner Agent
        print("\n[1] Planner Agent")
        plan = self.planner.create_plan(user_request)
        print(plan)

        # 2. Study Planner Tool
        study_plan_result = None

        if (
            "study plan" in user_request.lower()
            or "study schedule" in user_request.lower()
        ):
            print("\n[Tool] Study Planner Tool")

            study_plan_result = self.study_planner.execute(
                subject="Python",
                days=5
            )

            print(study_plan_result)

        # 3. Research Agent
        print("\n[2] Research Agent")
        research_result = self.researcher.research(user_request)
        print(research_result["information"])

        # 4. Analysis Agent
        print("\n[3] Analysis Agent")
        analysis_result = self.analyzer.analyze(research_result)
        print(analysis_result["analysis"])

        # 5. Decision Agent
        print("\n[4] Decision Agent")
        decision_result = self.decision_maker.make_decision(
            analysis_result
        )
        print(decision_result["decision"])

        return {
            "plan": plan,
            "study_plan": study_plan_result,
            "research": research_result,
            "analysis": analysis_result,
            "decision": decision_result
        }


if __name__ == "__main__":

    workflow = AgentWorkflow()

    request = "Create a 5-day Python study plan"

    result = workflow.run(request)

    print("\n===== FINAL RESULT =====")
    print(result["decision"]["decision"])
