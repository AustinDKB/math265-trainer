import random
from fractions import Fraction
from math_utils import R, pick, sign_str

def _plus_C(tex): return tex + " + C"

# ── diff1 — basic antiderivatives ─────────────────────────────────────────────

def _power_rule():
    n = pick([-3,-2,1,2,3,4,5])  # exclude -1
    a = R(1, 8)
    # ∫ ax^n dx = a/(n+1) * x^(n+1) + C
    f = Fraction(a, n + 1)
    num, den = f.numerator, f.denominator
    coeff_tex = str(num) if den == 1 else f"\\dfrac{{{num}}}{{{den}}}"
    if den == 1 and num == 1:
        coeff_tex = ""
    exp = n + 1
    if exp == 1:
        ans_tex = f"{coeff_tex}x"
    elif exp == 0:
        ans_tex = coeff_tex or "1"
    else:
        ans_tex = f"{coeff_tex}x^{{{exp}}}"
    expr_tex = f"{a}x^{{{n}}}" if n not in [1,-1] else (f"{a}x" if n==1 else f"{a}/x")
    return {
        "problemTex": f"\\displaystyle\\int {expr_tex}\\,dx",
        "answerTex": _plus_C(ans_tex),
        "answerNorm": f"{num}/{den}*x^({exp})+C",
        "steps": [
            {"label": "Power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1)+C", "math": f"\\dfrac{{{a}}}{{{{n+1}}}}x^{{{exp}}}+C = {ans_tex}+C", "note": ""},
        ],
    }


def _one_over_x():
    return {
        "problemTex": "\\displaystyle\\int \\dfrac{1}{x}\\,dx",
        "answerTex": _plus_C("\\ln|x|"),
        "answerNorm": "ln|x|+C",
        "steps": [{"label": "Special case n=−1", "math": "\\ln|x|+C", "note": "undefined at x=0; absolute value needed"}],
    }


def _exp_rule():
    a = R(1, 5)
    a_tex = "" if a == 1 else str(a)
    ans_tex = f"e^{{{a_tex}x}}" if a > 1 else "e^x"
    ans_full = ans_tex if a == 1 else f"\\dfrac{{1}}{{{a}}}e^{{{a}x}}"
    ans_norm = f"e^({a}*x)/{a}+C"
    return {
        "problemTex": f"\\displaystyle\\int e^{{{a_tex}x}}\\,dx",
        "answerTex": _plus_C(ans_full),
        "answerNorm": ans_norm,
        "steps": [
            {"label": "∫e^(ax) dx = e^(ax)/a + C", "math": _plus_C(ans_full), "note": ""},
        ],
    }


def _basic_trig():
    cases = [
        ("\\sin x",     "-\\cos x",         "-cos(x)+C"),
        ("\\cos x",     "\\sin x",           "sin(x)+C"),
        ("\\sec^2 x",   "\\tan x",           "tan(x)+C"),
        ("\\csc^2 x",   "-\\cot x",          "-cot(x)+C"),
        ("\\sec x\\tan x", "\\sec x",        "sec(x)+C"),
        ("\\csc x\\cot x","-\\csc x",        "-csc(x)+C"),
    ]
    f_tex, ans_tex, ans_norm = pick(cases)
    return {
        "problemTex": f"\\displaystyle\\int {f_tex}\\,dx",
        "answerTex": _plus_C(ans_tex),
        "answerNorm": ans_norm,
        "steps": [{"label": "Standard trig antiderivative", "math": _plus_C(ans_tex), "note": "memorize"}],
    }


