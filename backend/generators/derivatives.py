import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from symbolic import (X, Const, Mul, Pow, Sin, Cos, Tan, Exp, Ln, Var, Add, Neg, Div,
                      add, mul, neg, pow_expr, diff_and_simplify, numeric_equal)
from math_utils import R, pick, sign_str

def _d_tex(expr_tex): return f"\\dfrac{{d}}{{dx}}\\!\\left[{expr_tex}\\right]"


# ── diff1 — basic rules ────────────────────────────────────────────────────────

def _power_rule():
    n = pick([-3,-2,-1,1,2,3,4,5,6,7,8])
    a = R(1, 8)
    an = a * n
    n_minus = n - 1
    if n == 0:
        return _power_rule()
    expr_tex = f"{a}x^{{{n}}}" if n not in [1,-1] else (f"{a}x" if n==1 else f"\\dfrac{{{a}}}{{x}}")
    if n - 1 == 0:
        ans_tex = str(an)
        ans_norm = str(an)
    elif n - 1 == 1:
        ans_tex = f"{an}x"
        ans_norm = f"{an}*x"
    else:
        ans_tex = f"{an}x^{{{n_minus}}}"
        ans_norm = f"{an}*x^({n_minus})"
    return {
        "problemTex": _d_tex(expr_tex),
        "answerTex": ans_tex,
        "answerNorm": ans_norm,
        "steps": [
            {"label": "Power rule: d/dx[ax^n] = an·x^(n-1)", "math": f"\\text{{multiply exponent by coefficient: }} {a} \\cdot {n} = {an}", "note": f"bring the {n} down, reduce exponent by 1"},
            {"label": "Reduce exponent by 1", "math": f"n-1 = {n}-1 = {n_minus}", "note": ""},
            {"label": "Result", "math": ans_tex, "note": ""},
        ],
    }


def _trig_basic():
    cases = [
        ("\\sin x",    "\\cos x",           "cos(x)",        "sine becomes cosine"),
        ("\\cos x",    "-\\sin x",          "-sin(x)",       "cosine becomes negative sine"),
        ("\\tan x",    "\\sec^2 x",         "sec^2(x)",      "tangent becomes secant squared"),
        ("\\cot x",    "-\\csc^2 x",        "-csc^2(x)",     "cotangent becomes negative cosecant squared"),
        ("\\sec x",    "\\sec x\\tan x",    "sec(x)*tan(x)", "secant becomes secant times tangent"),
        ("\\csc x",    "-\\csc x\\cot x",   "-csc(x)*cot(x)","cosecant becomes negative cosecant times cotangent"),
    ]
    f_tex, d_tex, d_norm, reason = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [
            {"label": "Recall standard trig derivative", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": reason},
        ],
    }


def _exponential_rule():
    cases = [
        ("e^x",   "e^x",          "e^x",          "e^x is its own derivative"),
        ("e^x",   "e^x",          "e^x",          "e^x is its own derivative"),
        ("2^x",   "2^x \\ln 2",   "2^x*ln(2)",    "for a^x: multiply by ln(a)"),
        ("3^x",   "3^x \\ln 3",   "3^x*ln(3)",    "for a^x: multiply by ln(a)"),
        ("10^x",  "10^x \\ln 10", "10^x*ln(10)",  "for a^x: multiply by ln(a)"),
    ]
    f_tex, d_tex, d_norm, reason = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [
            {"label": "Exponential derivative rule", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": reason},
        ],
    }


def _log_rule():
    cases = [
        ("\\ln x",       "\\dfrac{1}{x}",          "1/x",           "d/dx[ln x] = 1/x"),
        ("\\log_2 x",    "\\dfrac{1}{x \\ln 2}",   "1/(x*ln(2))",   "d/dx[log_a x] = 1/(x·ln a)"),
        ("\\log_{10} x", "\\dfrac{1}{x \\ln 10}",  "1/(x*ln(10))",  "d/dx[log_a x] = 1/(x·ln a)"),
    ]
    f_tex, d_tex, d_norm, reason = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [
            {"label": "Logarithm derivative rule", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": reason},
        ],
    }


def _sum_difference():
    m, n = pick([2,3,4,5]), pick([0,1,2,3])
    while m == n: n = pick([0,1,2,3])
    a, b = R(1,6), R(1,6)
    pm = a * m; pn = b * n
    def term_tex(coeff, exp):
        if exp == 0: return str(coeff)
        if exp == 1: return f"{coeff}x"
        return f"{coeff}x^{{{exp}}}"
    def dterm_tex(coeff, exp):
        if exp == 0: return "0"
        if exp - 1 == 0: return str(coeff)
        if exp - 1 == 1: return f"{coeff}x"
        return f"{coeff}x^{{{exp-1}}}"
    sign = pick(["+", "-"])
    prob = f"{term_tex(a,m)}{'+' if sign=='+' else '-'}{term_tex(b,n)}"
    dm = pm; dn = pn
    ans_dm = dterm_tex(dm, m)
    ans_dn = dterm_tex(dn, n)
    if dn == "0":
        ans_tex = ans_dm
        ans_norm = ans_dm.replace("{","").replace("}","")
    elif sign == "+":
        ans_tex = f"{ans_dm}+{ans_dn}"
        ans_norm = f"{ans_dm}+{ans_dn}".replace("{","").replace("}","")
    else:
        ans_tex = f"{ans_dm}-{ans_dn}"
        ans_norm = f"{ans_dm}-{ans_dn}".replace("{","").replace("}","")
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans_tex,
        "answerNorm": ans_norm,
        "steps": [
            {"label": "Sum/difference rule: differentiate each term separately", "math": f"\\dfrac{{d}}{{dx}}[{term_tex(a,m)}] {'+' if sign=='+' else '-'} \\dfrac{{d}}{{dx}}[{term_tex(b,n)}]", "note": ""},
            {"label": f"Apply power rule to each term", "math": f"{ans_dm} {'+' if sign=='+' else '-'} {ans_dn}", "note": f"d/dx[{term_tex(a,m)}]={ans_dm},\\; d/dx[{term_tex(b,n)}]={ans_dn}"},
        ],
    }


