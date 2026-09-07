from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from prompts.prompts import RESEARCH_PROMPT


class ResearchAgent:
    def __init__(self):
        self.name = "Research Agent"

        self.prompt = PromptTemplate(
            template=RESEARCH_PROMPT,
            input_variables=["user_request"]
        )

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

    def research(self, user_request):
        formatted_prompt = self.prompt.format(
            user_request=user_request
        )

        response = self.llm.invoke(formatted_prompt)

        return {
            "topic": user_request,
            "information": response.content
        }


if __name__ == "__main__":
    agent = ResearchAgent()

    request = "How can AI improve business decision making?"

    result = agent.research(request)

    print("\n===== RESEARCH AGENT =====")
    print(result["information"])