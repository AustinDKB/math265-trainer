from math_utils import R, pick, sign_str
from problem_builder import problem, dual_problem, step

# ── extrema1 — local extrema from f'(x) ───────────────────────────────────────

def _local_extrema_first_derivative():
    """Find local max/min using first derivative test"""
    # f'(x) = (x+2)(x-1)(x-4)
    # Critical points: x = -2, 1, 4
    # Sign changes: + to - at -2 (local max), - to + at 1 (local min), + to - at 4 (local max)
    
    return problem(
        problem_tex="f'(x) = (x+2)(x-1)(x-4). \\text{ Classify each critical point as local max, local min, or neither.}",
        answer_tex="x = -2: \\text{local max}; \\quad x = 1: \\text{local min}; \\quad x = 4: \\text{local max}",
        answer_norm="x=-2:local_max;x=1:local_min;x=4:local_max",
        steps=[
            step("Critical points", "x = -2, \\quad x = 1, \\quad x = 4"),
            step("Test intervals", "(-\\infty, -2): f' > 0; \\quad (-2, 1): f' < 0; \\quad (1, 4): f' > 0; \\quad (4, \\infty): f' < 0"),
            step("First derivative test at x=-2", "f' \\text{ changes from + to -} \\implies \\text{local max}"),
            step("First derivative test at x=1", "f' \\text{ changes from - to +} \\implies \\text{local min}"),
            step("First derivative test at x=4", "f' \\text{ changes from + to -} \\implies \\text{local max}"),
        ],
    )


def _local_extrema_from_graph():
    """Identify local extrema from derivative sign chart description"""
    cases = [
        {
            "description": "f'(x) > 0 \\text{ on } (-\\infty, -3), \\quad f'(x) < 0 \\text{ on } (-3, 2), \\quad f'(x) > 0 \\text{ on } (2, \\infty)",
            "answer": "x = -3: \\text{local max}; \\quad x = 2: \\text{local min}",
            "norm": "x=-3:local_max;x=2:local_min",
            "steps": [
                step("At x=-3", "f' \\text{ changes from + to -} \\implies \\text{local max}"),
                step("At x=2", "f' \\text{ changes from - to +} \\implies \\text{local min}"),
            ],
        },
    ]
    c = pick(cases)
    
    return problem(
        problem_tex=f"\\text{{Given: }} {c['description']}. \\text{{ Classify the critical points.}}",
        answer_tex=c["answer"],
        answer_norm=c["norm"],
        steps=c["steps"],
    )


# ── extrema2 — absolute extrema on closed interval ────────────────────────────

def _absolute_extrema_closed_interval():
    """Find absolute max/min on [a, b] — evaluate at critical points and endpoints"""
    # f(x) = x³ - 3x on [-2, 2]
    # f'(x) = 3x² - 3 = 0 → x = ±1
    # f(-2) = -2, f(-1) = 2, f(1) = -2, f(2) = 2
    # Abs max = 2, Abs min = -2
    
    return problem(
        problem_tex="f(x) = x^3 - 3x \\text{ on } [-2, 2]. \\text{ Find the absolute maximum and minimum.}",
        answer_tex="\\text{Absolute max: } 2 \\text{ at } x = -1, 2; \\quad \\text{Absolute min: } -2 \\text{ at } x = -2, 1",
        answer_norm="max=2;min=-2",
        requiresDualAnswer=True,
        answerNorm2="-2",
        steps=[
            step("Differentiate", "f'(x) = 3x^2 - 3 = 3(x-1)(x+1)"),
            step("Critical points in [-2, 2]", "x = -1, \\quad x = 1"),
            step("Evaluate at endpoints and critical points", "f(-2) = -2; \\quad f(-1) = 2; \\quad f(1) = -2; \\quad f(2) = 2"),
            step("Absolute maximum", "\\max\\{-2, 2, -2, 2\\} = 2 \\text{ at } x = -1, 2"),
            step("Absolute minimum", "\\min\\{-2, 2, -2, 2\\} = -2 \\text{ at } x = -2, 1"),
        ],
    )


