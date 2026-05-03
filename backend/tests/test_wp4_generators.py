import pytest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import (
    asymptotes, increasing_decreasing, extrema, mvt,
    numerical_methods, indeterminate_forms, epsilon_delta,
    hyperbolic_apps, center_of_mass, function_construction,
)
from checker_registry import get_checker

random.seed(42)

WP4_MODULES = {
    "asymptotes": asymptotes,
    "increasing_decreasing": increasing_decreasing,
    "extrema": extrema,
    "mvt": mvt,
    "numerical_methods": numerical_methods,
    "indeterminate_forms": indeterminate_forms,
    "epsilon_delta": epsilon_delta,
    "hyperbolic_apps": hyperbolic_apps,
    "center_of_mass": center_of_mass,
    "function_construction": function_construction,
}


def _call_generator(fn):
    """Call a generator with up to 5 attempts (some are stochastic)."""
    for _ in range(5):
        try:
            result = fn()
            if isinstance(result, dict) and "answerNorm" in result:
                return result
        except Exception:
            pass
    return fn()


class TestWP4Asymptotes:
    def test_asymptotes_d1_d3(self):
        """Diff 1-3: ha_degree_less, ha_degree_equal, va_rational, slant_asymptote."""
        fns = (
            asymptotes.POOLS[1][:2]
            + asymptotes.POOLS[2][:2]
            + asymptotes.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("asymptotes")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "x=y=999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_asymptotes_d4_d5(self):
        """Diff 4-5: all_asymptotes, asymptote_with_hole."""
        fns = asymptotes.POOLS[4][:1] + asymptotes.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("asymptotes")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4IncreasingDecreasing:
    def test_inc_dec_d1_d3(self):
        """Diff 1-3: increasing/decreasing from derivative, critical points, rational."""
        fns = (
            increasing_decreasing.POOLS[1]
            + increasing_decreasing.POOLS[2]
            + increasing_decreasing.POOLS[3][:2]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("increasing_decreasing")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "(-inf,inf)")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_inc_dec_d4_d5(self):
        """Diff 4-5: full_interval_analysis, trig_increasing_decreasing."""
        fns = increasing_decreasing.POOLS[4][:1] + increasing_decreasing.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("increasing_decreasing")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4Extrema:
    def test_extrema_d1_d3(self):
        """Diff 1-3: local_extrema_first_derivative, absolute_extrema_closed_interval, second_derivative_test."""
        fns = (
            extrema.POOLS[1][:1]
            + extrema.POOLS[2][:1]
            + extrema.POOLS[3][:2]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("extrema")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "max=999,min=999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_extrema_d4_d5(self):
        """Diff 4-5: optimization_extrema, extrema_with_parameter."""
        fns = extrema.POOLS[4][:1] + extrema.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("extrema")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4MVT:
    def test_mvt_d1_d3(self):
        """Diff 1-3: mvt_basic, rolles_basic, mvt_show_unique."""
        fns = mvt.POOLS[1][:1] + mvt.POOLS[2][:1] + mvt.POOLS[3][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("mvt")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_mvt_d4_d5(self):
        """Diff 4-5: mvt_corollary_constant, mvt_trig, mvt_ivt_combo."""
        fns = mvt.POOLS[4][:1] + mvt.POOLS[5][:2]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("mvt")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4NumericalMethods:
    def test_numerical_methods_d1_d3(self):
        """Diff 1-3: bisection_basic, newton_basic, secant_basic."""
        fns = (
            numerical_methods.POOLS[1][:1]
            + numerical_methods.POOLS[2][:1]
            + numerical_methods.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("numerical_methods")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"

    def test_numerical_methods_d4_d5(self):
        """Diff 4-5: taylor_error_bound, bisection_vs_newton."""
        fns = numerical_methods.POOLS[4][:1] + numerical_methods.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("numerical_methods")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4IndeterminateForms:
    def test_indeterminate_forms_d1_d3(self):
        """Diff 1-3: lhospital_0over0, lhospital_trig, product_0timesinf."""
        fns = (
            indeterminate_forms.POOLS[1][:1]
            + indeterminate_forms.POOLS[2][:1]
            + indeterminate_forms.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("indeterminate_forms")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_indeterminate_forms_d4_d5(self):
        """Diff 4-5: power_indeterminate, repeated_lhospital, hospital_with_param."""
        fns = indeterminate_forms.POOLS[4][:1] + indeterminate_forms.POOLS[5][:2]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("indeterminate_forms")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4EpsilonDelta:
    def test_epsilon_delta_d1_d3(self):
        """Diff 1-3: epsilon_delta_basic, epsilon_delta_quadratic, find_delta."""
        fns = epsilon_delta.POOLS[1][:2] + epsilon_delta.POOLS[2][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("epsilon_delta")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"

    def test_epsilon_delta_d4_d5(self):
        """Diff 4-5: limit_dne_epsilon_delta, epsilon_delta_squeeze."""
        fns = epsilon_delta.POOLS[4][:1] + epsilon_delta.POOLS[5][:1]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("epsilon_delta")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4HyperbolicApps:
    def test_hyperbolic_apps_d1_d3(self):
        """Diff 1-3: sinh_cosh_identity, integral_sinh, catenary_shape."""
        fns = (
            hyperbolic_apps.POOLS[1][:1]
            + hyperbolic_apps.POOLS[2][:1]
            + hyperbolic_apps.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("hyperbolic_apps")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"

    def test_hyperbolic_apps_d4_d5(self):
        """Diff 4-5: arsinh, hyperbolic_surface_area, hyperbolic_vs_trig."""
        fns = hyperbolic_apps.POOLS[4][:1] + hyperbolic_apps.POOLS[5][:2]
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("hyperbolic_apps")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"


class TestWP4CenterOfMass:
    def test_center_of_mass_d1_d3(self):
        """Diff 1-3: cm_discrete_basic, cm_rod_variable_density, cm_lamina_rectangle."""
        fns = (
            center_of_mass.POOLS[1][:1]
            + center_of_mass.POOLS[2][:1]
            + center_of_mass.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("center_of_mass")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "(999,999)")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"


class TestWP4FunctionConstruction:
    def test_function_construction_d1_d3(self):
        """Diff 1-3: antiderivative_basic, second_antiderivative, velocity_from_acceleration."""
        fns = (
            function_construction.POOLS[1][:1]
            + function_construction.POOLS[2][:1]
            + function_construction.POOLS[3][:1]
        )
        for fn in fns:
            p = _call_generator(fn)
            assert "problemTex" in p
            assert "answerNorm" in p
            checker = get_checker("function_construction")
            result = checker(p, p["answerNorm"])
            assert result.get("result") == "correct", f"{fn.__name__} correct answer rejected"
            wrong = checker(p, "999")
            assert wrong.get("result") == "wrong", f"{fn.__name__} wrong answer accepted"
