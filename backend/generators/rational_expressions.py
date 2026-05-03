from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── rational1 — simplify rational expressions ─────────────────────────────────

def _simplify_rational():
    # (x² - 4)/(x - 2) = (x+2)(x-2)/(x-2) = x+2 (for x≠2)
    a = R(2, 5)
    a2 = a * a
    return problem(
        problem_tex=f"\\dfrac{{x^2 - {a2}}}{{x - {a}}}",
        answer_tex=f"x + {a} \\quad (x \\neq {a})",
        answer_norm=f"x+{a}",
        steps=[
            step("Factor numerator", f"x^2 - {a2} = (x - {a})(x + {a})"),
            step("Cancel", f"\\dfrac{{(x - {a})(x + {a})}}{{x - {a}}} = x + {a}"),
            step("Domain note", f"x \\neq {a}"),
        ],
    )


def _simplify_rational_complex():
    # (x² + 5x + 6)/(x² + 4x + 3) = (x+2)(x+3)/((x+1)(x+3)) = (x+2)/(x+1)
    return problem(
        problem_tex="\\dfrac{x^2 + 5x + 6}{x^2 + 4x + 3}",
        answer_tex="\\dfrac{x+2}{x+1} \\quad (x \\neq -1, -3)",
        answer_norm="(x+2)/(x+1)",
        steps=[
            step("Factor numerator", "x^2 + 5x + 6 = (x+2)(x+3)"),
            step("Factor denominator", "x^2 + 4x + 3 = (x+1)(x+3)"),
            step("Cancel (x+3)", "\\dfrac{(x+2)(x+3)}{(x+1)(x+3)} = \\dfrac{x+2}{x+1}"),
            step("Domain", "x \\neq -1, -3"),
        ],
    )


# ── rational2 — multiply/divide rational expressions ─────────────────────────

def _multiply_rationals():
    # (x+1)/(x-3) · (x+3)/(x+1) = (x+3)/(x-3)
    return problem(
        problem_tex="\\dfrac{x+1}{x-3} \\cdot \\dfrac{x+3}{x+1}",
        answer_tex="\\dfrac{x+3}{x-3} \\quad (x \\neq -1, 3)",
        answer_norm="(x+3)/(x-3)",
        steps=[
            step("Cancel common factor", "x+1 \\text{ in numerator and denominator}"),
            step("Multiply", "\\dfrac{x+3}{x-3}"),
            step("Domain", "x \\neq -1, 3 \\text{ (original)}"),
        ],
    )


def _divide_rationals():
    # (x²-1)/(x+2) ÷ (x-1)/(x+3) = (x²-1)(x+3)/((x+2)(x-1)) = (x+1)(x+3)/(x+2)
    return problem(
        problem_tex="\\dfrac{x^2-1}{x+2} \\div \\dfrac{x-1}{x+3}",
        answer_tex="\\dfrac{x+1}{x+2}(x+3)",
        answer_norm="(x+1)(x+3)/(x+2)",
        steps=[
            step("Multiply by reciprocal", "\\dfrac{x^2-1}{x+2} \\cdot \\dfrac{x+3}{x-1}"),
            step("Factor x²-1", "\\dfrac{(x-1)(x+1)}{x+2} \\cdot \\dfrac{x+3}{x-1}"),
            step("Cancel x-1", "\\dfrac{(x+1)(x+3)}{x+2}"),
        ],
    )


# ── rational3 — add/subtract rational expressions ──────────────────────────────

def _add_rationals():
    # 1/(x+1) + 1/(x+2) = (x+2+x+1)/((x+1)(x+2)) = (2x+3)/((x+1)(x+2))
    return problem(
        problem_tex="\\dfrac{1}{x+1} + \\dfrac{1}{x+2}",
        answer_tex="\\dfrac{2x+3}{(x+1)(x+2)}",
        answer_norm="(2x+3)/((x+1)(x+2))",
        steps=[
            step("Find LCD", "(x+1)(x+2)"),
            step("Rewrite each fraction", "\\dfrac{x+2}{(x+1)(x+2)} + \\dfrac{x+1}{(x+1)(x+2)}"),
            step("Add numerators", "\\dfrac{(x+2)+(x+1)}{(x+1)(x+2)} = \\dfrac{2x+3}{(x+1)(x+2)}"),
        ],
    )