def _absolute_extrema_different_interval():
    """Absolute extrema on a different interval"""
    # f(x) = x⁴ - 4x³ on [0, 5]
    # f'(x) = 4x³ - 12x² = 4x²(x-3)
    # Critical: x = 0, 3
    # f(0) = 0, f(3) = -27, f(5) = 125
    # Abs max = 125, Abs min = -27
    
    return problem(
        problem_tex="f(x) = x^4 - 4x^3 \\text{ on } [0, 5]. \\text{ Find the absolute maximum and minimum.}",
        answer_tex="\\text{Absolute max: } 125 \\text{ at } x = 5; \\quad \\text{Absolute min: } -27 \\text{ at } x = 3",
        answer_norm="max=125;min=-27",
        requiresDualAnswer=True,
        answerNorm2="-27",
        steps=[
            step("Differentiate", "f'(x) = 4x^3 - 12x^2 = 4x^2(x-3)"),
            step("Critical points in [0, 5]", "x = 0, \\quad x = 3"),
            step("Evaluate", "f(0) = 0; \\quad f(3) = 81 - 108 = -27; \\quad f(5) = 625 - 500 = 125"),
            step("Absolute maximum", "125 \\text{ at } x = 5"),
            step("Absolute minimum", "-27 \\text{ at } x = 3"),
        ],
    )


# ── extrema3 — second derivative test ─────────────────────────────────────────

def _second_derivative_test():
    """Classify critical points using second derivative test"""
    # f(x) = x⁴ - 4x³
    # f'(x) = 4x³ - 12x² = 4x²(x-3)
    # f''(x) = 12x² - 24x = 12x(x-2)
    # At x=3: f''(3) = 36 > 0 → local min
    # At x=0: f''(0) = 0 → test fails
    
    return problem(
        problem_tex="f(x) = x^4 - 4x^3. \\text{ Use the second derivative test to classify critical points.}",
        answer_tex="x = 3: \\text{local min}; \\quad x = 0: \\text{test fails}",
        answer_norm="x=3:local_min;x=0:test_fails",
        steps=[
            step("First derivative", "f'(x) = 4x^3 - 12x^2 = 4x^2(x-3)"),
            step("Critical points", "x = 0, \\quad x = 3"),
            step("Second derivative", "f''(x) = 12x^2 - 24x = 12x(x-2)"),
            step("Test x=3", "f''(3) = 12(3)(1) = 36 > 0 \\implies \\text{local min}"),
            step("Test x=0", "f''(0) = 0 \\implies \\text{second derivative test fails (use first derivative test)}"),
        ],
    )


def _second_derivative_classify():
    """Given f''(x) and critical points, classify"""
    cases = [
        {
            "f_double": "6x - 6",
            "critical": "x = 0, \\quad x = 2",
            "f_double_0": "-6",
            "f_double_2": "6",
            "answer": "x = 0: \\text{local max}; \\quad x = 2: \\text{local min}",
            "norm": "x=0:local_max;x=2:local_min",
            "steps": [
                step("Evaluate f'' at x=0", "f''(0) = -6 < 0 \\implies \\text{concave down} \\implies \\text{local max}"),
                step("Evaluate f'' at x=2", "f''(2) = 6 > 0 \\implies \\text{concave up} \\implies \\text{local min}"),
            ],
        },
    ]
    c = pick(cases)
    
    return problem(
        problem_tex=f"f''(x) = {c['f_double']}. \\text{{ Critical points: }} {c['critical']}. \\text{{ Classify each.}}",
        answer_tex=c["answer"],
        answer_norm=c["norm"],
        steps=c["steps"],
    )


# ── extrema4 — word problems leading to extrema ───────────────────────────────

def _optimization_extrema():
    """Word problem requiring finding global optimum"""
    # Revenue R(x) = x(100 - 2x) = 100x - 2x² where x = price
    # R'(x) = 100 - 4x = 0 → x = 25
    # R''(x) = -4 < 0 → maximum
    
    return problem(
        problem_tex="\\text{Revenue function: } R(x) = 100x - 2x^2, \\text{ where } x \\text{ is price in dollars. Find the price that maximizes revenue.}",
        answer_tex="x = 25 \\text{ dollars}",
        answer_norm="25",
        steps=[
            step("Differentiate", "R'(x) = 100 - 4x"),
            step("Find critical point", "100 - 4x = 0 \\implies x = 25"),
            step("Second derivative test", "R''(x) = -4 < 0 \\implies \\text{concave down} \\implies \\text{maximum}"),
            step("Answer", "x = 25 \\text{ dollars maximizes revenue}"),
        ],
    )


