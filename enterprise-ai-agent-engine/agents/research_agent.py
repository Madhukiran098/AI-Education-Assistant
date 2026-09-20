class ResearchAgent:
    """Fast rule-based research agent for education and career requests."""

    def __init__(self):
        self.name = "Research Agent"

    def research(self, user_request):
        request = user_request.strip()

        lower_request = request.lower()

        if "career" in lower_request:
            information = (
                "AI can support students in career selection by analyzing "
                "their interests, skills, academic background, and career goals. "
                "It can provide career recommendations, identify skill gaps, "
                "suggest suitable learning paths, and help students compare "
                "different career options. AI should be used as decision support "
                "along with the student's own interests and guidance from educators."
            )

        elif "study" in lower_request or "python" in lower_request:
            information = (
                "AI can help students create personalized study plans, "
                "identify learning gaps, recommend resources, generate practice "
                "questions, and track learning progress."
            )

        elif "education" in lower_request or "student" in lower_request:
            information = (
                "AI can support education through personalized learning, "
                "academic assistance, study planning, skill assessment, "
                "content recommendations, and progress analysis."
            )

        else:
            information = (
                "The Research Agent analyzed the request and identified "
                "the key information required to provide an appropriate "
                "education or career recommendation."
            )

        return {
            "topic": request,
            "information": information
        }


if __name__ == "__main__":
    agent = ResearchAgent()

    request = "How can AI improve business decision making?"

    result = agent.research(request)

    print("\n===== RESEARCH AGENT =====")
    print(result["information"])