diff1 = [_power_rule, _power_rule, _trig_basic, _exponential_rule, _log_rule, _sum_difference]

# ── diff2 — product, quotient, chain ─────────────────────────────────────────

def _product_rule():
    cases = [
        (X,                "x",    Sin(X),             "\\sin x"),
        (X,                "x",    Cos(X),             "\\cos x"),
        (X,                "x",    Exp(X),             "e^x"),
        (pow_expr(X,2),    "x^2",  Sin(X),             "\\sin x"),
        (pow_expr(X,2),    "x^2",  Exp(X),             "e^x"),
        (pow_expr(X,3),    "x^3",  Ln(X),              "\\ln x"),
        (mul(Const(2),X),  "2x",   Cos(X),             "\\cos x"),
    ]
    f_expr, f_tex, g_expr, g_tex = pick(cases)
    product = Mul(f_expr, g_expr)
    deriv = product.diff().simplify()
    deriv_tex = deriv.to_tex()
    f_d_tex = f_expr.diff().simplify().to_tex()
    g_d_tex = g_expr.diff().simplify().to_tex()
    return {
        "problemTex": _d_tex(f"{f_tex} \\cdot {g_tex}"),
        "answerTex": deriv_tex,
        "answerNorm": deriv.to_norm(),
        "steps": [
            {"label": "Identify the two factors", "math": f"f = {f_tex}, \\quad g = {g_tex}", "note": ""},
            {"label": "Differentiate each factor separately", "math": f"f' = {f_d_tex}, \\quad g' = {g_d_tex}", "note": ""},
            {"label": "Product rule: (fg)' = f'g + fg'", "math": f"({f_d_tex})({g_tex}) + ({f_tex})({g_d_tex})", "note": "first · derivative of second + second · derivative of first"},
            {"label": "Simplify", "math": deriv_tex, "note": ""},
        ],
    }


def _quotient_rule():
    cases = [
        (Sin(X),        "\\sin x",  X,              "x"),
        (Exp(X),        "e^x",      pow_expr(X,2),  "x^2"),
        (Ln(X),         "\\ln x",   X,              "x"),
        (pow_expr(X,2), "x^2",      add(X,Const(1)),"x+1"),
        (Sin(X),        "\\sin x",  Cos(X),         "\\cos x"),
    ]
    f_expr, f_tex, g_expr, g_tex = pick(cases)
    quotient = Div(f_expr, g_expr)
    deriv = quotient.diff().simplify()
    deriv_tex = deriv.to_tex()
    f_d_tex = f_expr.diff().simplify().to_tex()
    g_d_tex = g_expr.diff().simplify().to_tex()
    return {
        "problemTex": _d_tex(f"\\dfrac{{{f_tex}}}{{{g_tex}}}"),
        "answerTex": deriv_tex,
        "answerNorm": deriv.to_norm(),
        "steps": [
            {"label": "Identify numerator and denominator", "math": f"f = {f_tex}, \\quad g = {g_tex}", "note": ""},
            {"label": "Differentiate each", "math": f"f' = {f_d_tex}, \\quad g' = {g_d_tex}", "note": ""},
            {"label": "Quotient rule: (f/g)' = (f'g − fg')/g²", "math": f"\\dfrac{{({f_d_tex})({g_tex})-({f_tex})({g_d_tex})}}{{{g_tex}^2}}", "note": "low d-high minus high d-low, over low squared"},
            {"label": "Simplify", "math": deriv_tex, "note": ""},
        ],
    }


def _chain_single():
    cases = [
        ("\\sin(x^2)",  "2x\\cos(x^2)",      "2x*cos(x^2)",
         "x^2",    "\\sin(u)",     "\\cos(x^2)",  "2x",
         "outer = sin(u), inner = x²"),
        ("e^{3x}",      "3e^{3x}",            "3*e^(3x)",
         "3x",     "e^u",          "e^{3x}",      "3",
         "outer = e^u, inner = 3x"),
        ("\\ln(x^2)",   "\\dfrac{2}{x}",      "2/x",
         "x^2",    "\\ln(u)",      "\\dfrac{1}{x^2}", "2x",
         "outer = ln(u), inner = x²"),
        ("\\sin^2 x",   "2\\sin x\\cos x",    "2*sin(x)*cos(x)",
         "\\sin x","u^2",          "2\\sin x",    "\\cos x",
         "outer = u², inner = sin(x)"),
        ("\\sin(x+3)",  "\\cos(x+3)",         "cos(x+3)",
         "x+3",    "\\sin(u)",     "\\cos(x+3)",  "1",
         "outer = sin(u), inner = x+3"),
        ("e^{x^2+x}",  "e^{x^2+x}(2x+1)",   "e^(x^2+x)*(2x+1)",
         "x^2+x",  "e^u",          "e^{x^2+x}",  "2x+1",
         "outer = e^u, inner = x²+x"),
    ]
    func_tex, ans_tex, ans_norm, inner_tex, outer_name, outer_d_tex, inner_d_tex, structure = pick(cases)
    return {
        "problemTex": _d_tex(func_tex),
        "answerTex": ans_tex,
        "answerNorm": ans_norm,
        "steps": [
            {"label": "Identify outer and inner functions", "math": f"\\text{{{structure}}}", "note": "chain rule: differentiate outside first, keep inside intact"},
            {"label": "Differentiate the outer function (leave inner unchanged)", "math": f"\\dfrac{{d}}{{du}}[{outer_name}] \\text{{ evaluated at inner}} = {outer_d_tex}", "note": ""},
            {"label": "Differentiate the inner function", "math": f"\\dfrac{{d}}{{dx}}[{inner_tex}] = {inner_d_tex}", "note": ""},
            {"label": "Multiply: outer derivative × inner derivative", "math": f"{outer_d_tex} \\cdot {inner_d_tex} = {ans_tex}", "note": ""},
        ],
    }


