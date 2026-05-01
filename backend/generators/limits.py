import random
from fractions import Fraction
from math_utils import R, pick, sign_str
from symbolic import X, Const, Mul, Pow, Sin, Cos, Exp, Ln, Var, add, mul, neg, pow_expr, diff_and_simplify
from problem_builder import problem, step

# ── diff1 ──────────────────────────────────────────────────────────────────────

def _direct_substitution():
    # lim(x→a) of polynomial
    a = R(-4, 4)
    coeffs = [R(-3,3), R(-5,5), R(-8,8)]  # cx² + bx + d
    while all(c == 0 for c in coeffs):
        coeffs = [R(-3,3), R(-5,5), R(-8,8)]
    c, b, d = coeffs
    result = c * a**2 + b * a + d
    c_tex = "" if c == 0 else (f"{c}x^2" if c != 1 else "x^2")
    b_tex = "" if b == 0 else sign_str(b) + "x" if c != 0 else (str(b) + "x")
    d_tex = "" if d == 0 else sign_str(d) if (c != 0 or b != 0) else str(d)
    poly = c_tex + b_tex + d_tex or "0"
    return problem(
        problem_tex=f"\\lim_{{x \\to {a}}} \\left({poly}\\right)",
        answer_tex=str(result),
        answer_norm=str(result),
        steps=[
            step("Direct substitution", f"\\text{{Plug in }} x={a}", "polynomial → just substitute"),
            step("Compute", f"{poly.replace('x', f'({a})')} = {result}"),
        ],
    )


def _factor_cancel():
    a = R(1, 8)
    # lim(x→a) (x² - a²)/(x - a) = x + a, limit = 2a
    a2 = a * a
    result = 2 * a
    return problem(
        problem_tex=f"\\lim_{{x \\to {a}}} \\dfrac{{x^2-{a2}}}{{x-{a}}}",
        answer_tex=str(result),
        answer_norm=str(result),
        steps=[
            step("Try direct substitution", f"\\dfrac{{{a}^2-{a2}}}{{{a}-{a}}}=\\dfrac{{0}}{{0}}", "indeterminate — factor"),
            step("Factor numerator", f"\\dfrac{{(x+{a})(x-{a})}}{{x-{a}}}", "difference of squares"),
            step("Cancel (x−a)", f"x+{a}", f"x \\neq {a}"),
            step("Evaluate at x={a}", f"{a}+{a}={result}"),
        ],
    )


def _factor_cancel_cubic():
    a = R(1, 5)
    # lim(x→a) (x³ - a³)/(x - a) = x² + ax + a², limit = 3a²
    a3 = a**3; a2 = a**2
    result = 3 * a2
    return problem(
        problem_tex=f"\\lim_{{x \\to {a}}} \\dfrac{{x^3-{a3}}}{{x-{a}}}",
        answer_tex=str(result),
        answer_norm=str(result),
        steps=[
            step("Try direct substitution", f"\\dfrac{{{a}^3-{a3}}}{{{a}-{a}}}=\\dfrac{{0}}{{0}}", "factor sum of cubes"),
            step("Factor", f"\\dfrac{{(x-{a})(x^2+{a}x+{a2})}}{{x-{a}}}", "difference of cubes: a³-b³=(a-b)(a²+ab+b²)"),
            step("Cancel", f"x^2+{a}x+{a2}"),
            step("Substitute", f"{a}^2+{a}\\cdot{a}+{a2}={result}"),
        ],
    )


