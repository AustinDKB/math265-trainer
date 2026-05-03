from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── incdec1 — increasing from derivative ──────────────────────────────────────

def _increasing_from_derivative():
    """Given f'(x) as factored polynomial, find where f is increasing (f' > 0)"""
    a = R(-3, -1)
    b = R(1, 4)
    
    # f'(x) = (x - a)(x - b), parabola opening up
    # f' > 0 when x < a or x > b
    
    a_tex = f"x - ({a})" if a < 0 else f"x - {a}"
    b_tex = f"x - {b}"
    
    return problem(
        problem_tex=f"f'(x) = {a_tex}({b_tex}). \\text{{ Find where }} f(x) \\text{{ is increasing.}}",
        answer_tex=f"(-\\infty, {a}) \\cup ({b}, \\infty)",
        answer_norm=f"(-inf,{a})U({b},inf)",
        steps=[
            step("Find critical points", f"f'(x) = 0 \\implies x = {a}, {b}"),
            step("Test intervals", f"\\text{{Intervals: }} (-\\infty, {a}), ({a}, {b}), ({b}, \\infty)"),
            step("Sign analysis", f"f' > 0 \\text{{ on }} (-\\infty, {a}) \\cup ({b}, \\infty) \\text{{ (parabola opens up)}}"),
            step("Conclusion", f"f \\text{{ is increasing on }} (-\\infty, {a}) \\cup ({b}, \\infty)"),
        ],
    )


def _decreasing_from_derivative():
    """Given f'(x), find where f is decreasing (f' < 0)"""
    a = R(-2, -1)
    b = R(2, 4)
    
    a_tex = f"x + {-a}" if a < 0 else f"x - {a}"
    b_tex = f"x - {b}"
    
    return problem(
        problem_tex=f"f'(x) = {a_tex}({b_tex}). \\text{{ Find where }} f(x) \\text{{ is decreasing.}}",
        answer_tex=f"({a}, {b})",
        answer_norm=f"({a},{b})",
        steps=[
            step("Find critical points", f"f'(x) = 0 \\implies x = {a}, {b}"),
            step("Test intervals", f"\\text{{Intervals: }} (-\\infty, {a}), ({a}, {b}), ({b}, \\infty)"),
            step("Sign analysis", f"f' < 0 \\text{{ on }} ({a}, {b}) \\text{{ (between roots, parabola opens up)}}"),
            step("Conclusion", f"f \\text{{ is decreasing on }} ({a}, {b})"),
        ],
    )


# ── incdec2 — from f(x) polynomial ────────────────────────────────────────────

def _increasing_from_function():
    """Given f(x) polynomial, find increasing intervals (requires differentiation first)"""
    # f(x) = x³ - 3x² - 9x + 5
    # f'(x) = 3x² - 6x - 9 = 3(x+1)(x-3)
    # f' > 0 when x < -1 or x > 3
    
    return problem(
        problem_tex="f(x) = x^3 - 3x^2 - 9x + 5. \\text{ Find where } f(x) \\text{ is increasing.}",
        answer_tex="(-\\infty, -1) \\cup (3, \\infty)",
        answer_norm="(-inf,-1)U(3,inf)",
        steps=[
            step("Differentiate", "f'(x) = 3x^2 - 6x - 9"),
            step("Factor", "f'(x) = 3(x^2 - 2x - 3) = 3(x+1)(x-3)"),
            step("Find critical points", "f'(x) = 0 \\implies x = -1, 3"),
            step("Sign chart", "f' > 0 \\text{ on } (-\\infty, -1) \\cup (3, \\infty)"),
            step("Conclusion", "f \\text{ is increasing on } (-\\infty, -1) \\cup (3, \\infty)"),
        ],
    )


def _decreasing_from_function():
    """Given f(x), find decreasing intervals"""
    # f(x) = x³ - 6x² + 9x + 2
    # f'(x) = 3x² - 12x + 9 = 3(x-1)(x-3)
    # f' < 0 when 1 < x < 3
    
    return problem(
        problem_tex="f(x) = x^3 - 6x^2 + 9x + 2. \\text{ Find where } f(x) \\text{ is decreasing.}",
        answer_tex="(1, 3)",
        answer_norm="(1,3)",
        steps=[
            step("Differentiate", "f'(x) = 3x^2 - 12x + 9"),
            step("Factor", "f'(x) = 3(x^2 - 4x + 3) = 3(x-1)(x-3)"),
            step("Find critical points", "f'(x) = 0 \\implies x = 1, 3"),
            step("Sign chart", "f' < 0 \\text{ on } (1, 3)"),
            step("Conclusion", "f \\text{ is decreasing on } (1, 3)"),
        ],
    )


