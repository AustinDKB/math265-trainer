import random
from fractions import Fraction
from math_utils import R, pick, sign_str
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from symbolic import X, Const, Mul, Pow, Sin, Cos, Exp, Ln, Var, add, mul, neg, pow_expr, diff_and_simplify

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
    return {
        "problemTex": f"\\lim_{{x \\to {a}}} \\left({poly}\\right)",
        "answerTex": str(result),
        "answerNorm": str(result),
        "steps": [
            {"label": "Direct substitution", "math": f"\\text{{Plug in }} x={a}", "note": "polynomial → just substitute"},
            {"label": "Compute", "math": f"{poly.replace('x', f'({a})')} = {result}", "note": ""},
        ],
    }


def _factor_cancel():
    a = R(1, 8)
    # lim(x→a) (x² - a²)/(x - a) = x + a, limit = 2a
    a2 = a * a
    result = 2 * a
    return {
        "problemTex": f"\\lim_{{x \\to {a}}} \\dfrac{{x^2-{a2}}}{{x-{a}}}",
        "answerTex": str(result),
        "answerNorm": str(result),
        "steps": [
            {"label": "Try direct substitution","math": f"\\dfrac{{{a}^2-{a2}}}{{{a}-{a}}}=\\dfrac{{0}}{{0}}", "note": "indeterminate — factor"},
            {"label": "Factor numerator", "math": f"\\dfrac{{(x+{a})(x-{a})}}{{x-{a}}}", "note": "difference of squares"},
            {"label": "Cancel (x−a)", "math": f"x+{a}", "note": f"x \\neq {a}"},
            {"label": "Evaluate at x={a}", "math": f"{a}+{a}={result}", "note": ""},
        ],
    }


def _factor_cancel_cubic():
    a = R(1, 5)
    # lim(x→a) (x³ - a³)/(x - a) = x² + ax + a², limit = 3a²
    a3 = a**3; a2 = a**2
    result = 3 * a2
    return {
        "problemTex": f"\\lim_{{x \\to {a}}} \\dfrac{{x^3-{a3}}}{{x-{a}}}",
        "answerTex": str(result),
        "answerNorm": str(result),
        "steps": [
            {"label": "Try direct substitution","math": f"\\dfrac{{{a}^3-{a3}}}{{{a}-{a}}}=\\dfrac{{0}}{{0}}", "note": "factor sum of cubes"},
            {"label": "Factor", "math": f"\\dfrac{{(x-{a})(x^2+{a}x+{a2})}}{{x-{a}}}", "note": "difference of cubes: a³-b³=(a-b)(a²+ab+b²)"},
            {"label": "Cancel", "math": f"x^2+{a}x+{a2}", "note": ""},
            {"label": "Substitute", "math": f"{a}^2+{a}\\cdot{a}+{a2}={result}", "note": ""},
        ],
    }


