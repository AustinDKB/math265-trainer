from math_utils import R, pick, sign_str, simplify_frac
from problem_builder import problem, step

# ── asympt1 — horizontal asymptotes ────────────────────────────────────────────

def _ha_degree_less():
    """deg(numerator) < deg(denominator) → y = 0"""
    a = R(1, 5)
    b = R(1, 5)
    n_deg = R(1, 2)
    d_deg = R(n_deg + 1, n_deg + 3)
    
    num_tex = f"{a}x^{{{n_deg}}}" if n_deg > 1 else f"{a}x"
    den_tex = f"{b}x^{{{d_deg}}}" if d_deg > 1 else f"{b}x"
    
    return problem(
        problem_tex=f"\\text{{Find the horizontal asymptote of }} f(x) = \\dfrac{{{num_tex}}}{{{den_tex}}}",
        answer_tex="y = 0",
        answer_norm="y=0",
        steps=[
            step("Compare degrees", f"\\text{{deg(numerator)}} = {n_deg}, \\text{{deg(denominator)}} = {d_deg}"),
            step("Apply rule", f"\\text{{deg(num)}} < \\text{{deg(den)}} \\implies \\text{{horizontal asymptote is }} y = 0"),
        ],
    )


def _ha_degree_equal():
    """deg(numerator) = deg(denominator) → y = ratio of leading coeffs"""
    deg = R(1, 3)
    a = R(2, 7)
    b = R(2, 7)
    n, d = simplify_frac(a, b)
    
    num_tex = f"{a}x^{{{deg}}}" if deg > 1 else f"{a}x"
    den_tex = f"{b}x^{{{deg}}}" if deg > 1 else f"{b}x"
    
    if d == 1:
        ans_tex = f"y = {n}"
        ans_norm = f"y={n}"
    else:
        ans_tex = f"y = \\dfrac{{{n}}}{{{d}}}"
        ans_norm = f"y={n}/{d}"
    
    return problem(
        problem_tex=f"\\text{{Find the horizontal asymptote of }} f(x) = \\dfrac{{{num_tex}}}{{{den_tex}}}",
        answer_tex=ans_tex,
        answer_norm=ans_norm,
        steps=[
            step("Compare degrees", f"\\text{{deg(numerator)}} = \\text{{deg(denominator)}} = {deg}"),
            step("Apply rule", f"\\text{{HA: }} y = \\dfrac{{\\text{{leading coeff num}}}}{{\\text{{leading coeff den}}}} = \\dfrac{{{a}}}{{{b}}}"),
            step("Simplify", ans_tex),
        ],
    )


def _ha_degree_greater():
    """deg(numerator) > deg(denominator) → no horizontal asymptote"""
    a = R(2, 5)
    b = R(2, 5)
    n_deg = R(3, 5)
    d_deg = R(1, n_deg - 1)
    
    num_tex = f"{a}x^{{{n_deg}}}" if n_deg > 1 else f"{a}x"
    den_tex = f"{b}x^{{{d_deg}}}" if d_deg > 1 else f"{b}x"
    
    return problem(
        problem_tex=f"\\text{{Find the horizontal asymptote of }} f(x) = \\dfrac{{{num_tex}}}{{{den_tex}}}",
        answer_tex="\\text{none}",
        answer_norm="none",
        steps=[
            step("Compare degrees", f"\\text{{deg(numerator)}} = {n_deg}, \\text{{deg(denominator)}} = {d_deg}"),
            step("Apply rule", f"\\text{{deg(num)}} > \\text{{deg(den)}} \\implies \\text{{no horizontal asymptote}}"),
            step("Note", "\\text{There may be a slant (oblique) asymptote instead}"),
        ],
    )


# ── asympt2 — vertical asymptotes ─────────────────────────────────────────────