def _inf_rational():
    # lim(x→∞) (ax^n + ...) / (bx^m + ...)
    case = pick([1, 2, 3])
    if case == 1:
        # deg num < deg denom → 0
        a, b = R(1,5), R(1,5)
        return problem(
            problem_tex=f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x+{R(1,5)}}}{{{b}x^2+1}}",
            answer_tex="0",
            answer_norm="0",
            steps=[
                step("Highest power in denominator", "x^2"),
                step("Divide all terms by x²", f"\\dfrac{{{a}/x+{R(1,5)}/x^2}}{{{b}+1/x^2}} \\to \\dfrac{{0}}{{{b}}}=0"),
            ],
        )
    elif case == 2:
        # deg num = deg denom → a/b
        a, b = R(1,6), R(1,6)
        f = Fraction(a, b)
        res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
        return problem(
            problem_tex=f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x^2+3x}}{{{b}x^2-1}}",
            answer_tex=res_tex,
            answer_norm=f"{f.numerator}/{f.denominator}",
            steps=[
                step("Equal degrees → ratio of leading coefficients", f"\\dfrac{{{a}}}{{{b}}}={res_tex}"),
            ],
        )
    else:
        # deg num > deg denom → ∞
        a = R(1,4)
        return problem(
            problem_tex=f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x^3+1}}{{x^2+5}}",
            answer_tex="\\infty",
            answer_norm="inf",
            steps=[
                step("Numerator degree > denominator degree", "\\to \\infty", "numerator grows faster"),
            ],
        )


diff1 = [_direct_substitution, _factor_cancel, _factor_cancel, _factor_cancel_cubic, _inf_rational]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _rationalize():
    # lim(x→a) (√x - √a) / (x - a) = 1/(2√a); a ∈ {1,4,9,16}
    a = pick([1, 4, 9, 16])
    sa = int(a**0.5)
    # result = 1/(2√a) = 1/(2·sa)
    f = Fraction(1, 2 * sa)
    res_tex = f"\\dfrac{{1}}{{2\\sqrt{{{a}}}}} = \\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    res_norm = f"{f.numerator}/{f.denominator}"
    return problem(
        problem_tex=f"\\lim_{{x \\to {a}}} \\dfrac{{\\sqrt{{x}}-{sa}}}{{x-{a}}}",
        answer_tex=res_tex,
        answer_norm=res_norm,
        steps=[
            step("0/0 — multiply by conjugate", f"\\cdot \\dfrac{{\\sqrt{{x}}+{sa}}}{{\\sqrt{{x}}+{sa}}}"),
            step("Numerator: difference of squares", f"\\dfrac{{x-{a}}}{{(x-{a})(\\sqrt{{x}}+{sa})}}", "(√x−a)(√x+a)=x−a"),
            step("Cancel (x−a)", f"\\dfrac{{1}}{{\\sqrt{{x}}+{sa}}}"),
            step("Substitute x={a}", f"\\dfrac{{1}}{{{sa}+{sa}}}={res_tex}"),
        ],
    )


def _trig_sin_over_x():
    # lim(x→0) sin(kx)/(mx) = k/m
    k, m = R(1,7), R(1,7)
    f = Fraction(k, m)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return problem(
        problem_tex=f"\\lim_{{x \\to 0}} \\dfrac{{\\sin({k}x)}}{{{m}x}}",
        answer_tex=res_tex,
        answer_norm=f"{f.numerator}/{f.denominator}",
        steps=[
            step("Goal: get sin(argument)/same argument", f"\\dfrac{{\\sin({k}x)}}{{{m}x}}", f"The denominator is {m}x but sin's argument is {k}x — they must match for the trig limit to apply."),
            step(f"Multiply numerator and denominator by {k}", f"\\dfrac{{{k}}}{{{m}}} \\cdot \\dfrac{{\\sin({k}x)}}{{{k}x}}", f"Multiplying by {k}/{k} = 1 doesn't change the value. Now sin({k}x) is divided by its own argument {k}x."),
            step("Substitute u = " + f"{k}x", f"\\dfrac{{{k}}}{{{m}}} \\cdot \\dfrac{{\\sin(u)}}{{u}}, \\quad u = {k}x", f"As x → 0, u = {k}x → 0 as well. This is the standard form of the fundamental trig limit."),
            step("Fundamental trig limit: sin(u)/u → 1 as u → 0", f"\\dfrac{{{k}}}{{{m}}} \\cdot 1 = {res_tex}", "This limit comes from the squeeze theorem and is a foundational result. The sine of a small angle is approximately equal to that angle itself."),
        ],
    )


