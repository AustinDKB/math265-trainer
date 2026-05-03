import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import trig_circle, derivatives, factoring, limits, integration_basic
from checker_registry import get_checker


class TestTrigFlags:
    def test_trig_factoring_flag_accepted(self):
        checker = get_checker("derivatives")
        problem = {
            "problemTex": r"Factor \(\sin(2x)\) using double angle",
            "answerTex": r"\(2\sin(x)\cos(x)\)",
            "answerNorm": "2*sin(x)*cos(x)",
            "isTrigFactoring": True,
            "trigFunc": "sin",
            "steps": [],
        }
        result = checker(problem, "2*sin(x)*cos(x)")
        assert result.get("result") == "correct", "trig factoring answer rejected"

    def test_trig_factoring_validNorms(self):
        checker = get_checker("derivatives")
        problem = {
            "problemTex": r"Factor \(\sin(2x)\)",
            "answerTex": r"\(2\sin(x)\cos(x)\)",
            "answerNorm": "2*sin(x)*cos(x)",
            "validNorms": ["2*sin(x)*cos(x)", "sin(2*x)"],
            "isTrigFactoring": True,
            "steps": [],
        }
        result = checker(problem, "sin(2*x)")
        assert result.get("result") == "correct", "valid alternate trig form rejected"


class TestValidForms:
    def test_validNorms_alternate_accepted_limits(self):
        checker = get_checker("limits")
        problem = {
            "problemTex": r"Find limit",
            "answerTex": r"2",
            "answerNorm": "2",
            "validNorms": ["2", "1+1"],
            "steps": [],
        }
        result = checker(problem, "1+1")
        assert result.get("result") == "correct", "validNorms alternate rejected"


class TestUndefinedDne:
    def test_limits_dne_accepted(self):
        checker = get_checker("limits")
        problem = {
            "problemTex": r"Find \(\lim_{x\to\infty} \sin(x)\)",
            "answerTex": r"does not exist",
            "answerNorm": "dne",
            "steps": [],
        }
        result = checker(problem, "dne")
        assert result.get("result") == "correct", "dne not accepted for limits"

    def test_limits_undefined_accepted_when_answerNorm_undefined(self):
        checker = get_checker("limits")
        problem = {
            "problemTex": r"Find limit",
            "answerTex": r"undefined",
            "answerNorm": "undefined",
            "steps": [],
        }
        r1 = checker(problem, "undefined")
        r2 = checker(problem, "dne")
        assert r1.get("result") == "correct"
        assert r2.get("result") == "correct"


class TestTolerance:
    def test_fraction_tolerance(self):
        checker = get_checker("fractions")
        problem = {
            "problemTex": r"Simplify \(\frac{6}{8}\)",
            "answerTex": r"\(\frac{3}{4}\)",
            "answerNorm": "3/4",
            "steps": [],
        }
        result = checker(problem, "0.75")
        assert result.get("result") == "correct", "decimal equivalent rejected"
