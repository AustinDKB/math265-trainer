from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── inequal1 — solve linear inequalities ──────────────────────────────────────

def _solve_linear_ineq():
    # 3x - 4 < 8 → x < 4
    a = R(2, 6)
    b = R(-8, 8)
    rhs = R(5, 20)
    lhs_val = a * R(1, 5) + b
    return problem(
        problem_tex=f"{a}x {sign_str(b)} < {lhs_val}",
        answer_tex=f"x < {(lhs_val - b) // a}",
        answer_norm=f"x<{(lhs_val - b)//a}",
        steps=[
            step("Add " + str(-b if b < 0 else "+" + str(b)), f"{a}x < {lhs_val} - ({b}) = {lhs_val - b}"),
            step("Divide by " + str(a), f"x < \\dfrac{{{lhs_val - b}}}{{{a}}} = {(lhs_val - b)//a}"),
        ],
    )


def _solve_ineq_reverse():
    # -2x + 5 > 1 → -2x > -4 → x < 2 (flip sign)
    a = -R(2, 5)
    b = R(-5, 8)
    rhs = a * R(1, 5) + b
    return problem(
        problem_tex=f"{a}x {sign_str(b)} > {rhs}",
        answer_tex=f"x < {(rhs - b) // a}",
        answer_norm=f"x<{(rhs - b)//a}",
        steps=[
            step("Subtract " + str(b), f"{a}x > {rhs} - ({b}) = {rhs - b}"),
            step("Divide by " + str(a) + " (flip sign)", f"x < \\dfrac{{{rhs - b}}}{{{a}}} = {(rhs - b)//a}"),
        ],
    )


# ── inequal2 — compound inequalities ─────────────────────────────────────────

def _and_compound():
    # -3 < 2x + 1 < 7 → -4 < 2x < 6 → -2 < x < 3
    a = 2
    b = R(-3, 3)
    lower = R(-5, -1)
    upper = R(5, 10)
    return problem(
        problem_tex=f"{lower} < {a}x {sign_str(b)} < {upper}",
        answer_tex=f"\\dfrac{{{lower - b}}}{{{a}}} < x < \\dfrac{{{upper - b}}}{{{a}}}",
        answer_norm=f"({(lower-b)//a},{(upper-b)//a})",
        steps=[
            step("Subtract " + str(b), f"{lower - b} < {a}x < {upper - b}"),
            step("Divide by " + str(a), f"\\dfrac{{{lower - b}}}{{{a}}} < x < \\dfrac{{{upper - b}}}{{{a}}}"),
            step("Simplify", f"{int((lower-b)/a)} < x < {int((upper-b)/a)}"),
        ],
    )


def _or_compound():
    # x < -2 or x > 3 → interval notation
    a = -R(1, 3)
    return problem(
        problem_tex="x < -2 \\quad \\text{or} \\quad x > 3",
        answer_tex="(-\\infty, -2) \\cup (3, \\infty)",
        answer_norm="(-inf,-2)U(3,inf)",
        steps=[
            step("First inequality", "x < -2 \\implies (-\\infty, -2)"),
            step("Second inequality", "x > 3 \\implies (3, \\infty)"),
            step("Union", "(-\\infty, -2) \\cup (3, \\infty)"),
        ],
    )


# ── inequal3 — quadratic inequalities ─────────────────────────────────────────

def _quadratic_ineq():
    # x² - 4x - 5 < 0 → (x-5)(x+1) < 0 → -1 < x < 5
    # roots at x = -1, 5 (product = -5, sum = 4)
    a = 1
    r1 = R(-5, 0)
    r2 = R(1, 6)
    b_val = -(r1 + r2)
    c_val = r1 * r2
    return problem(
        problem_tex=f"x^2 {sign_str(b_val)}x {sign_str(c_val)} < 0",
        answer_tex=f"\\text{{Between the roots: }} {r1} < x < {r2}",
        answer_norm=f"({r1},{r2})",
        steps=[
            step("Factor", f"x^2 {sign_str(b_val)}x {sign_str(c_val)} = (x{r1})(x{r2}) = 0"),
            step("Find roots", f"x = {r1}, {r2}"),
            step("Parabola opens up", f"< 0 \\text{{ between the roots }} \\implies {r1} < x < {r2}"),
        ],
    )


# ── inequal4 — rational inequalities ─────────────────────────────────────────

def _rational_ineq():
    # (x-1)/(x+2) > 0 → critical points at x=1, x=-2
    # Sign chart: (-inf,-2): -, (-2,1): +, (1,inf): -
    return problem(
        problem_tex="\\dfrac{x-1}{x+2} > 0",
        answer_tex="(-\\infty, -2) \\cup (1, \\infty)",
        answer_norm="(-inf,-2)U(1,inf)",
        steps=[
            step("Critical points", "x - 1 = 0 \\implies x = 1; \\quad x + 2 = 0 \\implies x = -2"),
            step("Sign chart", "\\text{Numerator: } x-1; \\text{ Denominator: } x+2"),
            step("Test intervals", "(-\\infty, -2): \\frac{-}{-} = + \\checkmark; (-2, 1): \\frac{-}{+} = -; (1, \\infty): \\frac{+}{+} = +"),
            step("Solution", "(-\\infty, -2) \\cup (1, \\infty)"),
        ],
    )


# ── inequal5 — interval notation ─────────────────────────────────────────────

def _interval_union():
    # Express solution set as interval union
    return problem(
        problem_tex="\\text{Solve } x^2 \\leq 4. \\text{ Write answer in interval notation.}",
        answer_tex="[-2, 2]",
        answer_norm="[-2,2]",
        steps=[
            step("Take square root", "x^2 \\leq 4 \\implies -2 \\leq x \\leq 2"),
            step("Interval notation", "[-2, 2]"),
        ],
    )


def _ineq_word_problem():
    # "A number increased by 5 is at most 12. What is the number?"
    # x + 5 <= 12 → x <= 7
    a = R(1, 5)
    b = R(5, 15)
    rhs = a * R(2, 6) + b
    return problem(
        problem_tex=f"\\text{{A number multiplied by }} {a} \\text{{ plus }} {b} \\text{{ is at most }} {rhs}. \\text{{ Find the range of possible values.}}",
        answer_tex=f"x \\leq {(rhs - b) // a}",
        answer_norm=f"x<={(rhs-b)//a}",
        steps=[
            step("Set up inequality", f"{a}x + {b} \\leq {rhs}"),
            step("Subtract " + str(b), f"{a}x \\leq {rhs - b}"),
            step("Divide by " + str(a), f"x \\leq \\dfrac{{{rhs - b}}}{{{a}}} = {(rhs - b)//a}"),
        ],
    )


inequalities1 = [_solve_linear_ineq, _solve_ineq_reverse]
inequalities2 = [_and_compound, _or_compound]
inequalities3 = [_quadratic_ineq]
inequalities4 = [_rational_ineq]
inequalities5 = [_interval_union, _ineq_word_problem]

POOLS = {1: inequalities1, 2: inequalities2, 3: inequalities3, 4: inequalities4, 5: inequalities5}