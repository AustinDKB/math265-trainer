from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── quad1 — solve by factoring ─────────────────────────────────────────────────

def _factorable_quadratic():
    # x² + 5x + 6 = 0 → (x+2)(x+3) = 0 → x = -2, -3
    p = pick([1, 2, 3, 4, 5, 6])
    q = pick([1, 2, 3, 4, 5, 6])
    while p == q:
        q = pick([1, 2, 3, 4, 5, 6])
    roots = sorted([-p, -q], reverse=True)
    b = -(roots[0] + roots[1])  # sum = -b/a → b = -sum
    c = roots[0] * roots[1]  # product = c/a → c = product
    return problem(
        problem_tex=f"x^2 {sign_str(b)}x {sign_str(c)} = 0. \\text{{ Solve by factoring.}}",
        answer_tex=f"x = {roots[0]}, \\quad x = {roots[1]}",
        answer_norm=f"x={roots[0]},x={roots[1]}",
        steps=[
            step("Find two numbers", f"\\text{{Product }} {c}, \\text{{ sum }} {-b} \\implies {-roots[0]} \\text{{ and }} {-roots[1]}"),
            step("Factor", f"(x {sign_str(-roots[0])})(x {sign_str(-roots[1])}) = 0"),
            step("Zero product", f"x {sign_str(-roots[0])} = 0 \\implies x = {roots[0]} \\quad \\text{{or}} \\quad x {sign_str(-roots[1])} = 0 \\implies x = {roots[1]}"),
        ],
    )


def _factor_diff_squares():
    # x² - 9 = 0 → (x-3)(x+3) = 0 → x = 3, -3
    a = R(2, 8)
    a2 = a * a
    return problem(
        problem_tex=f"x^2 - {a2} = 0",
        answer_tex=f"x = {a}, \\quad x = {-a}",
        answer_norm=f"x={a},x={-a}",
        steps=[
            step("Recognize difference of squares", f"x^2 - {a2} = (x - {a})(x + {a})"),
            step("Set each to zero", f"x - {a} = 0 \\implies x = {a}; \\quad x + {a} = 0 \\implies x = {-a}"),
        ],
    )


# ── quad2 — quadratic formula ──────────────────────────────────────────────────

def _quadratic_formula():
    # 2x² + 5x - 3 = 0 → x = (-5 ± √49)/4 = (-5 ± 7)/4 → x = 0.5, x = -3
    a = R(1, 3)
    b = R(-10, 10)
    c_val = R(-10, 10)
    disc = b * b - 4 * a * c_val
    disc_sqrt = int(disc ** 0.5)
    r1 = (-b + disc_sqrt) / (2 * a)
    r2 = (-b - disc_sqrt) / (2 * a)
    return problem(
        problem_tex=f"{a}x^2 {sign_str(b)}x {sign_str(c_val)} = 0. \\text{{ Solve using the quadratic formula.}}",
        answer_tex=f"x = \\dfrac{{{sign_str(-b)} {disc_sqrt}}}{{{2*a}}}",
        answer_norm=f"x={r1},x={r2}",
        steps=[
            step("Identify a, b, c", f"a = {a}, \\quad b = {b}, \\quad c = {c_val}"),
            step("Compute discriminant", f"\\Delta = b^2 - 4ac = ({b})^2 - 4({a})({c_val}) = {disc}"),
            step("Quadratic formula", f"x = \\dfrac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} = \\dfrac{{{-b} \\pm {disc_sqrt}}}{{{2*a}}}"),
            step("Simplify", f"x = \\dfrac{{{-b + disc_sqrt}}}{{{2*a}}} = {r1} \\quad \\text{{or}} \\quad x = \\dfrac{{{-b - disc_sqrt}}}{{{2*a}}} = {r2}"),
        ],
    )


def _quadratic_word():
    # x² + bx + c = 0 with integer roots p and q, where l-w = p+q and area = -c
    # We set up: w is one root, l-w is the difference, the other root gives area
    w = R(2, 6)
    l_diff = R(2, 5)
    l = w + l_diff
    area = w * l

    return problem(
        problem_tex=f"\\text{{A rectangle has area }} {area}. \\text{{ Length is }} {l_diff} \\text{{ more than width. Find dimensions.}}",
        answer_tex=f"\\text{{Width }} = {w}, \\quad \\text{{Length }} = {l}",
        answer_norm=f"w={w},l={l}",
        steps=[
            step("Set up equation", f"w^2 + {l_diff}w - {area} = 0 \\quad (\\text{{since }} w(l) = w(w+{l_diff}) = {area})"),
            step("Use width as one root", f"\\text{{Width }} = {w}"),
            step("Compute length", f"\\text{{Length }} = w + {l_diff} = {w} + {l_diff} = {l}"),
        ],
    )