def _inf_rational():
    # lim(x→∞) (ax^n + ...) / (bx^m + ...)
    case = pick([1, 2, 3])
    if case == 1:
        # deg num < deg denom → 0
        a, b = R(1,5), R(1,5)
        return {
            "problemTex": f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x+{R(1,5)}}}{{{b}x^2+1}}",
            "answerTex": "0",
            "answerNorm": "0",
            "steps": [
                {"label": "Highest power in denominator", "math": "x^2", "note": ""},
                {"label": "Divide all terms by x²", "math": f"\\dfrac{{{a}/x+{R(1,5)}/x^2}}{{{b}+1/x^2}} \\to \\dfrac{{0}}{{{b}}}=0", "note": ""},
            ],
        }
    elif case == 2:
        # deg num = deg denom → a/b
        a, b = R(1,6), R(1,6)
        f = Fraction(a, b)
        res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
        return {
            "problemTex": f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x^2+3x}}{{{b}x^2-1}}",
            "answerTex": res_tex,
            "answerNorm": f"{f.numerator}/{f.denominator}",
            "steps": [
                {"label": "Equal degrees → ratio of leading coefficients", "math": f"\\dfrac{{{a}}}{{{b}}}={res_tex}", "note": ""},
            ],
        }
    else:
        # deg num > deg denom → ∞
        a = R(1,4)
        return {
            "problemTex": f"\\lim_{{x \\to \\infty}} \\dfrac{{{a}x^3+1}}{{x^2+5}}",
            "answerTex": "\\infty",
            "answerNorm": "inf",
            "steps": [
                {"label": "Numerator degree > denominator degree", "math": "\\to \\infty", "note": "numerator grows faster"},
            ],
        }


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
    return {
        "problemTex": f"\\lim_{{x \\to {a}}} \\dfrac{{\\sqrt{{x}}-{sa}}}{{x-{a}}}",
        "answerTex": res_tex,
        "answerNorm": res_norm,
        "steps": [
            {"label": "0/0 — multiply by conjugate", "math": f"\\cdot \\dfrac{{\\sqrt{{x}}+{sa}}}{{\\sqrt{{x}}+{sa}}}", "note": ""},
            {"label": "Numerator: difference of squares", "math": f"\\dfrac{{x-{a}}}{{(x-{a})(\\sqrt{{x}}+{sa})}}", "note": "(√x−a)(√x+a)=x−a"},
            {"label": "Cancel (x−a)", "math": f"\\dfrac{{1}}{{\\sqrt{{x}}+{sa}}}", "note": ""},
            {"label": "Substitute x={a}", "math": f"\\dfrac{{1}}{{{sa}+{sa}}}={res_tex}", "note": ""},
        ],
    }


def _trig_sin_over_x():
    # lim(x→0) sin(kx)/(mx) = k/m
    k, m = R(1,7), R(1,7)
    f = Fraction(k, m)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return {
        "problemTex": f"\\lim_{{x \\to 0}} \\dfrac{{\\sin({k}x)}}{{{m}x}}",
        "answerTex": res_tex,
        "answerNorm": f"{f.numerator}/{f.denominator}",
        "steps": [
            {"label": "Goal: get sin(argument)/same argument", "math": f"\\dfrac{{\\sin({k}x)}}{{{m}x}}", "note": f"The denominator is {m}x but sin's argument is {k}x — they must match for the trig limit to apply."},
            {"label": f"Multiply numerator and denominator by {k}", "math": f"\\dfrac{{{k}}}{{{m}}} \\cdot \\dfrac{{\\sin({k}x)}}{{{k}x}}", "note": f"Multiplying by {k}/{k} = 1 doesn't change the value. Now sin({k}x) is divided by its own argument {k}x."},
            {"label": "Substitute u = " + f"{k}x", "math": f"\\dfrac{{{k}}}{{{m}}} \\cdot \\dfrac{{\\sin(u)}}{{u}}, \\quad u = {k}x", "note": f"As x → 0, u = {k}x → 0 as well. This is the standard form of the fundamental trig limit."},
            {"label": "Fundamental trig limit: sin(u)/u → 1 as u → 0", "math": f"\\dfrac{{{k}}}{{{m}}} \\cdot 1 = {res_tex}", "note": "This limit comes from the squeeze theorem and is a foundational result. The sine of a small angle is approximately equal to that angle itself."},
        ],
    }


def _trig_one_minus_cos():
    # lim(x→0) (1 - cos(kx)) / x² = k²/2
    k = R(1, 5)
    k2 = k * k
    f = Fraction(k2, 2)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return {
        "problemTex": f"\\lim_{{x \\to 0}} \\dfrac{{1-\\cos({k}x)}}{{x^2}}",
        "answerTex": res_tex,
        "answerNorm": f"{f.numerator}/{f.denominator}",
        "steps": [
            {"label": "Rewrite with k²", "math": f"k^2 \\cdot \\dfrac{{1-\\cos({k}x)}}{{{k}^2x^2}}", "note": ""},
            {"label": "Known limit: (1-cos u)/u² → 1/2", "math": f"{k2} \\cdot \\dfrac{{1}}{{2}} = {res_tex}", "note": ""},
        ],
    }


