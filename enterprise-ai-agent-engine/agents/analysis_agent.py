class AnalysisAgent:
    """Fast rule-based analysis agent for education and career requests."""

    def __init__(self, tool_registry=None):
        self.name = "Analysis Agent"
        self.tool_registry = tool_registry

    def analyze(self, research_result):
        research_information = research_result.get("information", "")
        topic = research_result.get("topic", "")

        lower_topic = topic.lower()

        if "career" in lower_topic:
            analysis = (
                "**Analysis and Insights**\n\n"
                "The research indicates that AI can support students in making "
                "career decisions through personalized recommendations and "
                "skill analysis.\n\n"
                "**Key Insights:**\n\n"
                "1. **Career Recommendations**: AI can analyze interests, skills, "
                "academic background, and career goals.\n\n"
                "2. **Skill-Gap Identification**: AI can identify skills that "
                "students need to develop for selected careers.\n\n"
                "3. **Personalized Learning Paths**: AI can suggest courses, "
                "resources, and learning paths based on student needs.\n\n"
                "4. **Decision Support**: AI can help students compare career "
                "options, while the final decision remains with the student.\n\n"
                "**Recommendation:** Use AI as a career decision-support system "
                "combined with guidance from educators and career counselors."
            )

        elif "study" in lower_topic or "python" in lower_topic:
            analysis = (
                "**Analysis and Insights**\n\n"
                "AI can improve study effectiveness by creating personalized "
                "plans, identifying learning gaps, recommending resources, "
                "and supporting continuous practice.\n\n"
                "**Recommendation:** Use a structured study plan with regular "
                "practice, revision, and progress tracking."
            )

        elif "education" in lower_topic or "student" in lower_topic:
            analysis = (
                "**Analysis and Insights**\n\n"
                "AI can support students through personalized learning, "
                "academic assistance, skill assessment, and progress analysis.\n\n"
                "**Recommendation:** Combine AI assistance with teacher guidance "
                "and regular student feedback."
            )

        else:
            analysis = (
                "**Analysis and Insights**\n\n"
                "The available research information was reviewed and the key "
                "requirements of the user's request were identified.\n\n"
                "**Recommendation:** Use the identified information to provide "
                "a practical and user-focused response."
            )

        return {
            "topic": topic,
            "analysis": analysis
        }


if __name__ == "__main__":
    agent = AnalysisAgent()

    research_result = {
        "topic": "AI in business decision making",
        "information": "AI can improve business decision making through data analysis."
    }

    result = agent.analyze(research_result)

    print("\n===== ANALYSIS AGENT =====")
    print(result["analysis"])
