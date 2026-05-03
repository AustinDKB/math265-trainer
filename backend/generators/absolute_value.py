from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── abs1 — solve |ax + b| = c ─────────────────────────────────────────────────

def _abs_basic():
    # |2x - 3| = 5 → 2x - 3 = 5 or 2x - 3 = -5 → x = 4 or x = -1
    a = R(2, 5)
    b = R(-8, 8)
    c_val = pick([3, 5, 7, 9])
    inner_at_pos = (c_val - b) / a
    inner_at_neg = (-c_val - b) / a
    if inner_at_pos == int(inner_at_pos):
        inner_at_pos = int(inner_at_pos)
    if inner_at_neg == int(inner_at_neg):
        inner_at_neg = int(inner_at_neg)

    return problem(
        problem_tex=f"|{a}x {sign_str(b)}| = {c_val}",
        answer_tex=f"x = {inner_at_pos}, \\quad x = {inner_at_neg}",
        answer_norm=f"x={inner_at_pos},x={inner_at_neg}",
        steps=[
            step("Set up two cases", f"{a}x {sign_str(b)} = {c_val} \\quad \\text{{or}} \\quad {a}x {sign_str(b)} = -{c_val}"),
            step("Case 1", f"{a}x = {c_val} - ({b}) = {c_val - b} \\implies x = {inner_at_pos}"),
            step("Case 2", f"{a}x = -{c_val} - ({b}) = {-c_val - b} \\implies x = {inner_at_neg}"),
        ],
    )


def _abs_no_solution():
    # |x + 1| = -3 → no solution
    return problem(
        problem_tex="|x + 1| = -3",
        answer_tex="\\text{No solution}",
        answer_norm="no_solution",
        steps=[
            step("Absolute value is always non-negative", "|x + 1| \\geq 0 \\text{ for all } x"),
            step("Compare to RHS", "-3 < 0, \\text{ so no solution}"),
        ],
    )


# ── abs2 — solve |ax + b| < c, |ax + b| > c ────────────────────────────────────

def _abs_inequality_lt():
    # |x - 3| < 5 → -5 < x - 3 < 5 → -2 < x < 8
    a = 1
    b = R(-5, 5)
    c_val = pick([3, 4, 5, 6])
    lower = b - c_val
    upper = b + c_val
    return problem(
        problem_tex=f"|x {sign_str(b)}| < {c_val}",
        answer_tex=f"{-b - c_val} < x < {-b + c_val}",
        answer_norm=f"({lower},{upper})",
        steps=[
            step("Split into two inequalities", f"-{c_val} < x {sign_str(b)} < {c_val}"),
            step("Isolate x", f"{-c_val} {sign_str(-b)} < x < {c_val} {sign_str(-b)}"),
            step("Simplify", f"{lower} < x < {upper}"),
        ],
    )


def _abs_inequality_gt():
    # |2x + 1| > 3 → 2x + 1 > 3 or 2x + 1 < -3 → x > 1 or x < -2
    a = R(2, 4)
    b = R(-5, 5)
    c_val = pick([2, 3, 4])
    right_lower = (c_val - b) / a
    left_upper = (-c_val - b) / a
    if right_lower == int(right_lower):
        right_lower = int(right_lower)
    if left_upper == int(left_upper):
        left_upper = int(left_upper)

    return problem(
        problem_tex=f"|{a}x {sign_str(b)}| > {c_val}",
        answer_tex=f"x > {right_lower} \\quad \\text{{or}} \\quad x < {left_upper}",
        answer_norm=f"x>{right_lower} or x<{left_upper}",
        steps=[
            step("Set up compound inequality", f"{a}x {sign_str(b)} > {c_val} \\quad \\text{{OR}} \\quad {a}x {sign_str(b)} < -{c_val}"),
            step("Case 1", f"x > \\dfrac{{{c_val} - ({b})}}{{{a}}} = {right_lower}"),
            step("Case 2", f"x < \\dfrac{{-{c_val} - ({b})}}{{{a}}} = {left_upper}"),
        ],
    )


