import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from math_utils import R, pick, gcd, lcm, simplify_frac, sign_str, poly_to_tex, expand_expression

CONFIG = {
    "diffSquares_a":   (2, 200),
    "simpleTrinomial": (-16, 16),
    "gcf_k":           (2, 13),
    "gcf_pq":          (-16, 16),
    "leadCoeff_a":     [2,3,5,6,7,8,9],
    "leadCoeff_pq":    (-12, 12),
    "cubes_a":         (2, 8),
    "quartic_a":       (2, 12),
    "grouping_ab":     (-16, 16),
    "quadDisguise_pq": (-16, 16),
    "allXterms_k":     (2, 19),
    "allXterms_pq":    (-16, 16),
    "fracNegGcf_k":    (2, 12),
    "trigTrinomial_pq":(-9, 9),
    "trigLeadCoeff_a": (2, 5),
    "cubicRoots":      (-4, 4),
    "repeatedRoot_ab": (1, 4),
}


def _fac(r):
    return f"+{r}" if r >= 0 else str(r)


# ─── diff1 ───

def _diff_squares():
    a = R(*CONFIG["diffSquares_a"])
    a2 = a * a
    return {
        "problemTex": f"x^2 - {a2}",
        "answerTex": f"(x+{a})(x-{a})",
        "answerNorm": None,
        "originalExpanded": f"x^2-{a2}",
        "steps": [
            {"label": "Recognize pattern", "math": f"x^2 - {a2} = x^2 - {a}^2", "note": "Difference of squares: a²−b²"},
            {"label": "Apply formula", "math": f"(x+{a})(x-{a})", "note": "a²−b² = (a+b)(a−b)"},
        ],
    }


def _simple_trinomial():
    lo, hi = CONFIG["simpleTrinomial"]
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(lo, hi); q = R(lo, hi); attempts += 1
    b, c = p + q, p * q
    bstr = sign_str(b) if b != 0 else ""
    cstr = sign_str(c)
    f1 = f"(x{sign_str(p)})"
    f2 = f"(x{sign_str(q)})"
    return {
        "problemTex": f"x^2 {bstr}x {cstr}",
        "answerTex": f"{f1}{f2}",
        "answerNorm": None,
        "originalExpanded": poly_to_tex([1, b, c]),
        "steps": [
            {"label": "Find two numbers", "math": f"p+q={b},\\; pq={c}", "note": f"Need two numbers that add to {b} and multiply to {c}"},
            {"label": "Those numbers", "math": f"p={p},\\; q={q}", "note": f"Check: sum={b}, product={c}"},
            {"label": "Factor", "math": f"{f1}{f2}", "note": ""},
        ],
    }


def _all_x_terms():
    klo, khi = CONFIG["allXterms_k"]
    pqlo, pqhi = CONFIG["allXterms_pq"]
    k = R(klo, khi)
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(pqlo, pqhi); q = R(pqlo, pqhi); attempts += 1
    b, c = p + q, p * q
    kb, kc = k * b, k * c
    kbstr = sign_str(kb) if kb != 0 else ""
    kcstr = sign_str(kc)
    f1 = f"(x{sign_str(p)})"
    f2 = f"(x{sign_str(q)})"
    bstr = sign_str(b) if b != 0 else ""
    cstr = sign_str(c)
    return {
        "problemTex": f"{k}x^3{kbstr}x^2{kcstr}x",
        "answerTex": f"{k}x{f1}{f2}",
        "answerNorm": None,
        "originalExpanded": poly_to_tex([k, kb, kc, 0]),
        "steps": [
            {"label": "Factor out GCF", "math": f"{k}x(x^2{bstr}x{cstr})", "note": f"GCF = {k}x"},
            {"label": "Factor trinomial", "math": f"{k}x{f1}{f2}", "note": ""},
        ],
    }


diff1 = [_diff_squares, _simple_trinomial, _all_x_terms]


# ─── diff2 ───

def _gcf():
    klo, khi = CONFIG["gcf_k"]
    pqlo, pqhi = CONFIG["gcf_pq"]
    k = R(klo, khi)
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(pqlo, pqhi); q = R(pqlo, pqhi); attempts += 1
    b, c = p + q, p * q
    kb, kc = k * b, k * c
    bstr = sign_str(b) if b != 0 else ""
    cstr = sign_str(c)
    kbstr = sign_str(kb) if kb != 0 else ""
    kcstr = sign_str(kc)
    f1 = f"(x{sign_str(p)})"
    f2 = f"(x{sign_str(q)})"
    return {
        "problemTex": f"{k}x^2 {kbstr}x {kcstr}",
        "answerTex": f"{k}{f1}{f2}",
        "answerNorm": None,
        "originalExpanded": poly_to_tex([k, kb, kc]),
        "steps": [
            {"label": "Factor out GCF", "math": f"{k}(x^2{bstr}x{cstr})", "note": f"GCF = {k}"},
            {"label": "Factor trinomial", "math": f"{k}{f1}{f2}", "note": ""},
        ],
    }


