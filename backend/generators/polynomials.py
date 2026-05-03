from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── poly1 — classify by degree/type ───────────────────────────────────────────

def _classify_polynomial():
    cases = [
        ("3x^4 - 2x^2 + 1", "quartic polynomial", "quartic"),
        ("x^3 + 4x", "cubic polynomial", "cubic"),
        ("5x^2 - 3x + 7", "quadratic polynomial", "quadratic"),
        ("-2x + 8", "linear polynomial", "linear"),
        ("7", "constant polynomial", "constant"),
    ]
    expr, label, norm = pick(cases)
    return problem(
        problem_tex=f"f(x) = {expr}. \\text{{ Classify by degree and type.}}",
        answer_tex=label,
        answer_norm=norm,
        steps=[step("Identify highest power of x", label)],
    )


def _identify_coefficients():
    # 4x³ - 3x² + 2x - 7 = 0 → coefficients: 4, -3, 2, -7
    a = R(1, 5)
    b = pick([-5, -4, -3, -2, 2, 3, 4, 5])
    c = pick([-5, -4, -3, -2, 2, 3, 4, 5])
    d = R(-10, 10)
    return problem(
        problem_tex=f"{a}x^3 {sign_str(b)}x^2 {sign_str(c)}x {sign_str(d)} = 0. \\text{{ What are the coefficients?}}",
        answer_tex=f"a_3 = {a}, \\quad a_2 = {b}, \\quad a_1 = {c}, \\quad a_0 = {d}",
        answer_norm=f"{a},{b},{c},{d}",
        steps=[
            step("Standard form", f"{a}x^3 {sign_str(b)}x^2 {sign_str(c)}x {sign_str(d)}"),
            step("Read coefficients", f"a_3 = {a} \\text{{ (leading)}}, a_2 = {b}, a_1 = {c}, a_0 = {d} \\text{{ (constant)}}"),
        ],
    )


# ── poly2 — polynomial arithmetic ─────────────────────────────────────────────

def _poly_addition():
    # (x² + 3x + 2) + (2x² - x + 4) = 3x² + 2x + 6
    return problem(
        problem_tex="(x^2 + 3x + 2) + (2x^2 - x + 4)",
        answer_tex="3x^2 + 2x + 6",
        answer_norm="3x^2+2x+6",
        steps=[
            step("Group like terms", "x^2 + 2x^2 + 3x - x + 2 + 4"),
            step("Combine", "3x^2 + 2x + 6"),
        ],
    )


def _poly_subtraction():
    # (5x² + 3x) - (2x² - x + 4) = 3x² + 4x - 4
    return problem(
        problem_tex="(5x^2 + 3x) - (2x^2 - x + 4)",
        answer_tex="3x^2 + 4x - 4",
        answer_norm="3x^2+4x-4",
        steps=[
            step("Distribute negative", "5x^2 + 3x - 2x^2 + x - 4"),
            step("Combine like terms", "3x^2 + 4x - 4"),
        ],
    )


# ── poly3 — multiply polynomials ──────────────────────────────────────────────

def _foil_binomials():
    # (x + 3)(x - 2) = x² + x - 6
    a = R(1, 5)
    b = pick([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
    while b == -a:
        b = pick([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
    return problem(
        problem_tex=f"(x {sign_str(a)})(x {sign_str(b)})",
        answer_tex=f"x^2 {sign_str(a+b)}x {sign_str(a*b)}",
        answer_norm=f"x^2+{a+b}x+{a*b}",
        steps=[
            step("FOIL", f"(x)(x) + (x)({b}) + ({a})(x) + ({a})({b})"),
            step("Multiply", f"x^2 {sign_str(b)}x {sign_str(a)}x {sign_str(a*b)}"),
            step("Combine", f"x^2 {sign_str(a+b)}x {sign_str(a*b)}"),
        ],
    )


def _special_product():
    # (x + 4)² = x² + 8x + 16
    a = R(2, 7)
    return problem(
        problem_tex=f"(x {sign_str(a)})^2",
        answer_tex=f"x^2 {sign_str(2*a)}x {sign_str(a*a)}",
        answer_norm=f"x^2+{2*a}x+{a*a}",
        steps=[
            step("Apply (a+b)² formula", f"(x {sign_str(a)})(x {sign_str(a)})"),
            step("Multiply", f"x^2 {sign_str(a)}x {sign_str(a)}x {sign_str(a*a)}"),
            step("Combine", f"x^2 {sign_str(2*a)}x {sign_str(a*a)}"),
        ],
    )


# ── poly4 — synthetic division ───────────────────────────────────────────────

def _synthetic_basic():
    # Divide x³ - 6x² + 11x - 6 by (x - 2)
    # Synthetic: 2 | 1  -6  11  -6
    #            ↓   2  -8   6
    #              1  -4   3   0
    # Result: x² - 4x + 3
    return problem(
        problem_tex="\\text{Divide } x^3 - 6x^2 + 11x - 6 \\text{ by } (x - 2) \\text{ using synthetic division.}",
        answer_tex="x^2 - 4x + 3",
        answer_norm="x^2-4x+3",
        steps=[
            step("Set up synthetic division", "2 \\quad \\overline{1} \\quad -6 \\quad 11 \\quad -6"),
            step("Bring down 1", "1"),
            step("Multiply and add", "2(1)=2 \\to -4; \\quad 2(-4)=-8 \\to 3; \\quad 2(3)=6 \\to 0"),
            step("Result", "x^2 - 4x + 3"),
        ],
    )


# ── poly5 — factor theorem / roots ───────────────────────────────────────────

def _factor_theorem():
    # f(x) = x³ - 7x + 6, f(1) = 0, so (x-1) is a factor
    # f(x) = (x-1)(x²+x-6) = (x-1)(x+3)(x-2)
    return problem(
        problem_tex="f(x) = x^3 - 7x + 6. \\text{ Show that } x = 1 \\text{ is a root and factor } f(x).",
        answer_tex="f(1) = 0, \\quad f(x) = (x-1)(x+3)(x-2)",
        answer_norm="(x-1)(x+3)(x-2)",
        steps=[
            step("Evaluate f(1)", "f(1) = 1 - 7 + 6 = 0 \\implies x-1 \\text{ is a factor}"),
            step("Divide to find other factor", "x^3 - 7x + 6 = (x-1)(x^2 + x - 6)"),
            step("Factor quadratic", "x^2 + x - 6 = (x+3)(x-2)"),
            step("Complete factorization", "f(x) = (x-1)(x+3)(x-2)"),
        ],
    )


polynomial1 = [_classify_polynomial, _identify_coefficients]
polynomial2 = [_poly_addition, _poly_subtraction]
polynomial3 = [_foil_binomials, _special_product]
polynomial4 = [_synthetic_basic]
polynomial5 = [_factor_theorem]

POOLS = {1: polynomial1, 2: polynomial2, 3: polynomial3, 4: polynomial4, 5: polynomial5}