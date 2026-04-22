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
    # d/dx[ax^n] = an·x^(n-1)
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
            {"label": "Power rule: d/dx[ax^n] = anx^(n-1)", "math": f"{an}x^{{{n_minus}}}", "note": f"multiply by exponent, reduce by 1"},
        ],
    }


def _trig_basic():
    cases = [
        ("\\sin x",    "\\cos x",           "cos(x)"),
        ("\\cos x",    "-\\sin x",          "-sin(x)"),
        ("\\tan x",    "\\sec^2 x",         "sec^2(x)"),
        ("\\cot x",    "-\\csc^2 x",        "-csc^2(x)"),
        ("\\sec x",    "\\sec x\\tan x",    "sec(x)*tan(x)"),
        ("\\csc x",    "-\\csc x\\cot x",   "-csc(x)*cot(x)"),
    ]
    f_tex, d_tex, d_norm = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [{"label": "Standard trig derivative", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": "memorize"}],
    }


def _exponential_rule():
    cases = [
        ("e^x",         "e^x",         "e^x"),
        ("e^x",         "e^x",         "e^x"),
        ("2^x",         "2^x \\ln 2",  "2^x*ln(2)"),
        ("3^x",         "3^x \\ln 3",  "3^x*ln(3)"),
        ("10^x",        "10^x \\ln 10","10^x*ln(10)"),
    ]
    f_tex, d_tex, d_norm = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [{"label": "Exponential derivative", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": ""}],
    }


def _log_rule():
    cases = [
        ("\\ln x",      "\\dfrac{1}{x}",          "1/x"),
        ("\\log_2 x",   "\\dfrac{1}{x \\ln 2}",   "1/(x*ln(2))"),
        ("\\log_{10} x","\\dfrac{1}{x \\ln 10}",  "1/(x*ln(10))"),
    ]
    f_tex, d_tex, d_norm = pick(cases)
    return {
        "problemTex": _d_tex(f_tex),
        "answerTex": d_tex,
        "answerNorm": d_norm,
        "steps": [{"label": "Logarithm derivative", "math": f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", "note": ""}],
    }


def _sum_difference():
    # d/dx[ax^m ± bx^n]
    m, n = pick([2,3,4,5]), pick([0,1,2,3])
    while m == n: n = pick([0,1,2,3])
    a, b = R(1,6), R(1,6)
    pm = a * m; pn = b * n
    # Build tex
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
            {"label": "Differentiate term by term", "math": f"{ans_dm} {'+' if sign=='+' else '-'} {ans_dn}", "note": "sum/difference rule"},
        ],
    }


diff1 = [_power_rule, _power_rule, _trig_basic, _exponential_rule, _log_rule, _sum_difference]

# ── diff2 — product, quotient, chain ─────────────────────────────────────────

def _product_rule():
    # d/dx[x^m * trig or exp]
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
        "answerNorm": deriv_tex.replace("{","").replace("}","").replace("\\","").replace("dfrac",""),
        "steps": [
            {"label": "Product rule: (fg)' = f'g + fg'", "math": f"({f_d_tex})({g_tex}) + ({f_tex})({g_d_tex})", "note": ""},
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
        "answerNorm": deriv_tex.replace("{","").replace("}","").replace("\\","").replace("dfrac",""),
        "steps": [
            {"label": "Quotient rule: (f/g)' = (f'g − fg')/g²", "math": f"\\dfrac{{({f_d_tex})({g_tex})-({f_tex})({g_d_tex})}}{{{g_tex}^2}}", "note": ""},
            {"label": "Simplify", "math": deriv_tex, "note": ""},
        ],
    }


def _chain_single():
    cases = [
        (Sin(X),  "\\sin",  pow_expr(X,2),  "x^2",  Cos(pow_expr(X,2)),  "\\cos(x^2)",  mul(Const(2),X),  "2x"),
        (Exp(X),  "e^u",    mul(Const(3),X),"3x",   Exp(mul(Const(3),X)),"e^{3x}",      Const(3),         "3"),
        (Ln(X),   "\\ln",   pow_expr(X,2),  "x^2",  Div(Const(2),X),     "2/x",         mul(Const(2),X),  "2x"),
        (pow_expr(X,2),"u^2",Sin(X),"\\sin x",
            mul(mul(Const(2),Sin(X)),Cos(X)), "2\\sin x\\cos x",Cos(X),"\\cos x"),
        (Sin(X),"\\sin",add(X,Const(3)),"x+3",Sin(add(X,Const(3))),"\\sin(x+3)",Const(1),"1"),
        (Exp(X),"e^u",add(pow_expr(X,2),X),"x^2+x",
            Mul(Exp(add(pow_expr(X,2),X)),add(mul(Const(2),X),Const(1))),
            "e^{x^2+x}(2x+1)",add(mul(Const(2),X),Const(1)),"2x+1"),
    ]
    outer, outer_name, inner_expr, inner_tex, deriv, deriv_tex, inner_deriv, inner_deriv_tex = pick(cases)
    return {
        "problemTex": _d_tex(deriv_tex.replace("(2x+1)","").rstrip() or f"{outer_name}({inner_tex})"),
        "answerTex": deriv_tex,
        "answerNorm": deriv_tex.replace("{","").replace("}","").replace("\\",""),
        "steps": [
            {"label": "Chain rule: d/dx[f(g)] = f'(g)·g'", "math": f"f'({inner_tex}) \\cdot \\dfrac{{d}}{{dx}}[{inner_tex}]", "note": ""},
            {"label": f"Outer derivative evaluated at inner", "math": f"... \\cdot {inner_deriv_tex}", "note": ""},
            {"label": "Result", "math": deriv_tex, "note": ""},
        ],
    }


diff2 = [_product_rule, _product_rule, _quotient_rule, _chain_single, _chain_single]

# ── diff3 — advanced combinations ─────────────────────────────────────────────

def _chain_nested():
    # d/dx[sin(cos(x²))]
    cases = [
        (
            "\\sin(\\cos(x^2))",
            "\\cos(\\cos(x^2)) \\cdot (-\\sin(x^2)) \\cdot 2x",
            "cos(cos(x^2))*(-sin(x^2))*2x",
        ),
        (
            "e^{\\sin(x^2)}",
            "e^{\\sin(x^2)} \\cdot \\cos(x^2) \\cdot 2x",
            "e^sin(x^2)*cos(x^2)*2x",
        ),
        (
            "\\ln(\\sin(x))",
            "\\dfrac{\\cos x}{\\sin x} = \\cot x",
            "cos(x)/sin(x)",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Identify layers (outermost → innermost)", "math": "\\text{Apply chain rule from outside in}", "note": ""},
            {"label": "Result", "math": ans, "note": ""},
        ],
    }


def _product_chain():
    # d/dx[x^n · trig(ax)]
    n = pick([2,3]); a = R(2,5)
    cases = [
        (f"x^{n}\\sin({a}x)",
         f"{n}x^{{{n-1}}}\\sin({a}x) + {a}x^{n}\\cos({a}x)",
         f"{n}x^{n-1}*sin({a}x)+{a}x^{n}*cos({a}x)"),
        (f"x^{n}e^{{{a}x}}",
         f"{n}x^{{{n-1}}}e^{{{a}x}} + {a}x^{n}e^{{{a}x}} = x^{{{n-1}}}e^{{{a}x}}({n}+{a}x)",
         f"x^{n-1}*e^({a}x)*({n}+{a}x)"),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Product rule: (uv)' = u'v + uv'", "math": "f = x^n,\\; g = \\text{(second factor)}", "note": ""},
            {"label": "Chain rule on second factor", "math": "\\text{apply chain to inner function}", "note": ""},
            {"label": "Result", "math": ans, "note": ""},
        ],
    }


def _quotient_chain():
    cases = [
        (
            "\\dfrac{e^{2x}}{x^2+1}",
            "\\dfrac{2e^{2x}(x^2+1) - e^{2x}(2x)}{(x^2+1)^2} = \\dfrac{2e^{2x}(x^2-x+1)}{(x^2+1)^2}",
            "2e^(2x)*(x^2-x+1)/(x^2+1)^2",
        ),
        (
            "\\dfrac{\\sin(3x)}{x}",
            "\\dfrac{3x\\cos(3x) - \\sin(3x)}{x^2}",
            "(3x*cos(3x)-sin(3x))/x^2",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Quotient + chain rule", "math": "\\text{(f'g - fg')}/g^2, \\text{ chain on numerator}", "note": ""},
            {"label": "Result", "math": ans, "note": ""},
        ],
    }


def _implicit_differentiation():
    cases = [
        (
            "x^2 + y^2 = r^2",
            "\\dfrac{dy}{dx} = -\\dfrac{x}{y}",
            "-x/y",
        ),
        (
            "x^2 + xy + y^2 = 7",
            "\\dfrac{dy}{dx} = -\\dfrac{2x+y}{x+2y}",
            "-(2x+y)/(x+2y)",
        ),
        (
            "\\sin(xy) = x",
            "\\dfrac{dy}{dx} = \\dfrac{1 - y\\cos(xy)}{x\\cos(xy)}",
            "(1-y*cos(xy))/(x*cos(xy))",
        ),
    ]
    implicit, ans, norm = pick(cases)
    return {
        "problemTex": f"\\text{{Given }} {implicit},\\text{{ find }} \\dfrac{{dy}}{{dx}}.",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Differentiate both sides with respect to x", "math": "\\text{remember: d/dx[y] = dy/dx (chain rule)}", "note": ""},
            {"label": "Collect dy/dx terms", "math": "\\text{move dy/dx to one side}", "note": ""},
            {"label": "Solve for dy/dx", "math": ans, "note": ""},
        ],
    }