def _lead_coeff():
    a = pick(CONFIG["leadCoeff_a"])
    pqlo, pqhi = CONFIG["leadCoeff_pq"]
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(pqlo, pqhi); q = R(pqlo, pqhi); attempts += 1
    B, C = p + a * q, p * q
    f1p = f"({a}x{sign_str(p)})"
    f2q = f"(x{sign_str(q)})"
    Bstr = sign_str(B) if B != 0 else ""
    Cstr = sign_str(C)
    return {
        "problemTex": f"{a}x^2 {Bstr}x {Cstr}",
        "answerTex": f"{f1p}{f2q}",
        "answerNorm": None,
        "originalExpanded": poly_to_tex([a, B, C]),
        "steps": [
            {"label": "AC method", "math": f"a\\cdot c = {a}\\cdot{C} = {a*C}", "note": ""},
            {"label": "Find factors", "math": f"{p}\\cdot{a*q}={a*C},\\quad {p}+{a*q}={B}", "note": ""},
            {"label": "Factor", "math": f"{f1p}{f2q}", "note": ""},
        ],
    }


def _diff_cubes():
    a = R(*CONFIG["cubes_a"])
    a3 = a ** 3
    return {
        "problemTex": f"x^3 - {a3}",
        "answerTex": f"(x-{a})(x^2+{a}x+{a*a})",
        "answerNorm": None,
        "originalExpanded": f"x^3 - {a3}",
        "steps": [
            {"label": "Recognize difference of cubes", "math": f"x^3 - {a}^3", "note": "a³−b³=(a−b)(a²+ab+b²)"},
            {"label": "Apply formula", "math": f"(x-{a})(x^2+{a}x+{a*a})", "note": f"a=x, b={a}"},
        ],
    }


def _sum_cubes():
    a = R(*CONFIG["cubes_a"])
    a3 = a ** 3
    return {
        "problemTex": f"x^3 + {a3}",
        "answerTex": f"(x+{a})(x^2-{a}x+{a*a})",
        "answerNorm": None,
        "originalExpanded": f"x^3 + {a3}",
        "steps": [
            {"label": "Recognize sum of cubes", "math": f"x^3 + {a}^3", "note": "a³+b³=(a+b)(a²−ab+b²)"},
            {"label": "Apply formula", "math": f"(x+{a})(x^2-{a}x+{a*a})", "note": f"a=x, b={a}"},
        ],
    }


diff2 = [_gcf, _lead_coeff, _diff_cubes, _sum_cubes]


# ─── diff3 ───

def _quartic():
    a = R(*CONFIG["quartic_a"])
    a2, a4 = a * a, a ** 4
    return {
        "problemTex": f"x^4 - {a4}",
        "answerTex": f"(x^2+{a2})(x+{a})(x-{a})",
        "answerNorm": None,
        "originalExpanded": f"x^4 - {a4}",
        "steps": [
            {"label": "Difference of squares (outer)", "math": f"(x^2)^2-({a2})^2=(x^2+{a2})(x^2-{a2})", "note": ""},
            {"label": "Factor second bracket", "math": f"x^2-{a2}=(x+{a})(x-{a})", "note": "Difference of squares again"},
        ],
    }


def _grouping():
    lo, hi = CONFIG["grouping_ab"]
    a, b, attempts = 0, 0, 0
    while (a == 0 or b == 0) and attempts < 50:
        a = R(lo, hi); b = R(lo, hi); attempts += 1
    term2 = sign_str(a) + "x^2"
    term3 = sign_str(b) + "x"
    term4 = sign_str(a * b)
    f1a = sign_str(a)
    f1b = sign_str(b)
    return {
        "problemTex": f"x^3{term2}{term3}{term4}",
        "answerTex": f"(x^2{f1b})(x{f1a})",
        "answerNorm": None,
        "originalExpanded": f"x^3{term2}{term3}{term4}",
        "isGrouping": True,
        "steps": [
            {"label": "Group first two and last two", "math": f"(x^3{term2})+({b}x{term4})", "note": ""},
            {"label": "Factor from each group", "math": f"x^2(x{f1a})+{b}(x{f1a})", "note": ""},
            {"label": "Factor common binomial", "math": f"(x^2{f1b})(x{f1a})", "note": ""},
        ],
    }