def _sum_diff():
    n, m = pick([2,3,4]), pick([0,1])
    a, b = R(1,5), R(1,5)
    sign = pick(["+","-"])
    f1 = Fraction(a, n+1); f2 = Fraction(b, m+1)
    c1 = f"{f1.numerator}" if f1.denominator == 1 else f"\\dfrac{{{f1.numerator}}}{{{f1.denominator}}}"
    c2 = f"{f2.numerator}" if f2.denominator == 1 else f"\\dfrac{{{f2.numerator}}}{{{f2.denominator}}}"
    t1_tex = f"{a}x^{n}" if n > 1 else (f"{a}x" if n == 1 else str(a))
    t2_tex = f"{b}x^{m}" if m > 1 else (f"{b}x" if m == 1 else str(b))
    a1_tex = f"{c1}x^{{{n+1}}}" if n+1 > 1 else f"{c1}x"
    a2_tex = f"{c2}x^{{{m+1}}}" if m+1 > 1 else f"{c2}x"
    prob = f"({t1_tex}{'+' if sign=='+' else '-'}{t2_tex})"
    ans = f"{a1_tex}{'+' if sign=='+' else '-'}{a2_tex}"
    # Build evaluatable norm (no LaTeX dfrac — uses a/b*x^n form)
    def _coeff_norm(f):
        return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
    def _term_norm(coeff_n, exp):
        if exp == 0: return coeff_n
        base = f"x^{exp}" if exp > 1 else "x"
        return base if coeff_n == "1" else f"{coeff_n}*{base}"
    t1_n = _term_norm(_coeff_norm(f1), n + 1)
    t2_n = _term_norm(_coeff_norm(f2), m + 1)
    sep = "+" if sign == "+" else "-"
    return {
        "problemTex": f"\\displaystyle\\int {prob}\\,dx",
        "answerTex": _plus_C(ans),
        "answerNorm": f"{t1_n}{sep}{t2_n}+C",
        "steps": [{"label": "Integrate term by term", "math": _plus_C(ans), "note": ""}],
    }


diff1 = [_power_rule, _power_rule, _one_over_x, _exp_rule, _basic_trig, _sum_diff]

# ── diff2 — u-substitution (backward generation) ─────────────────────────────

def _usub_linear():
    # ∫ f(ax+b) dx — backward: F(x)=G(ax+b)/a
    a = R(2, 6); b = R(-4, 4)
    n = pick([2,3,4])
    # F(x) = (ax+b)^(n+1) / (a*(n+1))
    denom = a * (n + 1)
    f = Fraction(1, denom)
    num_tex = f"({{a}}x{sign_str(b)})^{{{n+1}}}"
    prob_tex = f"({a}x{sign_str(b)})^{n}"
    ans_tex = f"\\dfrac{{({a}x{sign_str(b)})^{{{n+1}}}}}{{{denom}}}" + " + C"
    return {
        "problemTex": f"\\displaystyle\\int {prob_tex}\\,dx",
        "answerTex": ans_tex,
        "answerNorm": f"({a}x+{b})^({n+1})/{denom}+C",
        "steps": [
            {"label": "u = inner linear", "math": f"u={a}x{sign_str(b)},\\; du={a}\\,dx", "note": ""},
            {"label": "Rewrite", "math": f"\\dfrac{{1}}{{{a}}}\\int u^{n}\\,du", "note": ""},
            {"label": "Integrate", "math": f"\\dfrac{{1}}{{{a}}} \\cdot \\dfrac{{u^{{{n+1}}}}}{{{n+1}}}+C", "note": ""},
            {"label": "Substitute back", "math": ans_tex, "note": ""},
        ],
    }


