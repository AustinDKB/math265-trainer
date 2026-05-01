import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestGetProblem:
    def test_basic_problem(self, client):
        resp = client.get("/api/problem?module=factoring&difficulty=1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "problemTex" in data
        assert "answerTex" in data
        assert "answerNorm" in data
        assert "steps" in data
        assert data["module"] == "factoring"
        assert data["difficulty"] == 1

    def test_all_modules(self, client):
        modules = ["factoring", "exponents", "fractions", "trig", "logs",
                    "composition", "limits", "derivatives", "integration", "adv_integration"]
        for mod in modules:
            resp = client.get(f"/api/problem?module={mod}&difficulty=1")
            assert resp.status_code == 200, f"Module {mod} returned {resp.status_code}"
            data = resp.get_json()
            assert "problemTex" in data, f"Module {mod} missing problemTex"

    def test_invalid_module(self, client):
        resp = client.get("/api/problem?module=nonexistent&difficulty=1")
        assert resp.status_code == 400

    def test_original_expanded_serialized(self, client):
        resp = client.get("/api/problem?module=factoring&difficulty=1")
        data = resp.get_json()
        if "originalExpanded" in data:
            assert isinstance(data["originalExpanded"], dict) or isinstance(data["originalExpanded"], str)
            if isinstance(data["originalExpanded"], dict):
                for key in data["originalExpanded"]:
                    assert isinstance(key, str), f"originalExpanded key {key} is not a string"

    def test_difficulty_clamp(self, client):
        resp = client.get("/api/problem?module=factoring&difficulty=99")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["difficulty"] in [1, 2, 3, 4, 5]


class TestCheckEndpoint:
    def test_correct_answer(self, client):
        resp = client.get("/api/problem?module=exponents&difficulty=1")
        problem = resp.get_json()
        check_resp = client.post("/api/check", json={
            "problem": problem,
            "input": problem.get("answerNorm", ""),
            "timeSec": 10,
        })
        assert check_resp.status_code == 200
        data = check_resp.get_json()
        assert data["result"] == "correct"

    def test_wrong_answer(self, client):
        resp = client.get("/api/problem?module=exponents&difficulty=1")
        problem = resp.get_json()
        check_resp = client.post("/api/check", json={
            "problem": problem,
            "input": "definitely_wrong_answer_xyz",
            "timeSec": 10,
        })
        assert check_resp.status_code == 200
        data = check_resp.get_json()
        assert data["result"] == "wrong"

    def test_empty_input(self, client):
        resp = client.get("/api/problem?module=exponents&difficulty=1")
        problem = resp.get_json()
        check_resp = client.post("/api/check", json={
            "problem": problem,
            "input": "",
            "timeSec": 10,
        })
        assert check_resp.status_code == 200
        data = check_resp.get_json()
        assert data["result"] == "empty"

    def test_xp_in_response(self, client):
        resp = client.get("/api/problem?module=exponents&difficulty=1")
        problem = resp.get_json()
        check_resp = client.post("/api/check", json={
            "problem": problem,
            "input": problem.get("answerNorm", ""),
            "timeSec": 10,
        })
        data = check_resp.get_json()
        assert "xpEarned" in data
        assert "totalXp" in data
        assert "level" in data


class TestAutoProblem:
    def test_auto_endpoint(self, client):
        resp = client.get("/api/problem/auto")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "problemTex" in data
        assert "module" in data
        assert "difficulty" in data


class TestStatsEndpoints:
    def test_overview(self, client):
        resp = client.get("/api/stats/overview")
        assert resp.status_code == 200

    def test_trend(self, client):
        resp = client.get("/api/stats/trend?days=7")
        assert resp.status_code == 200

    def test_weak(self, client):
        resp = client.get("/api/stats/weak?min_attempts=1&limit=5")
        assert resp.status_code == 200


class TestXP:
    def test_xp_endpoint(self, client):
        resp = client.get("/api/xp")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "totalXp" in data
        assert "level" in data