"""Tests for sympy_utils.py adapter."""
import sys
sys.path.insert(0, '..')
import sympy
from sympy import symbols, diff, simplify, sin, cos, exp, log
from sympy_utils import to_norm, to_tex, x

def test_to_norm_power():
    """Test power notation conversion."""
    expr = x**2
    assert to_norm(expr) == "x^2"
    
    expr = x**3 + 2*x
    norm = to_norm(expr)
    assert "**" not in norm
    assert "^" in norm


def test_to_norm_exp():
    """Test exp() → e^() conversion."""
    expr = exp(x)
    norm = to_norm(expr)
    assert "exp(" not in norm
    assert "e^" in norm


def test_to_norm_log():
    """Test log() → ln() conversion."""
    expr = log(x)
    norm = to_norm(expr)
    assert "log(" not in norm
    assert "ln(" in norm


def test_to_norm_no_spaces():
    """Test spaces are removed around operators."""
    expr = x**2 + 2*x
    norm = to_norm(expr)
    assert " * " not in norm
    assert " + " not in norm
    assert " - " not in norm


def test_to_tex_basic():
    """Test LaTeX output."""
    expr = x**2
    tex = to_tex(expr)
    assert "x" in tex
    assert "2" in tex


def test_product_derivatives():
    """Test all product rule derivative cases."""
    cases = [
        (x * sin(x), x),
        (x * cos(x), x),
        (x * exp(x), x),
        (x**2 * sin(x), x),
        (x**2 * exp(x), x),
        (x**3 * log(x), x),
        (2*x * cos(x), x),
    ]
    for expr, var in cases:
        deriv = simplify(diff(expr, var))
        norm = to_norm(deriv)
        tex = to_tex(deriv)
        assert isinstance(norm, str) and len(norm) > 0
        assert isinstance(tex, str) and len(tex) > 0
        # Verify norm uses answerNorm conventions
        assert "**" not in norm, f"SymPy ** not translated: {norm}"
        assert "exp(" not in norm, f"SymPy exp() not translated: {norm}"
        assert "log(" not in norm, f"SymPy log() not translated: {norm}"


def test_quotient_derivatives():
    """Test all quotient rule derivative cases."""
    cases = [
        (sin(x) / x, x),
        (exp(x) / x**2, x),
        (log(x) / x, x),
        (x**2 / (x + 1), x),
        (sin(x) / cos(x), x),
    ]
    for expr, var in cases:
        deriv = simplify(diff(expr, var))
        norm = to_norm(deriv)
        tex = to_tex(deriv)
        assert isinstance(norm, str) and len(norm) > 0
        assert isinstance(tex, str) and len(tex) > 0
        assert "**" not in norm, f"SymPy ** not translated: {norm}"
        assert "exp(" not in norm, f"SymPy exp() not translated: {norm}"
        assert "log(" not in norm, f"SymPy log() not translated: {norm}"


def test_specific_product_case():
    """Test specific product rule case: d/dx[x*e^x]."""
    expr = x * exp(x)
    deriv = simplify(diff(expr, x))
    norm = to_norm(deriv)
    # Should be equivalent to (x+1)*e^x or e^x+x*e^x
    assert "e^" in norm or "e^" in norm


def test_specific_quotient_case():
    """Test specific quotient rule case: d/dx[sin(x)/x]."""
    expr = sin(x) / x
    deriv = simplify(diff(expr, x))
    norm = to_norm(deriv)
    # Should contain sin and cos
    assert "sin" in norm or "cos" in norm


if __name__ == "__main__":
    # Run tests
    test_to_norm_power()
    test_to_norm_exp()
    test_to_norm_log()
    test_to_norm_no_spaces()
    test_to_tex_basic()
    test_product_derivatives()
    test_quotient_derivatives()
    test_specific_product_case()
    test_specific_quotient_case()
    print("All sympy_utils tests passed!")