def _usub_polynomial():
    # ∫ x·f(x²) dx — backward: u=x², du=2x dx
    cases = [
        ("x \\cdot e^{x^2}", "\\dfrac{1}{2}e^{x^2}+C", "0.5*e^(x^2)+C",
         "u=x^2", "du=2x\\,dx", "\\frac{1}{2}\\int e^u\\,du"),
        ("x\\sqrt{x^2+1}", "\\dfrac{1}{3}(x^2+1)^{3/2}+C", "(x^2+1)^(3/2)/3+C",
         "u=x^2+1", "du=2x\\,dx", "\\frac{1}{2}\\int u^{1/2}\\,du"),
        ("\\dfrac{x}{x^2+4}", "\\dfrac{1}{2}\\ln(x^2+4)+C", "0.5*ln(x^2+4)+C",
         "u=x^2+4", "du=2x\\,dx", "\\frac{1}{2}\\int \\frac{1}{u}\\,du"),
    ]
    prob, ans, norm, u_sub, du, integral = pick(cases)
    return {
        "problemTex": f"\\displaystyle\\int {prob}\\,dx",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Identify u", "math": u_sub, "note": ""},
            {"label": "Compute du", "math": du, "note": ""},
            {"label": "Rewrite integral", "math": integral, "note": ""},
            {"label": "Integrate and back-substitute", "math": ans, "note": ""},
        ],
    }


def _usub_trig():
    cases = [
        ("\\sin x \\cos x", "\\dfrac{\\sin^2 x}{2}+C", "sin^2(x)/2+C", "u=\\sin x","du=\\cos x\\,dx"),
        ("\\sin^3 x \\cos x", "\\dfrac{\\sin^4 x}{4}+C", "sin^4(x)/4+C", "u=\\sin x","du=\\cos x\\,dx"),
        ("\\tan x \\sec^2 x",  "\\dfrac{\\tan^2 x}{2}+C", "tan^2(x)/2+C", "u=\\tan x","du=\\sec^2 x\\,dx"),
    ]
    prob, ans, norm, u_sub, du = pick(cases)
    return {
        "problemTex": f"\\displaystyle\\int {prob}\\,dx",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "u-substitution", "math": u_sub, "note": ""},
            {"label": "du", "math": du, "note": ""},
            {"label": "Result", "math": ans, "note": ""},
        ],
    }


def _rewrite_then_integrate():
    cases = [
        ("\\sqrt{x}", "\\dfrac{2}{3}x^{3/2}+C", "2*x^(3/2)/3+C",
         "\\sqrt{x} = x^{1/2}", "\\int x^{1/2}\\,dx = \\dfrac{x^{3/2}}{3/2}=\\dfrac{2}{3}x^{3/2}"),
        ("\\dfrac{1}{x^3}", "-\\dfrac{1}{2x^2}+C", "-1/(2*x^2)+C",
         "\\dfrac{1}{x^3}=x^{-3}", "\\int x^{-3}\\,dx = \\dfrac{x^{-2}}{-2}"),
        ("\\dfrac{1}{\\sqrt{x}}", "2\\sqrt{x}+C", "2*sqrt(x)+C",
         "x^{-1/2}", "\\int x^{-1/2}\\,dx = \\dfrac{x^{1/2}}{1/2}=2x^{1/2}"),
    ]
    prob, ans, norm, rewrite, integral = pick(cases)
    return {
        "problemTex": f"\\displaystyle\\int {prob}\\,dx",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Rewrite as power", "math": rewrite, "note": ""},
            {"label": "Apply power rule", "math": integral, "note": ""},
            {"label": "Simplify", "math": ans, "note": ""},
        ],
    }


diff2 = [_usub_linear, _usub_linear, _usub_polynomial, _usub_trig, _rewrite_then_integrate]

# ── diff3 — definite integrals, initial value ─────────────────────────────────

def _definite_integral():
    n = pick([2,3])
    a, b = 0, R(1,3)
    # ∫[0,b] x^n dx = b^(n+1)/(n+1)
    f = Fraction(b**(n+1), n+1)
    ans = str(int(f)) if f.denominator == 1 else f"\\dfrac{{{f.numerator}}}{{{f.denominator}}}"
    return {
        "problemTex": f"\\displaystyle\\int_0^{b} x^{n}\\,dx",
        "answerTex": ans,
        "answerNorm": f"{f.numerator}/{f.denominator}",
        "steps": [
            {"label": "Antiderivative", "math": f"\\left[\\dfrac{{x^{{{n+1}}}}}{{{n+1}}}\\right]_0^{b}", "note": ""},
            {"label": "Evaluate", "math": f"\\dfrac{{{b}^{{{n+1}}}}}{{{n+1}}} - 0 = {ans}", "note": ""},
        ],
    }