diff2 = [_product_rule, _product_rule, _quotient_rule, _chain_single, _chain_single]

# ── diff3 — advanced combinations ─────────────────────────────────────────────

def _chain_nested():
    cases = [
        {
            "prob": "\\sin(\\cos(x^2))",
            "ans": "\\cos(\\cos(x^2)) \\cdot (-\\sin(x^2)) \\cdot 2x",
            "norm": "cos(cos(x^2))*(-sin(x^2))*2x",
            "steps": [
                {"label": "Three nested layers: sin( cos( x² ) )", "math": "\\text{outermost} \\to \\text{middle} \\to \\text{innermost}", "note": "apply chain rule once per layer, working outside in"},
                {"label": "Layer 1 — outer: d/dx[sin(u)] = cos(u), keep u = cos(x²)", "math": "\\cos(\\cos(x^2))", "note": "differentiate sin, leave everything inside untouched"},
                {"label": "Layer 2 — middle: d/dx[cos(x²)] = −sin(x²), keep x² inside", "math": "\\cdot(-\\sin(x^2))", "note": "differentiate cos, still leave x² alone"},
                {"label": "Layer 3 — inner: d/dx[x²] = 2x", "math": "\\cdot 2x", "note": "differentiate the innermost expression"},
                {"label": "Multiply all three layers together", "math": "\\cos(\\cos(x^2)) \\cdot (-\\sin(x^2)) \\cdot 2x", "note": ""},
            ],
        },
        {
            "prob": "e^{\\sin(x^2)}",
            "ans": "e^{\\sin(x^2)} \\cdot \\cos(x^2) \\cdot 2x",
            "norm": "e^sin(x^2)*cos(x^2)*2x",
            "steps": [
                {"label": "Three nested layers: e^( sin( x² ) )", "math": "\\text{outermost} \\to \\text{middle} \\to \\text{innermost}", "note": "apply chain rule once per layer, outside in"},
                {"label": "Layer 1 — outer: d/dx[e^u] = e^u, keep u = sin(x²)", "math": "e^{\\sin(x^2)}", "note": "e^u derivative is itself — leave the exponent unchanged"},
                {"label": "Layer 2 — middle: d/dx[sin(x²)] = cos(x²), keep x²", "math": "\\cdot \\cos(x^2)", "note": "differentiate sin, leave x² inside"},
                {"label": "Layer 3 — inner: d/dx[x²] = 2x", "math": "\\cdot 2x", "note": ""},
                {"label": "Multiply all three layers together", "math": "e^{\\sin(x^2)} \\cdot \\cos(x^2) \\cdot 2x", "note": ""},
            ],
        },
        {
            "prob": "\\ln(\\sin(x))",
            "ans": "\\dfrac{\\cos x}{\\sin x} = \\cot x",
            "norm": "cos(x)/sin(x)",
            "steps": [
                {"label": "Two layers: ln( sin(x) )", "math": "\\text{outer} = \\ln(u), \\quad \\text{inner} = \\sin(x)", "note": ""},
                {"label": "Layer 1 — outer: d/dx[ln(u)] = 1/u, evaluated at u = sin(x)", "math": "\\dfrac{1}{\\sin(x)}", "note": ""},
                {"label": "Layer 2 — inner: d/dx[sin(x)] = cos(x)", "math": "\\cdot \\cos(x)", "note": ""},
                {"label": "Multiply and simplify", "math": "\\dfrac{\\cos x}{\\sin x} = \\cot x", "note": "cos/sin = cot by definition"},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _product_chain():
    n = pick([2,3]); a = R(2,5)
    cases = [
        {
            "prob": f"x^{n}\\sin({a}x)",
            "ans": f"{n}x^{{{n-1}}}\\sin({a}x) + {a}x^{n}\\cos({a}x)",
            "norm": f"{n}x^{n-1}*sin({a}x)+{a}x^{n}*cos({a}x)",
            "steps": [
                {"label": f"Product rule: f = x^{n}, g = sin({a}x)", "math": f"f = x^{n}, \\quad g = \\sin({a}x)", "note": "identify the two factors before differentiating"},
                {"label": f"Differentiate f using power rule", "math": f"f' = {n}x^{{{n-1}}}", "note": ""},
                {"label": f"Differentiate g using chain rule: outer = sin(u), inner = {a}x", "math": f"g' = \\cos({a}x) \\cdot {a} = {a}\\cos({a}x)", "note": f"d/dx[sin({a}x)] = cos({a}x) · {a}"},
                {"label": "Apply product rule: f'g + fg'", "math": f"{n}x^{{{n-1}}}\\sin({a}x) + x^{n}\\cdot {a}\\cos({a}x)", "note": ""},
            ],
        },
        {
            "prob": f"x^{n}e^{{{a}x}}",
            "ans": f"{n}x^{{{n-1}}}e^{{{a}x}} + {a}x^{n}e^{{{a}x}} = x^{{{n-1}}}e^{{{a}x}}({n}+{a}x)",
            "norm": f"x^{n-1}*e^({a}x)*({n}+{a}x)",
            "steps": [
                {"label": f"Product rule: f = x^{n}, g = e^{{{a}x}}", "math": f"f = x^{n}, \\quad g = e^{{{a}x}}", "note": ""},
                {"label": "Differentiate f using power rule", "math": f"f' = {n}x^{{{n-1}}}", "note": ""},
                {"label": f"Differentiate g using chain rule: outer = e^u, inner = {a}x", "math": f"g' = e^{{{a}x}} \\cdot {a} = {a}e^{{{a}x}}", "note": f"d/dx[e^({a}x)] = e^({a}x) · {a}"},
                {"label": "Apply product rule: f'g + fg'", "math": f"{n}x^{{{n-1}}}e^{{{a}x}} + x^{n} \\cdot {a}e^{{{a}x}}", "note": ""},
                {"label": "Factor out common terms", "math": f"x^{{{n-1}}}e^{{{a}x}}({n}+{a}x)", "note": f"x^{n-1} and e^({a}x) appear in both terms"},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _quotient_chain():
    cases = [
        {
            "prob": "\\dfrac{e^{2x}}{x^2+1}",
            "ans": "\\dfrac{2e^{2x}(x^2+1) - e^{2x}(2x)}{(x^2+1)^2} = \\dfrac{2e^{2x}(x^2-x+1)}{(x^2+1)^2}",
            "norm": "2e^(2x)*(x^2-x+1)/(x^2+1)^2",
            "steps": [
                {"label": "Identify numerator and denominator", "math": "f = e^{2x}, \\quad g = x^2+1", "note": ""},
                {"label": "Differentiate f using chain rule: outer = e^u, inner = 2x", "math": "f' = e^{2x} \\cdot 2 = 2e^{2x}", "note": "multiply e^(2x) by the derivative of the exponent"},
                {"label": "Differentiate g using power rule", "math": "g' = 2x", "note": ""},
                {"label": "Quotient rule: (f'g − fg')/g²", "math": "\\dfrac{2e^{2x}(x^2+1) - e^{2x}(2x)}{(x^2+1)^2}", "note": ""},
                {"label": "Factor e^(2x) from the numerator and simplify", "math": "\\dfrac{2e^{2x}(x^2-x+1)}{(x^2+1)^2}", "note": ""},
            ],
        },
        {
            "prob": "\\dfrac{\\sin(3x)}{x}",
            "ans": "\\dfrac{3x\\cos(3x) - \\sin(3x)}{x^2}",
            "norm": "(3x*cos(3x)-sin(3x))/x^2",
            "steps": [
                {"label": "Identify numerator and denominator", "math": "f = \\sin(3x), \\quad g = x", "note": ""},
                {"label": "Differentiate f using chain rule: outer = sin(u), inner = 3x", "math": "f' = \\cos(3x) \\cdot 3 = 3\\cos(3x)", "note": "derivative of sin is cos, then multiply by derivative of 3x which is 3"},
                {"label": "Differentiate g using power rule", "math": "g' = 1", "note": ""},
                {"label": "Quotient rule: (f'g − fg')/g²", "math": "\\dfrac{3\\cos(3x) \\cdot x - \\sin(3x) \\cdot 1}{x^2}", "note": ""},
                {"label": "Simplify", "math": "\\dfrac{3x\\cos(3x) - \\sin(3x)}{x^2}", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _implicit_differentiation():
    cases = [
        {
            "implicit": "x^2 + y^2 = r^2",
            "ans": "\\dfrac{dy}{dx} = -\\dfrac{x}{y}",
            "norm": "-x/y",
            "steps": [
                {"label": "Differentiate both sides with respect to x", "math": "\\dfrac{d}{dx}[x^2] + \\dfrac{d}{dx}[y^2] = 0", "note": ""},
                {"label": "d/dx[x²] = 2x by power rule", "math": "2x", "note": ""},
                {"label": "d/dx[y²] = 2y·(dy/dx) by chain rule — y is a function of x", "math": "2y \\cdot \\dfrac{dy}{dx}", "note": "treat y like a composite function: d/dx[y²] = 2y · y'"},
                {"label": "Write the full equation", "math": "2x + 2y\\dfrac{dy}{dx} = 0", "note": ""},
                {"label": "Isolate dy/dx", "math": "2y\\dfrac{dy}{dx} = -2x \\implies \\dfrac{dy}{dx} = -\\dfrac{x}{y}", "note": "divide both sides by 2y"},
            ],
        },
        {
            "implicit": "x^2 + xy + y^2 = 7",
            "ans": "\\dfrac{dy}{dx} = -\\dfrac{2x+y}{x+2y}",
            "norm": "-(2x+y)/(x+2y)",
            "steps": [
                {"label": "Differentiate every term with respect to x", "math": "\\dfrac{d}{dx}[x^2] + \\dfrac{d}{dx}[xy] + \\dfrac{d}{dx}[y^2] = 0", "note": ""},
                {"label": "d/dx[x²] = 2x", "math": "2x", "note": "power rule"},
                {"label": "d/dx[xy] = y + x·(dy/dx) by product rule", "math": "y + x\\dfrac{dy}{dx}", "note": "treat x and y as two separate functions multiplied together"},
                {"label": "d/dx[y²] = 2y·(dy/dx) by chain rule", "math": "2y\\dfrac{dy}{dx}", "note": ""},
                {"label": "Full equation after differentiation", "math": "2x + y + x\\dfrac{dy}{dx} + 2y\\dfrac{dy}{dx} = 0", "note": ""},
                {"label": "Collect all dy/dx terms on one side", "math": "(x + 2y)\\dfrac{dy}{dx} = -(2x+y)", "note": ""},
                {"label": "Divide both sides to isolate dy/dx", "math": "\\dfrac{dy}{dx} = -\\dfrac{2x+y}{x+2y}", "note": ""},
            ],
        },
        {
            "implicit": "\\sin(xy) = x",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{1 - y\\cos(xy)}{x\\cos(xy)}",
            "norm": "(1-y*cos(xy))/(x*cos(xy))",
            "steps": [
                {"label": "Differentiate both sides with respect to x", "math": "\\dfrac{d}{dx}[\\sin(xy)] = \\dfrac{d}{dx}[x]", "note": ""},
                {"label": "Left side: chain rule — outer = sin(u), inner = xy", "math": "\\cos(xy) \\cdot \\dfrac{d}{dx}[xy]", "note": "derivative of sin is cos, then multiply by derivative of the inside"},
                {"label": "d/dx[xy] = y + x·(dy/dx) by product rule", "math": "\\cos(xy) \\cdot \\left(y + x\\dfrac{dy}{dx}\\right)", "note": ""},
                {"label": "Right side: d/dx[x] = 1", "math": "= 1", "note": ""},
                {"label": "Expand the left side", "math": "y\\cos(xy) + x\\cos(xy)\\dfrac{dy}{dx} = 1", "note": ""},
                {"label": "Isolate dy/dx", "math": "\\dfrac{dy}{dx} = \\dfrac{1 - y\\cos(xy)}{x\\cos(xy)}", "note": "subtract y·cos(xy), then divide by x·cos(xy)"},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": f"\\text{{Given }} {c['implicit']},\\text{{ find }} \\dfrac{{dy}}{{dx}}.", "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _log_differentiation():
    return {
        "problemTex": "y = x^x,\\quad \\text{find } \\dfrac{dy}{dx}",
        "answerTex": "x^x(\\ln x + 1)",
        "answerNorm": "x^x*(ln(x)+1)",
        "steps": [
            {"label": "Take ln of both sides to bring down the exponent", "math": "\\ln y = \\ln(x^x) = x \\ln x", "note": "log rule: ln(a^b) = b·ln(a)"},
            {"label": "Differentiate both sides with respect to x", "math": "\\dfrac{d}{dx}[\\ln y] = \\dfrac{d}{dx}[x \\ln x]", "note": ""},
            {"label": "Left side: chain rule — d/dx[ln(y)] = (1/y)·(dy/dx)", "math": "\\dfrac{1}{y}\\dfrac{dy}{dx}", "note": "y is a function of x, so use chain rule"},
            {"label": "Right side: product rule on x·ln(x)", "math": "1 \\cdot \\ln x + x \\cdot \\dfrac{1}{x} = \\ln x + 1", "note": "d/dx[x]=1, d/dx[ln x]=1/x"},
            {"label": "Equation so far", "math": "\\dfrac{1}{y}\\dfrac{dy}{dx} = \\ln x + 1", "note": ""},
            {"label": "Multiply both sides by y to isolate dy/dx", "math": "\\dfrac{dy}{dx} = y(\\ln x+1) = x^x(\\ln x+1)", "note": "substitute y = x^x back in"},
        ],
    }


def _higher_order():
    cases = [
        ("\\sin x",  "f'(x) = \\cos x",   "f''(x) = -\\sin x", "-sin(x)"),
        ("\\cos x",  "f'(x) = -\\sin x",  "f''(x) = -\\cos x", "-cos(x)"),
        ("e^x",      "f'(x) = e^x",        "f''(x) = e^x",      "e^x"),
        ("x^4",      "f'(x) = 4x^3",       "f''(x) = 12x^2",    "12*x^2"),
        ("x^5",      "f'(x) = 5x^4",       "f''(x) = 20x^3",    "20*x^3"),
    ]
    f_tex, fp_tex, d2_tex, d2_norm = pick(cases)
    return {
        "problemTex": f"f(x) = {f_tex},\\quad \\text{{find }} f''(x).",
        "answerTex": d2_tex,
        "answerNorm": d2_norm,
        "steps": [
            {"label": "First derivative: differentiate f(x) once", "math": fp_tex, "note": ""},
            {"label": "Second derivative: differentiate f'(x) again", "math": d2_tex, "note": "apply the same derivative rules to f'(x)"},
        ],
    }


def _y_prime_and_double_prime():
    cases = [
        {
            "prob":      "y = (2 + \\sqrt{x})^3, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = \\dfrac{3(2+\\sqrt{x})^2}{2\\sqrt{x}}",
            "ans1_norm": "3*(2+sqrt(x))^2/(2*sqrt(x))",
            "ans2_tex":  "y'' = \\dfrac{3(x-4)}{4x^{3/2}}",
            "ans2_norm": "3*(x-4)/(4*x^(3/2))",
            "steps": [
                {"label": "Identify: outer = u^3, inner = 2 + √x",
                 "math": "y = (2+\\sqrt{x})^3", "note": "chain rule applies"},
                {"label": "y′ via chain rule: 3u²·u′, where u′ = 1/(2√x)",
                 "math": "y' = 3(2+\\sqrt{x})^2 \\cdot \\dfrac{1}{2\\sqrt{x}} = \\dfrac{3(2+\\sqrt{x})^2}{2\\sqrt{x}}", "note": ""},
                {"label": "y″: differentiate y′ with quotient/product rule, factor (2+√x)(√x−2) = x−4",
                 "math": "y'' = \\dfrac{3(x-4)}{4x^{3/2}}", "note": ""},
            ],
        },
        {
            "prob":      "y = (1 + x^2)^4, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = 8x(1+x^2)^3",
            "ans1_norm": "8*x*(1+x^2)^3",
            "ans2_tex":  "y'' = 8(1+x^2)^2(1+7x^2)",
            "ans2_norm": "8*(1+x^2)^2*(1+7*x^2)",
            "steps": [
                {"label": "Chain rule: outer = u^4, inner = 1 + x²",
                 "math": "y' = 4(1+x^2)^3 \\cdot 2x = 8x(1+x^2)^3", "note": ""},
                {"label": "Product rule on y′ = 8x·(1+x²)^3",
                 "math": "y'' = 8(1+x^2)^3 + 8x \\cdot 3(1+x^2)^2 \\cdot 2x", "note": ""},
                {"label": "Factor (1+x²)²",
                 "math": "y'' = 8(1+x^2)^2[(1+x^2)+6x^2] = 8(1+x^2)^2(1+7x^2)", "note": ""},
            ],
        },
        {
            "prob":      "y = \\sin^2(x), \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = 2\\sin(x)\\cos(x)",
            "ans1_norm": "2*sin(x)*cos(x)",
            "ans2_tex":  "y'' = 2\\cos(2x)",
            "ans2_norm": "2*cos(2x)",
            "steps": [
                {"label": "Chain rule: outer = u², inner = sin(x)",
                 "math": "y' = 2\\sin x\\cos x", "note": "also equals sin(2x)"},
                {"label": "Rewrite y′ = sin(2x), then chain rule",
                 "math": "y'' = \\cos(2x) \\cdot 2 = 2\\cos(2x)", "note": ""},
            ],
        },
        {
            "prob":      "y = xe^x, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = e^x(1+x)",
            "ans1_norm": "e^x*(1+x)",
            "ans2_tex":  "y'' = e^x(2+x)",
            "ans2_norm": "e^x*(2+x)",
            "steps": [
                {"label": "Product rule: f = x, g = e^x",
                 "math": "y' = e^x + xe^x = e^x(1+x)", "note": "f′=1, g′=e^x"},
                {"label": "Product rule on y′ = e^x(1+x)",
                 "math": "y'' = e^x(1+x) + e^x = e^x(2+x)", "note": ""},
            ],
        },
        {
            "prob":      "y = \\ln(x^2), \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = \\dfrac{2}{x}",
            "ans1_norm": "2/x",
            "ans2_tex":  "y'' = -\\dfrac{2}{x^2}",
            "ans2_norm": "-2/x^2",
            "steps": [
                {"label": "Simplify: ln(x²) = 2ln(x), differentiate",
                 "math": "y' = \\dfrac{2}{x}", "note": "or chain rule gives same result"},
                {"label": "Power rule on y′ = 2x^{−1}",
                 "math": "y'' = -2x^{-2} = -\\dfrac{2}{x^2}", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {
        "problemTex":         c["prob"],
        "requiresDualAnswer": True,
        "answerTex":          c["ans1_tex"],
        "answerTex2":         c["ans2_tex"],
        "answerNorm":         c["ans1_norm"],
        "answerNorm2":        c["ans2_norm"],
        "steps":              c["steps"],
    }


diff3 = [_chain_nested, _product_chain, _quotient_chain, _implicit_differentiation, _log_differentiation, _higher_order, _y_prime_and_double_prime]

# ── diff4 — multi-rule combos ─────────────────────────────────────────────────

def _all_three_rules():
    cases = [
        {
            "prob": "\\dfrac{x^2 \\sin x}{e^x}",
            "ans": "\\dfrac{x(2\\sin x + x\\cos x - x\\sin x)}{e^x}",
            "norm": "x*(2*sin(x)+x*cos(x)-x*sin(x))/e^x",
            "steps": [
                {"label": "Structure: quotient — numerator is x²·sin(x), denominator is e^x", "math": "f = x^2\\sin x, \\quad g = e^x", "note": ""},
                {"label": "Differentiate numerator f using product rule", "math": "f' = 2x\\sin x + x^2\\cos x", "note": "d/dx[x²]=2x, d/dx[sin x]=cos x"},
                {"label": "Differentiate denominator g", "math": "g' = e^x", "note": "e^x is its own derivative"},
                {"label": "Apply quotient rule: (f'g − fg')/g²", "math": "\\dfrac{(2x\\sin x + x^2\\cos x)e^x - x^2\\sin x \\cdot e^x}{e^{2x}}", "note": ""},
                {"label": "Factor e^x from numerator and cancel with e^(2x)", "math": "\\dfrac{e^x(2x\\sin x + x^2\\cos x - x^2\\sin x)}{e^{2x}} = \\dfrac{2x\\sin x + x^2\\cos x - x^2\\sin x}{e^x}", "note": ""},
                {"label": "Factor x from numerator", "math": "\\dfrac{x(2\\sin x + x\\cos x - x\\sin x)}{e^x}", "note": ""},
            ],
        },
        {
            "prob": "x^2 e^{\\sin x}",
            "ans": "xe^{\\sin x}(2 + x\\cos x)",
            "norm": "x*e^(sin(x))*(2+x*cos(x))",
            "steps": [
                {"label": "Structure: product — f = x², g = e^(sin x)", "math": "f = x^2, \\quad g = e^{\\sin x}", "note": ""},
                {"label": "Differentiate f using power rule", "math": "f' = 2x", "note": ""},
                {"label": "Differentiate g using chain rule: outer = e^u, inner = sin(x)", "math": "g' = e^{\\sin x} \\cdot \\cos x", "note": "d/dx[e^u] = e^u · u', here u = sin(x), u' = cos(x)"},
                {"label": "Apply product rule: f'g + fg'", "math": "2x \\cdot e^{\\sin x} + x^2 \\cdot e^{\\sin x}\\cos x", "note": ""},
                {"label": "Factor x·e^(sin x) from both terms", "math": "xe^{\\sin x}(2 + x\\cos x)", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _implicit_second_order():
    return {
        "problemTex": "x^2 + y^2 = 25,\\quad \\text{find } \\dfrac{d^2y}{dx^2}",
        "answerTex": "-\\dfrac{25}{y^3}",
        "answerNorm": "-25/y^3",
        "steps": [
            {"label": "Step 1 — find dy/dx by implicit differentiation", "math": "2x + 2y\\dfrac{dy}{dx} = 0 \\implies \\dfrac{dy}{dx} = -\\dfrac{x}{y}", "note": "differentiate both sides, solve for dy/dx"},
            {"label": "Step 2 — differentiate dy/dx again using quotient rule", "math": "\\dfrac{d^2y}{dx^2} = \\dfrac{d}{dx}\\!\\left[-\\dfrac{x}{y}\\right] = -\\dfrac{y \\cdot 1 - x \\cdot \\frac{dy}{dx}}{y^2}", "note": "numerator: f=x (f'=1), denominator: g=y (g'=dy/dx)"},
            {"label": "Substitute dy/dx = −x/y into the expression", "math": "-\\dfrac{y - x(-x/y)}{y^2} = -\\dfrac{y + x^2/y}{y^2}", "note": ""},
            {"label": "Multiply numerator and denominator by y", "math": "-\\dfrac{y^2 + x^2}{y^3}", "note": ""},
            {"label": "Use the original equation: x² + y² = 25", "math": "-\\dfrac{25}{y^3}", "note": "substitute the constraint to simplify"},
        ],
    }


def _log_diff_complex():
    return {
        "problemTex": "y = \\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}},\\quad \\text{find } \\dfrac{dy}{dx}",
        "answerTex": "y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x - \\dfrac{1}{2(x+2)}\\right]",
        "answerNorm": "y*(6x/(x^2+1)+cot(x)-1/(2(x+2)))",
        "steps": [
            {"label": "Take ln of both sides — products become sums, powers come down", "math": "\\ln y = \\ln(x^2+1)^3 + \\ln(\\sin x) - \\ln\\sqrt{x+2}", "note": "log rules: ln(ab)=ln a+ln b, ln(a/b)=ln a−ln b"},
            {"label": "Simplify each log using power rules", "math": "\\ln y = 3\\ln(x^2+1) + \\ln(\\sin x) - \\tfrac{1}{2}\\ln(x+2)", "note": "ln(a^n) = n·ln(a), ln(√a) = (1/2)ln(a)"},
            {"label": "Differentiate both sides", "math": "\\dfrac{1}{y}\\dfrac{dy}{dx} = \\dfrac{d}{dx}\\left[3\\ln(x^2+1)\\right] + \\dfrac{d}{dx}[\\ln(\\sin x)] - \\dfrac{d}{dx}\\left[\\tfrac{1}{2}\\ln(x+2)\\right]", "note": "left side: chain rule on ln(y)"},
            {"label": "Differentiate each term (chain rule each time)", "math": "\\dfrac{1}{y}y' = \\dfrac{3 \\cdot 2x}{x^2+1} + \\dfrac{\\cos x}{\\sin x} - \\dfrac{1}{2(x+2)}", "note": "d/dx[ln(u)] = u'/u for each term"},
            {"label": "Multiply both sides by y", "math": "y' = y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x-\\dfrac{1}{2(x+2)}\\right]", "note": "leave y as-is — substituting back the full fraction would be messy"},
        ],
    }


diff4 = [_all_three_rules, _all_three_rules, _implicit_second_order, _log_diff_complex]

# ── diff5 — parametric, inverse trig ─────────────────────────────────────────

def _parametric_derivative():
    cases = [
        {
            "prob": "x=t^2,\\; y=t^3",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{3t^2}{2t} = \\dfrac{3t}{2}",
            "norm": "3t/2",
            "steps": [
                {"label": "Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "math": "\\text{differentiate x and y each with respect to t, then divide}", "note": ""},
                {"label": "Differentiate x with respect to t", "math": "\\dfrac{dx}{dt} = 2t", "note": "power rule"},
                {"label": "Differentiate y with respect to t", "math": "\\dfrac{dy}{dt} = 3t^2", "note": "power rule"},
                {"label": "Divide dy/dt by dx/dt", "math": "\\dfrac{dy}{dx} = \\dfrac{3t^2}{2t}", "note": ""},
                {"label": "Simplify by cancelling t", "math": "\\dfrac{3t}{2}", "note": ""},
            ],
        },
        {
            "prob": "x=\\cos t,\\; y=\\sin t",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{\\cos t}{-\\sin t} = -\\cot t",
            "norm": "-cot(t)",
            "steps": [
                {"label": "Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "math": "\\text{differentiate x and y each with respect to t, then divide}", "note": ""},
                {"label": "Differentiate x with respect to t", "math": "\\dfrac{dx}{dt} = -\\sin t", "note": "d/dt[cos t] = −sin t"},
                {"label": "Differentiate y with respect to t", "math": "\\dfrac{dy}{dt} = \\cos t", "note": "d/dt[sin t] = cos t"},
                {"label": "Divide dy/dt by dx/dt", "math": "\\dfrac{dy}{dx} = \\dfrac{\\cos t}{-\\sin t}", "note": ""},
                {"label": "Simplify: cos/sin = cot", "math": "-\\cot t", "note": "negative because of the minus sign in dx/dt"},
            ],
        },
        {
            "prob": "x=e^t,\\; y=t^2",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{2t}{e^t}",
            "norm": "2t/e^t",
            "steps": [
                {"label": "Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "math": "\\text{differentiate x and y each with respect to t, then divide}", "note": ""},
                {"label": "Differentiate x with respect to t", "math": "\\dfrac{dx}{dt} = e^t", "note": "e^t is its own derivative"},
                {"label": "Differentiate y with respect to t", "math": "\\dfrac{dy}{dt} = 2t", "note": "power rule"},
                {"label": "Divide dy/dt by dx/dt", "math": "\\dfrac{dy}{dx} = \\dfrac{2t}{e^t}", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": f"\\text{{Parametric: }} {c['prob']}\\quad \\text{{Find }} dy/dx.", "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _inverse_trig_chain():
    cases = [
        {
            "prob": "\\arcsin(\\sqrt{x})",
            "ans": "\\dfrac{1}{2\\sqrt{x}\\sqrt{1-x}} = \\dfrac{1}{2\\sqrt{x-x^2}}",
            "norm": "1/(2*sqrt(x-x^2))",
            "steps": [
                {"label": "Formula: d/dx[arcsin(u)] = u' / √(1 − u²)", "math": "\\text{identify } u = \\sqrt{x}", "note": ""},
                {"label": "Find u': differentiate u = √x = x^(1/2)", "math": "u' = \\dfrac{1}{2\\sqrt{x}}", "note": "power rule: d/dx[x^(1/2)] = (1/2)x^(-1/2) = 1/(2√x)"},
                {"label": "Compute 1 − u²", "math": "1 - (\\sqrt{x})^2 = 1 - x", "note": ""},
                {"label": "Substitute into the formula", "math": "\\dfrac{u'}{\\sqrt{1-u^2}} = \\dfrac{1/(2\\sqrt{x})}{\\sqrt{1-x}}", "note": ""},
                {"label": "Simplify", "math": "\\dfrac{1}{2\\sqrt{x}\\sqrt{1-x}} = \\dfrac{1}{2\\sqrt{x-x^2}}", "note": "√x · √(1-x) = √(x(1-x)) = √(x-x²)"},
            ],
        },
        {
            "prob": "\\arctan(x^2)",
            "ans": "\\dfrac{2x}{1+x^4}",
            "norm": "2x/(1+x^4)",
            "steps": [
                {"label": "Formula: d/dx[arctan(u)] = u' / (1 + u²)", "math": "\\text{identify } u = x^2", "note": ""},
                {"label": "Find u': differentiate u = x²", "math": "u' = 2x", "note": "power rule"},
                {"label": "Compute 1 + u²", "math": "1 + (x^2)^2 = 1 + x^4", "note": ""},
                {"label": "Substitute into the formula", "math": "\\dfrac{2x}{1+x^4}", "note": ""},
            ],
        },
        {
            "prob": "\\arccos(2x)",
            "ans": "\\dfrac{-2}{\\sqrt{1-4x^2}}",
            "norm": "-2/sqrt(1-4x^2)",
            "steps": [
                {"label": "Formula: d/dx[arccos(u)] = −u' / √(1 − u²)", "math": "\\text{identify } u = 2x", "note": "note the negative sign — arccos derivative is negative arcsin derivative"},
                {"label": "Find u': differentiate u = 2x", "math": "u' = 2", "note": ""},
                {"label": "Compute 1 − u²", "math": "1 - (2x)^2 = 1 - 4x^2", "note": ""},
                {"label": "Substitute into the formula", "math": "\\dfrac{-2}{\\sqrt{1-4x^2}}", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


def _full_combo():
    cases = [
        {
            "prob": "x^2 \\arctan(x)",
            "ans": "2x\\arctan(x) + \\dfrac{x^2}{1+x^2}",
            "norm": "2x*arctan(x)+x^2/(1+x^2)",
            "steps": [
                {"label": "Structure: product — f = x², g = arctan(x)", "math": "f = x^2, \\quad g = \\arctan(x)", "note": ""},
                {"label": "Differentiate f", "math": "f' = 2x", "note": "power rule"},
                {"label": "Differentiate g using inverse trig formula", "math": "g' = \\dfrac{1}{1+x^2}", "note": "d/dx[arctan(u)] = u'/(1+u²), here u=x, u'=1"},
                {"label": "Apply product rule: f'g + fg'", "math": "2x \\cdot \\arctan(x) + x^2 \\cdot \\dfrac{1}{1+x^2}", "note": ""},
                {"label": "Simplify", "math": "2x\\arctan(x) + \\dfrac{x^2}{1+x^2}", "note": ""},
            ],
        },
        {
            "prob": "e^x \\ln(x^2+1)",
            "ans": "e^x\\ln(x^2+1)+\\dfrac{2xe^x}{x^2+1}",
            "norm": "e^x*ln(x^2+1)+2x*e^x/(x^2+1)",
            "steps": [
                {"label": "Structure: product — f = e^x, g = ln(x²+1)", "math": "f = e^x, \\quad g = \\ln(x^2+1)", "note": ""},
                {"label": "Differentiate f", "math": "f' = e^x", "note": "e^x is its own derivative"},
                {"label": "Differentiate g using chain rule: d/dx[ln(u)] = u'/u", "math": "g' = \\dfrac{2x}{x^2+1}", "note": "u = x²+1, u' = 2x"},
                {"label": "Apply product rule: f'g + fg'", "math": "e^x \\cdot \\ln(x^2+1) + e^x \\cdot \\dfrac{2x}{x^2+1}", "note": ""},
                {"label": "Simplify", "math": "e^x\\ln(x^2+1) + \\dfrac{2xe^x}{x^2+1}", "note": ""},
            ],
        },
        {
            "prob": "\\sin^2(\\cos(x))",
            "ans": "2\\sin(\\cos x)\\cos(\\cos x)\\cdot(-\\sin x)",
            "norm": "2*sin(cos(x))*cos(cos(x))*(-sin(x))",
            "steps": [
                {"label": "Three nested layers: [sin(cos(x))]²", "math": "\\text{outermost} = u^2, \\quad u = \\sin(\\cos x)", "note": ""},
                {"label": "Layer 1 — d/dx[u²] = 2u, keep u = sin(cos x) intact", "math": "2\\sin(\\cos x)", "note": "power rule on the outermost square"},
                {"label": "Layer 2 — d/dx[sin(cos x)] = cos(cos x), keep cos(x) inside", "math": "\\cdot \\cos(\\cos x)", "note": "derivative of sin is cos, leave inner cos(x) unchanged"},
                {"label": "Layer 3 — d/dx[cos(x)] = −sin(x)", "math": "\\cdot (-\\sin x)", "note": ""},
                {"label": "Multiply all three layers", "math": "2\\sin(\\cos x) \\cdot \\cos(\\cos x) \\cdot (-\\sin x)", "note": ""},
            ],
        },
    ]
    c = pick(cases)
    return {"problemTex": _d_tex(c["prob"]), "answerTex": c["ans"], "answerNorm": c["norm"], "steps": c["steps"]}


diff5 = [_parametric_derivative, _inverse_trig_chain, _full_combo, _full_combo]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
