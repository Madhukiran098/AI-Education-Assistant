from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from prompts.prompts import DECISION_PROMPT


class DecisionAgent:
    def __init__(self):
        self.name = "Decision Agent"

        self.prompt = PromptTemplate(
            template=DECISION_PROMPT,
            input_variables=["analysis"]
        )

        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

    def make_decision(self, analysis_result):
        analysis = analysis_result["analysis"]

        formatted_prompt = self.prompt.format(
            analysis=analysis
        )

        response = self.llm.invoke(formatted_prompt)

        return {
            "topic": analysis_result["topic"],
            "decision": response.content
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