# ── extrema5 — combined extrema analysis ──────────────────────────────────────

def _full_extrema_analysis():
    """Complete extrema analysis: local + absolute + classification"""
    # f(x) = x⁴ - 2x² on [-2, 2]
    # f'(x) = 4x³ - 4x = 4x(x-1)(x+1)
    # Critical: x = -1, 0, 1
    # f''(x) = 12x² - 4
    # f''(-1) = 8 > 0 (local min), f''(0) = -4 < 0 (local max), f''(1) = 8 > 0 (local min)
    # f(-2) = 8, f(-1) = -1, f(0) = 0, f(1) = -1, f(2) = 8
    # Abs max = 8, Abs min = -1
    
    return problem(
        problem_tex="f(x) = x^4 - 2x^2 \\text{ on } [-2, 2]. \\text{ Find all local and absolute extrema.}",
        answer_tex="\\text{Local max: } (0, 0); \\quad \\text{Local min: } (-1, -1), (1, -1); \\quad \\text{Abs max: } 8; \\quad \\text{Abs min: } -1",
        answer_norm="local_max:(0,0);local_min:(-1,-1),(1,-1);abs_max=8;abs_min=-1",
        steps=[
            step("First derivative", "f'(x) = 4x^3 - 4x = 4x(x-1)(x+1)"),
            step("Critical points", "x = -1, \\quad x = 0, \\quad x = 1"),
            step("Second derivative", "f''(x) = 12x^2 - 4"),
            step("Classify local extrema", "f''(-1) = 8 > 0 \\text{ (local min)}; \\quad f''(0) = -4 < 0 \\text{ (local max)}; \\quad f''(1) = 8 > 0 \\text{ (local min)}"),
            step("Evaluate at endpoints", "f(-2) = 8; \\quad f(2) = 8"),
            step("Absolute max", "\\max\\{8, -1, 0, -1, 8\\} = 8"),
            step("Absolute min", "\\min\\{8, -1, 0, -1, 8\\} = -1"),
        ],
    )


def _extrema_with_parameter():
    """Extrema problem with a parameter"""
    # f(x) = x³ - 3ax² + 2 where a > 0
    # f'(x) = 3x² - 6ax = 3x(x - 2a)
    # Critical: x = 0, x = 2a
    # f''(x) = 6x - 6a
    # f''(0) = -6a < 0 (local max), f''(2a) = 6a > 0 (local min)
    
    a = pick([1, 2, 3])
    ca3 = str(3 * a)
    ca6 = str(6 * a)
    ca2 = str(2 * a)

    return problem(
        problem_tex="f(x) = x^3 - " + ca3 + "x^2 + 2. \\text{ Find and classify all local extrema.}",
        answer_tex="x = 0: \\text{local max}; \\quad x = " + ca2 + ": \\text{local min}",
        answer_norm="x=0:local_max;x=" + ca2 + ":local_min",
        steps=[
            step("First derivative", "f'(x) = 3x^2 - " + ca6 + "x = 3x(x - " + ca2 + ")"),
            step("Critical points", "x = 0, \\quad x = " + ca2),
            step("Second derivative", "f''(x) = 6x - " + ca6),
            step("Classify x=0", "f''(0) = -" + ca6 + " < 0 \\implies \\text{local max}"),
            step("Classify x=" + ca2, "f''(" + ca2 + ") = " + ca6 + " > 0 \\implies \\text{local min}"),
        ],
    )


extrema1 = [_local_extrema_first_derivative, _local_extrema_from_graph]
extrema2 = [_absolute_extrema_closed_interval, _absolute_extrema_different_interval]
extrema3 = [_second_derivative_test, _second_derivative_classify]
extrema4 = [_optimization_extrema]
extrema5 = [_full_extrema_analysis, _extrema_with_parameter]

POOLS = {1: extrema1, 2: extrema2, 3: extrema3, 4: extrema4, 5: extrema5}