def _trig_one_minus_cos():
    # lim(x→0) (1 - cos(kx)) / x² = k²/2
    k = R(1, 5)
    k2 = k * k
    f = Fraction(k2, 2)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return problem(
        problem_tex=f"\\lim_{{x \\to 0}} \\dfrac{{1-\\cos({k}x)}}{{x^2}}",
        answer_tex=res_tex,
        answer_norm=f"{f.numerator}/{f.denominator}",
        steps=[
            step("Rewrite with k²", f"k^2 \\cdot \\dfrac{{1-\\cos({k}x)}}{{{k}^2x^2}}"),
            step("Known limit: (1-cos u)/u² → 1/2", f"{k2} \\cdot \\dfrac{{1}}{{2}} = {res_tex}"),
        ],
    )


def _trig_tan_sin():
    # lim(x→0) tan(kx)/sin(mx) = k/m
    k, m = R(1, 6), R(1, 6)
    f = Fraction(k, m)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return problem(
        problem_tex=f"\\lim_{{x \\to 0}} \\dfrac{{\\tan({k}x)}}{{\\sin({m}x)}}",
        answer_tex=res_tex,
        answer_norm=f"{f.numerator}/{f.denominator}",
        steps=[
            step("Write tan as sin/cos", f"\\dfrac{{\\sin({k}x)}}{{\\cos({k}x)\\cdot\\sin({m}x)}}"),
            step("Multiply/divide by x", f"\\dfrac{{{k}}}{{m}} \\cdot \\dfrac{{\\sin({k}x)/{k}x}}{{\\sin({m}x)/{m}x}} \\cdot \\dfrac{{1}}{{\\cos({k}x)}}"),
            step("Apply sin(u)/u → 1, cos(0)=1", f"\\dfrac{{{k}}}{{{m}}} \\cdot 1 \\cdot 1 = {res_tex}"),
        ],
    )


diff2 = [_rationalize, _trig_sin_over_x, _trig_sin_over_x, _trig_one_minus_cos, _trig_tan_sin]

# ── diff3 — L'Hôpital (uses symbolic engine) ──────────────────────────────────

def _lhopital_basic():
    # lim(x→0) (e^x - 1 - x) / x² = 1/2
    # Or lim(x→0) (sin x - x) / x³ = -1/6 — too hard, use simpler
    cases = [
        (
            "\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2}",
            "\\dfrac{1}{2}",
            "1/2",
            [
                step("Direct substitution: 0/0 indeterminate form", "\\dfrac{e^0-1-0}{0^2}=\\dfrac{0}{0}"),
                step("L'Hôpital: differentiate top and bottom", "\\lim_{x\\to0}\\dfrac{e^x-1}{2x}"),
                step("Still 0/0 — apply again", "\\lim_{x\\to0}\\dfrac{e^x}{2}=\\dfrac{1}{2}"),
            ],
        ),
        (
            "\\lim_{x \\to 0} \\dfrac{\\sin x}{x}",
            "1",
            "1",
            [
                step("Direct substitution: 0/0 indeterminate form", "\\dfrac{\\sin 0}{0}=\\dfrac{0}{0}"),
                step("L'Hôpital", "\\lim_{x\\to0}\\dfrac{\\cos x}{1}=1"),
            ],
        ),
        (
            "\\lim_{x \\to 0} \\dfrac{\\ln(1+x)}{x}",
            "1",
            "1",
            [
                step("Direct substitution: 0/0 indeterminate form", "\\dfrac{\\ln 1}{0}=\\dfrac{0}{0}"),
                step("L'Hôpital: d/dx[ln(1+x)]=1/(1+x)", "\\lim_{x\\to0}\\dfrac{1/(1+x)}{1}=1"),
            ],
        ),
    ]
    prob = pick(cases)
    return problem(problem_tex=prob[0], answer_tex=prob[1], answer_norm=prob[2], steps=prob[3])