def _quad_disguise():
    lo, hi = CONFIG["quadDisguise_pq"]
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0 or p == q) and attempts < 60:
        p = R(lo, hi); q = R(lo, hi); attempts += 1
    B, C = p + q, p * q
    Bstr = sign_str(B) if B != 0 else ""
    Cstr = sign_str(C)
    f1 = f"(x^2{sign_str(p)})"
    f2 = f"(x^2{sign_str(q)})"
    return {
        "problemTex": f"x^4{Bstr}x^2{Cstr}",
        "answerTex": f"{f1}{f2}",
        "answerNorm": None,
        "originalExpanded": f"x^4{Bstr}x^2{Cstr}",
        "isQuadDisguise": True,
        "steps": [
            {"label": "Substitute u = x²", "math": f"u^2{Bstr}u{Cstr}", "note": "Quadratic in disguise"},
            {"label": "Factor as quadratic", "math": f"(u{sign_str(p)})(u{sign_str(q)})", "note": ""},
            {"label": "Back-substitute", "math": f"{f1}{f2}", "note": "u = x²"},
        ],
    }


diff3 = [_quartic, _grouping, _quad_disguise]


# ─── diff4 (frac/neg exponent GCF) ───

def _frac_gcf_a():
    r = R(2, 6)
    return {
        "problemTex": f"x^{{5/2}} - x^{{1/2}}",
        "answerTex": f"x^{{1/2}}(x+1)(x-1)",
        "answerNorm": None,
        "validForms": ["x^(1/2)(x+1)(x-1)", "x^(1/2)(x-1)(x+1)", "(x+1)(x-1)x^(1/2)"],
        "isFracExpGcf": True,
        "steps": [
            {"label": "Factor out x^(1/2)", "math": "x^{1/2}(x^{5/2-1/2} - x^{1/2-1/2})", "note": ""},
            {"label": "Simplify", "math": "x^{1/2}(x^2 - 1)", "note": ""},
            {"label": "Factor diff of squares", "math": "x^{1/2}(x+1)(x-1)", "note": ""},
        ],
    }


def _frac_gcf_b():
    k = R(*CONFIG["fracNegGcf_k"])
    m = R(2, 5)
    return {
        "problemTex": f"{k}x^{{-1}} - {k*m}x^{{-2}}",
        "answerTex": f"{k}x^{{-2}}(x-{m})",
        "answerNorm": None,
        "validForms": [f"{k}x^(-2)(x-{m})", f"(x-{m}){k}x^(-2)"],
        "isFracExpGcf": True,
        "steps": [
            {"label": "Lowest exponent = -2", "math": f"\\text{{factor out }}{k}x^{{-2}}", "note": ""},
            {"label": "Simplify", "math": f"{k}x^{{-2}}(x-{m})", "note": ""},
        ],
    }


def _frac_gcf_c():
    k = R(2, 8)
    r = R(2, 6)
    return {
        "problemTex": f"{k}x^{{3/2}} - {k*r}x^{{1/2}}",
        "answerTex": f"{k}x^{{1/2}}(x-{r})",
        "answerNorm": None,
        "validForms": [f"{k}x^(1/2)(x-{r})", f"x^(1/2)({k}x-{k*r})"],
        "isFracExpGcf": True,
        "steps": [
            {"label": f"GCF = {k}x^(1/2)", "math": f"{k}x^{{1/2}}\\left(x - {r}\\right)", "note": "lowest power is 1/2"},
            {"label": "Simplify inner", "math": "x^{3/2-1/2}=x^1=x", "note": ""},
        ],
    }


def _frac_gcf_d():
    k = R(2, 6)
    m = R(2, 5)
    return {
        "problemTex": f"{k}x^{{-2}} - {k*m}x^{{-1}}",
        "answerTex": f"{k}x^{{-2}}(1-{m}x)",
        "answerNorm": None,
        "validForms": [f"{k}x^(-2)(1-{m}x)", f"(1-{m}x){k}x^(-2)"],
        "isFracExpGcf": True,
        "steps": [
            {"label": "Lowest exponent = -2", "math": f"\\text{{factor out }}{k}x^{{-2}}", "note": ""},
            {"label": "Simplify", "math": f"{k}x^{{-2}}(1-{m}x)", "note": ""},
        ],
    }