def _log_differentiation():
    return {
        "problemTex": "y = x^x,\\quad \\text{find } \\dfrac{dy}{dx}",
        "answerTex": "x^x(\\ln x + 1)",
        "answerNorm": "x^x*(ln(x)+1)",
        "steps": [
            {"label": "Take ln both sides", "math": "\\ln y = x \\ln x", "note": ""},
            {"label": "Differentiate implicitly", "math": "\\dfrac{1}{y}\\dfrac{dy}{dx} = \\ln x + 1", "note": "product rule on right"},
            {"label": "Multiply by y", "math": "\\dfrac{dy}{dx} = y(\\ln x+1) = x^x(\\ln x+1)", "note": ""},
        ],
    }


def _higher_order():
    cases = [
        ("\\sin x", "f''(x) = -\\sin x", "-sin(x)"),
        ("\\cos x", "f''(x) = -\\cos x", "-cos(x)"),
        ("e^x",     "f''(x) = e^x",      "e^x"),
        ("x^4",     "f''(x) = 12x^2",    "12*x^2"),
        ("x^5",     "f''(x) = 20x^3",    "20*x^3"),
    ]
    f_tex, d2_tex, d2_norm = pick(cases)
    return {
        "problemTex": f"f(x) = {f_tex},\\quad \\text{{find }} f''(x).",
        "answerTex": d2_tex,
        "answerNorm": d2_norm,
        "steps": [
            {"label": "Differentiate once", "math": f"f'(x) = \\dfrac{{d}}{{dx}}[{f_tex}]", "note": ""},
            {"label": "Differentiate again", "math": d2_tex, "note": ""},
        ],
    }