def _trig_tan_sin():
    # lim(x→0) tan(kx)/sin(mx) = k/m
    k, m = R(1, 6), R(1, 6)
    f = Fraction(k, m)
    res_tex = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return {
        "problemTex": f"\\lim_{{x \\to 0}} \\dfrac{{\\tan({k}x)}}{{\\sin({m}x)}}",
        "answerTex": res_tex,
        "answerNorm": f"{f.numerator}/{f.denominator}",
        "steps": [
            {"label": "Write tan as sin/cos", "math": f"\\dfrac{{\\sin({k}x)}}{{\\cos({k}x)\\cdot\\sin({m}x)}}", "note": ""},
            {"label": "Multiply/divide by x", "math": f"\\dfrac{{{k}}}{{m}} \\cdot \\dfrac{{\\sin({k}x)/{k}x}}{{\\sin({m}x)/{m}x}} \\cdot \\dfrac{{1}}{{\\cos({k}x)}}", "note": ""},
            {"label": "Apply sin(u)/u → 1, cos(0)=1", "math": f"\\dfrac{{{k}}}{{{m}}} \\cdot 1 \\cdot 1 = {res_tex}", "note": ""},
        ],
    }


diff2 = [_rationalize, _trig_sin_over_x, _trig_sin_over_x, _trig_one_minus_cos, _trig_tan_sin]

# ── diff3 — L'Hôpital (uses symbolic engine) ──────────────────────────────────

def _lhopital_basic():
    # lim(x→0) (e^x - 1 - x) / x² = 1/2
    # Or lim(x→0) (sin x - x) / x³ = -1/6 — too hard, use simpler
    cases = [
        # (problemTex, answerTex, answerNorm, steps)
        (
            "\\lim_{x \\to 0} \\dfrac{e^x - 1 - x}{x^2}",
            "\\dfrac{1}{2}",
            "1/2",
            [
                {"label": "Direct substitution: 0/0 indeterminate form", "math": "\\dfrac{e^0-1-0}{0^2}=\\dfrac{0}{0}", "note": ""},
                {"label": "L'Hôpital: differentiate top and bottom", "math": "\\lim_{x\\to0}\\dfrac{e^x-1}{2x}", "note": ""},
                {"label": "Still 0/0 — apply again", "math": "\\lim_{x\\to0}\\dfrac{e^x}{2}=\\dfrac{1}{2}", "note": ""},
            ],
        ),
        (
            "\\lim_{x \\to 0} \\dfrac{\\sin x}{x}",
            "1",
            "1",
            [
                {"label": "Direct substitution: 0/0 indeterminate form", "math": "\\dfrac{\\sin 0}{0}=\\dfrac{0}{0}", "note": ""},
                {"label": "L'Hôpital", "math": "\\lim_{x\\to0}\\dfrac{\\cos x}{1}=1", "note": ""},
            ],
        ),
        (
            "\\lim_{x \\to 0} \\dfrac{\\ln(1+x)}{x}",
            "1",
            "1",
            [
                {"label": "Direct substitution: 0/0 indeterminate form", "math": "\\dfrac{\\ln 1}{0}=\\dfrac{0}{0}", "note": ""},
                {"label": "L'Hôpital: d/dx[ln(1+x)]=1/(1+x)", "math": "\\lim_{x\\to0}\\dfrac{1/(1+x)}{1}=1", "note": ""},
            ],
        ),
    ]
    prob = pick(cases)
    return {
        "problemTex": prob[0],
        "answerTex": prob[1],
        "answerNorm": prob[2],
        "steps": prob[3],
    }