diff4 = [_frac_gcf_a, _frac_gcf_b, _frac_gcf_c, _frac_gcf_d]


# ─── diff5 (trig + rational roots) ───

def _trig_sin():
    lo, hi = CONFIG["trigTrinomial_pq"]
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(lo, hi); q = R(lo, hi); attempts += 1
    b, c = p + q, p * q
    bstr = sign_str(b) if b != 0 else ""
    cstr = sign_str(c)
    fp = sign_str(p); fq = sign_str(q)
    return {
        "problemTex": f"\\sin^2 x{bstr}\\sin x{cstr}",
        "answerTex": f"(\\sin x{fp})(\\sin x{fq})",
        "answerNorm": None,
        "isTrigFactoring": True,
        "trigFunc": "sin",
        "originalExpandedPoly": poly_to_tex([1, b, c]),
        "steps": [
            {"label": "Let u = sin x", "math": f"u^2{bstr}u{cstr}", "note": "substitute"},
            {"label": f"Find p, q: p+q={b}, pq={c}", "math": f"p={p},\\quad q={q}", "note": ""},
            {"label": "Back-substitute", "math": f"(\\sin x{fp})(\\sin x{fq})", "note": ""},
        ],
    }


def _trig_cos():
    a = R(*CONFIG["trigLeadCoeff_a"])
    lo, hi = CONFIG["leadCoeff_pq"]
    p, q, attempts = 0, 0, 0
    while (p == 0 or q == 0) and attempts < 50:
        p = R(lo, hi); q = R(lo, hi); attempts += 1
    B, C = p + a * q, p * q
    Bstr = sign_str(B) if B != 0 else ""
    Cstr = sign_str(C)
    fp = sign_str(p); fq = sign_str(q)
    return {
        "problemTex": f"{a}\\cos^2 x{Bstr}\\cos x{Cstr}",
        "answerTex": f"({a}\\cos x{fp})(\\cos x{fq})",
        "answerNorm": None,
        "isTrigFactoring": True,
        "trigFunc": "cos",
        "originalExpandedPoly": poly_to_tex([a, B, C]),
        "steps": [
            {"label": "Let u = cos x", "math": f"{a}u^2{Bstr}u{Cstr}", "note": ""},
            {"label": "Factor", "math": f"({a}\\cos x{fp})(\\cos x{fq})", "note": ""},
        ],
    }


def _trig_tan():
    k = R(2, 9)
    k2 = k * k
    return {
        "problemTex": f"\\tan^2 x - {k2}",
        "answerTex": f"(\\tan x+{k})(\\tan x-{k})",
        "answerNorm": None,
        "isTrigFactoring": True,
        "trigFunc": "tan",
        "originalExpandedPoly": poly_to_tex([1, 0, -k2]),
        "steps": [
            {"label": "Recognize diff of squares", "math": f"(\\tan x)^2 - {k}^2", "note": ""},
            {"label": "Factor", "math": f"(\\tan x+{k})(\\tan x-{k})", "note": ""},
        ],
    }


def _cubic_roots():
    lo, hi = CONFIG["cubicRoots"]
    r1, r2, r3, attempts = 0, 0, 0, 0
    while (r1 == 0 or r2 == 0 or r3 == 0 or len({r1,r2,r3}) < 3) and attempts < 60:
        r1 = R(lo, hi); r2 = R(lo, hi); r3 = R(lo, hi); attempts += 1
    B = -(r1+r2+r3)
    C = r1*r2 + r1*r3 + r2*r3
    D = -(r1*r2*r3)
    Bstr = sign_str(B) if B != 0 else ""
    Cstr = sign_str(C) if C != 0 else ""
    Dstr = sign_str(D) if D != 0 else ""
    def fac(r): return f"(x{sign_str(-r)})"
    return {
        "problemTex": f"x^3{Bstr}x^2{Cstr}x{Dstr}",
        "answerTex": f"{fac(r1)}{fac(r2)}{fac(r3)}",
        "answerNorm": None,
        "originalExpanded": poly_to_tex([1, B, C, D]),
        "steps": [
            {"label": "Rational Root candidates", "math": f"\\pm\\text{{factors of }}{abs(D)}", "note": "test each"},
            {"label": f"Roots", "math": f"x={r1},\\; x={r2},\\; x={r3}", "note": ""},
            {"label": "Factor", "math": f"{fac(r1)}{fac(r2)}{fac(r3)}", "note": ""},
        ],
    }


diff5 = [_trig_sin, _trig_cos, _trig_tan, _cubic_roots]


POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
