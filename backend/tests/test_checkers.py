import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import factoring

from checker import (
    check_answer, check_dual_answer, check_factoring_answer,
    check_exponent_answer, check_fraction_answer, check_norm_answer,
    check_integration_answer, check_exp_factoring_answer,
    check_trig_factoring_answer,
)


class TestCheckFactoringAnswer:
    def test_correct_factored_form(self):
        problem = {
            "module": "factoring",
            "originalExpanded": {0: -6, 1: -1, 2: 1},
            "isGrouping": False,
            "isQuadDisguise": False,
        }
        result = check_factoring_answer(problem, "(x+2)(x-3)")
        assert result["result"] == "correct"

    def test_expanded_not_factored(self):
        problem = {
            "module": "factoring",
            "originalExpanded": {0: -6, 1: -1, 2: 1},
            "isGrouping": False,
            "isQuadDisguise": False,
        }
        result = check_factoring_answer(problem, "x^2-x-6")
        assert result["result"] == "partial"

    def test_wrong_answer(self):
        problem = {
            "module": "factoring",
            "originalExpanded": {0: -6, 1: -1, 2: 1},
            "isGrouping": False,
            "isQuadDisguise": False,
        }
        result = check_factoring_answer(problem, "(x+5)(x-7)")
        assert result["result"] == "wrong"

    def test_empty_input(self):
        problem = {"module": "factoring"}
        result = check_answer(problem, "")
        assert result["result"] == "empty"

    def test_grouping_flag(self):
        problem = {
            "module": "factoring",
            "originalExpanded": "x^3+x^2+2x+2",
            "isGrouping": True,
            "isQuadDisguise": False,
        }
        result = check_factoring_answer(problem, "x^3+x^2+2x+2")
        assert result["result"] == "correct"


class TestCheckExponentAnswer:
    def test_correct_simple(self):
        problem = {"module": "exponents", "answerNorm": "x^6"}
        result = check_exponent_answer(problem, "x^6")
        assert result["result"] == "correct"

    def test_negative_exponent_reciprocal(self):
        problem = {"module": "exponents", "answerNorm": "x^(-2)"}
        result = check_exponent_answer(problem, "1/x^2")
        assert result["result"] == "correct"

    def test_wrong(self):
        problem = {"module": "exponents", "answerNorm": "x^6"}
        result = check_exponent_answer(problem, "x^5")
        assert result["result"] == "wrong"


class TestCheckFractionAnswer:
    def test_correct_fraction(self):
        problem = {"module": "fractions", "answerNorm": "3/4"}
        result = check_fraction_answer(problem, "6/8")
        assert result["result"] == "correct"

    def test_integer_equiv(self):
        problem = {"module": "fractions", "answerNorm": "2"}
        result = check_fraction_answer(problem, "2")
        assert result["result"] == "correct"


class TestCheckNormAnswer:
    def test_correct_exact(self):
        problem = {"module": "trig", "answerNorm": "1/2"}
        result = check_norm_answer(problem, "1/2")
        assert result["result"] == "correct"

    def test_undefined_variants(self):
        problem = {"module": "limits", "answerNorm": "undefined"}
        for inp in ["undefined", "dne", "doesnotexist"]:
            result = check_norm_answer(problem, inp)
            assert result["result"] == "correct"

    def test_valid_norms(self):
        problem = {"module": "trig", "answerNorm": "sin=1/2,cos=sqrt(3)/2",
                    "validNorms": ["sin=1/2,cos=sqrt(3)/2"]}
        result = check_norm_answer(problem, "sin=1/2,cos=sqrt(3)/2")
        assert result["result"] == "correct"

    def test_numeric_equality(self):
        problem = {"module": "limits", "answerNorm": "1/2"}
        result = check_norm_answer(problem, "0.5")
        assert result["result"] == "correct"

    def test_wrong(self):
        problem = {"module": "trig", "answerNorm": "1/2"}
        result = check_norm_answer(problem, "3/4")
        assert result["result"] == "wrong"


class TestCheckIntegrationAnswer:
    def test_strips_plus_c(self):
        problem = {"module": "integration", "answerNorm": "x^2/2+C"}
        result = check_integration_answer(problem, "x^2/2")
        assert result["result"] == "correct"

    def test_with_plus_c(self):
        problem = {"module": "integration", "answerNorm": "x^2/2+C"}
        result = check_integration_answer(problem, "x^2/2+C")
        assert result["result"] == "correct"

    def test_diverges(self):
        problem = {"module": "adv_integration", "answerNorm": "diverges"}
        result = check_integration_answer(problem, "dne")
        assert result["result"] == "correct"


class TestCheckDualAnswer:
    def test_both_correct(self):
        problem = {
            "module": "derivatives",
            "answerNorm": "2*x",
            "answerNorm2": "2",
        }
        result = check_dual_answer(problem, "2x", "2")
        assert result["result"] == "correct"

    def test_one_wrong(self):
        problem = {
            "module": "derivatives",
            "answerNorm": "2*x",
            "answerNorm2": "2",
        }
        result = check_dual_answer(problem, "2x", "99")
        assert result["result"] == "wrong"
        assert 2 in result["wrongSlot"]

    def test_empty(self):
        problem = {"module": "derivatives", "requiresDualAnswer": True}
        result = check_answer(problem, "")
        assert result["result"] == "empty"


class TestCheckExpFactoringAnswer:
    def test_valid_form(self):
        problem = {
            "module": "factoring",
            "isFracExpGcf": True,
            "validForms": ["x^(1/2)(x+1)(x-1)", "x^(1/2)(x-1)(x+1)", "(x+1)(x-1)x^(1/2)"],
            "answerTex": "x^{1/2}(x+1)(x-1)",
        }
        result = check_exp_factoring_answer(problem, "x^(1/2)(x+1)(x-1)")
        assert result["result"] == "correct"


class TestCheckTrigFactoringAnswer:
    def test_mixed_trig(self):
        problem = {
            "module": "factoring",
            "isTrigFactoring": True,
            "trigFunc": "mixed",
            "validForms": ["(sinx+1)(cosx-2)"],
        }
        result = check_trig_factoring_answer(problem, "(sinx+1)(cosx-2)")
        assert result["result"] == "correct"

    def test_sin_factoring_polynomial(self):
        p = factoring._trig_sin()
        result = check_trig_factoring_answer(p, p["answerTex"].replace("\\", "").replace("{", "").replace("}", ""))
        assert result["result"] == "correct"


class TestCheckAnswerDispatch:
    def test_factoring_dispatch(self):
        problem = {"module": "factoring", "originalExpanded": {0: -4, 1: 0, 2: 1}}
        result = check_answer(problem, "(x-2)(x+2)")
        assert result["result"] == "correct"

    def test_unknown_module(self):
        problem = {"module": "nonexistent"}
        result = check_answer(problem, "42")
        assert result["result"] == "unknown"