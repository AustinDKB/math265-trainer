"""
Minimal symbolic differentiation engine for Math Trainer.
Expression tree with diff(), simplify(), to_tex(), eval().
"""
import math
from fractions import Fraction


class Expr:
    def diff(self): raise NotImplementedError
    def simplify(self): return self
    def to_tex(self): raise NotImplementedError
    def eval(self, x): raise NotImplementedError

    def __add__(self, other): return add(self, other)
    def __radd__(self, other): return add(Const(other), self)
    def __mul__(self, other): return mul(self, other)
    def __rmul__(self, other): return mul(Const(other), self)
    def __neg__(self): return neg(self)
    def __sub__(self, other): return add(self, neg(other))
    def __truediv__(self, other): return Div(self, other)


# ── Leaf nodes ────────────────────────────────────────────────────────────────

class Const(Expr):
    def __init__(self, val):
        if isinstance(val, Fraction):
            self.val = val
        elif isinstance(val, int):
            self.val = Fraction(val)
        else:
            self.val = Fraction(val).limit_denominator(10000)

    def diff(self): return Const(0)
    def simplify(self): return self

    def to_tex(self):
        f = self.val
        if f.denominator == 1:
            return str(int(f.numerator))
        return f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"

    def to_norm(self):
        f = self.val
        if f.denominator == 1:
            return str(int(f.numerator))
        return f"{f.numerator}/{f.denominator}"

    def eval(self, x): return float(self.val)
    def is_zero(self): return self.val == 0
    def is_one(self): return self.val == 1


class Var(Expr):
    def __init__(self, name="x"): self.name = name
    def diff(self): return Const(1) if self.name == "x" else Const(0)
    def simplify(self): return self
    def to_tex(self): return self.name
    def to_norm(self): return self.name
    def eval(self, x): return x


# ── Composite nodes ───────────────────────────────────────────────────────────

class Neg(Expr):
    def __init__(self, a): self.a = a
    def diff(self): return Neg(self.a.diff()).simplify()
    def simplify(self):
        a = self.a.simplify()
        if isinstance(a, Neg): return a.a
        if isinstance(a, Const) and a.is_zero(): return Const(0)
        if isinstance(a, Const): return Const(-a.val)
        return Neg(a)
    def to_tex(self):
        inner = self.a.to_tex()
        if isinstance(self.a, (Add,)):
            return f"-({inner})"
        return f"-{inner}"
    def to_norm(self):
        inner = self.a.to_norm()
        if isinstance(self.a, Add):
            return f"-({inner})"
        return f"-{inner}"
    def eval(self, x): return -self.a.eval(x)


class Add(Expr):
    def __init__(self, a, b): self.a, self.b = a, b
    def diff(self): return Add(self.a.diff(), self.b.diff()).simplify()
    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.is_zero(): return b
        if isinstance(b, Const) and b.is_zero(): return a
        if isinstance(a, Const) and isinstance(b, Const): return Const(a.val + b.val)
        # Handle Add(a, Neg(b)) as subtraction for cleaner tex
        return Add(a, b)
    def to_tex(self):
        a_tex = self.a.to_tex()
        b = self.b
        # If b is Neg, show as subtraction
        if isinstance(b, Neg):
            return f"{a_tex} - {b.a.to_tex()}"
        if isinstance(b, Const) and b.val < 0:
            return f"{a_tex} - {Const(-b.val).to_tex()}"
        return f"{a_tex} + {b.to_tex()}"
    def to_norm(self):
        a_n = self.a.to_norm()
        b = self.b
        # Detect leading-negative b for clean subtraction display
        if isinstance(b, Neg):
            return f"{a_n}-{b.a.to_norm()}"
        if isinstance(b, Const) and b.val < 0:
            return f"{a_n}-{Const(-b.val).to_norm()}"
        if isinstance(b, Mul):
            ba, bb = b.a, b.b
            if isinstance(bb, Neg):
                return f"{a_n}-{Mul(ba, bb.a).to_norm()}"
            if isinstance(ba, Neg):
                return f"{a_n}-{Mul(ba.a, bb).to_norm()}"
            if isinstance(ba, Const) and ba.val < 0:
                return f"{a_n}-{Mul(Const(-ba.val), bb).to_norm()}"
        return f"{a_n}+{b.to_norm()}"
    def eval(self, x): return self.a.eval(x) + self.b.eval(x)


