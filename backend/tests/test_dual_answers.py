import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import extrema, derivatives
from checker import check_dual_answer
from checker_registry import get_checker


class TestDualAnswers:
    def test_derivatives_has_dual_answer_generator(self):
        found = False
        for diff in range(1, 6):
            for fn in derivatives.POOLS.get(diff, []):
                problem = fn()
                if problem.get("requiresDualAnswer"):
                    assert "answerNorm2" in problem
                    assert "answerTex2" in problem
                    found = True
                    break
            if found:
                break
        assert found, "No dual-answer derivatives generator found"

    def test_derivatives_both_dual_answers_correct(self):
        for fn in derivatives.POOLS[3]:
            problem = fn()
            if not problem.get("requiresDualAnswer"):
                continue
            correct_both = check_dual_answer(
                problem,
                problem["answerNorm"],
                problem["answerNorm2"],
            )
            assert correct_both.get("result") == "correct", f"{fn.__name__} both correct answers rejected"
            break

    def test_derivatives_second_wrong_returns_wrong_slot(self):
        for fn in derivatives.POOLS[3]:
            problem = fn()
            if not problem.get("requiresDualAnswer"):
                continue
            wrong_second = check_dual_answer(
                problem,
                problem["answerNorm"],
                "x=99999",
            )
            assert wrong_second.get("result") == "wrong", f"{fn.__name__} accepted wrong second answer"
            assert "wrongSlot" in wrong_second, f"{fn.__name__} wrongSlot missing"
            break

    def test_neither_dual_answer_correct(self):
        for fn in derivatives.POOLS[3]:
            problem = fn()
            if not problem.get("requiresDualAnswer"):
                continue
            wrong = check_dual_answer(problem, "x=99999", "y=88888")
            assert wrong.get("result") == "wrong", f"{fn.__name__} accepted completely wrong answers"
            break

    def test_check_dual_answer_exists(self):
        assert callable(check_dual_answer)