def _initial_value_problem():
    n = pick([2,3])
    a_val = R(0,3)   # f(a_val) = k
    k = R(1, 10)
    # f'(x) = x^n; F(x) = x^(n+1)/(n+1) + C
    denom = n + 1
    # F(a_val) = a_val^(n+1)/(n+1) + C = k → C = k - a_val^(n+1)/(n+1)
    f_a = Fraction(a_val**(n+1), denom)
    C = Fraction(k) - f_a
    C_tex = str(int(C)) if C.denominator == 1 else f"\\dfrac{{{C.numerator}}}{{{C.denominator}}}"
    C_sign = sign_str(int(C) if C.denominator == 1 else C.numerator / C.denominator)
    return {
        "problemTex": f"f'(x)=x^{{{n}}},\\; f({a_val})={k}.\\quad \\text{{Find }}f(x).",
        "answerTex": f"\\dfrac{{x^{{{n+1}}}}}{{{denom}}}{C_sign if C != 0 else ''}",
        "answerNorm": f"x^({n+1})/{denom}+{float(C):.4f}",
        "steps": [
            {"label": "Antiderivative", "math": f"f(x)=\\dfrac{{x^{{{n+1}}}}}{{{denom}}}+C", "note": ""},
            {"label": "Apply initial condition", "math": f"f({a_val})=\\dfrac{{{a_val}^{{{n+1}}}}}{{{denom}}}+C={k}", "note": ""},
            {"label": "Solve for C", "math": f"C={C_tex}", "note": ""},
            {"label": "Final answer", "math": f"f(x)=\\dfrac{{x^{{{n+1}}}}}{{{denom}}}+{C_tex}", "note": ""},
        ],
    }


diff3 = [_definite_integral, _definite_integral, _initial_value_problem]

# ── diff4 — definite u-sub, split intervals ───────────────────────────────────