class Mul(Expr):
    def __init__(self, a, b): self.a, self.b = a, b
    def diff(self):
        return Add(Mul(self.a.diff(), self.b), Mul(self.a, self.b.diff())).simplify()
    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.is_zero(): return Const(0)
        if isinstance(b, Const) and b.is_zero(): return Const(0)
        if isinstance(a, Const) and a.is_one(): return b
        if isinstance(b, Const) and b.is_one(): return a
        if isinstance(a, Const) and isinstance(b, Const): return Const(a.val * b.val)
        if isinstance(a, Neg) and isinstance(b, Neg): return Mul(a.a, b.a).simplify()
        return Mul(a, b)
    def to_tex(self):
        a, b = self.a, self.b
        a_tex = a.to_tex()
        b_tex = b.to_tex()
        # Const * something: no dot
        if isinstance(a, Const):
            if isinstance(b, (Sin, Cos, Tan, Exp, Ln, Var)):
                return f"{a_tex}{b_tex}"
            if isinstance(b, Pow) and isinstance(b.base, Var):
                return f"{a_tex}{b_tex}"
        # Neg const * something
        if isinstance(a, Neg) and isinstance(a.a, Const):
            return f"-{a.a.to_tex()}{b_tex}"
        return f"{a_tex} \\cdot {b_tex}"
    def to_norm(self):
        a, b = self.a, self.b
        # Pull out leading negative for clean form
        if isinstance(a, Neg):
            return f"-{Mul(a.a, b).to_norm()}"
        if isinstance(b, Neg):
            return f"-{Mul(a, b.a).to_norm()}"
        return f"{a.to_norm()}*{b.to_norm()}"
    def eval(self, x): return self.a.eval(x) * self.b.eval(x)


class Div(Expr):
    def __init__(self, a, b): self.a, self.b = a, b
    def diff(self):
        # (a'b - ab') / b²
        num = Add(Mul(self.a.diff(), self.b), Neg(Mul(self.a, self.b.diff())))
        den = Pow(self.b, Const(2))
        return Div(num, den).simplify()
    def simplify(self):
        a = self.a.simplify()
        b = self.b.simplify()
        if isinstance(a, Const) and a.is_zero(): return Const(0)
        if isinstance(b, Const) and b.is_one(): return a
        if isinstance(a, Const) and isinstance(b, Const) and not b.is_zero():
            return Const(a.val / b.val)
        return Div(a, b)
    def to_tex(self):
        return f"\\dfrac{{{self.a.to_tex()}}}{{{self.b.to_tex()}}}"
    def to_norm(self):
        num = self.a.to_norm()
        den = self.b.to_norm()
        if isinstance(self.b, (Add, Mul)):
            den = f"({den})"
        return f"{num}/({den})"
    def eval(self, x):
        d = self.b.eval(x)
        if abs(d) < 1e-12: return float('nan')
        return self.a.eval(x) / d


class Pow(Expr):
    def __init__(self, base, exp): self.base, self.exp = base, exp
    def diff(self):
        if isinstance(self.exp, Const):
            n = self.exp.val
            if n == 0: return Const(0)
            # Power rule + chain: n * base^(n-1) * base'
            new_pow = Pow(self.base, Const(n - 1)).simplify()
            return Mul(Mul(Const(n), new_pow), self.base.diff()).simplify()
        # General case (not handled for now)
        return Const(0)
    def simplify(self):
        base = self.base.simplify()
        exp = self.exp.simplify()
        if isinstance(exp, Const):
            if exp.is_zero(): return Const(1)
            if exp.is_one(): return base
        if isinstance(base, Const) and isinstance(exp, Const):
            try:
                return Const(float(base.val) ** float(exp.val))
            except Exception:
                pass
        return Pow(base, exp)
    def to_tex(self):
        base_tex = self.base.to_tex()
        exp_tex = self.exp.to_tex()
        # Wrap base in braces if complex
        if isinstance(self.base, (Add, Mul, Div, Neg)):
            base_tex = f"({base_tex})"
        if isinstance(self.exp, Const) and self.exp.val.denominator > 1:
            f = self.exp.val
            exp_str = f"{{{f.numerator}/{f.denominator}}}"
        else:
            exp_str = f"{{{exp_tex}}}"
        return f"{base_tex}^{exp_str}"
    def to_norm(self):
        base = self.base.to_norm()
        exp = self.exp.to_norm()
        if isinstance(self.base, (Add, Mul, Div, Neg)):
            base = f"({base})"
        return f"{base}^({exp})"
    def eval(self, x):
        b = self.base.eval(x)
        e = self.exp.eval(x)
        try:
            return b ** e
        except Exception:
            return float('nan')


