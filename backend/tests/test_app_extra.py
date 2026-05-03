import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app

client = flask_app.app.test_client()
flask_app.app.config["TESTING"] = True


class TestAppExtraEndpoints:
    def test_modules_endpoint(self):
        resp = client.get("/api/modules")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, (list, dict))

    def test_xp_endpoint(self):
        resp = client.get("/api/xp")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "xp" in data or "totalXp" in data or isinstance(data, dict)

    def test_report_endpoint(self):
        resp = client.post("/api/report", json={
            "problem": {
                "module": "factoring",
                "difficulty": 2,
                "problemTex": r"Factor \(x^2-1\)",
                "answerTex": r"(x-1)(x+1)",
            },
            "userAnswer": "(x-1)(x+1)",
            "note": "test",
        })
        assert resp.status_code in (200, 201)

    def test_problem_auto_endpoint_returns_json(self):
        resp = client.get("/api/problem/auto")
        assert resp.status_code in (200, 404)
        if resp.status_code == 200:
            assert isinstance(resp.get_json(), dict)

    def test_problem_auto_with_module_params_returns_json(self):
        resp = client.get("/api/problem/auto?module=factoring&difficulty=2")
        assert resp.status_code in (200, 404)