# ── quad3 — complete the square ────────────────────────────────────────────────

def _complete_square():
    b = R(4, 12)
    b_half = b // 2
    b_sq = b_half * b_half
    c_val = R(-b_sq - 10, -b_sq + 1)
    rhs = b_sq - c_val
    r = int(rhs ** 0.5)
    return problem(
        problem_tex=f"x^2 {sign_str(b)}x {sign_str(c_val)} = 0. \\text{{ Solve by completing the square.}}",
        answer_tex=f"x = {-b_half + r}, \\quad x = {-b_half - r}",
        answer_norm=f"x={-b_half + r},x={-b_half - r}",
        steps=[
            step("Move constant", f"x^2 {sign_str(b)}x = {-c_val}"),
            step("Add (b/2)²", f"(x + {b_half})^2 = {-c_val} + {b_sq} = {b_sq - c_val}"),
            step("Take square root", f"x + {b_half} = \\pm \\sqrt{{{b_sq - c_val}}}"),
            step("Solve", f"x = {-b_half} \\pm {r}"),
        ],
    )


# ── quad4 — discriminant analysis ──────────────────────────────────────────────

def _discriminant_nature():
    # Given discriminant, determine number of real roots
    disc = pick([16, 9, 0, -4])
    disc_sqrt = int(disc ** 0.5) if disc >= 0 else None
    return problem(
        problem_tex=f"\\text{{The discriminant of a quadratic equation is }} {disc}. \\text{{ How many real solutions does it have?}}",
        answer_tex="Two distinct real solutions" if disc > 0 else ("One real solution (repeated)" if disc == 0 else "No real solutions"),
        answer_norm="2" if disc > 0 else ("1" if disc == 0 else "0"),
        steps=[
            step("Recall discriminant rule", "\\Delta > 0: 2 real; \\Delta = 0: 1 real; \\Delta < 0: 0 real"),
            step("Apply", "\\Delta = " + str(disc) + (" > 0" if disc > 0 else (" = 0" if disc == 0 else " < 0"))),
            step("Conclusion", "Two distinct real solutions" if disc > 0 else ("One real solution (repeated)" if disc == 0 else "No real solutions")),
        ],
    )


# ── quad5 — vertex form + graphing ─────────────────────────────────────────────

def _vertex_of_parabola():
    # f(x) = 2x² - 4x + 1 → vertex at x = -b/2a = 4/4 = 1, f(1) = -1
    a = R(1, 3)
    h = R(-5, 5)
    k = R(-10, 10)
    b_val = -2 * a * h
    c_val = k + a * h * h
    return problem(
        problem_tex=f"f(x) = {a}x^2 {sign_str(b_val)}x {sign_str(c_val)}. \\text{{ Find the vertex.}}",
        answer_tex=f"({h}, {k})",
        answer_norm=f"({h},{k})",
        steps=[
            step("x-coordinate of vertex", f"x_v = -b/(2a) = {-b_val}/(2 \\cdot {a}) = {h}"),
            step("y-coordinate", f"f({h}) = {a}({h})^2 {sign_str(b_val)}({h}) {sign_str(c_val)} = {k}"),
            step("Vertex", f"({h}, {k})"),
        ],
    )


def _max_min_quadratic():
    # f(x) = -x² + 4x + 1 → vertex at (2, 5) → max = 5
    a = -R(1, 3)  # negative for max
    h = R(1, 5)
    k = R(1, 10)
    b_val = -2 * a * h
    c_val = k + a * h * h
    is_max = a < 0

    return problem(
        problem_tex=f"f(x) = {a}x^2 {sign_str(b_val)}x {sign_str(c_val)}. \\text{{ Find the maximum or minimum value.}}",
        answer_tex=f"\\text{{Maximum }} = {k}" if is_max else f"\\text{{Minimum }} = {k}",
        answer_norm=f"{'max' if is_max else 'min'}={k}",
        steps=[
            step("Vertex x-coordinate", f"x_v = -b/(2a) = {-b_val}/(2 \\cdot {a}) = {h}"),
            step("Maximum" if is_max else "Minimum", f"f({h}) = {a}({h})^2 {sign_str(b_val)}({h}) {sign_str(c_val)} = {k}"),
        ],
    )


quadratic1 = [_factorable_quadratic, _factor_diff_squares]
quadratic2 = [_quadratic_formula, _quadratic_word]
quadratic3 = [_complete_square]
quadratic4 = [_discriminant_nature]
quadratic5 = [_vertex_of_parabola, _max_min_quadratic]

POOLS = {1: quadratic1, 2: quadratic2, 3: quadratic3, 4: quadratic4, 5: quadratic5}