def _subtract_rationals():
    # 2x/(x+3) - 3/(x-1) = (2x²-2x-9)/((x+3)(x-1))... 
    # Let's use simpler: 1/(x+1) - 1/x = (x-(x+1))/(x(x+1)) = -1/(x(x+1))
    return problem(
        problem_tex="\\dfrac{1}{x+1} - \\dfrac{1}{x}",
        answer_tex="-\\dfrac{1}{x(x+1)}",
        answer_norm="-1/(x(x+1))",
        steps=[
            step("Find LCD", "x(x+1)"),
            step("Rewrite each fraction", "\\dfrac{x}{x(x+1)} - \\dfrac{x+1}{x(x+1)}"),
            step("Subtract numerators", "\\dfrac{x-(x+1)}{x(x+1)} = \\dfrac{-1}{x(x+1)}"),
        ],
    )


# ── rational4 — complex fractions ─────────────────────────────────────────────

def _simplify_complex_frac():
    # (1 + 1/x) / (1 - 1/x) = ((x+1)/x) / ((x-1)/x) = (x+1)/(x-1)
    x_val = R(2, 6)
    return problem(
        problem_tex="\\dfrac{1 + \\dfrac{1}{x}}{1 - \\dfrac{1}{x}}",
        answer_tex="\\dfrac{x+1}{x-1} \\quad (x \\neq 0, \\pm 1)",
        answer_norm="(x+1)/(x-1)",
        steps=[
            step("Rewrite numerator", "1 + \\dfrac{1}{x} = \\dfrac{x+1}{x}"),
            step("Rewrite denominator", "1 - \\dfrac{1}{x} = \\dfrac{x-1}{x}"),
            step("Divide", "\\dfrac{x+1}{x} \\cdot \\dfrac{x}{x-1} = \\dfrac{x+1}{x-1}"),
        ],
    )


# ── rational5 — solve rational equations ──────────────────────────────────────

def _solve_rational_equation():
    # 1/x + 1/3 = 1/2 → multiply by 6x: 6 + 2x = 3x → x = 6
    x_val = R(2, 10)
    a = pick([2, 3])
    b = pick([4, 5, 6])
    while x_val == a or x_val == b:
        x_val = R(2, 10)
    rhs = 1/a - 1/b + 1/x_val
    return problem(
        problem_tex=f"\\dfrac{{1}}{{x}} + \\dfrac{{1}}{{{a}}} = \\dfrac{{1}}{{{b}}}",
        answer_tex=f"x = {x_val}",
        answer_norm=f"x={x_val}",
        steps=[
            step("Multiply by LCD", f"x \\cdot {a} \\cdot {b} = {a*b*x_val}x"),
            step("Clear denominators", f"{a*b} + {b}x = {a}x"),
            step("Solve", f"{b}x - {a}x = {a*b} \\implies ({b-a})x = {a*b} \\implies x = {x_val}"),
        ],
    )


def _rational_word_rate():
    # "Pump A fills pool in 4 hours, pump B in 6 hours. Together?"
    # Rate A = 1/4, Rate B = 1/6 → together = 1/4 + 1/6 = 5/12 → 12/5 = 2.4 hours
    a = pick([3, 4, 5])
    b = pick([5, 6, 7, 8])
    time_together = 1 / (1/a + 1/b)
    return problem(
        problem_tex=f"\\text{{Pump A fills a pool in {a}h, pump B in {b}h. How long together?}}",
        answer_tex=f"\\dfrac{{{a*b}}}{{{a+b}}} = {time_together:.2f} \\text{{ hours}}",
        answer_norm=f"{a*b/(a+b):.2f}",
        steps=[
            step("Rates", f"\\text{{A: }} 1/{a}, \\text{{ B: }} 1/{b}"),
            step("Combined rate", f"1/{a} + 1/{b} = ({b}+{a})/({a*b}) = {a+b}/{a*b}"),
            step("Time = 1/rate", f"\\dfrac{{{a*b}}}{{{a+b}}} = {time_together:.2f} \\text{{ h}}"),
        ],
    )


rational1 = [_simplify_rational, _simplify_rational_complex]
rational2 = [_multiply_rationals, _divide_rationals]
rational3 = [_add_rationals, _subtract_rationals]
rational4 = [_simplify_complex_frac]
rational5 = [_solve_rational_equation, _rational_word_rate]

POOLS = {1: rational1, 2: rational2, 3: rational3, 4: rational4, 5: rational5}