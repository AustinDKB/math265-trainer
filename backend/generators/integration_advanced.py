"""
Trainer 10: Advanced Integration
Techniques: by-parts, trig identities, partial fractions, trig substitution, improper integrals.
"""
import random
import math
from fractions import Fraction
from math_utils import R, pick

def _plus_C(tex):
    return tex + " + C"

# ── diff 1: Integration by parts basics, half-angle identities ────────────────

def _byparts_x_exp():
    a = pick([1, 2, 3])
    # ∫ x·e^(ax) dx = e^(ax)(x/a - 1/a²)
    if a == 1:
        prob = r"\int x e^x \, dx"
        ans = r"e^x(x - 1)"
        ans_norm = "e^x*(x-1)"
    else:
        prob = rf"\int x e^{{{a}x}} \, dx"
        ans = rf"e^{{{a}x}}\!\left(\dfrac{{x}}{{{a}}} - \dfrac{{1}}{{{a**2}}}\right)"
        ans_norm = f"e^({a}x)*(x/{a}-1/{a**2})"
    steps = [
        {"label": "Choose u and dv", "math": r"u = x,\quad dv = e^{" + (str(a) if a>1 else "") + r"x}\,dx"},
        {"label": "Compute du and v", "math": r"du = dx,\quad v = \dfrac{e^{" + (str(a) if a>1 else "") + r"x}}{" + str(a) + r"}"},
        {"label": "Apply formula ∫u dv = uv − ∫v du", "math": rf"= \dfrac{{xe^{{{a}x}}}}{{{a}}} - \dfrac{{1}}{{{a}}}\int e^{{{a}x}}\,dx"},
        {"label": "Integrate remaining", "math": rf"= \dfrac{{xe^{{{a}x}}}}{{{a}}} - \dfrac{{e^{{{a}x}}}}{{{a**2}}} + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _byparts_x_sin():
    a = pick([1, 2, 3])
    # ∫ x·sin(ax) dx = -x·cos(ax)/a + sin(ax)/a²
    if a == 1:
        prob = r"\int x \sin(x) \, dx"
        ans = r"-x\cos(x) + \sin(x)"
        ans_norm = "-x*cos(x)+sin(x)"
    else:
        prob = rf"\int x \sin({a}x) \, dx"
        ans = rf"-\dfrac{{x\cos({a}x)}}{{{a}}} + \dfrac{{\sin({a}x)}}{{{a**2}}}"
        ans_norm = f"-x*cos({a}x)/{a}+sin({a}x)/{a**2}"
    steps = [
        {"label": "Integration by parts: u=x, dv=sin(ax)dx", "math": r"u=x,\;dv=\sin(" + str(a) + r"x)\,dx"},
        {"label": "du=dx, v=−cos(ax)/a", "math": rf"du=dx,\;v=-\dfrac{{\cos({a}x)}}{{{a}}}"},
        {"label": "Apply formula: uv minus integral of v du", "math": rf"-\dfrac{{x\cos({a}x)}}{{{a}}} + \dfrac{{1}}{{{a}}}\int\cos({a}x)\,dx"},
        {"label": "Final", "math": rf"-\dfrac{{x\cos({a}x)}}{{{a}}} + \dfrac{{\sin({a}x)}}{{{a**2}}} + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _half_angle_sin2():
    # ∫ sin²(x) dx = x/2 - sin(2x)/4
    a = pick([1, 2])
    if a == 1:
        prob = r"\int \sin^2(x)\,dx"
        ans = r"\dfrac{x}{2} - \dfrac{\sin(2x)}{4}"
        ans_norm = "x/2-sin(2x)/4"
    else:
        prob = rf"\int \sin^2({a}x)\,dx"
        ans = rf"\dfrac{{x}}{{2}} - \dfrac{{\sin({2*a}x)}}{{{4*a}}}"
        ans_norm = f"x/2-sin({2*a}x)/{4*a}"
    steps = [
        {"label": "Half-angle identity", "math": r"\sin^2(u) = \dfrac{1-\cos(2u)}{2}"},
        {"label": "Rewrite integrand", "math": rf"\dfrac{{1-\cos({2*a}x)}}{{2}}"},
        {"label": "Integrate term by term", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _half_angle_cos2():
    # ∫ cos²(x) dx = x/2 + sin(2x)/4
    prob = r"\int \cos^2(x)\,dx"
    ans = r"\dfrac{x}{2} + \dfrac{\sin(2x)}{4}"
    ans_norm = "x/2+sin(2x)/4"
    steps = [
        {"label": "Half-angle identity", "math": r"\cos^2(x) = \dfrac{1+\cos(2x)}{2}"},
        {"label": "Integrate", "math": r"\dfrac{x}{2} + \dfrac{\sin(2x)}{4} + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


diff1 = [_byparts_x_exp, _byparts_x_sin, _half_angle_sin2, _half_angle_cos2]


# ── diff 2: IBP repeated, trig powers, partial fractions (distinct) ───────────

def _byparts_x2_exp():
    # ∫ x²·e^x dx = e^x(x²-2x+2)
    prob = r"\int x^2 e^x \, dx"
    ans = r"e^x(x^2 - 2x + 2)"
    ans_norm = "e^x*(x^2-2x+2)"
    steps = [
        {"label": "Integration by parts twice", "math": r"u=x^2,\;dv=e^x\,dx \Rightarrow \text{apply twice}"},
        {"label": "First application", "math": r"x^2 e^x - 2\int xe^x\,dx"},
        {"label": "Second application", "math": r"x^2 e^x - 2(xe^x - e^x)"},
        {"label": "Simplify", "math": r"e^x(x^2-2x+2)+C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _byparts_x_cos():
    # ∫ x·cos(x) dx = x·sin(x) + cos(x)
    prob = r"\int x \cos(x) \, dx"
    ans = r"x\sin(x) + \cos(x)"
    ans_norm = "x*sin(x)+cos(x)"
    steps = [
        {"label": "Integration by parts: u=x, dv=cos(x)dx", "math": r"u=x,\;dv=\cos(x)\,dx"},
        {"label": "du=dx, v=sin(x)", "math": r"du=dx,\;v=\sin(x)"},
        {"label": "Apply formula", "math": r"x\sin(x) - \int\sin(x)\,dx"},
        {"label": "Final", "math": r"x\sin(x) + \cos(x) + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _trig_power_sin3():
    # ∫ sin³(x) dx = -cos(x) + cos³(x)/3
    prob = r"\int \sin^3(x)\,dx"
    ans = r"-\cos(x) + \dfrac{\cos^3(x)}{3}"
    ans_norm = "-cos(x)+cos^3(x)/3"
    steps = [
        {"label": "Split off one factor", "math": r"\sin^2(x)\cdot\sin(x) = (1-\cos^2 x)\sin(x)"},
        {"label": "u-substitution: u=cos(x), du=-sin(x)dx", "math": r"-\int(1-u^2)\,du"},
        {"label": "Integrate", "math": r"-(u - \tfrac{u^3}{3}) = -\cos(x)+\tfrac{\cos^3(x)}{3}+C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _partial_fractions_distinct():
    # ∫ 1/((x+a)(x+b)) dx — distinct linear factors
    pairs = [(0, 2), (1, 3), (0, 3)]
    a, b = pick(pairs)
    # PF: 1/((x+a)(x+b)) = A/(x+a) + B/(x+b), A=1/(a-b), B=1/(b-a)
    denom = (a - b)
    # A = 1/(a-b), B = -1/(a-b)
    # Simplified: use concrete example for clarity
    if a == 0 and b == 2:
        prob = r"\int \dfrac{1}{x(x+2)}\,dx"
        ans = r"\dfrac{1}{2}\ln|x| - \dfrac{1}{2}\ln|x+2|"
        ans_norm = "(1/2)*ln|x|-(1/2)*ln|x+2|"
        pf_step = r"\dfrac{1}{x(x+2)} = \dfrac{1/2}{x} - \dfrac{1/2}{x+2}"
    elif a == 1 and b == 3:
        prob = r"\int \dfrac{1}{(x-1)(x-3)}\,dx"
        ans = r"\dfrac{1}{2}\ln|x-1| - \dfrac{1}{2}\ln|x-3|"
        ans_norm = "(1/2)*ln|x-1|-(1/2)*ln|x-3|"
        pf_step = r"\dfrac{1}{(x-1)(x-3)} = \dfrac{-1/2}{x-1} + \dfrac{1/2}{x-3}"
        ans = r"-\dfrac{1}{2}\ln|x-1| + \dfrac{1}{2}\ln|x-3|"
        ans_norm = "-(1/2)*ln|x-1|+(1/2)*ln|x-3|"
    else:
        prob = r"\int \dfrac{1}{x(x+3)}\,dx"
        ans = r"\dfrac{1}{3}\ln|x| - \dfrac{1}{3}\ln|x+3|"
        ans_norm = "(1/3)*ln|x|-(1/3)*ln|x+3|"
        pf_step = r"\dfrac{1}{x(x+3)} = \dfrac{1/3}{x} - \dfrac{1/3}{x+3}"
    steps = [
        {"label": "Partial fraction decomposition", "math": pf_step},
        {"label": "Integrate each term", "math": r"\int \dfrac{A}{x+a}\,dx = A\ln|x+a|"},
        {"label": "Final answer", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


diff2 = [_byparts_x2_exp, _byparts_x_cos, _trig_power_sin3, _partial_fractions_distinct]


# ── diff 3: IBP circular, PF quadratic (arctan), trig substitution ────────────

def _byparts_circular():
    # ∫ e^x·cos(x) dx — circular IBP, solve for I
    which = random.random() < 0.5
    if which:
        prob = r"\int e^x \cos(x)\,dx"
        ans = r"\dfrac{e^x(\cos(x)+\sin(x))}{2}"
        ans_norm = "e^x*(cos(x)+sin(x))/2"
        steps = [
            {"label": "Integration by parts: u=e^x, dv=cos(x)dx", "math": r"I = e^x\sin(x) - \int e^x\sin(x)\,dx"},
            {"label": "Integration by parts again on remainder", "math": r"I = e^x\sin(x) + e^x\cos(x) - I"},
            {"label": "Solve for I", "math": r"2I = e^x(\sin(x)+\cos(x))"},
            {"label": "Final", "math": ans + " + C"},
        ]
    else:
        prob = r"\int e^x \sin(x)\,dx"
        ans = r"\dfrac{e^x(\sin(x)-\cos(x))}{2}"
        ans_norm = "e^x*(sin(x)-cos(x))/2"
        steps = [
            {"label": "Integration by parts: u=e^x, dv=sin(x)dx", "math": r"I = -e^x\cos(x) + \int e^x\cos(x)\,dx"},
            {"label": "Integration by parts again on remainder", "math": r"I = -e^x\cos(x) + e^x\sin(x) - I"},
            {"label": "Solve for I", "math": r"2I = e^x(\sin(x)-\cos(x))"},
            {"label": "Final", "math": ans + " + C"},
        ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _partial_fractions_arctan():
    # ∫ 1/(x²+a²) dx = (1/a)arctan(x/a)
    a = pick([1, 2, 3])
    if a == 1:
        prob = r"\int \dfrac{1}{x^2+1}\,dx"
        ans = r"\arctan(x)"
        ans_norm = "arctan(x)"
    else:
        prob = rf"\int \dfrac{{1}}{{x^2+{a**2}}}\,dx"
        ans = rf"\dfrac{{1}}{{{a}}}\arctan\!\left(\dfrac{{x}}{{{a}}}\right)"
        ans_norm = f"(1/{a})*arctan(x/{a})"
    steps = [
        {"label": "Standard form", "math": rf"\int\dfrac{{1}}{{x^2+a^2}}\,dx = \dfrac{{1}}{{a}}\arctan\!\left(\dfrac{{x}}{{a}}\right)"},
        {"label": f"Here a={a}", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _trig_sub_sqrt():
    # ∫ sqrt(1-x²) dx = (x/2)sqrt(1-x²) + (1/2)arcsin(x)
    which = random.randint(0, 1)
    if which == 0:
        prob = r"\int \sqrt{1-x^2}\,dx"
        ans = r"\dfrac{x}{2}\sqrt{1-x^2} + \dfrac{1}{2}\arcsin(x)"
        ans_norm = "(x/2)*sqrt(1-x^2)+(1/2)*arcsin(x)"
        steps = [
            {"label": "Trig sub: x=sin(θ)", "math": r"dx=\cos\theta\,d\theta,\;\sqrt{1-x^2}=\cos\theta"},
            {"label": "Integral becomes", "math": r"\int\cos^2\theta\,d\theta = \dfrac{\theta}{2}+\dfrac{\sin(2\theta)}{4}"},
            {"label": "Back-substitute", "math": ans + " + C"},
        ]
    else:
        # ∫ 1/sqrt(1-x²) dx = arcsin(x)
        prob = r"\int \dfrac{1}{\sqrt{1-x^2}}\,dx"
        ans = r"\arcsin(x)"
        ans_norm = "arcsin(x)"
        steps = [
            {"label": "Standard form", "math": r"\int\dfrac{dx}{\sqrt{1-x^2}} = \arcsin(x)+C"},
        ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _combo_usub_byparts():
    # ∫ x·e^(x²) dx — u-sub first, then done
    prob = r"\int x e^{x^2}\,dx"
    ans = r"\dfrac{1}{2}e^{x^2}"
    ans_norm = "(1/2)*e^(x^2)"
    steps = [
        {"label": "u-substitution: u=x², du=2x dx", "math": r"\dfrac{1}{2}\int e^u\,du"},
        {"label": "Integrate", "math": r"\dfrac{1}{2}e^u = \dfrac{1}{2}e^{x^2} + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


diff3 = [_byparts_circular, _partial_fractions_arctan, _trig_sub_sqrt, _combo_usub_byparts]


# ── diff 4: Long division + PF, trig sub with complete the square, IBP+u-sub ──

def _long_div_then_pf():
    # ∫ (x²+1)/(x²-1) dx = x + ln|(x-1)/(x+1)| * (1/2) + C...
    # Use simpler: ∫ x²/(x²-1) dx = x + (1/2)ln|(x-1)/(x+1)|
    prob = r"\int \dfrac{x^2}{x^2-1}\,dx"
    ans = r"x + \dfrac{1}{2}\ln\!\left|\dfrac{x-1}{x+1}\right|"
    ans_norm = "x+(1/2)*ln|(x-1)/(x+1)|"
    steps = [
        {"label": "Long division: x²/(x²-1) = 1 + 1/(x²-1)", "math": r"= 1 + \dfrac{1}{(x-1)(x+1)}"},
        {"label": "Partial fractions: 1/((x-1)(x+1)) = (1/2)·[1/(x-1) − 1/(x+1)]", "math": r"\dfrac{1}{2}\cdot\dfrac{1}{x-1} - \dfrac{1}{2}\cdot\dfrac{1}{x+1}"},
        {"label": "Integrate", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _complete_square_trig_sub():
    # ∫ 1/(x²+2x+5) dx = complete square → ∫ 1/((x+1)²+4) dx = (1/2)arctan((x+1)/2)
    prob = r"\int \dfrac{1}{x^2+2x+5}\,dx"
    ans = r"\dfrac{1}{2}\arctan\!\left(\dfrac{x+1}{2}\right)"
    ans_norm = "(1/2)*arctan((x+1)/2)"
    steps = [
        {"label": "Complete the square", "math": r"x^2+2x+5 = (x+1)^2+4"},
        {"label": "Standard arctan form with a=2", "math": r"\int\dfrac{du}{u^2+4} = \dfrac{1}{2}\arctan\!\left(\dfrac{u}{2}\right)"},
        {"label": "Substitute back u=x+1", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _byparts_ln():
    # ∫ ln(x) dx = x·ln(x) - x
    prob = r"\int \ln(x)\,dx"
    ans = r"x\ln(x) - x"
    ans_norm = "x*ln(x)-x"
    steps = [
        {"label": "Integration by parts: u=ln(x), dv=dx", "math": r"du=\dfrac{1}{x}dx,\;v=x"},
        {"label": "Apply formula", "math": r"x\ln(x) - \int x\cdot\dfrac{1}{x}\,dx"},
        {"label": "Simplify", "math": r"x\ln(x) - x + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _trig_power_reduction():
    # ∫ cos⁴(x) dx = 3x/8 + sin(2x)/4 + sin(4x)/32
    prob = r"\int \cos^4(x)\,dx"
    ans = r"\dfrac{3x}{8} + \dfrac{\sin(2x)}{4} + \dfrac{\sin(4x)}{32}"
    ans_norm = "3x/8+sin(2x)/4+sin(4x)/32"
    steps = [
        {"label": "Apply cos²=½(1+cos2x) twice", "math": r"\cos^4(x) = \left(\dfrac{1+\cos(2x)}{2}\right)^2"},
        {"label": "Expand", "math": r"\dfrac{1}{4}(1 + 2\cos(2x) + \cos^2(2x))"},
        {"label": "Apply half-angle to cos²(2x)", "math": r"\dfrac{1}{4}\left(\dfrac{3}{2} + 2\cos(2x) + \dfrac{\cos(4x)}{2}\right)"},
        {"label": "Integrate", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


diff4 = [_long_div_then_pf, _complete_square_trig_sub, _byparts_ln, _trig_power_reduction]


# ── diff 5: Improper integrals, three-technique combos ────────────────────────

def _improper_convergent():
    cases = [
        {
            "prob": r"\int_1^{\infty} \dfrac{1}{x^2}\,dx",
            "ans": "1",
            "ans_norm": "1",
            "steps": [
                {"label": "Limit form", "math": r"\lim_{b\to\infty}\int_1^b x^{-2}\,dx"},
                {"label": "Antiderivative", "math": r"\lim_{b\to\infty}\left[-\dfrac{1}{x}\right]_1^b"},
                {"label": "Evaluate", "math": r"\lim_{b\to\infty}\left(-\dfrac{1}{b}+1\right) = 1"},
            ]
        },
        {
            "prob": r"\int_0^{\infty} e^{-x}\,dx",
            "ans": "1",
            "ans_norm": "1",
            "steps": [
                {"label": "Limit form", "math": r"\lim_{b\to\infty}\int_0^b e^{-x}\,dx"},
                {"label": "Antiderivative", "math": r"\lim_{b\to\infty}\left[-e^{-x}\right]_0^b"},
                {"label": "Evaluate", "math": r"\lim_{b\to\infty}(-e^{-b}+1) = 1"},
            ]
        },
        {
            "prob": r"\int_1^{\infty} \dfrac{1}{x^3}\,dx",
            "ans": r"\dfrac{1}{2}",
            "ans_norm": "1/2",
            "steps": [
                {"label": "Limit form", "math": r"\lim_{b\to\infty}\left[-\dfrac{1}{2x^2}\right]_1^b"},
                {"label": "Evaluate", "math": r"\lim_{b\to\infty}\left(-\dfrac{1}{2b^2}+\dfrac{1}{2}\right) = \dfrac{1}{2}"},
            ]
        },
    ]
    case = pick(cases)
    return {"problemTex": case["prob"], "answerTex": case["ans"], "answerNorm": case["ans_norm"], "steps": case["steps"]}


def _improper_divergent():
    cases = [
        {
            "prob": r"\int_1^{\infty} \dfrac{1}{x}\,dx",
            "ans": "diverges",
            "ans_norm": "diverges",
            "steps": [
                {"label": "Limit form", "math": r"\lim_{b\to\infty}[\ln x]_1^b = \lim_{b\to\infty}\ln b"},
                {"label": "Conclusion", "math": r"\ln b \to \infty \Rightarrow \text{diverges}"},
            ]
        },
        {
            "prob": r"\int_0^1 \dfrac{1}{\sqrt{x}}\,dx",
            "ans": "2",
            "ans_norm": "2",
            "steps": [
                {"label": "Improper at x=0", "math": r"\lim_{a\to 0^+}\int_a^1 x^{-1/2}\,dx"},
                {"label": "Antiderivative", "math": r"\lim_{a\to 0^+}\left[2\sqrt{x}\right]_a^1"},
                {"label": "Evaluate", "math": r"2 - 2\sqrt{a}\to 2"},
            ]
        },
    ]
    case = pick(cases)
    return {"problemTex": case["prob"], "answerTex": case["ans"], "answerNorm": case["ans_norm"], "steps": case["steps"]}


def _three_technique_combo():
    # ∫ x·ln(x) dx — IBP with u=ln(x)
    prob = r"\int x\ln(x)\,dx"
    ans = r"\dfrac{x^2}{2}\ln(x) - \dfrac{x^2}{4}"
    ans_norm = "(x^2/2)*ln(x)-x^2/4"
    steps = [
        {"label": "Integration by parts: u=ln(x), dv=x dx", "math": r"du=\dfrac{dx}{x},\;v=\dfrac{x^2}{2}"},
        {"label": "Apply formula: uv minus integral of v du", "math": r"\dfrac{x^2\ln(x)}{2} - \int\dfrac{x}{2}\,dx"},
        {"label": "Final", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


def _trig_sub_sqrt_x2_plus():
    # ∫ 1/sqrt(x²+1) dx = ln|x+sqrt(x²+1)|
    prob = r"\int \dfrac{1}{\sqrt{x^2+1}}\,dx"
    ans = r"\ln\!\left|x + \sqrt{x^2+1}\right|"
    ans_norm = "ln|x+sqrt(x^2+1)|"
    steps = [
        {"label": "Trig sub: x=tan(θ)", "math": r"dx=\sec^2\theta\,d\theta,\;\sqrt{x^2+1}=\sec\theta"},
        {"label": "Integral becomes", "math": r"\int\sec\theta\,d\theta = \ln|\sec\theta+\tan\theta|"},
        {"label": "Back-substitute", "math": ans + " + C"},
    ]
    return {"problemTex": prob, "answerTex": _plus_C(ans), "answerNorm": ans_norm + "+C", "steps": steps}


diff5 = [_improper_convergent, _improper_divergent, _three_technique_combo, _trig_sub_sqrt_x2_plus]


POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
