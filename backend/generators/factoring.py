from math_utils import R, pick, gcd, lcm, simplify_frac, sign_str, poly_to_tex, expand_expression
from problem_builder import problem, step

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


# ─── diff1 ───

def _diff_squares():
    a = R(*CONFIG["diffSquares_a"])
    a2 = a * a
    return problem(
        problem_tex=f"x^2 - {a2}",
        answer_tex=f"(x+{a})(x-{a})",
        answer_norm=None,
        steps=[
            step("Recognize pattern", f"x^2 - {a2} = x^2 - {a}^2", "Difference of squares: a²−b²"),
            step("Apply formula", f"(x+{a})(x-{a})", "a²−b² = (a+b)(a−b)"),
        ],
        originalExpanded=f"x^2-{a2}",
    )


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
    return problem(
        problem_tex=f"x^2 {bstr}x {cstr}",
        answer_tex=f"{f1}{f2}",
        answer_norm=None,
        steps=[
            step("Find two numbers", f"p+q={b},\\; pq={c}", f"Need two numbers that add to {b} and multiply to {c}"),
            step("Those numbers", f"p={p},\\; q={q}", f"Check: sum={b}, product={c}"),
            step("Factor", f"{f1}{f2}", ""),
        ],
        originalExpanded=poly_to_tex([1, b, c]),
    )


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
    return problem(
        problem_tex=f"{k}x^3{kbstr}x^2{kcstr}x",
        answer_tex=f"{k}x{f1}{f2}",
        answer_norm=None,
        steps=[
            step("Factor out GCF", f"{k}x(x^2{bstr}x{cstr})", f"GCF = {k}x"),
            step("Factor trinomial", f"{k}x{f1}{f2}", ""),
        ],
        originalExpanded=poly_to_tex([k, kb, kc, 0]),
    )


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
    return problem(
        problem_tex=f"{k}x^2 {kbstr}x {kcstr}",
        answer_tex=f"{k}{f1}{f2}",
        answer_norm=None,
        steps=[
            step("Factor out GCF", f"{k}(x^2{bstr}x{cstr})", f"GCF = {k}"),
            step("Factor trinomial", f"{k}{f1}{f2}", ""),
        ],
        originalExpanded=poly_to_tex([k, kb, kc]),
    )


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
    return problem(
        problem_tex=f"{a}x^2 {Bstr}x {Cstr}",
        answer_tex=f"{f1p}{f2q}",
        answer_norm=None,
        steps=[
            step("AC method", f"a\\cdot c = {a}\\cdot{C} = {a*C}", ""),
            step("Find factors", f"{p}\\cdot{a*q}={a*C},\\quad {p}+{a*q}={B}", ""),
            step("Factor", f"{f1p}{f2q}", ""),
        ],
        originalExpanded=poly_to_tex([a, B, C]),
    )


def _diff_cubes():
    a = R(*CONFIG["cubes_a"])
    a3 = a ** 3
    return problem(
        problem_tex=f"x^3 - {a3}",
        answer_tex=f"(x-{a})(x^2+{a}x+{a*a})",
        answer_norm=None,
        steps=[
            step("Recognize difference of cubes", f"x^3 - {a}^3", "a³−b³=(a−b)(a²+ab+b²)"),
            step("Apply formula", f"(x-{a})(x^2+{a}x+{a*a})", f"a=x, b={a}"),
        ],
        originalExpanded=f"x^3 - {a3}",
    )


def _sum_cubes():
    a = R(*CONFIG["cubes_a"])
    a3 = a ** 3
    return problem(
        problem_tex=f"x^3 + {a3}",
        answer_tex=f"(x+{a})(x^2-{a}x+{a*a})",
        answer_norm=None,
        steps=[
            step("Recognize sum of cubes", f"x^3 + {a}^3", "a³+b³=(a+b)(a²−ab+b²)"),
            step("Apply formula", f"(x+{a})(x^2-{a}x+{a*a})", f"a=x, b={a}"),
        ],
        originalExpanded=f"x^3 + {a3}",
    )


diff2 = [_gcf, _lead_coeff, _diff_cubes, _sum_cubes]


# ─── diff3 ───

def _quartic():
    a = R(*CONFIG["quartic_a"])
    a2, a4 = a * a, a ** 4
    return problem(
        problem_tex=f"x^4 - {a4}",
        answer_tex=f"(x^2+{a2})(x+{a})(x-{a})",
        answer_norm=None,
        steps=[
            step("Difference of squares (outer)", f"(x^2)^2-({a2})^2=(x^2+{a2})(x^2-{a2})", ""),
            step("Factor second bracket", f"x^2-{a2}=(x+{a})(x-{a})", "Difference of squares again"),
        ],
        originalExpanded=f"x^4 - {a4}",
    )


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
    return problem(
        problem_tex=f"x^3{term2}{term3}{term4}",
        answer_tex=f"(x^2{f1b})(x{f1a})",
        answer_norm=None,
        steps=[
            step("Group first two and last two", f"(x^3{term2})+({b}x{term4})", ""),
            step("Factor from each group", f"x^2(x{f1a})+{b}(x{f1a})", ""),
            step("Factor common binomial", f"(x^2{f1b})(x{f1a})", ""),
        ],
        originalExpanded=f"x^3{term2}{term3}{term4}",
        isGrouping=True,
    )


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
    return problem(
        problem_tex=f"x^4{Bstr}x^2{Cstr}",
        answer_tex=f"{f1}{f2}",
        answer_norm=None,
        steps=[
            step("Substitute u = x²", f"u^2{Bstr}u{Cstr}", "Quadratic in disguise"),
            step("Factor as quadratic", f"(u{sign_str(p)})(u{sign_str(q)})", ""),
            step("Back-substitute", f"{f1}{f2}", "u = x²"),
        ],
        originalExpanded=f"x^4{Bstr}x^2{Cstr}",
        isQuadDisguise=True,
    )


