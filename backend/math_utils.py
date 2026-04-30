import random
import math
import re
from fractions import Fraction


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def simplify_frac(n, d):
    if d == 0:
        return (n, d)
    g = gcd(abs(n), abs(d))
    return (n // g, d // g)


def R(a, b):
    return random.randint(a, b)


def pick(arr):
    return random.choice(arr)


def sign_str(n):
    return f"+{n}" if n >= 0 else str(n)


def frac_to_tex(sn, sd):
    return str(sn) if sd == 1 else f"\\frac{{{sn}}}{{{sd}}}"


def exp_frac_to_norm(sn, sd):
    return f"x^{sn}" if sd == 1 else f"x^({sn}/{sd})"


def poly_to_tex(coeffs):
    """Convert [a_n, ..., a_1, a_0] to LaTeX string."""
    degree = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        exp = degree - i
        if c == 0:
            continue
        if exp == 0:
            terms.append(f"{c:+}" if terms else str(c))
        elif exp == 1:
            if c == 1:
                terms.append("+x" if terms else "x")
            elif c == -1:
                terms.append("-x")
            else:
                terms.append(f"{c:+}x" if terms else f"{c}x")
        else:
            if c == 1:
                terms.append(f"+x^{exp}" if terms else f"x^{exp}")
            elif c == -1:
                terms.append(f"-x^{exp}")
            else:
                terms.append(f"{c:+}x^{exp}" if terms else f"{c}x^{exp}")
    return "".join(terms) if terms else "0"


# ── Polynomial arithmetic (sparse: dict degree→coeff) ──

def poly_add(a, b):
    result = dict(a)
    for deg, coef in b.items():
        result[deg] = result.get(deg, 0) + coef
    return result


def poly_mul(a, b):
    result = {}
    for da, ca in a.items():
        for db, cb in b.items():
            d = da + db
            result[d] = result.get(d, 0) + ca * cb
    return result


def poly_scale(a, s):
    return {d: c * s for d, c in a.items()}


def poly_pow(p, n):
    result = {0: 1}
    for _ in range(n):
        result = poly_mul(result, p)
    return result


def normalize_poly(p, tol=1e-6):
    return {d: round(c, 6) for d, c in p.items() if abs(c) > tol}


# ── Minimal recursive-descent polynomial parser ──

class _Parser:
    def __init__(self, s):
        self.s = s.replace(' ', '')
        self.pos = 0

    def peek(self):
        return self.s[self.pos] if self.pos < len(self.s) else ''

    def consume(self, ch=None):
        if ch and self.s[self.pos] != ch:
            raise ValueError(f"Expected {ch!r} got {self.s[self.pos]!r}")
        c = self.s[self.pos]
        self.pos += 1
        return c

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            if op == '+':
                left = poly_add(left, right)
            else:
                left = poly_add(left, poly_scale(right, -1))
        return left

    def parse_term(self):
        left = self.parse_power()
        while self.peek() in ('*', '('):
            if self.peek() == '*':
                self.consume('*')
            right = self.parse_power()
            left = poly_mul(left, right)
        return left

    def parse_power(self):
        base = self.parse_atom()
        if self.peek() == '^':
            self.consume('^')
            exp = int(self._parse_int())
            base = poly_pow(base, exp)
        return base

    def _parse_int(self):
        s = ''
        if self.peek() == '-':
            s += self.consume()
        while self.peek().isdigit():
            s += self.consume()
        return s

    def parse_atom(self):
        if self.peek() == '(':
            self.consume('(')
            val = self.parse_expr()
            self.consume(')')
            return val
        if self.peek() == '-':
            self.consume('-')
            atom = self.parse_atom()
            return poly_scale(atom, -1)
        if self.peek() == 'x':
            self.consume('x')
            return {1: 1}
        # number
        s = ''
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            s += self.consume()
        if not s:
            raise ValueError(f"Unexpected char {self.peek()!r} at {self.pos}")
        return {0: float(s)}


def expand_expression(expr):
    """Expand a factored polynomial expression to sparse dict form."""
    # Preprocess: strip LaTeX, normalize
    s = expr
    s = re.sub(r'\\[a-zA-Z]+', '', s)     # remove LaTeX commands
    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'\^(\d+)', r'^\1', s)     # x^2 stays x^2
    # Add * between )(  and between digit and (
    s = re.sub(r'\)\s*\(', ')*(', s)
    s = re.sub(r'(\d)\s*\(', r'\1*(', s)
    s = re.sub(r'(\d)(x)', r'\1*\2', s)   # 18x → 18*x
    parser = _Parser(s)
    result = parser.parse_expr()
    return normalize_poly(result)


def polys_equal(a, b, tol=0.001):
    all_degs = set(a.keys()) | set(b.keys())
    for d in all_degs:
        if abs(a.get(d, 0) - b.get(d, 0)) > tol:
            return False
    return True


# ── Answer normalization (mirrors JS userInputToNorm) ──

def user_input_to_norm(s):
    s = s.strip().lower().replace(' ', '')
    s = re.sub(r'\\d?frac\{([^}]*)\}\{([^}]*)\}', r'(\1)/(\2)', s)  # \frac{A}{B} → (A)/(B)
    s = re.sub(r'x\^\{([^}]*)\}', r'x^(\1)', s)          # x^{3} → x^(3)
    s = re.sub(r'x\^(-?\d+(?:/\d+)?)(?!\))', r'x^(\1)', s)  # x^-3/2 → x^(-3/2)
    return s
