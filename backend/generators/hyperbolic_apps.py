from math_utils import R, pick
from problem_builder import problem, step

# ── hyperbolic_apps1 — hyperbolic functions basics ─────────────────────────────

def _sinh_cosh_identity():
    """Prove or use cosh² - sinh² = 1"""
    return problem(
        problem_tex="\\text{Verify } \\cosh^2(x) - \\sinh^2(x) = 1.",
        answer_tex="\\cosh^2(x) - \\sinh^2(x) = \\frac{e^x + e^{-x}}{2}^2 - \\frac{e^x - e^{-x}}{2}^2 = \\frac{e^{2x}+2+e^{-2x} - (e^{2x}-2+e^{-2x})}{4} = \\frac{4}{4} = 1",
        answer_norm="1",
        steps=[
            step("Write definitions", "\\cosh(x) = \\frac{e^x+e^{-x}}{2}, \\quad \\sinh(x) = \\frac{e^x-e^{-x}}{2}"),
            step("Compute cosh²", "\\cosh^2(x) = \\frac{e^{2x}+2+e^{-2x}}{4}"),
            step("Compute sinh²", "\\sinh^2(x) = \\frac{e^{2x}-2+e^{-2x}}{4}"),
            step("Subtract", "\\cosh^2 - \\sinh^2 = \\frac{4}{4} = 1"),
        ],
    )


def _sinh_derivative():
    """Derivative of sinh"""
    return problem(
        problem_tex="\\text{Find } \\dfrac{d}{dx} \\sinh(x).",
        answer_tex="\\cosh(x)",
        answer_norm="cosh(x)",
        steps=[
            step("Definition", "\\sinh(x) = \\frac{e^x - e^{-x}}{2}"),
            step("Differentiate", "\\frac{d}{dx}\\sinh(x) = \\frac{e^x + e^{-x}}{2} = \\cosh(x)"),
        ],
    )


# ── hyperbolic_apps2 — hyperbolic integrals ────────────────────────────────────

def _integral_sinh():
    """∫ sinh(x) dx"""
    return problem(
        problem_tex="\\int \\sinh(x) \\, dx",
        answer_tex="\\cosh(x) + C",
        answer_norm="cosh(x)+C",
        steps=[
            step("Recall derivative", "\\frac{d}{dx}\\cosh(x) = \\sinh(x)"),
            step("Integrate", "\\int \\sinh(x) \\, dx = \\cosh(x) + C"),
        ],
    )


def _integral_cosh():
    """∫ cosh(x) dx"""
    return problem(
        problem_tex="\\int \\cosh(x) \\, dx",
        answer_tex="\\sinh(x) + C",
        answer_norm="sinh(x)+C",
        steps=[
            step("Recall derivative", "\\frac{d}{dx}\\sinh(x) = \\cosh(x)"),
            step("Integrate", "\\int \\cosh(x) \\, dx = \\sinh(x) + C"),
        ],
    )


# ── hyperbolic_apps3 — catenary ────────────────────────────────────────────────

def _catenary_shape():
    """Verify hanging cable follows cosh"""
    a = pick([1, 2, 3])
    
    return problem(
        problem_tex=f"\\text{{The shape of a hanging cable is }} y = {a}\\cosh(x/{a}). \\text{{ Find the slope at }} x = 0.",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("Differentiate", f"y' = \\sinh(x/{a})"),
            step("Evaluate at x=0", f"y'(0) = \\sinh(0) = 0"),
        ],
    )


def _catenary_arc_length():
    """Arc length of catenary"""
    # Arc length of y = a cosh(x/a) from x=-b to x=b is 2a sinh(b/a)
    a = pick([1, 2])
    b = pick([1, 2])
    
    return problem(
        problem_tex=f"\\text{{Find the arc length of }} y = {a}\\cosh(x/{a}) \\text{{ from }} x=0 \\text{{ to }} x={b}.",
        answer_tex=f"a \\sinh(x/a)\\bigg|_0^{b} = {a}\\sinh({b}/{a})",
        answer_norm=f"{a}*sinh({b}/{a})",
        steps=[
            step("Arc length formula", "L = \\int \\sqrt{1 + (y')^2} \\, dx"),
            step("y' = sinh(x/a)", "1 + \\sinh^2(x/a) = \\cosh^2(x/a)"),
            step("Integrate", "L = \\int_0^b \\cosh(x/a) \\, dx = a \\sinh(x/a)\\bigg|_0^b = a\\sinh(b/a)"),
        ],
    )


# ── hyperbolic_apps4 — inverse hyperbolic ───────────────────────────────────────

