from fastapi.testclient import TestClient

from api.main import app


def test_selected_calculation_tool_preserves_operator_precedence():
    response = TestClient(app).post(
        "/tools/run-selected",
        json={
            "tool_name": "calculation",
            "request": "20 * 30 + 20",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["result"] == 620
    assert response.json()["answer"] == "The calculation result is 620."


def test_selected_calculation_tool_accepts_calculate_prefix():
    response = TestClient(app).post(
        "/tools/run-selected",
        json={
            "tool_name": "calculation",
            "request": "calculate 20*30+20",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["result"] == 620