# ── incdec3 — critical points + classification ────────────────────────────────

def _find_critical_points():
    """Find all critical points of a function"""
    cases = [
        {
            "f": "x^3 - 3x^2 + 1",
            "f_prime": "3x^2 - 6x = 3x(x-2)",
            "critical": "x = 0, \\quad x = 2",
            "norm": "0,2",
            "steps": [
                step("Differentiate", "f'(x) = 3x^2 - 6x"),
                step("Factor", "f'(x) = 3x(x-2)"),
                step("Set to zero", "3x(x-2) = 0"),
                step("Solve", "x = 0, \\quad x = 2"),
            ],
        },
        {
            "f": "x^4 - 4x^3",
            "f_prime": "4x^3 - 12x^2 = 4x^2(x-3)",
            "critical": "x = 0, \\quad x = 3",
            "norm": "0,3",
            "steps": [
                step("Differentiate", "f'(x) = 4x^3 - 12x^2"),
                step("Factor", "f'(x) = 4x^2(x-3)"),
                step("Set to zero", "4x^2(x-3) = 0"),
                step("Solve", "x = 0 \\text{ (multiplicity 2)}, \\quad x = 3"),
            ],
        },
    ]
    c = pick(cases)
    f_str = c["f"]
    return problem(
        problem_tex="f(x) = " + f_str + ". \\text{ Find all critical points.}",
        answer_tex=c["critical"],
        answer_norm=c["norm"],
        steps=c["steps"],
    )


def _classify_intervals():
    """Given f(x), classify all intervals as increasing or decreasing"""
    # f(x) = x³ - 3x² - 9x + 5
    # f'(x) = 3(x+1)(x-3)
    # Inc: (-∞,-1) ∪ (3,∞); Dec: (-1,3)
    
    return problem(
        problem_tex="f(x) = x^3 - 3x^2 - 9x + 5. \\text{ Find all intervals where } f \\text{ is increasing or decreasing.}",
        answer_tex="\\text{Increasing: } (-\\infty, -1) \\cup (3, \\infty); \\quad \\text{Decreasing: } (-1, 3)",
        answer_norm="inc:(-inf,-1)U(3,inf);dec:(-1,3)",
        steps=[
            step("Differentiate", "f'(x) = 3x^2 - 6x - 9 = 3(x+1)(x-3)"),
            step("Critical points", "x = -1, \\quad x = 3"),
            step("Test intervals", "(-\\infty, -1): f' > 0; \\quad (-1, 3): f' < 0; \\quad (3, \\infty): f' > 0"),
            step("Increasing", "(-\\infty, -1) \\cup (3, \\infty)"),
            step("Decreasing", "(-1, 3)"),
        ],
    )


# ── incdec4 — rational functions ──────────────────────────────────────────────

def _increasing_rational():
    """Increasing/decreasing for rational functions"""
    # f(x) = 1/(x²+1)
    # f'(x) = -2x/(x²+1)²
    # f' > 0 when x < 0; f' < 0 when x > 0
    
    return problem(
        problem_tex="f(x) = \\dfrac{1}{x^2 + 1}. \\text{ Find where } f(x) \\text{ is increasing.}",
        answer_tex="(-\\infty, 0)",
        answer_norm="(-inf,0)",
        steps=[
            step("Differentiate (quotient or chain rule)", "f'(x) = \\dfrac{-2x}{(x^2+1)^2}"),
            step("Find critical points", "f'(x) = 0 \\implies -2x = 0 \\implies x = 0"),
            step("Sign analysis", "f' > 0 \\text{ when } x < 0; \\quad f' < 0 \\text{ when } x > 0"),
            step("Conclusion", "f \\text{ is increasing on } (-\\infty, 0)"),
        ],
    )