diff3 = [_chain_nested, _product_chain, _quotient_chain, _implicit_differentiation, _log_differentiation, _higher_order]

# ── diff4 — multi-rule combos ─────────────────────────────────────────────────

def _all_three_rules():
    cases = [
        (
            "\\dfrac{x^2 \\sin x}{e^x}",
            "\\dfrac{e^x(2x\\sin x + x^2\\cos x) - x^2\\sin x \\cdot e^x}{e^{2x}} = \\dfrac{x(2\\sin x + x\\cos x - x\\sin x)}{e^x}",
            "x*(2*sin(x)+x*cos(x)-x*sin(x))/e^x",
        ),
        (
            "x^2 e^{\\sin x}",
            "2xe^{\\sin x} + x^2 e^{\\sin x}\\cos x = xe^{\\sin x}(2 + x\\cos x)",
            "x*e^(sin(x))*(2+x*cos(x))",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Identify rules needed: quotient/product + chain", "math": "\\text{plan before differentiating}", "note": ""},
            {"label": "Apply carefully", "math": ans, "note": ""},
        ],
    }


def _implicit_second_order():
    return {
        "problemTex": "x^2 + y^2 = 25,\\quad \\text{find } \\dfrac{d^2y}{dx^2}",
        "answerTex": "-\\dfrac{25}{y^3}",
        "answerNorm": "-25/y^3",
        "steps": [
            {"label": "First: dy/dx = -x/y", "math": "\\dfrac{dy}{dx} = -\\dfrac{x}{y}", "note": "implicit diff"},
            {"label": "Differentiate again (quotient rule + chain)", "math": "\\dfrac{d^2y}{dx^2} = -\\dfrac{y - x(dy/dx)}{y^2}", "note": ""},
            {"label": "Substitute dy/dx", "math": "-\\dfrac{y-x(-x/y)}{y^2} = -\\dfrac{y^2+x^2}{y^3} = -\\dfrac{25}{y^3}", "note": "use x²+y²=25"},
        ],
    }


