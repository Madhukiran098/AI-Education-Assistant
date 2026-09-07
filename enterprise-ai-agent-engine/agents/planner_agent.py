from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from prompts.prompts import PLANNER_PROMPT


class PlannerAgent:
    def __init__(self):
        self.name = "Planner Agent"

        self.prompt = PromptTemplate(
            template=PLANNER_PROMPT,
            input_variables=["user_request"]
        )

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

    def create_plan(self, user_request):
        formatted_prompt = self.prompt.format(
            user_request=user_request
        )

        response = self.llm.invoke(formatted_prompt)

        return response.content


if __name__ == "__main__":
    agent = PlannerAgent()

    request = "How can AI improve business decision making?"

    result = agent.create_plan(request)

    print("\n===== PLANNER AGENT =====")
    print(result)