"""
Fast Planner Agent
"""


class PlannerAgent:
    """Fast rule-based planning agent"""

    def __init__(self):
        self.name = "Planner Agent"

    def create_plan(self, user_request):

        request = user_request.strip()

        return (
            "As a Planner Agent, I have created the following execution plan:\n\n"
            f"Task: {request}\n\n"
            "Step 1: Understand the user's request.\n"
            "Step 2: Identify the information or data required.\n"
            "Step 3: Select and execute the appropriate project tool.\n"
            "Step 4: Analyze the gathered information.\n"
            "Step 5: Generate a recommendation or decision.\n"
            "Step 6: Prepare the final response for the user."
        )


if __name__ == "__main__":

    agent = PlannerAgent()

    request = "How can AI improve business decision making?"

    result = agent.create_plan(request)

    print("\n===== PLANNER AGENT =====")
    print(result)