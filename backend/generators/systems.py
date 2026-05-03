from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── systems1 — solve by substitution ──────────────────────────────────────────

def _substitution_basic():
    # y = 2x + 1, x + y = 7 → x + 2x + 1 = 7 → 3x = 6 → x = 2, y = 5
    a = R(1, 3)
    y_expr = f"{a}x {sign_str(R(1,5))}"
    b = pick([3, 4, 5])
    c_val = a * b + R(1, 6)
    return problem(
        problem_tex=f"y = {y_expr}, \\quad x + y = {c_val}",
        answer_tex=f"x = {b}, \\quad y = {a*b + R(1,6)}",
        answer_norm=f"x={b},y={a*b+R(1,6)}",
        steps=[
            step("Substitute y", f"x + ({y_expr}) = {c_val}"),
            step("Solve for x", f"{a+1}x = {c_val} \\implies x = {(c_val - R(1,5)) // (a+1)}"),
            step("Back-substitute y", f"y = {y_expr} \\text{{ at }} x = {(c_val - R(1,5)) // (a+1)}"),
        ],
    )


def _substitution_nonlinear():
    # y = x² - 4, x + y = 2 → x + x² - 4 = 2 → x² + x - 6 = 0 → (x+3)(x-2)=0
    # x = 2 or x = -3
    return problem(
        problem_tex="y = x^2 - 4, \\quad x + y = 2",
        answer_tex="x = 2, y = 0 \\quad \\text{or} \\quad x = -3, y = 5",
        answer_norm="x=2,y=0;x=-3,y=5",
        steps=[
            step("Substitute y", "x + (x^2 - 4) = 2 \\implies x^2 + x - 6 = 0"),
            step("Factor", "(x+3)(x-2) = 0 \\implies x = 2 \\text{ or } x = -3"),
            step("Find y", "x=2: y=0; \\quad x=-3: y=5"),
        ],
    )


# ── systems2 — solve by elimination ─────────────────────────────────────────

def _elimination_basic():
    # 2x + 3y = 16, x - 3y = -1 → add: 3x = 15 → x = 5, y = 2
    return problem(
        problem_tex="2x + 3y = 16, \\quad x - 3y = -1",
        answer_tex="x = 5, \\quad y = 2",
        answer_norm="x=5,y=2",
        steps=[
            step("Add equations", "(2x+3y) + (x-3y) = 16 + (-1) \\implies 3x = 15"),
            step("Solve x", "x = 5"),
            step("Substitute back", "2(5) + 3y = 16 \\implies 3y = 6 \\implies y = 2"),
        ],
    )


def _elimination_multiply():
    # 3x + 2y = 7, 5x - 3y = 4 → multiply first by 3, second by 2
    # 9x + 6y = 21, 10x - 6y = 8 → add: 19x = 29 → x = 29/19...
    # Let's use simpler numbers
    a = R(2, 4)
    b = R(1, 3)
    c_val = R(5, 12)
    d = R(1, 3)
    e = R(2, 5)
    f_val = R(3, 10)
    det = a * e - b * d
    if det == 0:
        det = 1
        a = 2
        b = 1
        c_val = 5
        d = 1
        e = 3
        f_val = 7
    x_val = (c_val * e - b * f_val) / det
    y_val = (a * f_val - c_val * d) / det
    if x_val == int(x_val):
        x_val = int(x_val)
    if y_val == int(y_val):
        y_val = int(y_val)

    return problem(
        problem_tex=f"{a}x {sign_str(b)}y = {c_val}, \\quad {d}x {sign_str(e if e>0 else e)}y = {f_val}",
        answer_tex=f"x = {x_val}, \\quad y = {y_val}",
        answer_norm=f"x={x_val},y={y_val}",
        steps=[
            step("Set up for elimination", f"\\text{{Multiply to eliminate one variable}}"),
            step("Solve", f"x = {x_val}, \\quad y = {y_val}"),
        ],
    )


# ── systems3 — three variables ────────────────────────────────────────────────

def _three_variable_basic():
    # x + y + z = 6, x - y = 1, y + z = 4 → substitute: from x-y=1 → x=1+y
    # then x+y+z=6 → 1+y+y+z=6 → 2y+z=5; y+z=4 → subtract → y=1, then z=3, x=2
    return problem(
        problem_tex="x + y + z = 6, \\quad x - y = 1, \\quad y + z = 4",
        answer_tex="x = 2, \\quad y = 1, \\quad z = 3",
        answer_norm="x=2,y=1,z=3",
        steps=[
            step("From x - y = 1", "x = 1 + y"),
            step("Substitute into first", "(1+y) + y + z = 6 \\implies 2y + z = 5"),
            step("Subtract from y + z = 4", "(2y+z) - (y+z) = 5-4 \\implies y = 1"),
            step("Find z and x", "z = 4 - y = 3; \\quad x = 1 + y = 2"),
        ],
    )


# ── systems4 — word problems ─────────────────────────────────────────────────

def _ticket_problem():
    # "Adult tickets $5, student $2. 100 tickets for $320. How many of each?"
    # a + s = 100, 5a + 2s = 320 → s = 100-a → 5a + 200 - 2a = 320 → 3a = 120 → a=40, s=60
    a = R(20, 50)
    s = R(30, 70)
    while a + s > 200 or a + s < 50:
        a = R(20, 50)
        s = R(30, 70)
    total = a + s
    revenue = 5 * a + 2 * s

    return problem(
        problem_tex=f"\\text{{Adult tickets cost \\$5, student \\$2. {{total}} tickets sold for \\${revenue}. How many adult tickets?}}",
        answer_tex=f"{a} \\text{{ adult tickets}}, \\quad {s} \\text{{ student tickets}}",
        answer_norm=f"adult={a},student={s}",
        steps=[
            step("Set up equations", f"a + s = {total}, \\quad 5a + 2s = {revenue}"),
            step("Solve", f"a = {total} - s \\implies 5({total}-s) + 2s = {revenue} \\implies 3s = {5*total - revenue} \\implies s = {s}"),
            step("Find a", f"a = {total} - {s} = {a}"),
        ],
    )


# ── systems5 — inconsistent/dependent ─────────────────────────────────────────

def _classify_system():
    # 2x + 4y = 6, x + 2y = 3 → dependent (same line)
    return problem(
        problem_tex="2x + 4y = 6, \\quad x + 2y = 3. \\text{ Classify the system.}}",
        answer_tex="\\text{Infinitely many solutions (dependent)}",
        answer_norm="infinitely_many",
        steps=[
            step("Notice second equation", "x + 2y = 3 \\implies 2x + 4y = 6 \\text{ (multiply by 2)}"),
            step("Same line", "\\text{Both equations represent the same line}"),
            step("Classification", "\\text{Infinitely many solutions (dependent system)}"),
        ],
    )


systems1 = [_substitution_basic, _substitution_nonlinear]
systems2 = [_elimination_basic, _elimination_multiply]
systems3 = [_three_variable_basic]
systems4 = [_ticket_problem]
systems5 = [_classify_system]

POOLS = {1: systems1, 2: systems2, 3: systems3, 4: systems4, 5: systems5}