def _log_diff_complex():
    return {
        "problemTex": "y = \\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}},\\quad \\text{find } \\dfrac{dy}{dx}",
        "answerTex": "y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x - \\dfrac{1}{2(x+2)}\\right]",
        "answerNorm": "y*(6x/(x^2+1)+cot(x)-1/(2(x+2)))",
        "steps": [
            {"label": "Take ln both sides", "math": "\\ln y = 3\\ln(x^2+1)+\\ln(\\sin x)-\\tfrac{1}{2}\\ln(x+2)", "note": ""},
            {"label": "Differentiate implicitly", "math": "\\dfrac{1}{y}y' = \\dfrac{6x}{x^2+1}+\\cot x-\\dfrac{1}{2(x+2)}", "note": ""},
            {"label": "Multiply by y", "math": "y' = y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x-\\dfrac{1}{2(x+2)}\\right]", "note": ""},
        ],
    }


diff4 = [_all_three_rules, _all_three_rules, _implicit_second_order, _log_diff_complex]

# ── diff5 — parametric, inverse trig ─────────────────────────────────────────

def _parametric_derivative():
    cases = [
        (
            "x=t^2,\\; y=t^3",
            "\\dfrac{dy}{dx} = \\dfrac{3t^2}{2t} = \\dfrac{3t}{2}",
            "3t/2",
        ),
        (
            "x=\\cos t,\\; y=\\sin t",
            "\\dfrac{dy}{dx} = \\dfrac{\\cos t}{-\\sin t} = -\\cot t",
            "-cot(t)",
        ),
        (
            "x=e^t,\\; y=t^2",
            "\\dfrac{dy}{dx} = \\dfrac{2t}{e^t}",
            "2t/e^t",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": f"\\text{{Parametric: }} {prob}\\quad \\text{{Find }} dy/dx.",
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "dy/dx = (dy/dt) / (dx/dt)", "math": "\\text{divide derivatives with respect to parameter}", "note": ""},
            {"label": "Compute", "math": ans, "note": ""},
        ],
    }


def _inverse_trig_chain():
    cases = [
        (
            "\\arcsin(\\sqrt{x})",
            "\\dfrac{1}{2\\sqrt{x}\\sqrt{1-x}} = \\dfrac{1}{2\\sqrt{x-x^2}}",
            "1/(2*sqrt(x-x^2))",
        ),
        (
            "\\arctan(x^2)",
            "\\dfrac{2x}{1+x^4}",
            "2x/(1+x^4)",
        ),
        (
            "\\arccos(2x)",
            "\\dfrac{-2}{\\sqrt{1-4x^2}}",
            "-2/sqrt(1-4x^2)",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Inverse trig derivative + chain rule", "math": "\\dfrac{d}{dx}[\\arcsin u]=\\dfrac{u'}{\\sqrt{1-u^2}},\\; \\dfrac{d}{dx}[\\arctan u]=\\dfrac{u'}{1+u^2}", "note": ""},
            {"label": "Apply to problem", "math": ans, "note": ""},
        ],
    }


def _full_combo():
    cases = [
        (
            "x^2 \\arctan(x)",
            "2x\\arctan(x) + \\dfrac{x^2}{1+x^2}",
            "2x*arctan(x)+x^2/(1+x^2)",
        ),
        (
            "e^x \\ln(x^2+1)",
            "e^x\\ln(x^2+1)+\\dfrac{2xe^x}{x^2+1}",
            "e^x*ln(x^2+1)+2x*e^x/(x^2+1)",
        ),
        (
            "\\sin^2(\\cos(x))",
            "2\\sin(\\cos x)\\cos(\\cos x)\\cdot(-\\sin x)",
            "2*sin(cos(x))*cos(cos(x))*(-sin(x))",
        ),
    ]
    prob, ans, norm = pick(cases)
    return {
        "problemTex": _d_tex(prob),
        "answerTex": ans,
        "answerNorm": norm,
        "steps": [
            {"label": "Multiple rules required — plan first", "math": "\\text{identify all rules needed}", "note": ""},
            {"label": "Apply systematically", "math": ans, "note": ""},
        ],
    }


diff5 = [_parametric_derivative, _inverse_trig_chain, _full_combo, _full_combo]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