def _definite_usub():
    cases = [
        (
            "\\int_0^1 x e^{x^2}\\,dx",
            "\\dfrac{e-1}{2}",
            "(e-1)/2",
            [
                {"label": "u = x², du = 2x dx", "math": "\\dfrac{1}{2}\\int_0^1 e^u\\,du", "note": "bounds: u(0)=0, u(1)=1"},
                {"label": "Evaluate", "math": "\\dfrac{1}{2}[e^u]_0^1=\\dfrac{e-1}{2}", "note": ""},
            ],
        ),
        (
            "\\int_0^{\\pi/2} \\sin x\\cos x\\,dx",
            "\\dfrac{1}{2}",
            "1/2",
            [
                {"label": "u = sin x, du = cos x dx", "math": "\\int_0^1 u\\,du", "note": "bounds: u(0)=0, u(π/2)=1"},
                {"label": "Evaluate", "math": "\\left[\\dfrac{u^2}{2}\\right]_0^1 = \\dfrac{1}{2}", "note": ""},
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


def _usub_algebra():
    # ∫ x/sqrt(x+1) dx — complete algebra to isolate du
    return {
        "problemTex": "\\displaystyle\\int \\dfrac{x}{\\sqrt{x+1}}\\,dx",
        "answerTex": "\\dfrac{2}{3}(x+1)^{3/2} - 2\\sqrt{x+1} + C",
        "answerNorm": "2*(x+1)^(3/2)/3-2*sqrt(x+1)+C",
        "steps": [
            {"label": "u = x+1, x = u−1, du = dx", "math": "\\int\\dfrac{u-1}{\\sqrt{u}}\\,du = \\int(u^{1/2}-u^{-1/2})\\,du", "note": ""},
            {"label": "Integrate", "math": "\\dfrac{2}{3}u^{3/2} - 2u^{1/2}+C", "note": ""},
            {"label": "Back-substitute", "math": "\\dfrac{2}{3}(x+1)^{3/2}-2\\sqrt{x+1}+C", "note": ""},
        ],
    }


def _split_interval():
    return {
        "problemTex": "\\displaystyle\\int_{-2}^{3} |x|\\,dx",
        "answerTex": "\\dfrac{4}{2}+\\dfrac{9}{2} = \\dfrac{13}{2}",
        "answerNorm": "13/2",
        "steps": [
            {"label": "Split at x=0 (where |x| changes)", "math": "\\int_{-2}^0(-x)\\,dx + \\int_0^3 x\\,dx", "note": ""},
            {"label": "Evaluate first", "math": "\\left[-\\dfrac{x^2}{2}\\right]_{-2}^0 = 0-(-2)=2", "note": ""},
            {"label": "Evaluate second", "math": "\\left[\\dfrac{x^2}{2}\\right]_0^3 = \\dfrac{9}{2}", "note": ""},
            {"label": "Sum", "math": "2+\\dfrac{9}{2}=\\dfrac{13}{2}", "note": ""},
        ],
    }


diff4 = [_definite_usub, _definite_usub, _usub_algebra, _split_interval]

# ── diff5 — second antiderivative, disguised u-sub ───────────────────────────

def _second_antiderivative():
    return {
        "problemTex": "f''(x)=6x,\\; f'(0)=1,\\; f(0)=2.\\quad \\text{Find }f(x).",
        "answerTex": "x^3+x+2",
        "answerNorm": "x^3+x+2",
        "steps": [
            {"label": "Integrate f'' to get f'", "math": "f'(x)=3x^2+C_1", "note": ""},
            {"label": "Apply f'(0)=1", "math": "3(0)^2+C_1=1 \\Rightarrow C_1=1,\\; f'(x)=3x^2+1", "note": ""},
            {"label": "Integrate f' to get f", "math": "f(x)=x^3+x+C_2", "note": ""},
            {"label": "Apply f(0)=2", "math": "C_2=2,\\; f(x)=x^3+x+2", "note": ""},
        ],
    }


def _disguised_usub():
    cases = [
        ("\\tan x", "-\\ln|\\cos x|+C", "-ln|cos(x)|+C",
         "\\tan x = \\sin x/\\cos x", "u=\\cos x,\\; du=-\\sin x\\,dx",
         "-\\int\\dfrac{1}{u}\\,du = -\\ln|u|+C"),
        ("\\cot x", "\\ln|\\sin x|+C", "ln|sin(x)|+C",
         "\\cot x = \\cos x/\\sin x", "u=\\sin x,\\; du=\\cos x\\,dx",
         "\\int\\dfrac{1}{u}\\,du = \\ln|u|+C"),
    ]
    prob, ans, norm, rewrite, u_sub, integral = pick(cases)
    return {
        "problemTex": f"\\displaystyle\\int {prob}\\,dx",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Rewrite", "math": rewrite, "note": "not obvious — write as fraction"},
            {"label": "u-substitution", "math": u_sub, "note": ""},
            {"label": "Integrate", "math": integral, "note": ""},
            {"label": "Back-substitute", "math": ans, "note": ""},
        ],
    }


def _definite_usub_trig():
    return {
        "problemTex": "\\displaystyle\\int_0^{\\pi/2} \\sin x \\cos^2 x\\,dx",
        "answerTex": "\\dfrac{1}{3}",
        "answerNorm": "1/3",
        "steps": [
            {"label": "u = cos x, du = −sin x dx", "math": "-\\int_1^0 u^2\\,du = \\int_0^1 u^2\\,du", "note": "bounds flip"},
            {"label": "Evaluate", "math": "\\left[\\dfrac{u^3}{3}\\right]_0^1 = \\dfrac{1}{3}", "note": ""},
        ],
    }


diff5 = [_second_antiderivative, _disguised_usub, _disguised_usub, _definite_usub_trig]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