diff3 = [_quartic, _grouping, _quad_disguise]


# ─── diff4 (frac/neg exponent GCF) ───

def _frac_gcf_a():
    r = R(2, 6)
    return problem(
        problem_tex="x^{5/2} - x^{1/2}",
        answer_tex="x^{1/2}(x+1)(x-1)",
        answer_norm=None,
        steps=[
            step("Factor out x^(1/2)", "x^{1/2}(x^{5/2-1/2} - x^{1/2-1/2})", ""),
            step("Simplify", "x^{1/2}(x^2 - 1)", ""),
            step("Factor diff of squares", "x^{1/2}(x+1)(x-1)", ""),
        ],
        validForms=["x^(1/2)(x+1)(x-1)", "x^(1/2)(x-1)(x+1)", "(x+1)(x-1)x^(1/2)"],
        isFracExpGcf=True,
    )


def _frac_gcf_b():
    k = R(*CONFIG["fracNegGcf_k"])
    m = R(2, 5)
    return problem(
        problem_tex=f"{k}x^{{-1}} - {k*m}x^{{-2}}",
        answer_tex=f"{k}x^{{-2}}(x-{m})",
        answer_norm=None,
        steps=[
            step("Lowest exponent = -2", f"\\text{{factor out }}{k}x^{{-2}}", ""),
            step("Simplify", f"{k}x^{{-2}}(x-{m})", ""),
        ],
        validForms=[f"{k}x^(-2)(x-{m})", f"(x-{m}){k}x^(-2)"],
        isFracExpGcf=True,
    )


def _frac_gcf_c():
    k = R(2, 8)
    r = R(2, 6)
    return problem(
        problem_tex=f"{k}x^{{3/2}} - {k*r}x^{{1/2}}",
        answer_tex=f"{k}x^{{1/2}}(x-{r})",
        answer_norm=None,
        steps=[
            step(f"GCF = {k}x^(1/2)", f"{k}x^{{1/2}}\\left(x - {r}\\right)", "lowest power is 1/2"),
            step("Simplify inner", "x^{3/2-1/2}=x^1=x", ""),
        ],
        validForms=[f"{k}x^(1/2)(x-{r})", f"x^(1/2)({k}x-{k*r})"],
        isFracExpGcf=True,
    )


def _frac_gcf_d():
    k = R(2, 6)
    m = R(2, 5)
    return problem(
        problem_tex=f"{k}x^{{-2}} - {k*m}x^{{-1}}",
        answer_tex=f"{k}x^{{-2}}(1-{m}x)",
        answer_norm=None,
        steps=[
            step("Lowest exponent = -2", f"\\text{{factor out }}{k}x^{{-2}}", ""),
            step("Simplify", f"{k}x^{{-2}}(1-{m}x)", ""),
        ],
        validForms=[f"{k}x^(-2)(1-{m}x)", f"(1-{m}x){k}x^(-2)"],
        isFracExpGcf=True,
    )


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
    return problem(
        problem_tex=f"\\sin^2 x{bstr}\\sin x{cstr}",
        answer_tex=f"(\\sin x{fp})(\\sin x{fq})",
        answer_norm=None,
        steps=[
            step("Let u = sin x", f"u^2{bstr}u{cstr}", "substitute"),
            step(f"Find p, q: p+q={b}, pq={c}", f"p={p},\\quad q={q}", ""),
            step("Back-substitute", f"(\\sin x{fp})(\\sin x{fq})", ""),
        ],
        isTrigFactoring=True,
        trigFunc="sin",
        originalExpandedPoly=poly_to_tex([1, b, c]),
    )


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
    return problem(
        problem_tex=f"{a}\\cos^2 x{Bstr}\\cos x{Cstr}",
        answer_tex=f"({a}\\cos x{fp})(\\cos x{fq})",
        answer_norm=None,
        steps=[
            step("Let u = cos x", f"{a}u^2{Bstr}u{Cstr}", ""),
            step("Factor", f"({a}\\cos x{fp})(\\cos x{fq})", ""),
        ],
        isTrigFactoring=True,
        trigFunc="cos",
        originalExpandedPoly=poly_to_tex([a, B, C]),
    )


def _trig_tan():
    k = R(2, 9)
    k2 = k * k
    return problem(
        problem_tex=f"\\tan^2 x - {k2}",
        answer_tex=f"(\\tan x+{k})(\\tan x-{k})",
        answer_norm=None,
        steps=[
            step("Recognize diff of squares", f"(\\tan x)^2 - {k}^2", ""),
            step("Factor", f"(\\tan x+{k})(\\tan x-{k})", ""),
        ],
        isTrigFactoring=True,
        trigFunc="tan",
        originalExpandedPoly=poly_to_tex([1, 0, -k2]),
    )


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
    return problem(
        problem_tex=f"x^3{Bstr}x^2{Cstr}x{Dstr}",
        answer_tex=f"{fac(r1)}{fac(r2)}{fac(r3)}",
        answer_norm=None,
        steps=[
            step("Rational Root candidates", f"\\pm\\text{{factors of }}{abs(D)}", "test each"),
            step(f"Roots", f"x={r1},\\; x={r2},\\; x={r3}", ""),
            step("Factor", f"{fac(r1)}{fac(r2)}{fac(r3)}", ""),
        ],
        originalExpanded=poly_to_tex([1, B, C, D]),
    )


diff5 = [_trig_sin, _trig_cos, _trig_tan, _cubic_roots]


POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}