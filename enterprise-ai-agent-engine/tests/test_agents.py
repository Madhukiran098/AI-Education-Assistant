from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent


def test_planner_agent():
    agent = PlannerAgent()

    plan = agent.create_plan(
        "How can AI improve business decision making?"
    )

    assert len(plan) > 0


def test_research_agent():
    agent = ResearchAgent()

    result = agent.research(
        "How can AI improve business decision making?"
    )

    assert result["topic"] != ""
    assert len(result["information"]) > 0


def test_analysis_agent():
    agent = AnalysisAgent()

    research_result = {
        "topic": "AI in business decision making",
        "information": [
            "Collect important facts",
            "Identify relevant information"
        ]
    }

    result = agent.analyze(research_result)

    assert result["topic"] != ""
    assert len(result["key_points"]) > 0


def test_decision_agent():
    agent = DecisionAgent()

    analysis_result = {
        "topic": "AI in business decision making",
        "summary": "AI can support business analysis.",
        "key_points": [
            "Analyze information",
            "Evaluate options"
        ]
    }

    result = agent.make_decision(analysis_result)

    assert result["decision"] != ""
    assert result["reason"] != ""