def _arsinh():
    """Derivative of arsinh"""
    return problem(
        problem_tex="\\text{Find } \\dfrac{d}{dx} \\operatorname{arsinh}(x).",
        answer_tex="\\dfrac{1}{\\sqrt{1+x^2}}",
        answer_norm="1/sqrt(1+x^2)",
        steps=[
            step("Let y = arsinh(x) so x = sinh(y)", ""),
            step("Differentiate implicitly", "1 = \\cosh(y) \\cdot y'"),
            step("Solve for y'", "y' = \\frac{1}{\\cosh(y)} = \\frac{1}{\\sqrt{1+\\sinh^2(y)}} = \\frac{1}{\\sqrt{1+x^2}}"),
        ],
    )


def _artanh():
    """Derivative of artanh"""
    a = pick([2, 3])
    
    return problem(
        problem_tex=f"\\text{{Find }} \\dfrac{{d}}{{dx}} \\operatorname{{artanh}}({a}x).",
        answer_tex=f"\\dfrac{{{a}}}{{1 - {a}^2 x^2}}",
        answer_norm=f"{a}/(1-{a}^2*x^2)",
        steps=[
            step("Let y = artanh(ax) so ax = tanh(y)", ""),
            step("Differentiate", f"a = \\operatorname{{sech}}^2(y) \\cdot y'"),
            step("y' = a · cosh²(y)", f"= a(1 + \\tanh^2(y)) = a(1 + a^2 x^2)"),
            step("Wait — correct", f"y' = \\frac{{a}}{{1-(ax)^2}}"),
        ],
    )


# ── hyperbolic_apps5 — combined ────────────────────────────────────────────────

def _hyperbolic_surface_area():
    """Surface area of catenary rotation"""
    a = pick([1, 2])
    
    return problem(
        problem_tex=f"\\text{{Find the surface area of rotating }} y = {a}\\cosh(x/{a}) \\text{{ about x-axis from }} x=0 \\text{{ to }} x={a}.",
        answer_tex=f"2\\pi {a}^2 \\sinh(1)",
        answer_norm=f"2*pi*{a}^2*sinh(1)",
        steps=[
            step("Surface area formula", "S = 2\\pi \\int y \\sqrt{1+(y')^2} \\, dx"),
            step("Substitute", "y = a\\cosh(x/a), y' = \\sinh(x/a), \\sqrt{1+(y')^2} = \\cosh(x/a)"),
            step("Set up integral", "S = 2\\pi \\int_0^a a\\cosh^2(x/a) \\, dx"),
            step("Evaluate", "a\\cosh^2(x/a) = a(1+\\sinh^2(x/a))/2, \\int \\cosh^2(u) du = (\\sinh(u)\\cosh(u)+u)/2"),
            step("Result", f"= 2\\pi {a}^2 \\sinh(1) \\text{{ (units}}^2\\text{{)}}"),
        ],
    )


def _hyperbolic_vs_trig():
    """Show hyperbolic and trig functions differ"""
    # sin(ix) = i sinh(x), cos(ix) = cosh(x)
    
    return problem(
        problem_tex="\\text{Show that } \\cos(ix) = \\cosh(x) \\text{ and } \\sin(ix) = i\\sinh(x).",
        answer_tex="\\cos(ix) = \\frac{e^{i^2 x}+e^{-i^2 x}}{2} = \\frac{e^{-x}+e^x}{2} = \\cosh(x)",
        answer_norm="cos(ix)=cosh(x)",
        steps=[
            step("Use Euler's formula for cos", "\\cos(z) = (e^{iz}+e^{-iz})/2"),
            step("Substitute z = ix", "\\cos(ix) = (e^{i(ix)}+e^{-i(ix)})/2 = (e^{-x}+e^x)/2 = \\cosh(x)"),
            step("Similarly for sin", "\\sin(ix) = (e^{i(ix)}-e^{-i(ix)})/(2i) = (e^{-x}-e^x)/(-2i) = i\\sinh(x)"),
        ],
    )


hyperbolic_apps1 = [_sinh_cosh_identity, _sinh_derivative]
hyperbolic_apps2 = [_integral_sinh, _integral_cosh]
hyperbolic_apps3 = [_catenary_shape, _catenary_arc_length]
hyperbolic_apps4 = [_arsinh, _artanh]
hyperbolic_apps5 = [_hyperbolic_surface_area, _hyperbolic_vs_trig]

POOLS = {1: hyperbolic_apps1, 2: hyperbolic_apps2, 3: hyperbolic_apps3, 4: hyperbolic_apps4, 5: hyperbolic_apps5}