def _va_rational():
    """Find vertical asymptotes where denominator = 0, numerator ≠ 0"""
    a = R(1, 5)
    b = R(1, 5)
    while b == a:
        b = R(1, 5)
    
    num_tex = f"x - {b}" if b != 0 else "x"
    den_tex = f"(x - {a})(x - {b})" if b != 0 else f"x(x - {a})"
    
    return problem(
        problem_tex=f"\\text{{Find the vertical asymptote(s) of }} f(x) = \\dfrac{{{num_tex}}}{{{den_tex}}}",
        answer_tex=f"x = {a}",
        answer_norm=f"x={a}",
        steps=[
            step("Factor denominator", f"\\text{{denominator}} = {den_tex}"),
            step("Find zeros of denominator", f"x = {a}, {b}"),
            step("Check numerator", f"\\text{{numerator}} = {num_tex} \\text{{ is zero at }} x = {b}"),
            step("Cancel common factors", f"(x - {b}) \\text{{ cancels, leaving a hole at }} x = {b}"),
            step("Vertical asymptote", f"\\text{{VA: }} x = {a}"),
        ],
    )


def _va_simple_rational():
    """Simple rational: 1/(x-a)"""
    a = R(-5, 5)
    while a == 0:
        a = R(-5, 5)
    
    den_tex = f"x - {a}" if a > 0 else f"x + {-a}"
    
    return problem(
        problem_tex=f"\\text{{Find the vertical asymptote of }} f(x) = \\dfrac{{1}}{{{den_tex}}}",
        answer_tex=f"x = {a}",
        answer_norm=f"x={a}",
        steps=[
            step("Set denominator to zero", f"{den_tex} = 0"),
            step("Solve", f"x = {a}"),
            step("Vertical asymptote", f"x = {a}"),
        ],
    )


# ── asympt3 — slant (oblique) asymptotes ──────────────────────────────────────

def _slant_asymptote():
    """deg(numerator) = deg(denominator) + 1 → slant asymptote via polynomial division"""
    a = R(2, 5)
    b = R(-3, 3)
    c = R(1, 3)
    d = R(-3, 3)
    
    # (ax² + bx + c) / (cx + d) → quotient is (a/c)x + (bc-ad)/c²
    slope = simplify_frac(a, c)
    intercept_num = b * c - a * d
    intercept_den = c * c
    intercept = simplify_frac(intercept_num, intercept_den)
    
    num_tex = f"{a}x^2 {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)}"
    den_tex = f"{c}x {'+' if d >= 0 else '-'} {abs(d)}"
    
    if slope[1] == 1:
        slope_tex = str(slope[0])
    else:
        slope_tex = f"\\dfrac{{{slope[0]}}}{{{slope[1]}}}"
    
    if intercept[1] == 1:
        intercept_tex = str(intercept[0])
    else:
        intercept_tex = f"\\dfrac{{{intercept[0]}}}{{{intercept[1]}}}"
    
    ans_norm = f"y={slope[0]}/{slope[1]}*x+{intercept[0]}/{intercept[1]}" if slope[1] != 1 or intercept[1] != 1 else f"y={slope[0]}*x+{intercept[0]}"
    
    return problem(
        problem_tex=f"\\text{{Find the slant asymptote of }} f(x) = \\dfrac{{{num_tex}}}{{{den_tex}}}",
        answer_tex=f"y = {slope_tex}x {'+' if intercept[0] >= 0 else '-'} {abs(intercept[0]) if intercept[1] == 1 else f'\\dfrac{{{abs(intercept[0])}}}{{{intercept[1]}}}'}",
        answer_norm=ans_norm,
        steps=[
            step("Check degrees", f"\\text{{deg(num)}} = 2, \\text{{deg(den)}} = 1 \\implies \\text{{slant asymptote exists}}"),
            step("Polynomial long division", f"\\dfrac{{{num_tex}}}{{{den_tex}}} = {slope_tex}x {'+' if intercept[0] >= 0 else '-'} \\dfrac{{{abs(intercept[0])}}}{{{intercept[1]}}} + \\text{{remainder}}"),
            step("Slant asymptote", f"y = {slope_tex}x {'+' if intercept[0] >= 0 else '-'} \\dfrac{{{abs(intercept[0])}}}{{{intercept[1]}}}"),
        ],
    )


# ── asympt4 — combined: all asymptotes ────────────────────────────────────────

