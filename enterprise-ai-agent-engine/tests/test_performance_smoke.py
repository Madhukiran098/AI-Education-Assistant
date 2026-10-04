from time import perf_counter

from agents.research_agent import ResearchAgent
from college_admin_dashboard import seed_sample_colleges
from tools.data_retrieval_tool import DataRetrievalTool


def test_college_research_latency_smoke(tmp_path):
    database = tmp_path / "benchmark-colleges.db"
    seed_sample_colleges(database)
    retrieval_tool = DataRetrievalTool(college_db_path=database)

    class TestRegistry:
        def get_tool(self, name):
            if name == "data_retrieval":
                return retrieval_tool
            raise LookupError(name)

    agent = ResearchAgent(
        tool_registry=TestRegistry(),
        college_db_path=database,
    )
    started = perf_counter()
    result = agent.research("Best career after MPC with 85% marks")
    elapsed = perf_counter() - started

    assert len(result["tool_results"]["College Catalog"]) == 4
    assert elapsed < 5.0