def _increasing_exponential():
    """Increasing/decreasing for exponential functions"""
    # f(x) = xe^(-x)
    # f'(x) = e^(-x) - xe^(-x) = e^(-x)(1-x)
    # f' > 0 when x < 1
    
    return problem(
        problem_tex="f(x) = x e^{-x}. \\text{ Find where } f(x) \\text{ is increasing.}",
        answer_tex="(-\\infty, 1)",
        answer_norm="(-inf,1)",
        steps=[
            step("Differentiate (product rule)", "f'(x) = e^{-x} + x(-e^{-x}) = e^{-x}(1-x)"),
            step("Find critical points", "f'(x) = 0 \\implies 1-x = 0 \\implies x = 1"),
            step("Sign analysis", "e^{-x} > 0 \\text{ always}; \\quad 1-x > 0 \\text{ when } x < 1"),
            step("Conclusion", "f \\text{ is increasing on } (-\\infty, 1)"),
        ],
    )


# ── incdec5 — combined analysis ───────────────────────────────────────────────

def _full_interval_analysis():
    """Complete increasing/decreasing analysis with multiple critical points"""
    # f(x) = x⁴ - 4x³ + 2
    # f'(x) = 4x³ - 12x² = 4x²(x-3)
    # Inc: (3,∞); Dec: (-∞,0) ∪ (0,3)
    
    return problem(
        problem_tex="f(x) = x^4 - 4x^3 + 2. \\text{ Find all intervals where } f \\text{ is increasing or decreasing.}",
        answer_tex="\\text{Increasing: } (3, \\infty); \\quad \\text{Decreasing: } (-\\infty, 0) \\cup (0, 3)",
        answer_norm="inc:(3,inf);dec:(-inf,0)U(0,3)",
        steps=[
            step("Differentiate", "f'(x) = 4x^3 - 12x^2 = 4x^2(x-3)"),
            step("Critical points", "x = 0 \\text{ (multiplicity 2)}, \\quad x = 3"),
            step("Test intervals", "(-\\infty, 0): f' < 0; \\quad (0, 3): f' < 0; \\quad (3, \\infty): f' > 0"),
            step("Note", "x = 0 \\text{ is a critical point but } f' \\text{ doesn't change sign}"),
            step("Increasing", "(3, \\infty)"),
            step("Decreasing", "(-\\infty, 0) \\cup (0, 3)"),
        ],
    )


def _trig_increasing_decreasing():
    """Increasing/decreasing for trig functions on a given interval"""
    # f(x) = sin(x) on [0, 2π]
    # f'(x) = cos(x)
    # f' > 0 on (0, π/2) ∪ (3π/2, 2π); f' < 0 on (π/2, 3π/2)
    
    return problem(
        problem_tex="f(x) = \\sin(x) \\text{ on } [0, 2\\pi]. \\text{ Find where } f \\text{ is increasing.}",
        answer_tex="\\left(0, \\dfrac{\\pi}{2}\\right) \\cup \\left(\\dfrac{3\\pi}{2}, 2\\pi\\right)",
        answer_norm="(0,pi/2)U(3pi/2,2pi)",
        steps=[
            step("Differentiate", "f'(x) = \\cos(x)"),
            step("Find critical points in [0, 2π]", "\\cos(x) = 0 \\implies x = \\dfrac{\\pi}{2}, \\dfrac{3\\pi}{2}"),
            step("Test intervals", "(0, \\pi/2): \\cos > 0; \\quad (\\pi/2, 3\\pi/2): \\cos < 0; \\quad (3\\pi/2, 2\\pi): \\cos > 0"),
            step("Conclusion", "f \\text{ is increasing on } (0, \\pi/2) \\cup (3\\pi/2, 2\\pi)"),
        ],
    )


incdec1 = [_increasing_from_derivative, _decreasing_from_derivative]
incdec2 = [_increasing_from_function, _decreasing_from_function]
incdec3 = [_find_critical_points, _classify_intervals]
incdec4 = [_increasing_rational, _increasing_exponential]
incdec5 = [_full_interval_analysis, _trig_increasing_decreasing]

POOLS = {1: incdec1, 2: incdec2, 3: incdec3, 4: incdec4, 5: incdec5}