def _all_asymptotes():
    """Find all asymptotes (HA, VA, slant) for a rational function"""
    cases = [
        {
            "num": "2x^2 + 3x - 1",
            "den": "x^2 - 4",
            "ha": "y = 2",
            "ha_norm": "y=2",
            "va": "x = -2, \\quad x = 2",
            "va_norm": "x=-2,x=2",
            "steps": [
                step("Horizontal asymptote", "\\text{deg(num)} = \\text{deg(den)} = 2 \\implies y = \\dfrac{2}{1} = 2"),
                step("Vertical asymptotes", "x^2 - 4 = 0 \\implies (x-2)(x+2) = 0 \\implies x = \\pm 2"),
                step("Slant asymptote", "\\text{deg(num)} = \\text{deg(den)} \\implies \\text{no slant asymptote}"),
            ],
        },
        {
            "num": "x^2 - 1",
            "den": "x - 3",
            "ha": "\\text{none}",
            "ha_norm": "none",
            "va": "x = 3",
            "va_norm": "x=3",
            "slant": "y = x + 3",
            "slant_norm": "y=x+3",
            "steps": [
                step("Horizontal asymptote", "\\text{deg(num)} = 2 > \\text{deg(den)} = 1 \\implies \\text{no HA}"),
                step("Vertical asymptote", "x - 3 = 0 \\implies x = 3"),
                step("Slant asymptote", "\\text{deg(num)} = \\text{deg(den)} + 1 \\implies \\text{slant exists}"),
                step("Polynomial division", "\\dfrac{x^2 - 1}{x - 3} = x + 3 + \\dfrac{8}{x-3}"),
                step("Slant asymptote", "y = x + 3"),
            ],
        },
    ]
    c = pick(cases)
    
    ans_tex = f"\\text{{HA: }} {c['ha']}; \\quad \\text{{VA: }} {c['va']}"
    if "slant" in c:
        ans_tex += f"; \\quad \\text{{Slant: }} {c['slant']}"
    
    return problem(
        problem_tex=f"\\text{{Find all asymptotes of }} f(x) = \\dfrac{{{c['num']}}}{{{c['den']}}}",
        answer_tex=ans_tex,
        answer_norm=c["ha_norm"] + ";" + c["va_norm"],
        steps=c["steps"],
    )


# ── asympt5 — advanced asymptote problems ─────────────────────────────────────

def _asymptote_with_hole():
    """Rational function with both a hole and vertical asymptote"""
    cases = [
        {
            "num": "(x-2)(x+1)",
            "den": "(x-2)(x-3)",
            "hole": "x = 2",
            "va": "x = 3",
            "ha": "y = 1",
            "steps": [
                step("Factor", "f(x) = \\dfrac{(x-2)(x+1)}{(x-2)(x-3)}"),
                step("Cancel common factors", "f(x) = \\dfrac{x+1}{x-3}, \\quad x \\neq 2"),
                step("Hole", "x = 2 \\text{ (where factor canceled)}"),
                step("Vertical asymptote", "x - 3 = 0 \\implies x = 3"),
                step("Horizontal asymptote", "\\text{deg(num)} = \\text{deg(den)} = 1 \\implies y = \\dfrac{1}{1} = 1"),
            ],
        },
    ]
    c = pick(cases)
    
    return problem(
        problem_tex=f"\\text{{Find all asymptotes and holes of }} f(x) = \\dfrac{{{c['num']}}}{{{c['den']}}}",
        answer_tex=f"\\text{{HA: }} {c['ha']}; \\quad \\text{{VA: }} {c['va']}; \\quad \\text{{Hole: }} {c['hole']}",
        answer_norm=f"y={c['ha'].replace(' ','')};x={c['va'].replace(' ','')};hole={c['hole'].replace(' ','')}",
        steps=c["steps"],
    )


asympt1 = [_ha_degree_less, _ha_degree_equal, _ha_degree_greater]
asympt2 = [_va_rational, _va_simple_rational]
asympt3 = [_slant_asymptote]
asympt4 = [_all_asymptotes]
asympt5 = [_asymptote_with_hole]

POOLS = {1: asympt1, 2: asympt2, 3: asympt3, 4: asympt4, 5: asympt5}