def _difference_quotient():
    # lim(h→0) [f(x+h) - f(x)] / h for simple f
    cases = [
        ("x^2", "2x", "2x", [
            {"label": "Expand (x+h)²", "math": "\\dfrac{x^2+2xh+h^2-x^2}{h}", "note": ""},
            {"label": "Simplify", "math": "\\dfrac{2xh+h^2}{h}=2x+h", "note": ""},
            {"label": "h→0", "math": "2x", "note": ""},
        ]),
        ("x^3", "3x^2", "3x^2", [
            {"label": "Expand (x+h)³", "math": "\\dfrac{x^3+3x^2h+3xh^2+h^3-x^3}{h}", "note": ""},
            {"label": "Factor h", "math": "3x^2+3xh+h^2", "note": ""},
            {"label": "h→0", "math": "3x^2", "note": ""},
        ]),
        ("\\sqrt{x}", "\\dfrac{1}{2\\sqrt{x}}", "1/(2*sqrt(x))", [
            {"label": "Multiply by conjugate", "math": "\\dfrac{\\sqrt{x+h}-\\sqrt{x}}{h}\\cdot\\dfrac{\\sqrt{x+h}+\\sqrt{x}}{\\sqrt{x+h}+\\sqrt{x}}", "note": ""},
            {"label": "Numerator simplifies", "math": "\\dfrac{(x+h)-x}{h(\\sqrt{x+h}+\\sqrt{x})}=\\dfrac{1}{\\sqrt{x+h}+\\sqrt{x}}", "note": ""},
            {"label": "h→0", "math": "\\dfrac{1}{2\\sqrt{x}}", "note": ""},
        ]),
    ]
    case = pick(cases)
    return {
        "problemTex": f"\\lim_{{h \\to 0}} \\dfrac{{({case[0]}+h)_{{\\text{{at }}x+h}} - ({case[0]})}}{{h}}",
        "answerTex": case[1],
        "answerNorm": case[2],
        "steps": case[3],
    }


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
    return {
        "problemTex": (
            f"f(x) = \\begin{{cases}} {c}x{b_tex} & x < {a} \\\\ x^2 - {a*a} + {c*a} & x \\geq {a} \\end{{cases}}"
            f"\\quad \\text{{Is }} f \\text{{ continuous at }} x={a}?"
        ),
        "answerTex": "\\text{Yes}" if cts else "\\text{No}",
        "answerNorm": "yes" if cts else "no",
        "steps": [
            {"label": "Left limit", "math": f"\\lim_{{x\\to{a}^-}} ({c}x{b_tex}) = {int(left_val)}", "note": ""},
            {"label": "Right limit", "math": f"\\lim_{{x\\to{a}^+}} (x^2-{a*a}+{c*a}) = {int(right_val)}", "note": ""},
            {"label": "f(a)", "math": f"f({a}) = {int(right_val)}", "note": ""},
            {"label": "Conclusion", "math": "\\text{Continuous}" if cts else f"\\text{{Not continuous: limits differ ({int(left_val)} ≠ {int(right_val)})}}", "note": ""},
        ],
    }


diff3 = [_lhopital_basic, _lhopital_basic, _difference_quotient, _piecewise_continuity]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _lhopital_product_form():
    # lim(x→0+) x·ln(x) = 0 — classic 0·(-∞) form
    return {
        "problemTex": "\\lim_{x \\to 0^+} x \\ln x",
        "answerTex": "0",
        "answerNorm": "0",
        "steps": [
            {"label": "Form: 0·(-∞) — rewrite as fraction", "math": "\\lim_{x\\to0^+}\\dfrac{\\ln x}{1/x}", "note": "-∞/∞ form"},
            {"label": "L'Hôpital: d/dx[ln x]=1/x, d/dx[1/x]=-1/x²", "math": "\\lim_{x\\to0^+}\\dfrac{1/x}{-1/x^2}=\\lim_{x\\to0^+}(-x)", "note": ""},
            {"label": "Evaluate", "math": "\\lim_{x\\to0^+}(-x)=0", "note": ""},
        ],
    }


def _one_sided_limits():
    cases = [
        (
            "\\lim_{x \\to 0^+} \\dfrac{1}{x}",
            "+\\infty",
            "inf",
            [{"label": "x→0 from right, 1/x→+∞", "math": "\\to +\\infty", "note": ""}],
        ),
        (
            "\\lim_{x \\to 0^-} \\dfrac{1}{x}",
            "-\\infty",
            "-inf",
            [{"label": "x→0 from left, 1/x→-∞", "math": "\\to -\\infty", "note": ""}],
        ),
        (
            "\\lim_{x \\to 0} |x|/x",
            "\\text{DNE}",
            "DNE",
            [
                {"label": "Right limit", "math": "\\lim_{x\\to0^+}|x|/x = 1", "note": "x>0 so |x|=x"},
                {"label": "Left limit", "math": "\\lim_{x\\to0^-}|x|/x = -1", "note": "x<0 so |x|=-x"},
                {"label": "One-sided limits differ — limit does not exist", "math": "\\text{DNE}", "note": ""},
            ],
        ),
    ]
    prob = pick(cases)
    return {"problemTex": prob[0], "answerTex": prob[1], "answerNorm": prob[2], "steps": prob[3]}


