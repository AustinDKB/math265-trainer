import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checker_registry import get_checker

NEW_MODULES = [
    "asymptotes", "increasing_decreasing", "extrema", "mvt",
    "numerical_methods", "indeterminate_forms", "epsilon_delta",
    "hyperbolic_apps", "center_of_mass", "function_construction",
    "linear_equations", "quadratic", "polynomials", "rational_expressions",
    "systems", "absolute_value", "radicals", "inequalities",
    "sequences", "probability",
]


class TestNewCheckersRegistered:
    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_module_registered(self, module):
        from checker_registry import CHECKER_MAP
        assert module in CHECKER_MAP, f"{module} not in CHECKER_MAP"
        checker_fn = get_checker(module)
        assert callable(checker_fn), f"{module} checker is not callable"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_returns_dict(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "test",
            "steps": [],
        }
        result = checker_fn(mock_problem, "test")
        assert isinstance(result, dict), f"{module} checker did not return dict"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_has_result_field(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "test",
            "steps": [],
        }
        result = checker_fn(mock_problem, "test")
        assert "result" in result, f"{module} checker missing 'result' field"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_accepts_valid_answer(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "3/4",
            "steps": [],
        }
        result = checker_fn(mock_problem, "3/4")
        assert result.get("result") == "correct", f"{module} rejected valid answer"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_rejects_invalid_answer(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "3/4",
            "steps": [],
        }
        result = checker_fn(mock_problem, "999/888")
        assert result.get("result") == "wrong", f"{module} accepted invalid answer"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_handles_known_validNorms(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "sqrt(2)/2",
            "validNorms": ["sqrt(2)/2", "1/sqrt(2)"],
            "steps": [],
        }
        result = checker_fn(mock_problem, "1/sqrt(2)")
        assert result.get("result") == "correct", f"{module} rejected valid alternate form"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_dne_accepted_when_answerNorm_is_dne(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"does not exist",
            "answerNorm": "dne",
            "steps": [],
        }
        result = checker_fn(mock_problem, "dne")
        assert result.get("result") == "correct", f"{module} rejected 'dne'"

    @pytest.mark.parametrize("module", NEW_MODULES)
    def test_checker_handles_empty_string_answer(self, module):
        checker_fn = get_checker(module)
        mock_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "3/4",
            "steps": [],
        }
        result = checker_fn(mock_problem, "")
        assert result.get("result") == "wrong", f"{module} accepted empty string"

    def test_checker_derivatives_trig_flag(self):
        checker_fn = get_checker("derivatives")
        trig_problem = {
            "problemTex": r"Test problem",
            "answerTex": r"Test answer",
            "answerNorm": "cos(x)",
            "isTrigFactoring": True,
            "steps": [],
        }
        result = checker_fn(trig_problem, "cos(x)")
        assert result.get("result") == "correct", "derivatives checker rejected trig answer"
