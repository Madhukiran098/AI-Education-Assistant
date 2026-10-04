import re
class AnalysisAgent:
    """M3 Analysis Agent - Insight Analyzer."""

    def __init__(self, tool_registry=None):
        self.name = "Analysis Agent"
        self.role = "Insight Analyzer"
        self.tool_registry = tool_registry

    def analyze(self, research_result, student_profile=None):
        research_result = research_result or {}
        student_profile = student_profile or {}

        topic = str(
            research_result.get("topic", "")
        ).strip()

        information = str(
            research_result.get("information", "")
        ).strip()

        requirements = research_result.get(
            "research_requirements",
            []
        )

        preferences = student_profile.get(
            "career_preferences",
            ""
        )

        insights = []

        if requirements:
            insights.append(
                "The requested information has been organized according to "
                "the student's requirements."
            )

        if any(word in topic.lower() for word in [
            "college", "colleges", "university", "universities"
        ]):
            insights.append(
                "College options should be compared using course availability, "
                "eligibility, fees, location, and career outcomes."
            )

        if any(word in topic.lower() for word in [
            "career", "job", "profession", "employment"
        ]):
            insights.append(
                "Career options should be evaluated using qualifications, "
                "required skills, career scope, and relevant job roles."
            )

        if any(word in topic.lower() for word in [
            "fee", "fees", "cost", "affordable", "low fee"
        ]):
            insights.append(
                "Affordability should be considered together with course quality, "
                "eligibility, and expected career value."
            )

        if preferences:
            insights.append(
                f"Student career preference context: {preferences}"
            )

        if not insights:
            insights.append(
                "The available research should be reviewed against the "
                "student's stated requirement before making a final decision."
            )

        name_match = re.search(r"\b(?:my name is|i am|i'm|this is)\s+([A-Za-z][A-Za-z .'-]{0,39})", topic, re.IGNORECASE)
        display_name = name_match.group(1).strip().rstrip(".") if name_match else "Student"

        analysis = (
            f"Analysis for: {display_name}\n\n"
            "Key Insights:\n"
            + "\n".join(f"- {item}" for item in insights)
            + "\n\n"
            "Research Information:\n"
            + (information or "No additional research information available.")
        )

        return {
            "agent": self.name,
            "role": self.role,
            "topic": topic,
            "analysis": analysis,
            "key_insights": insights,
            "research_input": research_result,
            "student_profile": student_profile,
            "next_agent": "Decision Agent",
        }






