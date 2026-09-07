from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from prompts.prompts import ANALYSIS_PROMPT


class AnalysisAgent:
    def __init__(self):
        self.name = "Analysis Agent"

        self.prompt = PromptTemplate(
            template=ANALYSIS_PROMPT,
            input_variables=["research_information"]
        )

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

    def analyze(self, research_result):
        research_information = research_result["information"]

        formatted_prompt = self.prompt.format(
            research_information=research_information
        )

        response = self.llm.invoke(formatted_prompt)

        return {
            "topic": research_result["topic"],
            "analysis": response.content
        }


if __name__ == "__main__":
    agent = AnalysisAgent()

    research_result = {
        "topic": "AI in business decision making",
        "information": """
        AI can improve business decision making through predictive
        analytics, automation, pattern recognition, and data analysis.
        """
    }

    result = agent.analyze(research_result)

    print("\n===== ANALYSIS AGENT =====")
    print(result["analysis"])