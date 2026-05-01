"""SymPy adapter for Math Trainer generators.
Converts SymPy expressions to answerNorm and LaTeX formats.
"""
import re
import sympy
from sympy import symbols, diff, simplify, expand, latex, sin, cos, tan, exp, log, sqrt, Rational

x = symbols('x')


def to_norm(expr):
    """Convert SymPy expression to answerNorm string format.
    
    SymPy str uses ** for power; answerNorm uses ^.
    SymPy uses exp(); answerNorm uses e^().
    SymPy uses log(); answerNorm uses ln().
    
    Example: 3*x**2 + 2*x  →  "3*x^2+2*x"
    """
    s = sympy.sstr(expr)
    
    # Powers: x**2 → x^2
    s = s.replace('**', '^')
    
    # exp(x) → e^(x)
    s = re.sub(r'exp\(([^)]+)\)', r'e^(\1)', s)
    
    # log( → ln(
    s = s.replace('log(', 'ln(')
    
    # Remove spaces around operators for compact answerNorm format
    s = s.replace(' * ', '*').replace(' + ', '+').replace(' - ', '-')
    
    return s


def to_tex(expr):
    """Convert SymPy expression to LaTeX string.
    
    Uses sympy.latex() which produces standard LaTeX.
    """
    return latex(expr)


def diff_expr(expr, var=None):
    """Differentiate expression with respect to var (default x)."""
    if var is None:
        var = x
    return diff(expr, var)


# Pre-built common expressions for generator convenience
def sin_expr(arg):
    """Create sin expression."""
    return sin(arg)


def cos_expr(arg):
    """Create cos expression."""
    return cos(arg)


def tan_expr(arg):
    """Create tan expression."""
    return tan(arg)


def exp_expr(arg):
    """Create e^arg expression."""
    return exp(arg)


def ln_expr(arg):
    """Create ln(arg) expression."""
    return log(arg)


def pow_expr(base, exp_val):
    """Create base^exp expression."""
    return base ** exp_val
