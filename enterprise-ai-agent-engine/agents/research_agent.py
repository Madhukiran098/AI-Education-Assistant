import re
from tools.tool_registry import get_registry
from college_admin_dashboard import search_colleges


class ResearchAgent:
    """Research education and career information from local project data."""

    def __init__(self, tool_registry=None, college_db_path=None):
        self.name = "Research Agent"
        self.role = "Information Retriever"
        self.tool_registry = tool_registry or get_registry()
        self.college_db_path = college_db_path

    def research(self, planner_result):
        if isinstance(planner_result, str):
            request = planner_result.strip()
            plan = planner_result.strip()
        else:
            planner_result = planner_result or {}
            request = str(planner_result.get("query", "")).strip()
            plan = str(planner_result.get("plan", "")).strip()

        if not request:
            return {
                "agent": self.name,
                "role": self.role,
                "topic": "",
                "information": "No student request was provided.",
                "research_requirements": [],
                "source_tools": ["College Catalog", "Data Retrieval"],
                "tool_results": {},
                "next_agent": "Analysis Agent",
            }

        lower_request = request.lower()

        requirements = [
            "Relevant education or career information",
            "Eligibility and qualification requirements",
            "Available options and their key differences",
        ]

        needs_college_research = "mpc" in lower_request or any(word in lower_request for word in [
            "college", "colleges", "university", "universities"
        ])

        if needs_college_research:
            requirements.extend([
                "Relevant college or university options",
                "Course availability",
                "Fee structure",
                "Admission or eligibility details",
            ])

        if any(word in lower_request for word in [
            "career", "job", "profession", "employment"
        ]):
            requirements.extend([
                "Career scope and opportunities",
                "Required skills and qualifications",
                "Relevant job roles",
            ])

        if any(word in lower_request for word in [
            "fee", "fees", "cost", "affordable", "low fee"
        ]):
            requirements.append("Fee comparison and affordability information")

        data_retrieval_result = self._run_data_retrieval(request)
        college_results = []
        if needs_college_research:
            college_results = search_colleges(
                request,
                db_path=self.college_db_path,
            )

        tool_results = {
            "Data Retrieval": data_retrieval_result,
            "College Catalog": college_results,
        }

        data = getattr(data_retrieval_result, "data", None) or {}
        records = college_results or data.get("records", [])
        if records:
            college_summary = "\n".join(
                (
                    f'- {college["name"]} | {college["course"]} | '
                    f'Fees: '
                    f'{f"Rs. {college["fees"]:,.0f}" if college.get("fees") is not None else "not listed"} | '
                    f'Placement: '
                    f'{f"{college["placement"]:.0f}%" if college.get("placement") is not None else "not listed"} | '
                    f'{college["location"]}'
                )
                for college in records
            )
        else:
            college_summary = "No matching college records were found in the catalog."

        name_match = re.search(r"\b(?:my name is|i am|i'm|this is)\s+([A-Za-z][A-Za-z .'-]{0,39})", request, re.IGNORECASE)
        display_name = name_match.group(1).strip().rstrip(".") if name_match else "Student"

        information = (
            f"Research prepared for: {display_name}\n\n"
            "College options retrieved from the local College Admin catalog:\n"
            f"{college_summary}\n\n"
            "Research requirements:\n"
            + "\n".join(f"- {item}" for item in requirements)
            + f"\n\nPlanner context:\n{plan}"
        )

        return {
            "agent": self.name,
            "role": self.role,
            "topic": request,
            "information": information,
            "research_requirements": requirements,
            "source_tools": ["College Catalog", "Data Retrieval"],
            "tool_results": tool_results,
            "planner_output": planner_result,
            "next_agent": "Analysis Agent",
        }

    def _run_web_search(self, request):
        try:
            tool = self.tool_registry.get_tool("web_search")
            result = tool.execute(
                query=request,
                max_results=5,
                search_type="web",
                language="en",
            )
            data = getattr(result, "data", None) or {}
            if data.get("source") == "simulated_web_search":
                return {
                    "status": "not_configured",
                    "message": (
                        "Live web search is not configured. "
                        "Use the college catalog results for verified project data."
                    ),
                    "results": [],
                }
            return result
        except Exception as exc:
            return {
                "success": False,
                "error": f"Web Search execution failed: {exc}",
            }

    def _run_data_retrieval(self, request):
        try:
            tool = self.tool_registry.get_tool("data_retrieval")
            return tool.execute(
                source="database",
                query="colleges " + request,
                limit=10,
            )
        except Exception as exc:
            return {
                "success": False,
                "error": f"Data Retrieval execution failed: {exc}",
            }

    @staticmethod
    def _format_tool_result(result):
        if hasattr(result, "model_dump"):
            return str(result.model_dump())

        if hasattr(result, "dict"):
            return str(result.dict())

        return str(result)