def _limit_ln_exp():
    cases = [
        (
            "\\lim_{x \\to \\infty} x e^{-x}",
            "0",
            "0",
            [
                {"label": "Rewrite: xe^{-x} = x/e^x → ∞/∞", "math": "\\lim_{x\\to\\infty}\\dfrac{x}{e^x}", "note": ""},
                {"label": "L'Hôpital", "math": "\\lim_{x\\to\\infty}\\dfrac{1}{e^x}=0", "note": "e^x grows faster"},
            ],
        ),
        (
            "\\lim_{x \\to \\infty} \\dfrac{\\ln x}{x}",
            "0",
            "0",
            [
                {"label": "∞/∞ — L'Hôpital", "math": "\\lim_{x\\to\\infty}\\dfrac{1/x}{1}=0", "note": "ln grows slower than x"},
            ],
        ),
    ]
    prob = pick(cases)
    return {"problemTex": prob[0], "answerTex": prob[1], "answerNorm": prob[2], "steps": prob[3]}


diff4 = [_lhopital_product_form, _one_sided_limits, _one_sided_limits, _limit_ln_exp]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _indeterminate_inf_minus_inf():
    return {
        "problemTex": "\\lim_{x \\to 0} \\left(\\dfrac{1}{\\sin x} - \\dfrac{1}{x}\\right)",
        "answerTex": "0",
        "answerNorm": "0",
        "steps": [
            {"label": "∞−∞ form — combine fractions", "math": "\\dfrac{x - \\sin x}{x \\sin x}", "note": "common denominator"},
            {"label": "0/0 — L'Hôpital once", "math": "\\dfrac{1-\\cos x}{\\sin x + x\\cos x}", "note": ""},
            {"label": "Still 0/0 — L'Hôpital again", "math": "\\dfrac{\\sin x}{2\\cos x - x\\sin x}=\\dfrac{0}{2}=0", "note": ""},
        ],
    }


def _lhopital_three():
    return {
        "problemTex": "\\lim_{x \\to 0} \\dfrac{x - \\sin x}{x^3}",
        "answerTex": "\\dfrac{1}{6}",
        "answerNorm": "1/6",
        "steps": [
            {"label": "0/0 — L'Hôpital once", "math": "\\dfrac{1-\\cos x}{3x^2}", "note": ""},
            {"label": "Still 0/0 — again", "math": "\\dfrac{\\sin x}{6x}", "note": ""},
            {"label": "Apply trig limit sin(x)/x → 1", "math": "\\dfrac{1}{6}\\cdot 1 = \\dfrac{1}{6}", "note": ""},
        ],
    }


def _limit_sequence():
    cases = [
        (
            "\\lim_{n \\to \\infty} \\left(1+\\dfrac{1}{n}\\right)^n",
            "e",
            "e",
            [{"label": "Definition of e", "math": "e = \\lim_{n\\to\\infty}\\left(1+\\frac{1}{n}\\right)^n", "note": "fundamental limit"}],
        ),
        (
            "\\lim_{n \\to \\infty} n^{1/n}",
            "1",
            "1",
            [
                {"label": "Let y=n^{1/n}, take ln", "math": "\\ln y = \\dfrac{\\ln n}{n}\\to 0", "note": "L'Hôpital or squeeze"},
                {"label": "So y = e^0 = 1", "math": "\\lim n^{1/n}=1", "note": ""},
            ],
        ),
    ]
    prob = pick(cases)
    return {"problemTex": prob[0], "answerTex": prob[1], "answerNorm": prob[2], "steps": prob[3]}


diff5 = [_indeterminate_inf_minus_inf, _lhopital_three, _limit_sequence]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
