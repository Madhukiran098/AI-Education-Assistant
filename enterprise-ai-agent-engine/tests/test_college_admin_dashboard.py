from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.decision_agent import DecisionAgent
from college_admin_dashboard import (
    create_college,
    delete_college,
    list_colleges,
    seed_sample_colleges,
    update_college,
)
from tools.data_retrieval_tool import DataRetrievalTool


def test_college_catalog_crud_and_research(tmp_path):
    database = tmp_path / "college-test.db"
    college_id = create_college(
        "MPC Technical College",
        "MPC Engineering",
        45000,
        82,
        "Hyderabad",
        database,
    )

    colleges = list_colleges(database)
    assert len(colleges) == 1
    assert colleges[0]["id"] == college_id

    assert update_college(
        college_id,
        "MPC Technical College",
        "MPC Engineering",
        40000,
        85,
        "Hyderabad",
        database,
    )

    agent = ResearchAgent(college_db_path=database)
    agent._run_web_search = lambda request: {"success": True, "results": []}
    agent._run_data_retrieval = lambda request: {"success": True, "records": []}
    result = agent.research("Best colleges for MPC with low fees")

    matching_colleges = result["tool_results"]["College Catalog"]
    assert len(matching_colleges) == 1
    assert matching_colleges[0]["fees"] == 40000
    assert "MPC Technical College" in result["information"]

    assert delete_college(college_id, database)
    assert list_colleges(database) == []


def test_college_catalog_validates_records(tmp_path):
    database = tmp_path / "college-test.db"

    try:
        create_college("College", "Course", 1000, 101, db_path=database)
    except ValueError as exc:
        assert "between 0 and 100" in str(exc)
    else:
        raise AssertionError("Invalid placement percentage was accepted")


def test_mpc_query_retrieves_colleges_for_decision_agent(tmp_path):
    database = tmp_path / "career-colleges.db"
    seed_sample_colleges(database)
    data_tool = DataRetrievalTool(college_db_path=database)

    class TestRegistry:
        def get_tool(self, name):
            if name == "data_retrieval":
                return data_tool
            raise LookupError(f"No test tool registered for {name}")

    query = "Best career after MPC with 85 percent marks"
    direct_result = data_tool.execute(
        source="database",
        query="colleges " + query,
        limit=10,
    )
    assert direct_result.success
    assert direct_result.data["table"] == "colleges"
    assert len(direct_result.data["records"]) == 4
    assert all("department" not in row for row in direct_result.data["records"])

    research = ResearchAgent(
        tool_registry=TestRegistry(),
        college_db_path=database,
    ).research(query)
    assert "Web Search" not in research["tool_results"]
    assert "example.com" not in research["information"]
    assert "Tool Execution Results" not in research["information"]
    assert "M2 data-retrieval" not in research["information"]
    analysis = AnalysisAgent().analyze(research)
    decision = DecisionAgent().make_decision(
        analysis,
        m1_score=85,
        career_query=query,
    )["decision"]

    assert "JNTU Hyderabad" in decision
    assert "CBIT Hyderabad" in decision
    assert "OU Hyderabad" in decision
    assert "MGIT Hyderabad" in decision
    assert "Four-Year Career Roadmap" in decision
    assert "M1 TO M2 CONNECTION" not in decision
    assert "M1 Score" not in decision


def test_named_mpc_cse_request_recommends_mgit_without_inventing_metrics(tmp_path):
    database = tmp_path / "cse-colleges.db"
    seed_sample_colleges(database)
    research = ResearchAgent(college_db_path=database).research(
        "My name is Alex, I scored 85 percent in Intermediate MPC from "
        "Hyderabad. I am interested in CSE. Please generate my personalized "
        "career roadmap with best colleges including MGIT Hyderabad, skills "
        "to learn, and placement details."
    )
    analysis = AnalysisAgent().analyze(research)
    decision = DecisionAgent().make_decision(
        analysis,
        m1_score=85,
        career_query=research["topic"],
    )["decision"]

    assert "Personalized guidance for Alex" in decision
    assert "Computer Science and Engineering (CSE)" in decision
    assert "Top 3 CSE Career Paths" in decision
    assert "Cloud and Cybersecurity" in decision
    assert "MGIT Hyderabad" in decision
    assert "Java" in decision or "Python" in decision
    assert "data structures and algorithms" in decision
    assert "fees 120,000" in decision
    assert "placement 82%" in decision