# ── abs3 — abs properties ─────────────────────────────────────────────────────

def _abs_equation_compound():
    # |x| + |x-2| = 6 → solve by cases
    return problem(
        problem_tex="|x| + |x-2| = 6. \\text{ Find all solutions.}",
        answer_tex="x = -2, \\quad x = 4",
        answer_norm="x=-2,x=4",
        steps=[
            step("Case 1: x < 0", "-x + -(x-2) = 6 \\implies -2x + 2 = 6 \\implies x = -2 \\checkmark"),
            step("Case 2: 0 <= x < 2", "x + -(x-2) = 6 \\implies 2 = 6 \\implies \\text{no solution}"),
            step("Case 3: x >= 2", "x + x-2 = 6 \\implies 2x = 8 \\implies x = 4 \\checkmark"),
        ],
    )


# ── abs4 — abs value in context ───────────────────────────────────────────────

def _abs_distance():
    # "|x - 3| = 7 means x is 7 units from 3" → x = 10 or x = -4
    center = R(-5, 5)
    dist = pick([3, 5, 7])
    return problem(
        problem_tex=f"|x {sign_str(-center)}| = {dist}. \\text{{ What does this tell us about }} x?",
        answer_tex=f"x \\text{{ is exactly {dist} units from }} {center}. \\quad x = {center + dist} \\text{{ or }} x = {center - dist}",
        answer_norm=f"x={center+dist},x={center-dist}",
        steps=[
            step("Definition of absolute value", f"|x - {center}| = {dist} \\implies x - {center} = \\pm {dist}"),
            step("Case +", f"x = {center} + {dist} = {center + dist}"),
            step("Case -", f"x = {center} - {dist} = {center - dist}"),
        ],
    )


# ── abs5 — combined ──────────────────────────────────────────────────────────

def _abs_graphical():
    # |2x - 3| <= 7 → solve and graph
    a = R(2, 4)
    b = R(-5, 5)
    c_val = pick([5, 7, 9])
    lower = (b - c_val) / a
    upper = (b + c_val) / a
    if lower == int(lower):
        lower = int(lower)
    if upper == int(upper):
        upper = int(upper)

    return problem(
        problem_tex=f"|{a}x {sign_str(b)}| \\leq {c_val}",
        answer_tex=f"{lower} \\leq x \\leq {upper}",
        answer_norm=f"[{lower},{upper}]",
        steps=[
            step("Set up compound inequality", f"-{c_val} \\leq {a}x {sign_str(b)} \\leq {c_val}"),
            step("Isolate x", f"\\dfrac{{-{c_val} {sign_str(-b)}}}{{{a}}} \\leq x \\leq \\dfrac{{{c_val} {sign_str(-b)}}}{{{a}}}"),
            step("Simplify", f"{lower} \\leq x \\leq {upper}"),
        ],
    )


def _abs_midpoint():
    # "Find the midpoint between -4 and 7" → |-4 - 7|/2 = 11/2 = 5.5
    a = R(-10, 0)
    b = R(1, 10)
    while b <= a:
        b = R(1, 10)
    midpoint = (a + b) / 2
    dist = b - a

    return problem(
        problem_tex=f"\\text{{Find the distance between }} {a} \\text{{ and }} {b}.",
        answer_tex=f"|{b} - ({a})| = {dist}",
        answer_norm=str(dist),
        steps=[
            step("Absolute difference", f"|{b} - {a}| = |{b - a}| = {dist}"),
        ],
    )


abs1 = [_abs_basic, _abs_no_solution]
abs2 = [_abs_inequality_lt, _abs_inequality_gt]
abs3 = [_abs_equation_compound]
abs4 = [_abs_distance]
abs5 = [_abs_graphical, _abs_midpoint]

POOLS = {1: abs1, 2: abs2, 3: abs3, 4: abs4, 5: abs5}