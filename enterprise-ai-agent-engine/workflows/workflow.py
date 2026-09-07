from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent


class AgentWorkflow:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.analyzer = AnalysisAgent()
        self.decision_maker = DecisionAgent()

    def run(self, user_request):

        print("\n===== AI AGENT WORKFLOW =====")

        # 1. Planner Agent
        print("\n[1] Planner Agent")
        plan = self.planner.create_plan(user_request)
        print(plan)

        # 2. Research Agent
        print("\n[2] Research Agent")
        research_result = self.researcher.research(user_request)
        print(research_result["information"])

        # 3. Analysis Agent
        print("\n[3] Analysis Agent")
        analysis_result = self.analyzer.analyze(research_result)
        print(analysis_result["analysis"])

        # 4. Decision Agent
        print("\n[4] Decision Agent")
        decision_result = self.decision_maker.make_decision(
            analysis_result
        )
        print(decision_result["decision"])

        return {
            "plan": plan,
            "research": research_result,
            "analysis": analysis_result,
            "decision": decision_result
        }


if __name__ == "__main__":

    workflow = AgentWorkflow()

    request = "How can AI improve business decision making?"

    result = workflow.run(request)

    print("\n===== FINAL RESULT =====")
    print(result["decision"]["decision"])