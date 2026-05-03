import pytest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import (
    linear_equations, quadratic, polynomials, rational_expressions,
    systems, absolute_value, radicals, inequalities,
    sequences, probability,
)
from checker_registry import get_checker

random.seed(42)

WP5_MODULES = {
    "linear_equations": linear_equations,
    "quadratic": quadratic,
    "polynomials": polynomials,
    "rational_expressions": rational_expressions,
    "systems": systems,
    "absolute_value": absolute_value,
    "radicals": radicals,
    "inequalities": inequalities,
    "sequences": sequences,
    "probability": probability,
}


def _call_generator(fn):
    for _ in range(5):
        try:
            result = fn()
            if isinstance(result, dict) and "answerNorm" in result:
                return result
        except Exception:
            pass
    return fn()


class TestWP5LinearEquations:
    def test_linear_equations_d1_d3(self):
        """Diff 1-3: solve_linear_basic, linear_word_basic, solve_for_variable."""
        fns = (
            linear_equations.POOLS[1][:1]
            + linear_equations.POOLS[2][:1]
            + linear_equations.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("linear_equations")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_linear_equations_d4_d5(self):
        """Diff 4-5: solve_linear_inequality, linear_age_problem."""
        fns = linear_equations.POOLS[4][:1] + linear_equations.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("linear_equations")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5Quadratic:
    def test_quadratic_d1_d3(self):
        """Diff 1-3: factorable_quadratic, quadratic_formula, complete_square."""
        fns = (
            quadratic.POOLS[1][:1]
            + quadratic.POOLS[2][:1]
            + quadratic.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("quadratic")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "x=999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_quadratic_d4_d5(self):
        """Diff 4-5: discriminant_nature, vertex_of_parabola."""
        fns = quadratic.POOLS[4][:1] + quadratic.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("quadratic")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5Polynomials:
    def test_polynomials_d1_d3(self):
        """Diff 1-3: classify_polynomial, foil_binomials, synthetic_basic."""
        fns = (
            polynomials.POOLS[1][:1]
            + polynomials.POOLS[2][:1]
            + polynomials.POOLS[3][:2]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("polynomials")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_polynomials_d4_d5(self):
        """Diff 4-5: factor_theorem."""
        fns = polynomials.POOLS[4][:1] + polynomials.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("polynomials")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5RationalExpressions:
    def test_rational_expressions_d1_d3(self):
        """Diff 1-3: simplify_rational, multiply_rationals, add_rationals."""
        fns = (
            rational_expressions.POOLS[1][:1]
            + rational_expressions.POOLS[2][:1]
            + rational_expressions.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("rational_expressions")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "x=999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_rational_expressions_d4_d5(self):
        """Diff 4-5: simplify_complex_frac, solve_rational_equation."""
        fns = rational_expressions.POOLS[4][:1] + rational_expressions.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("rational_expressions")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5Systems:
    def test_systems_d1_d3(self):
        """Diff 1-3: substitution_basic, elimination_basic, three_variable_basic."""
        fns = (
            systems.POOLS[1][:1]
            + systems.POOLS[2][:1]
            + systems.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("systems")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "(999,999)")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_systems_d4_d5(self):
        """Diff 4-5: ticket_problem, classify_system."""
        fns = systems.POOLS[4][:1] + systems.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("systems")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5AbsoluteValue:
    def test_absolute_value_d1_d3(self):
        """Diff 1-3: abs_basic, abs_inequality_lt, abs_equation_compound."""
        fns = (
            absolute_value.POOLS[1][:1]
            + absolute_value.POOLS[2][:1]
            + absolute_value.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("absolute_value")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "x=999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_absolute_value_d4_d5(self):
        """Diff 4-5: abs_distance, abs_graphical, abs_midpoint."""
        fns = absolute_value.POOLS[4][:1] + absolute_value.POOLS[5][:2]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("absolute_value")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5Radicals:
    def test_radicals_d1_d3(self):
        """Diff 1-3: simplify_sqrt, add_radicals, multiply_radicals."""
        fns = (
            radicals.POOLS[1][:1]
            + radicals.POOLS[2][:1]
            + radicals.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("radicals")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "sqrt(999)")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_radicals_d4_d5(self):
        """Diff 4-5: solve_radical_basic, rational_exponent."""
        fns = radicals.POOLS[4][:1] + radicals.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("radicals")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5Inequalities:
    def test_inequalities_d1_d3(self):
        """Diff 1-3: solve_linear_ineq, and_compound, quadratic_ineq."""
        fns = (
            inequalities.POOLS[1][:1]
            + inequalities.POOLS[2][:1]
            + inequalities.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("inequalities")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "(999,inf)")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_inequalities_d4_d5(self):
        """Diff 4-5: rational_ineq, interval_union."""
        fns = inequalities.POOLS[4][:1] + inequalities.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("inequalities")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP5SequencesProbability:
    def test_sequences_probability(self):
        """Sequences diff 1-3 and probability diff 1-2."""
        seq_fns = (
            sequences.POOLS[1][:1]
            + sequences.POOLS[2][:1]
            + sequences.POOLS[3][:1]
        )
        for fn in seq_fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("sequences")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

        prob_fns = probability.POOLS[1][:1] + probability.POOLS[2][:1]
        for fn in prob_fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("probability")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "0.999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"
