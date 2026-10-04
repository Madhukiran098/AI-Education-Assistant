from fastapi.testclient import TestClient

import api.main as api_main
from monitoring import monitoring_summary


def test_m3_career_endpoint_invokes_workflow(monkeypatch):
    class FakeWorkflow:
        def invoke(self, state):
            assert state["student_request"] == "Best career after MPC"
            assert state["is_paid_user"] is False
            return {
                "workflow_status": "free_payment_required",
                "decision_data": {"decision": "Personalized roadmap"},
                "preview_answer": "Career preview",
                "purchase_required": True,
                "purchase_amount": 150.0,
                "agent_timings": {"Research": 0.02},
                "messages": [],
                "errors": [],
            }

    monkeypatch.setattr(api_main, "m3_workflow", FakeWorkflow())
    response = TestClient(api_main.app).post(
        "/career/run",
        json={"student_request": "Best career after MPC"},
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "Personalized roadmap"
    assert response.json()["purchase_required"] is True


def test_m3_career_endpoint_validates_input():
    response = TestClient(api_main.app).post(
        "/career/run",
        json={"student_request": "x"},
    )

    assert response.status_code == 422


def test_monitoring_summary_aggregates_without_request_contents():
    summary = monitoring_summary(
        [
            {"status": "success", "time_taken": 0.1, "student_request": "private"},
            {"status": "failed", "time_taken": 0.3, "student_request": "secret"},
        ]
    )

    assert summary == {
        "total_events": 2,
        "successful_events": 1,
        "failed_events": 1,
        "average_execution_seconds": 0.2,
        "p95_execution_seconds": 0.3,
    }
    assert "student_request" not in summary