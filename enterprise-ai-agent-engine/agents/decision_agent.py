class DecisionAgent:
    def __init__(self):
        self.name = "Decision Agent"

    def make_decision(self, analysis_result):
        analysis = analysis_result.get("analysis", "")
        topic = analysis_result.get("topic", "Unknown topic")

        # Generate a fast decision from the analysis
        if not analysis:
            decision = "No analysis was available to make a decision."

        elif any(word in analysis.lower() for word in [
            "recommend",
            "should",
            "benefit",
            "improve",
            "effective",
            "use"
        ]):
            decision = (
                f"Recommendation: Use the identified insights for '{topic}'. "
                "The analysis indicates that the proposed approach can provide "
                "practical benefits when implemented with appropriate monitoring "
                "and evaluation."
            )

        else:
            decision = (
                f"Decision: Based on the analysis of '{topic}', "
                "the identified findings can be considered for practical "
                "implementation after further evaluation."
            )

        return {
            "topic": topic,
            "decision": decision
        }


if __name__ == "__main__":
    agent = DecisionAgent()

    analysis_result = {
        "topic": "AI in business decision making",
        "analysis": """
        AI can improve business decision making through predictive
        analytics, automation, pattern recognition, and data analysis.
        Organizations can use AI to improve efficiency and make
        data-driven decisions.
        """
    }

    result = agent.make_decision(analysis_result)

    print("\n===== DECISION AGENT =====")
    print(result["decision"])