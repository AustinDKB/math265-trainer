import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_utils import (
    R, pick, sign_str, plus_C, interval_tex, gcd, lcm,
    simplify_frac, frac_to_tex, exp_frac_to_norm, poly_to_tex,
    expand_expression, polys_equal, user_input_to_norm,
)


class TestSignStr:
    def test_positive(self):
        assert sign_str(3) == "+3"

    def test_negative(self):
        assert sign_str(-3) == "-3"

    def test_zero(self):
        assert sign_str(0) == "+0"

    def test_fac_alias(self):
        from generators.factoring import sign_str as factoring_sign_str
        assert factoring_sign_str(5) == sign_str(5)


class TestPlusC:
    def test_appends_plus_c(self):
        assert plus_C("x^2/2") == "x^2/2 + C"

    def test_already_has_c(self):
        assert plus_C("x") == "x + C"


class TestIntervalTex:
    def test_closed_interval(self):
        assert interval_tex(0, 1) == "[0, 1]"

    def test_open_interval(self):
        assert interval_tex(0, 1, left_open=True, right_open=True) == "(0, 1)"

    def test_half_open(self):
        assert interval_tex(0, 1, left_open=False, right_open=True) == "[0, 1)"


class TestSimplifyFrac:
    def test_basic(self):
        assert simplify_frac(6, 8) == (3, 4)

    def test_negative(self):
        assert simplify_frac(-6, 8) == (-3, 4)

    def test_already_simple(self):
        assert simplify_frac(3, 5) == (3, 5)


class TestFracToTex:
    def test_whole_number(self):
        assert frac_to_tex(5, 1) == "5"

    def test_fraction(self):
        assert frac_to_tex(1, 2) == "\\frac{1}{2}"


class TestExpFracToNorm:
    def test_whole_exponent(self):
        assert exp_frac_to_norm(3, 1) == "x^3"

    def test_fractional_exponent(self):
        assert exp_frac_to_norm(1, 2) == "x^(1/2)"


class TestExpandExpression:
    def test_simple_product(self):
        result = expand_expression("(x+1)(x+2)")
        assert polys_equal(result, {0: 2, 1: 3, 2: 1})

    def test_single_polynomial(self):
        result = expand_expression("x^2+3x+2")
        assert polys_equal(result, {0: 2, 1: 3, 2: 1})


class TestPolysEqual:
    def test_equal_polynomials(self):
        assert polys_equal({0: 2, 1: 3, 2: 1}, {0: 2, 1: 3, 2: 1})

    def test_unequal_polynomials(self):
        assert not polys_equal({0: 1, 1: 2}, {0: 2, 1: 3})


class TestUserInputToNorm:
    def test_basic_normalization(self):
        result = user_input_to_norm("X^2 + 3X")
        assert "x" in result and "3" in result

    def test_frac_normalization(self):
        assert user_input_to_norm("\\frac{1}{2}") == "(1)/(2)"