def _difference_quotient():
    # lim(h→0) [f(x+h) - f(x)] / h for simple f
    cases = [
        ("x^2", "2x", "2x", [
            step("Expand (x+h)²", "\\dfrac{x^2+2xh+h^2-x^2}{h}"),
            step("Simplify", "\\dfrac{2xh+h^2}{h}=2x+h"),
            step("h→0", "2x"),
        ]),
        ("x^3", "3x^2", "3x^2", [
            step("Expand (x+h)³", "\\dfrac{x^3+3x^2h+3xh^2+h^3-x^3}{h}"),
            step("Factor h", "3x^2+3xh+h^2"),
            step("h→0", "3x^2"),
        ]),
        ("\\sqrt{x}", "\\dfrac{1}{2\\sqrt{x}}", "1/(2*sqrt(x))", [
            step("Multiply by conjugate", "\\dfrac{\\sqrt{x+h}-\\sqrt{x}}{h}\\cdot\\dfrac{\\sqrt{x+h}+\\sqrt{x}}{\\sqrt{x+h}+\\sqrt{x}}"),
            step("Numerator simplifies", "\\dfrac{(x+h)-x}{h(\\sqrt{x+h}+\\sqrt{x})}=\\dfrac{1}{\\sqrt{x+h}+\\sqrt{x}}"),
            step("h→0", "\\dfrac{1}{2\\sqrt{x}}"),
        ]),
    ]
    case = pick(cases)
    return problem(
        problem_tex=f"\\lim_{{h \\to 0}} \\dfrac{{({case[0]}+h)_{{\\text{{at }}x+h}} - ({case[0]})}}{{h}}",
        answer_tex=case[1],
        answer_norm=case[2],
        steps=case[3],
    )


def _piecewise_continuity():
    a = R(1, 6)
    c = R(-3, 3)
    # f(x) = cx + (a - c*a) if x < a, else x² - a²  + ca
    # left limit: ca + (a - ca) = a
    # right limit: a² - a² + ca = ca
    # continuous if ca = a → c = 1
    left_val = c * a + (a - c * a)
    right_val = a * a - a * a + c * a
    cts = abs(left_val - right_val) < 0.001
    b_const = a - c * a
    b_tex = f"+{b_const}" if b_const >= 0 else str(b_const)
    return problem(
        problem_tex=(
            f"f(x) = \\begin{{cases}} {c}x{b_tex} & x < {a} \\\\ x^2 - {a*a} + {c*a} & x \\geq {a} \\end{{cases}}"
            f"\\quad \\text{{Is }} f \\text{{ continuous at }} x={a}?"
        ),
        answer_tex="\\text{Yes}" if cts else "\\text{No}",
        answer_norm="yes" if cts else "no",
        steps=[
            step("Left limit", f"\\lim_{{x\\to{a}^-}} ({c}x{b_tex}) = {int(left_val)}"),
            step("Right limit", f"\\lim_{{x\\to{a}^+}} (x^2-{a*a}+{c*a}) = {int(right_val)}"),
            step("f(a)", f"f({a}) = {int(right_val)}"),
            step("Conclusion", "\\text{Continuous}" if cts else f"\\text{{Not continuous: limits differ ({int(left_val)} ≠ {int(right_val)})}}"),
        ],
    )


diff3 = [_lhopital_basic, _lhopital_basic, _difference_quotient, _piecewise_continuity]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _lhopital_product_form():
    # lim(x→0+) x·ln(x) = 0 — classic 0·(-∞) form
    return problem(
        problem_tex="\\lim_{x \\to 0^+} x \\ln x",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("Form: 0·(-∞) — rewrite as fraction", "\\lim_{x\\to0^+}\\dfrac{\\ln x}{1/x}", "-∞/∞ form"),
            step("L'Hôpital: d/dx[ln x]=1/x, d/dx[1/x]=-1/x²", "\\lim_{x\\to0^+}\\dfrac{1/x}{-1/x^2}=\\lim_{x\\to0^+}(-x)"),
            step("Evaluate", "\\lim_{x\\to0^+}(-x)=0"),
        ],
    )


