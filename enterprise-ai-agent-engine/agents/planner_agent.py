class PlannerAgent:
    """M3 Planner Agent - Study Plan Creator and workflow planner."""

    def __init__(self):
        self.name = "Planner Agent"
        self.role = "Study Plan Creator"

    def create_plan(self, user_request):
        request = (user_request or "").strip()

        if not request:
            return {
                "agent": self.name,
                "role": self.role,
                "query": "",
                "plan": "No student request was provided.",
                "next_agent": "Research Agent",
            }

        plan = (
            f"Student Query: {request}\n\n"
            "Execution Plan:\n"
            "1. Understand the student's education or career requirement.\n"
            "2. Identify the student information and external data required.\n"
            "3. Retrieve relevant colleges, careers, courses, fees, eligibility, "
            "scope, or other requested information.\n"
            "4. Analyze the retrieved information against the student's requirement.\n"
            "5. Prepare personalized options and supporting insights.\n"
            "6. Send the structured research requirements to the Research Agent.\n"
            "7. Send the analyzed findings to the Decision Agent for the final response "
            "and access decision."
        )

        return {
            "agent": self.name,
            "role": self.role,
            "query": request,
            "plan": plan,
            "next_agent": "Research Agent",
        }