class Sin(Expr):
    def __init__(self, a): self.a = a
    def diff(self): return Mul(Cos(self.a), self.a.diff()).simplify()
    def simplify(self): return Sin(self.a.simplify())
    def to_tex(self): return f"\\sin({self.a.to_tex()})"
    def to_norm(self): return f"sin({self.a.to_norm()})"
    def eval(self, x): return math.sin(self.a.eval(x))


class Cos(Expr):
    def __init__(self, a): self.a = a
    def diff(self): return Mul(Neg(Sin(self.a)), self.a.diff()).simplify()
    def simplify(self): return Cos(self.a.simplify())
    def to_tex(self): return f"\\cos({self.a.to_tex()})"
    def to_norm(self): return f"cos({self.a.to_norm()})"
    def eval(self, x): return math.cos(self.a.eval(x))


class Tan(Expr):
    def __init__(self, a): self.a = a
    def diff(self):
        # sec²(a) * a' = 1/cos²(a) * a'
        return Mul(Div(Const(1), Pow(Cos(self.a), Const(2))), self.a.diff()).simplify()
    def simplify(self): return Tan(self.a.simplify())
    def to_tex(self): return f"\\tan({self.a.to_tex()})"
    def to_norm(self): return f"tan({self.a.to_norm()})"
    def eval(self, x):
        c = math.cos(self.a.eval(x))
        if abs(c) < 1e-12: return float('nan')
        return math.tan(self.a.eval(x))


class Exp(Expr):
    def __init__(self, a): self.a = a
    def diff(self): return Mul(Exp(self.a), self.a.diff()).simplify()
    def simplify(self): return Exp(self.a.simplify())
    def to_tex(self):
        inner = self.a
        if isinstance(inner, Var) and inner.name == "x":
            return "e^x"
        return f"e^{{{inner.to_tex()}}}"
    def to_norm(self): return f"e^({self.a.to_norm()})"
    def eval(self, x):
        try: return math.exp(self.a.eval(x))
        except OverflowError: return float('inf')


class Ln(Expr):
    def __init__(self, a): self.a = a
    def diff(self): return Div(self.a.diff(), self.a).simplify()
    def simplify(self): return Ln(self.a.simplify())
    def to_tex(self): return f"\\ln({self.a.to_tex()})"
    def to_norm(self): return f"ln({self.a.to_norm()})"
    def eval(self, x):
        v = self.a.eval(x)
        if v <= 0: return float('nan')
        return math.log(v)


# ── Constructor helpers ───────────────────────────────────────────────────────

def add(a, b):
    if isinstance(a, (int, float)): a = Const(a)
    if isinstance(b, (int, float)): b = Const(b)
    return Add(a, b).simplify()


def mul(a, b):
    if isinstance(a, (int, float)): a = Const(a)
    if isinstance(b, (int, float)): b = Const(b)
    return Mul(a, b).simplify()


def neg(a):
    if isinstance(a, (int, float)): return Const(-a)
    return Neg(a).simplify()


def pow_expr(base, exp):
    if isinstance(exp, (int, float)): exp = Const(exp)
    return Pow(base, exp).simplify()


X = Var("x")


# ── Numeric equivalence check (for answer validation) ─────────────────────────

def numeric_equal(e1, e2, xs=None, tol=1e-6):
    if xs is None:
        xs = [0.5, 1.0, 1.5, 2.0, 3.0]
    for x in xs:
        try:
            v1 = e1.eval(x)
            v2 = e2.eval(x)
            if math.isnan(v1) or math.isnan(v2) or math.isinf(v1) or math.isinf(v2):
                continue
            if abs(v1 - v2) > tol:
                return False
        except Exception:
            continue
    return True


def diff_and_simplify(expr):
    return expr.diff().simplify()


# ── Pre-built common expressions ──────────────────────────────────────────────

def poly(coeffs):
    """Build polynomial from [a_n, ..., a_1, a_0] highest degree first."""
    result = Const(0)
    n = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        if c == 0: continue
        exp = n - i
        if exp == 0:
            term = Const(c)
        elif exp == 1:
            term = mul(Const(c), X)
        else:
            term = mul(Const(c), pow_expr(X, Const(exp)))
        result = add(result, term)
    return result