def _one_sided_limits():
    cases = [
        (
            "\\lim_{x \\to 0^+} \\dfrac{1}{x}",
            "+\\infty",
            "inf",
            [step("x→0 from right, 1/x→+∞", "\\to +\\infty")],
        ),
        (
            "\\lim_{x \\to 0^-} \\dfrac{1}{x}",
            "-\\infty",
            "-inf",
            [step("x→0 from left, 1/x→-∞", "\\to -\\infty")],
        ),
        (
            "\\lim_{x \\to 0} |x|/x",
            "\\text{DNE}",
            "DNE",
            [
                step("Right limit", "\\lim_{x\\to0^+}|x|/x = 1", "x>0 so |x|=x"),
                step("Left limit", "\\lim_{x\\to0^-}|x|/x = -1", "x<0 so |x|=-x"),
                step("One-sided limits differ — limit does not exist", "\\text{DNE}"),
            ],
        ),
    ]
    prob = pick(cases)
    return problem(problem_tex=prob[0], answer_tex=prob[1], answer_norm=prob[2], steps=prob[3])


def _limit_ln_exp():
    cases = [
        (
            "\\lim_{x \\to \\infty} x e^{-x}",
            "0",
            "0",
            [
                step("Rewrite: xe^{-x} = x/e^x → ∞/∞", "\\lim_{x\\to\\infty}\\dfrac{x}{e^x}"),
                step("L'Hôpital", "\\lim_{x\\to\\infty}\\dfrac{1}{e^x}=0", "e^x grows faster"),
            ],
        ),
        (
            "\\lim_{x \\to \\infty} \\dfrac{\\ln x}{x}",
            "0",
            "0",
            [
                step("∞/∞ — L'Hôpital", "\\lim_{x\\to\\infty}\\dfrac{1/x}{1}=0", "ln grows slower than x"),
            ],
        ),
    ]
    prob = pick(cases)
    return problem(problem_tex=prob[0], answer_tex=prob[1], answer_norm=prob[2], steps=prob[3])


diff4 = [_lhopital_product_form, _one_sided_limits, _one_sided_limits, _limit_ln_exp]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _indeterminate_inf_minus_inf():
    return problem(
        problem_tex="\\lim_{x \\to 0} \\left(\\dfrac{1}{\\sin x} - \\dfrac{1}{x}\\right)",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("∞−∞ form — combine fractions", "\\dfrac{x - \\sin x}{x \\sin x}", "common denominator"),
            step("0/0 — L'Hôpital once", "\\dfrac{1-\\cos x}{\\sin x + x\\cos x}"),
            step("Still 0/0 — L'Hôpital again", "\\dfrac{\\sin x}{2\\cos x - x\\sin x}=\\dfrac{0}{2}=0"),
        ],
    )


def _lhopital_three():
    return problem(
        problem_tex="\\lim_{x \\to 0} \\dfrac{x - \\sin x}{x^3}",
        answer_tex="\\dfrac{1}{6}",
        answer_norm="1/6",
        steps=[
            step("0/0 — L'Hôpital once", "\\dfrac{1-\\cos x}{3x^2}"),
            step("Still 0/0 — again", "\\dfrac{\\sin x}{6x}"),
            step("Apply trig limit sin(x)/x → 1", "\\dfrac{1}{6}\\cdot 1 = \\dfrac{1}{6}"),
        ],
    )


def _limit_sequence():
    cases = [
        (
            "\\lim_{n \\to \\infty} \\left(1+\\dfrac{1}{n}\\right)^n",
            "e",
            "e",
            [step("Definition of e", "e = \\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n", "fundamental limit")],
        ),
        (
            "\\lim_{n \\to \\infty} n^{1/n}",
            "1",
            "1",
            [
                step("Let y=n^{1/n}, take ln", "\\ln y = \\dfrac{\\ln n}{n}\\to 0", "L'Hôpital or squeeze"),
                step("So y = e^0 = 1", "\\lim n^{1/n}=1"),
            ],
        ),
    ]
    prob = pick(cases)
    return problem(problem_tex=prob[0], answer_tex=prob[1], answer_norm=prob[2], steps=prob[3])


diff5 = [_indeterminate_inf_minus_inf, _lhopital_three, _limit_sequence]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}