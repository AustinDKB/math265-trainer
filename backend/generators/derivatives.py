import random
from sympy import symbols, diff, simplify, sin, cos, tan, exp, log
from sympy_utils import to_norm, to_tex
from math_utils import R, pick, sign_str
from problem_builder import problem, step, dual_problem

x = symbols('x')

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
    return problem(
        problem_tex=_d_tex(expr_tex),
        answer_tex=ans_tex,
        answer_norm=ans_norm,
        steps=[
            step("Power rule: d/dx[ax^n] = an·x^(n-1)", f"\\text{{multiply exponent by coefficient: }} {a} \\cdot {n} = {an}", f"bring the {n} down, reduce exponent by 1"),
            step("Reduce exponent by 1", f"n-1 = {n}-1 = {n_minus}"),
            step("Result", ans_tex),
        ],
    )


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
    return problem(
        problem_tex=_d_tex(f_tex),
        answer_tex=d_tex,
        answer_norm=d_norm,
        steps=[
            step("Recall standard trig derivative", f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", reason),
        ],
    )


def _exponential_rule():
    cases = [
        ("e^x",   "e^x",          "e^x",          "e^x is its own derivative"),
        ("e^x",   "e^x",          "e^x",          "e^x is its own derivative"),
        ("2^x",   "2^x \\ln 2",   "2^x*ln(2)",    "for a^x: multiply by ln(a)"),
        ("3^x",   "3^x \\ln 3",   "3^x*ln(3)",    "for a^x: multiply by ln(a)"),
        ("10^x",  "10^x \\ln 10", "10^x*ln(10)",  "for a^x: multiply by ln(a)"),
    ]
    f_tex, d_tex, d_norm, reason = pick(cases)
    return problem(
        problem_tex=_d_tex(f_tex),
        answer_tex=d_tex,
        answer_norm=d_norm,
        steps=[
            step("Exponential derivative rule", f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", reason),
        ],
    )


def _log_rule():
    cases = [
        ("\\ln x",       "\\dfrac{1}{x}",          "1/x",           "d/dx[ln x] = 1/x"),
        ("\\log_2 x",    "\\dfrac{1}{x \\ln 2}",   "1/(x*ln(2))",   "d/dx[log_a x] = 1/(x·ln a)"),
        ("\\log_{10} x", "\\dfrac{1}{x \\ln 10}",  "1/(x*ln(10))",  "d/dx[log_a x] = 1/(x·ln a)"),
    ]
    f_tex, d_tex, d_norm, reason = pick(cases)
    return problem(
        problem_tex=_d_tex(f_tex),
        answer_tex=d_tex,
        answer_norm=d_norm,
        steps=[
            step("Logarithm derivative rule", f"\\dfrac{{d}}{{dx}}[{f_tex}] = {d_tex}", reason),
        ],
    )


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
    return problem(
        problem_tex=_d_tex(prob),
        answer_tex=ans_tex,
        answer_norm=ans_norm,
        steps=[
            step("Sum/difference rule: differentiate each term separately", f"\\dfrac{{d}}{{dx}}[{term_tex(a,m)}] {'+' if sign=='+' else '-'} \\dfrac{{d}}{{dx}}[{term_tex(b,n)}]"),
            step(f"Apply power rule to each term", f"{ans_dm} {'+' if sign=='+' else '-'} {ans_dn}", f"d/dx[{term_tex(a,m)}]={ans_dm},\\; d/dx[{term_tex(b,n)}]={ans_dn}"),
        ],
    )


diff1 = [_power_rule, _power_rule, _trig_basic, _exponential_rule, _log_rule, _sum_difference]

# ── diff2 — product, quotient, chain ─────────────────────────────────────────

def _product_rule():
    cases = [
        (x,               "x",    sin(x),       r"\sin x"),
        (x,               "x",    cos(x),       r"\cos x"),
        (x,               "x",    exp(x),       r"e^x"),
        (x**2,            "x^2",  sin(x),       r"\sin x"),
        (x**2,            "x^2",  exp(x),       r"e^x"),
        (x**3,            "x^3",  log(x),       r"\ln x"),
        (2*x,             "2x",   cos(x),       r"\cos x"),
    ]
    f_expr, f_tex, g_expr, g_tex = pick(cases)
    product = f_expr * g_expr
    deriv = simplify(diff(product, x))
    deriv_tex = to_tex(deriv)
    f_d = simplify(diff(f_expr, x))
    g_d = simplify(diff(g_expr, x))
    f_d_tex = to_tex(f_d)
    g_d_tex = to_tex(g_d)
    return problem(
        problem_tex=_d_tex(f"{f_tex} \\cdot {g_tex}"),
        answer_tex=deriv_tex,
        answer_norm=to_norm(deriv),
        steps=[
            step("Identify the two factors", f"f = {f_tex}, \\quad g = {g_tex}"),
            step("Differentiate each factor separately", f"f' = {f_d_tex}, \\quad g' = {g_d_tex}"),
            step("Product rule: (fg)' = f'g + fg'", f"({f_d_tex})({g_tex}) + ({f_tex})({g_d_tex})", "first · derivative of second + second · derivative of first"),
            step("Simplify", deriv_tex),
        ],
    )


def _quotient_rule():
    cases = [
        (sin(x),       r"\sin x",  x,             "x"),
        (exp(x),       r"e^x",     x**2,          "x^2"),
        (log(x),       r"\ln x",   x,             "x"),
        (x**2,         "x^2",      x+1,           "x+1"),
        (sin(x),       r"\sin x",  cos(x),        r"\cos x"),
    ]
    f_expr, f_tex, g_expr, g_tex = pick(cases)
    quotient = f_expr / g_expr
    deriv = simplify(diff(quotient, x))
    deriv_tex = to_tex(deriv)
    f_d = simplify(diff(f_expr, x))
    g_d = simplify(diff(g_expr, x))
    f_d_tex = to_tex(f_d)
    g_d_tex = to_tex(g_d)
    return problem(
        problem_tex=_d_tex(f"\\dfrac{{{f_tex}}}{{{g_tex}}}"),
        answer_tex=deriv_tex,
        answer_norm=to_norm(deriv),
        steps=[
            step("Identify numerator and denominator", f"f = {f_tex}, \\quad g = {g_tex}"),
            step("Differentiate each", f"f' = {f_d_tex}, \\quad g' = {g_d_tex}"),
            step("Quotient rule: (f/g)' = (f'g − fg')/g²", f"\\dfrac{{({f_d_tex})({g_tex})-({f_tex})({g_d_tex})}}{{{g_tex}^2}}", "low d-high minus high d-low, over low squared"),
            step("Simplify", deriv_tex),
        ],
    )


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
    return problem(
        problem_tex=_d_tex(func_tex),
        answer_tex=ans_tex,
        answer_norm=ans_norm,
        steps=[
            step("Identify outer and inner functions", f"\\text{{{structure}}}", "chain rule: differentiate outside first, keep inside intact"),
            step("Differentiate the outer function (leave inner unchanged)", f"\\dfrac{{d}}{{du}}[{outer_name}] \\text{{ evaluated at inner}} = {outer_d_tex}"),
            step("Differentiate the inner function", f"\\dfrac{{d}}{{dx}}[{inner_tex}] = {inner_d_tex}"),
            step("Multiply: outer derivative × inner derivative", f"{outer_d_tex} \\cdot {inner_d_tex} = {ans_tex}"),
        ],
    )


diff2 = [_product_rule, _product_rule, _quotient_rule, _chain_single, _chain_single]

# ── diff3 — advanced combinations ─────────────────────────────────────────────

def _chain_nested():
    cases = [
        {
            "prob": "\\sin(\\cos(x^2))",
            "ans": "\\cos(\\cos(x^2)) \\cdot (-\\sin(x^2)) \\cdot 2x",
            "norm": "cos(cos(x^2))*(-sin(x^2))*2x",
            "steps": [
                step("Three nested layers: sin( cos( x² ) )", "\\text{outermost} \\to \\text{middle} \\to \\text{innermost}", "apply chain rule once per layer, working outside in"),
                step("Layer 1 — outer: d/dx[sin(u)] = cos(u), keep u = cos(x²)", "\\cos(\\cos(x^2))", "differentiate sin, leave everything inside untouched"),
                step("Layer 2 — middle: d/dx[cos(x²)] = −sin(x²), keep x² inside", "\\cdot(-\\sin(x^2))", "differentiate cos, still leave x² alone"),
                step("Layer 3 — inner: d/dx[x²] = 2x", "\\cdot 2x"),
                step("Multiply all three layers together", "\\cos(\\cos(x^2)) \\cdot (-\\sin(x^2)) \\cdot 2x"),
            ],
        },
        {
            "prob": "e^{\\sin(x^2)}",
            "ans": "e^{\\sin(x^2)} \\cdot \\cos(x^2) \\cdot 2x",
            "norm": "e^sin(x^2)*cos(x^2)*2x",
            "steps": [
                step("Three nested layers: e^( sin( x² ) )", "\\text{outermost} \\to \\text{middle} \\to \\text{innermost}", "apply chain rule once per layer, outside in"),
                step("Layer 1 — outer: d/dx[e^u] = e^u, keep u = sin(x²)", "e^{\\sin(x^2)}", "e^u derivative is itself — leave the exponent unchanged"),
                step("Layer 2 — middle: d/dx[sin(x²)] = cos(x²), keep x²", "\\cdot \\cos(x^2)", "differentiate sin, leave x² inside"),
                step("Layer 3 — inner: d/dx[x²] = 2x", "\\cdot 2x"),
                step("Multiply all three layers together", "e^{\\sin(x^2)} \\cdot \\cos(x^2) \\cdot 2x"),
            ],
        },
        {
            "prob": "\\ln(\\sin(x))",
            "ans": "\\dfrac{\\cos x}{\\sin x} = \\cot x",
            "norm": "cos(x)/sin(x)",
            "steps": [
                step("Two layers: ln( sin(x) )", "\\text{outer} = \\ln(u), \\quad \\text{inner} = \\sin(x)"),
                step("Layer 1 — outer: d/dx[ln(u)] = 1/u, evaluated at u = sin(x)", "\\dfrac{1}{\\sin(x)}"),
                step("Layer 2 — inner: d/dx[sin(x)] = cos(x)", "\\cdot \\cos(x)"),
                step("Multiply and simplify", "\\dfrac{\\cos x}{\\sin x} = \\cot x", "cos/sin = cot by definition"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _product_chain():
    n = pick([2,3]); a = R(2,5)
    cases = [
        {
            "prob": f"x^{n}\\sin({a}x)",
            "ans": f"{n}x^{{{n-1}}}\\sin({a}x) + {a}x^{n}\\cos({a}x)",
            "norm": f"{n}x^{n-1}*sin({a}x)+{a}x^{n}*cos({a}x)",
            "steps": [
                step(f"Product rule: f = x^{n}, g = sin({a}x)", f"f = x^{n}, \\quad g = \\sin({a}x)", "identify the two factors before differentiating"),
                step(f"Differentiate f using power rule", f"f' = {n}x^{{{n-1}}}"),
                step(f"Differentiate g using chain rule: outer = sin(u), inner = {a}x", f"g' = \\cos({a}x) \\cdot {a} = {a}\\cos({a}x)", f"d/dx[sin({a}x)] = cos({a}x) · {a}"),
                step("Apply product rule: f'g + fg'", f"{n}x^{{{n-1}}}\\sin({a}x) + x^{n}\\cdot {a}\\cos({a}x)"),
            ],
        },
        {
            "prob": f"x^{n}e^{{{a}x}}",
            "ans": f"{n}x^{{{n-1}}}e^{{{a}x}} + {a}x^{n}e^{{{a}x}} = x^{{{n-1}}}e^{{{a}x}}({n}+{a}x)",
            "norm": f"x^{n-1}*e^({a}x)*({n}+{a}x)",
            "steps": [
                step(f"Product rule: f = x^{n}, g = e^{{{a}x}}", f"f = x^{n}, \\quad g = e^{{{a}x}}"),
                step("Differentiate f using power rule", f"f' = {n}x^{{{n-1}}}"),
                step(f"Differentiate g using chain rule: outer = e^u, inner = {a}x", f"g' = e^{{{a}x}} \\cdot {a} = {a}e^{{{a}x}}", f"d/dx[e^({a}x)] = e^({a}x) · {a}"),
                step("Apply product rule: f'g + fg'", f"{n}x^{{{n-1}}}e^{{{a}x}} + x^{n} \\cdot {a}e^{{{a}x}}"),
                step("Factor out common terms", f"x^{{{n-1}}}e^{{{a}x}}({n}+{a}x)", f"x^{n-1} and e^({a}x) appear in both terms"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _quotient_chain():
    cases = [
        {
            "prob": "\\dfrac{e^{2x}}{x^2+1}",
            "ans": "\\dfrac{2e^{2x}(x^2+1) - e^{2x}(2x)}{(x^2+1)^2} = \\dfrac{2e^{2x}(x^2-x+1)}{(x^2+1)^2}",
            "norm": "2e^(2x)*(x^2-x+1)/(x^2+1)^2",
            "steps": [
                step("Identify numerator and denominator", "f = e^{2x}, \\quad g = x^2+1"),
                step("Differentiate f using chain rule: outer = e^u, inner = 2x", "f' = e^{2x} \\cdot 2 = 2e^{2x}", "multiply e^(2x) by the derivative of the exponent"),
                step("Differentiate g using power rule", "g' = 2x"),
                step("Quotient rule: (f'g − fg')/g²", "\\dfrac{2e^{2x}(x^2+1) - e^{2x}(2x)}{(x^2+1)^2}"),
                step("Factor e^(2x) from the numerator and simplify", "\\dfrac{2e^{2x}(x^2-x+1)}{(x^2+1)^2}"),
            ],
        },
        {
            "prob": "\\dfrac{\\sin(3x)}{x}",
            "ans": "\\dfrac{3x\\cos(3x) - \\sin(3x)}{x^2}",
            "norm": "(3x*cos(3x)-sin(3x))/x^2",
            "steps": [
                step("Identify numerator and denominator", "f = \\sin(3x), \\quad g = x"),
                step("Differentiate f using chain rule: outer = sin(u), inner = 3x", "f' = \\cos(3x) \\cdot 3 = 3\\cos(3x)", "derivative of sin is cos, then multiply by derivative of 3x which is 3"),
                step("Differentiate g using power rule", "g' = 1"),
                step("Quotient rule: (f'g − fg')/g²", "\\dfrac{3\\cos(3x) \\cdot x - \\sin(3x) \\cdot 1}{x^2}"),
                step("Simplify", "\\dfrac{3x\\cos(3x) - \\sin(3x)}{x^2}"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _implicit_differentiation():
    cases = [
        {
            "implicit": "x^2 + y^2 = r^2",
            "ans": "\\dfrac{dy}{dx} = -\\dfrac{x}{y}",
            "norm": "-x/y",
            "steps": [
                step("Differentiate both sides with respect to x", "\\dfrac{d}{dx}[x^2] + \\dfrac{d}{dx}[y^2] = 0"),
                step("d/dx[x²] = 2x by power rule", "2x"),
                step("d/dx[y²] = 2y·(dy/dx) by chain rule — y is a function of x", "2y \\cdot \\dfrac{dy}{dx}", "treat y like a composite function: d/dx[y²] = 2y · y'"),
                step("Write the full equation", "2x + 2y\\dfrac{dy}{dx} = 0"),
                step("Isolate dy/dx", "2y\\dfrac{dy}{dx} = -2x \\implies \\dfrac{dy}{dx} = -\\dfrac{x}{y}", "divide both sides by 2y"),
            ],
        },
        {
            "implicit": "x^2 + xy + y^2 = 7",
            "ans": "\\dfrac{dy}{dx} = -\\dfrac{2x+y}{x+2y}",
            "norm": "-(2x+y)/(x+2y)",
            "steps": [
                step("Differentiate every term with respect to x", "\\dfrac{d}{dx}[x^2] + \\dfrac{d}{dx}[xy] + \\dfrac{d}{dx}[y^2] = 0"),
                step("d/dx[x²] = 2x", "2x", "power rule"),
                step("d/dx[xy] = y + x·(dy/dx) by product rule", "y + x\\dfrac{dy}{dx}", "treat x and y as two separate functions multiplied together"),
                step("d/dx[y²] = 2y·(dy/dx) by chain rule", "2y\\dfrac{dy}{dx}"),
                step("Full equation after differentiation", "2x + y + x\\dfrac{dy}{dx} + 2y\\dfrac{dy}{dx} = 0"),
                step("Collect all dy/dx terms on one side", "(x + 2y)\\dfrac{dy}{dx} = -(2x+y)"),
                step("Divide both sides to isolate dy/dx", "\\dfrac{dy}{dx} = -\\dfrac{2x+y}{x+2y}"),
            ],
        },
        {
            "implicit": "\\sin(xy) = x",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{1 - y\\cos(xy)}{x\\cos(xy)}",
            "norm": "(1-y*cos(xy))/(x*cos(xy))",
            "steps": [
                step("Differentiate both sides with respect to x", "\\dfrac{d}{dx}[\\sin(xy)] = \\dfrac{d}{dx}[x]"),
                step("Left side: chain rule — outer = sin(u), inner = xy", "\\cos(xy) \\cdot \\dfrac{d}{dx}[xy]", "derivative of sin is cos, then multiply by derivative of the inside"),
                step("d/dx[xy] = y + x·(dy/dx) by product rule", "\\cos(xy) \\cdot \\left(y + x\\dfrac{dy}{dx}\\right)"),
                step("Right side: d/dx[x] = 1", "= 1"),
                step("Expand the left side", "y\\cos(xy) + x\\cos(xy)\\dfrac{dy}{dx} = 1"),
                step("Isolate dy/dx", "\\dfrac{dy}{dx} = \\dfrac{1 - y\\cos(xy)}{x\\cos(xy)}", "subtract y·cos(xy), then divide by x·cos(xy)"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=f"\\text{{Given }} {c['implicit']},\\text{{ find }} \\dfrac{{dy}}{{dx}}.", answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _log_differentiation():
    return problem(
        problem_tex="y = x^x,\\quad \\text{find } \\dfrac{dy}{dx}",
        answer_tex="x^x(\\ln x + 1)",
        answer_norm="x^x*(ln(x)+1)",
        steps=[
            step("Take ln of both sides to bring down the exponent", "\\ln y = \\ln(x^x) = x \\ln x", "log rule: ln(a^b) = b·ln(a)"),
            step("Differentiate both sides with respect to x", "\\dfrac{d}{dx}[\\ln y] = \\dfrac{d}{dx}[x \\ln x]"),
            step("Left side: chain rule — d/dx[ln(y)] = (1/y)·(dy/dx)", "\\dfrac{1}{y}\\dfrac{dy}{dx}", "y is a function of x, so use chain rule"),
            step("Right side: product rule on x·ln(x)", "1 \\cdot \\ln x + x \\cdot \\dfrac{1}{x} = \\ln x + 1", "d/dx[x]=1, d/dx[ln x]=1/x"),
            step("Equation so far", "\\dfrac{1}{y}\\dfrac{dy}{dx} = \\ln x + 1"),
            step("Multiply both sides by y to isolate dy/dx", "\\dfrac{dy}{dx} = y(\\ln x+1) = x^x(\\ln x+1)", "substitute y = x^x back in"),
        ],
    )


def _higher_order():
    cases = [
        ("\\sin x",  "f'(x) = \\cos x",   "f''(x) = -\\sin x", "-sin(x)"),
        ("\\cos x",  "f'(x) = -\\sin x",  "f''(x) = -\\cos x", "-cos(x)"),
        ("e^x",      "f'(x) = e^x",        "f''(x) = e^x",      "e^x"),
        ("x^4",      "f'(x) = 4x^3",       "f''(x) = 12x^2",    "12*x^2"),
        ("x^5",      "f'(x) = 5x^4",       "f''(x) = 20x^3",    "20*x^3"),
    ]
    f_tex, fp_tex, d2_tex, d2_norm = pick(cases)
    return problem(
        problem_tex=f"f(x) = {f_tex},\\quad \\text{{find }} f''(x).",
        answer_tex=d2_tex,
        answer_norm=d2_norm,
        steps=[
            step("First derivative: differentiate f(x) once", fp_tex),
            step("Second derivative: differentiate f'(x) again", d2_tex, "apply the same derivative rules to f'(x)"),
        ],
    )


def _y_prime_and_double_prime():
    cases = [
        {
            "prob":      "y = (2 + \\sqrt{x})^3, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = \\dfrac{3(2+\\sqrt{x})^2}{2\\sqrt{x}}",
            "ans1_norm": "3*(2+sqrt(x))^2/(2*sqrt(x))",
            "ans2_tex":  "y'' = \\dfrac{3(x-4)}{4x^{3/2}}",
            "ans2_norm": "3*(x-4)/(4*x^(3/2))",
            "steps": [
                step("Identify: outer = u^3, inner = 2 + √x",
                     "y = (2+\\sqrt{x})^3", "chain rule applies"),
                step("y′ via chain rule: 3u²·u′, where u′ = 1/(2√x)",
                     "y' = 3(2+\\sqrt{x})^2 \\cdot \\dfrac{1}{2\\sqrt{x}} = \\dfrac{3(2+\\sqrt{x})^2}{2\\sqrt{x}}"),
                step("y″: differentiate y′ with quotient/product rule, factor (2+√x)(√x−2) = x−4",
                     "y'' = \\dfrac{3(x-4)}{4x^{3/2}}"),
            ],
        },
        {
            "prob":      "y = (1 + x^2)^4, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = 8x(1+x^2)^3",
            "ans1_norm": "8*x*(1+x^2)^3",
            "ans2_tex":  "y'' = 8(1+x^2)^2(1+7x^2)",
            "ans2_norm": "8*(1+x^2)^2*(1+7*x^2)",
            "steps": [
                step("Chain rule: outer = u^4, inner = 1 + x²",
                     "y' = 4(1+x^2)^3 \\cdot 2x = 8x(1+x^2)^3"),
                step("Product rule on y′ = 8x·(1+x²)^3",
                     "y'' = 8(1+x^2)^3 + 8x \\cdot 3(1+x^2)^2 \\cdot 2x"),
                step("Factor (1+x²)²",
                     "y'' = 8(1+x^2)^2[(1+x^2)+6x^2] = 8(1+x^2)^2(1+7x^2)"),
            ],
        },
        {
            "prob":      "y = \\sin^2(x), \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = 2\\sin(x)\\cos(x)",
            "ans1_norm": "2*sin(x)*cos(x)",
            "ans2_tex":  "y'' = 2\\cos(2x)",
            "ans2_norm": "2*cos(2x)",
            "steps": [
                step("Chain rule: outer = u², inner = sin(x)",
                     "y' = 2\\sin x\\cos x", "also equals sin(2x)"),
                step("Rewrite y′ = sin(2x), then chain rule",
                     "y'' = \\cos(2x) \\cdot 2 = 2\\cos(2x)"),
            ],
        },
        {
            "prob":      "y = xe^x, \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = e^x(1+x)",
            "ans1_norm": "e^x*(1+x)",
            "ans2_tex":  "y'' = e^x(2+x)",
            "ans2_norm": "e^x*(2+x)",
            "steps": [
                step("Product rule: f = x, g = e^x",
                     "y' = e^x + xe^x = e^x(1+x)", "f′=1, g′=e^x"),
                step("Product rule on y′ = e^x(1+x)",
                     "y'' = e^x(1+x) + e^x = e^x(2+x)"),
            ],
        },
        {
            "prob":      "y = \\ln(x^2), \\quad \\text{find } y' \\text{ and } y''",
            "ans1_tex":  "y' = \\dfrac{2}{x}",
            "ans1_norm": "2/x",
            "ans2_tex":  "y'' = -\\dfrac{2}{x^2}",
            "ans2_norm": "-2/x^2",
            "steps": [
                step("Simplify: ln(x²) = 2ln(x), differentiate",
                     "y' = \\dfrac{2}{x}", "or chain rule gives same result"),
                step("Power rule on y′ = 2x^{−1}",
                     "y'' = -2x^{-2} = -\\dfrac{2}{x^2}"),
            ],
        },
    ]
    c = pick(cases)
    return dual_problem(
        problem_tex=c["prob"],
        answer1_tex=c["ans1_tex"],
        answer1_norm=c["ans1_norm"],
        answer2_tex=c["ans2_tex"],
        answer2_norm=c["ans2_norm"],
        steps=c["steps"],
    )


diff3 = [_chain_nested, _product_chain, _quotient_chain, _implicit_differentiation, _log_differentiation, _higher_order, _y_prime_and_double_prime]

# ── diff4 — multi-rule combos ─────────────────────────────────────────────────

def _all_three_rules():
    cases = [
        {
            "prob": "\\dfrac{x^2 \\sin x}{e^x}",
            "ans": "\\dfrac{x(2\\sin x + x\\cos x - x\\sin x)}{e^x}",
            "norm": "x*(2*sin(x)+x*cos(x)-x*sin(x))/e^x",
            "steps": [
                step("Structure: quotient — numerator is x²·sin(x), denominator is e^x", "f = x^2\\sin x, \\quad g = e^x"),
                step("Differentiate numerator f using product rule", "f' = 2x\\sin x + x^2\\cos x", "d/dx[x²]=2x, d/dx[sin x]=cos x"),
                step("Differentiate denominator g", "g' = e^x", "e^x is its own derivative"),
                step("Apply quotient rule: (f'g − fg')/g²", "\\dfrac{(2x\\sin x + x^2\\cos x)e^x - x^2\\sin x \\cdot e^x}{e^{2x}}"),
                step("Factor e^x from numerator and cancel with e^(2x)", "\\dfrac{e^x(2x\\sin x + x^2\\cos x - x^2\\sin x)}{e^{2x}} = \\dfrac{2x\\sin x + x^2\\cos x - x^2\\sin x}{e^x}"),
                step("Factor x from numerator", "\\dfrac{x(2\\sin x + x\\cos x - x\\sin x)}{e^x}"),
            ],
        },
        {
            "prob": "x^2 e^{\\sin x}",
            "ans": "xe^{\\sin x}(2 + x\\cos x)",
            "norm": "x*e^(sin(x))*(2+x*cos(x))",
            "steps": [
                step("Structure: product — f = x², g = e^(sin x)", "f = x^2, \\quad g = e^{\\sin x}"),
                step("Differentiate f using power rule", "f' = 2x"),
                step("Differentiate g using chain rule: outer = e^u, inner = sin(x)", "g' = e^{\\sin x} \\cdot \\cos x", "d/dx[e^u] = e^u · u', here u = sin(x), u' = cos(x)"),
                step("Apply product rule: f'g + fg'", "2x \\cdot e^{\\sin x} + x^2 \\cdot e^{\\sin x}\\cos x"),
                step("Factor x·e^(sin x) from both terms", "xe^{\\sin x}(2 + x\\cos x)"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _implicit_second_order():
    return problem(
        problem_tex="x^2 + y^2 = 25,\\quad \\text{find } \\dfrac{d^2y}{dx^2}",
        answer_tex="-\\dfrac{25}{y^3}",
        answer_norm="-25/y^3",
        steps=[
            step("Step 1 — find dy/dx by implicit differentiation", "2x + 2y\\dfrac{dy}{dx} = 0 \\implies \\dfrac{dy}{dx} = -\\dfrac{x}{y}", "differentiate both sides, solve for dy/dx"),
            step("Step 2 — differentiate dy/dx again using quotient rule", "\\dfrac{d^2y}{dx^2} = \\dfrac{d}{dx}\\!\\left[-\\dfrac{x}{y}\\right] = -\\dfrac{y \\cdot 1 - x \\cdot \\frac{dy}{dx}}{y^2}", "numerator: f=x (f'=1), denominator: g=y (g'=dy/dx)"),
            step("Substitute dy/dx = −x/y into the expression", "-\\dfrac{y - x(-x/y)}{y^2} = -\\dfrac{y + x^2/y}{y^2}"),
            step("Multiply numerator and denominator by y", "-\\dfrac{y^2 + x^2}{y^3}"),
            step("Use the original equation: x² + y² = 25", "-\\dfrac{25}{y^3}", "substitute the constraint to simplify"),
        ],
    )


def _log_diff_complex():
    return problem(
        problem_tex="y = \\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}},\\quad \\text{find } \\dfrac{dy}{dx}",
        answer_tex="y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x - \\dfrac{1}{2(x+2)}\\right]",
        answer_norm="y*(6x/(x^2+1)+cot(x)-1/(2(x+2)))",
        steps=[
            step("Take ln of both sides — products become sums, powers come down", "\\ln y = \\ln(x^2+1)^3 + \\ln(\\sin x) - \\ln\\sqrt{x+2}", "log rules: ln(ab)=ln a+ln b, ln(a/b)=ln a−ln b"),
            step("Simplify each log using power rules", "\\ln y = 3\\ln(x^2+1) + \\ln(\\sin x) - \\tfrac{1}{2}\\ln(x+2)", "ln(a^n) = n·ln(a), ln(√a) = (1/2)ln(a)"),
            step("Differentiate both sides", "\\dfrac{1}{y}\\dfrac{dy}{dx} = \\dfrac{d}{dx}\\left[3\\ln(x^2+1)\\right] + \\dfrac{d}{dx}[\\ln(\\sin x)] - \\dfrac{d}{dx}\\left[\\tfrac{1}{2}\\ln(x+2)\\right]", "left side: chain rule on ln(y)"),
            step("Differentiate each term (chain rule each time)", "\\dfrac{1}{y}y' = \\dfrac{3 \\cdot 2x}{x^2+1} + \\dfrac{\\cos x}{\\sin x} - \\dfrac{1}{2(x+2)}", "d/dx[ln(u)] = u'/u for each term"),
            step("Multiply both sides by y", "y' = y\\!\\left[\\dfrac{6x}{x^2+1}+\\cot x-\\dfrac{1}{2(x+2)}\\right]", "leave y as-is — substituting back the full fraction would be messy"),
        ],
    )


diff4 = [_all_three_rules, _all_three_rules, _implicit_second_order, _log_diff_complex]

# ── diff5 — parametric, inverse trig ─────────────────────────────────────────

def _parametric_derivative():
    cases = [
        {
            "prob": "x=t^2,\\; y=t^3",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{3t^2}{2t} = \\dfrac{3t}{2}",
            "norm": "3t/2",
            "steps": [
                step("Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "\\text{differentiate x and y each with respect to t, then divide}"),
                step("Differentiate x with respect to t", "\\dfrac{dx}{dt} = 2t", "power rule"),
                step("Differentiate y with respect to t", "\\dfrac{dy}{dt} = 3t^2", "power rule"),
                step("Divide dy/dt by dx/dt", "\\dfrac{dy}{dx} = \\dfrac{3t^2}{2t}"),
                step("Simplify by cancelling t", "\\dfrac{3t}{2}"),
            ],
        },
        {
            "prob": "x=\\cos t,\\; y=\\sin t",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{\\cos t}{-\\sin t} = -\\cot t",
            "norm": "-cot(t)",
            "steps": [
                step("Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "\\text{differentiate x and y each with respect to t, then divide}"),
                step("Differentiate x with respect to t", "\\dfrac{dx}{dt} = -\\sin t", "d/dt[cos t] = −sin t"),
                step("Differentiate y with respect to t", "\\dfrac{dy}{dt} = \\cos t", "d/dt[sin t] = cos t"),
                step("Divide dy/dt by dx/dt", "\\dfrac{dy}{dx} = \\dfrac{\\cos t}{-\\sin t}"),
                step("Simplify: cos/sin = cot", "-\\cot t", "negative because of the minus sign in dx/dt"),
            ],
        },
        {
            "prob": "x=e^t,\\; y=t^2",
            "ans": "\\dfrac{dy}{dx} = \\dfrac{2t}{e^t}",
            "norm": "2t/e^t",
            "steps": [
                step("Parametric formula: dy/dx = (dy/dt) ÷ (dx/dt)", "\\text{differentiate x and y each with respect to t, then divide}"),
                step("Differentiate x with respect to t", "\\dfrac{dx}{dt} = e^t", "e^t is its own derivative"),
                step("Differentiate y with respect to t", "\\dfrac{dy}{dt} = 2t", "power rule"),
                step("Divide dy/dt by dx/dt", "\\dfrac{dy}{dx} = \\dfrac{2t}{e^t}"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=f"\\text{{Parametric: }} {c['prob']}\\quad \\text{{Find }} dy/dx.", answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _inverse_trig_chain():
    cases = [
        {
            "prob": "\\arcsin(\\sqrt{x})",
            "ans": "\\dfrac{1}{2\\sqrt{x}\\sqrt{1-x}} = \\dfrac{1}{2\\sqrt{x-x^2}}",
            "norm": "1/(2*sqrt(x-x^2))",
            "steps": [
                step("Formula: d/dx[arcsin(u)] = u' / √(1 − u²)", "\\text{identify } u = \\sqrt{x}"),
                step("Find u': differentiate u = √x = x^(1/2)", "u' = \\dfrac{1}{2\\sqrt{x}}", "power rule: d/dx[x^(1/2)] = (1/2)x^(-1/2) = 1/(2√x)"),
                step("Compute 1 − u²", "1 - (\\sqrt{x})^2 = 1 - x"),
                step("Substitute into the formula", "\\dfrac{u'}{\\sqrt{1-u^2}} = \\dfrac{1/(2\\sqrt{x})}{\\sqrt{1-x}}"),
                step("Simplify", "\\dfrac{1}{2\\sqrt{x}\\sqrt{1-x}} = \\dfrac{1}{2\\sqrt{x-x^2}}", "√x · √(1-x) = √(x(1-x)) = √(x-x²)"),
            ],
        },
        {
            "prob": "\\arctan(x^2)",
            "ans": "\\dfrac{2x}{1+x^4}",
            "norm": "2x/(1+x^4)",
            "steps": [
                step("Formula: d/dx[arctan(u)] = u' / (1 + u²)", "\\text{identify } u = x^2"),
                step("Find u': differentiate u = x²", "u' = 2x", "power rule"),
                step("Compute 1 + u²", "1 + (x^2)^2 = 1 + x^4"),
                step("Substitute into the formula", "\\dfrac{2x}{1+x^4}"),
            ],
        },
        {
            "prob": "\\arccos(2x)",
            "ans": "\\dfrac{-2}{\\sqrt{1-4x^2}}",
            "norm": "-2/sqrt(1-4x^2)",
            "steps": [
                step("Formula: d/dx[arccos(u)] = −u' / √(1 − u²)", "\\text{identify } u = 2x", "note the negative sign — arccos derivative is negative arcsin derivative"),
                step("Find u': differentiate u = 2x", "u' = 2"),
                step("Compute 1 − u²", "1 - (2x)^2 = 1 - 4x^2"),
                step("Substitute into the formula", "\\dfrac{-2}{\\sqrt{1-4x^2}}"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


def _full_combo():
    cases = [
        {
            "prob": "x^2 \\arctan(x)",
            "ans": "2x\\arctan(x) + \\dfrac{x^2}{1+x^2}",
            "norm": "2x*arctan(x)+x^2/(1+x^2)",
            "steps": [
                step("Structure: product — f = x², g = arctan(x)", "f = x^2, \\quad g = \\arctan(x)"),
                step("Differentiate f", "f' = 2x", "power rule"),
                step("Differentiate g using inverse trig formula", "g' = \\dfrac{1}{1+x^2}", "d/dx[arctan(u)] = u'/(1+u²), here u=x, u'=1"),
                step("Apply product rule: f'g + fg'", "2x \\cdot \\arctan(x) + x^2 \\cdot \\dfrac{1}{1+x^2}"),
                step("Simplify", "2x\\arctan(x) + \\dfrac{x^2}{1+x^2}"),
            ],
        },
        {
            "prob": "e^x \\ln(x^2+1)",
            "ans": "e^x\\ln(x^2+1)+\\dfrac{2xe^x}{x^2+1}",
            "norm": "e^x*ln(x^2+1)+2x*e^x/(x^2+1)",
            "steps": [
                step("Structure: product — f = e^x, g = ln(x²+1)", "f = e^x, \\quad g = \\ln(x^2+1)"),
                step("Differentiate f", "f' = e^x", "e^x is its own derivative"),
                step("Differentiate g using chain rule: d/dx[ln(u)] = u'/u", "g' = \\dfrac{2x}{x^2+1}", "u = x²+1, u' = 2x"),
                step("Apply product rule: f'g + fg'", "e^x \\cdot \\ln(x^2+1) + e^x \\cdot \\dfrac{2x}{x^2+1}"),
                step("Simplify", "e^x\\ln(x^2+1) + \\dfrac{2xe^x}{x^2+1}"),
            ],
        },
        {
            "prob": "\\sin^2(\\cos(x))",
            "ans": "2\\sin(\\cos x)\\cos(\\cos x)\\cdot(-\\sin x)",
            "norm": "2*sin(cos(x))*cos(cos(x))*(-sin(x))",
            "steps": [
                step("Three nested layers: [sin(cos(x))]²", "\\text{outermost} = u^2, \\quad u = \\sin(\\cos x)"),
                step("Layer 1 — d/dx[u²] = 2u, keep u = sin(cos x) intact", "2\\sin(\\cos x)", "power rule on the outermost square"),
                step("Layer 2 — d/dx[sin(cos x)] = cos(cos x), keep cos(x) inside", "\\cdot \\cos(\\cos x)", "derivative of sin is cos, leave inner cos(x) unchanged"),
                step("Layer 3 — d/dx[cos(x)] = −sin(x)", "\\cdot (-\\sin x)"),
                step("Multiply all three layers", "2\\sin(\\cos x) \\cdot \\cos(\\cos x) \\cdot (-\\sin x)"),
            ],
        },
    ]
    c = pick(cases)
    return problem(problem_tex=_d_tex(c["prob"]), answer_tex=c["ans"], answer_norm=c["norm"], steps=c["steps"])


diff5 = [_parametric_derivative, _inverse_trig_chain, _full_combo, _full_combo]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}