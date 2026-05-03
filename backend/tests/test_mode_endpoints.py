import pytest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as flask_app

client = flask_app.app.test_client()
flask_app.app.config["TESTING"] = True


class TestModeEndpoints:
    def test_justify_mode_accepts_nonempty_input(self):
        problem = {
            "problemTex": r"Explain why \(f(x) = x^2\) has a minimum at \(x=0\)",
            "answerTex": r"Because \(f'(0)=0\) and \(f''(0)>0\)",
            "mode": "justify",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "justify",
            "userInput": "Because the derivative is zero and second derivative is positive",
            "problem": problem,
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["result"] == "correct"

    def test_justify_mode_rejects_empty_input(self):
        problem = {
            "problemTex": r"Explain why...",
            "answerTex": r"...",
            "mode": "justify",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "justify",
            "userInput": "",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "wrong"
        assert data["reason"] == "empty_input"

    def test_backwards_mode_accepts_nonempty_input(self):
        problem = {
            "problemTex": r"What function has derivative \(2x\) and passes through (0,1)?",
            "answerTex": r"\(f(x) = x^2 + 1\)",
            "mode": "backwards",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "backwards",
            "userInput": "x^2 + 1",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "correct"

    def test_derive_mode_accepts_nonempty_input(self):
        problem = {
            "problemTex": r"Derive the formula for the area of a circle",
            "answerTex": r"\(A = \pi r^2\)",
            "mode": "derive",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "derive",
            "userInput": "Integrate 2*pi*r to get pi*r^2",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "correct"

    def test_break_mode_error_type_match(self):
        problem = {
            "problemTex": r"Find \(\frac{d}{dx}[x^3 + 2x]\)",
            "answerTex": r"\(3x^2 + 2\)",
            "answerNorm": "3*x^2+2",
            "modeData": {
                "error": {
                    "type": "power_rule",
                    "description": "Applied power rule incorrectly to x^3",
                }
            },
            "mode": "break",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "break",
            "selectedError": "power_rule",
            "userFix": "3*x^2+2",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "correct"

    def test_break_mode_error_type_mismatch(self):
        problem = {
            "problemTex": r"Find derivative",
            "answerTex": r"answer",
            "modeData": {
                "error": {"type": "power_rule"}
            },
            "mode": "break",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "break",
            "selectedError": "wrong_error_type",
            "userFix": "",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "wrong"
        assert data["reason"] == "error_type_mismatch"

    def test_break_mode_fix_incorrect(self):
        problem = {
            "problemTex": r"Find derivative",
            "answerTex": r"3*x^2+2",
            "answerNorm": "3*x^2+2",
            "modeData": {"error": {"type": "power_rule"}},
            "mode": "break",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "break",
            "selectedError": "power_rule",
            "userFix": "wrong_answer",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "wrong"
        assert data["reason"] == "fix_incorrect"

    def test_solve_mode_falls_back_to_check_answer(self):
        problem = {
            "module": "factoring",
            "problemTex": r"Factor \(x^2 - 1\)",
            "answerTex": r"(x-1)(x+1)",
            "answerNorm": "(x-1)(x+1)",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "solve",
            "userInput": "(x-1)(x+1)",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "correct", f"expected correct but got {data}"

    def test_mode_endpoint_returns_modelAnswer(self):
        problem = {
            "problemTex": r"Explain why...",
            "answerTex": r"\(f(x) = x^2 + 1\)",
            "mode": "justify",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "justify",
            "userInput": "some reasoning",
            "problem": problem,
        })
        data = resp.get_json()
        assert "modelAnswer" in data
        assert data["modelAnswer"] == r"\(f(x) = x^2 + 1\)"

    def test_mode_endpoint_unknown_mode_falls_to_solve(self):
        problem = {
            "module": "factoring",
            "problemTex": r"Factor",
            "answerTex": r"(x-1)(x+1)",
            "answerNorm": "(x-1)(x+1)",
        }
        resp = client.post("/api/check/mode", json={
            "mode": "unknown_mode",
            "userInput": "(x-1)(x+1)",
            "problem": problem,
        })
        data = resp.get_json()
        assert data["result"] == "correct", f"expected correct but got {data}"
