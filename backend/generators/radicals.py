from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── radical1 — simplify radicals ───────────────────────────────────────────────

def _simplify_sqrt():
    # sqrt(72) = sqrt(36*2) = 6sqrt(2)
    n = pick([8, 12, 18, 20, 24, 28, 32, 40, 45, 48, 50, 52, 54, 56, 60, 63, 72, 75, 80, 98])
    factors = []
    temp = n
    for p in [4, 9, 16, 25, 36, 49, 64, 81, 100]:
        while temp % p == 0:
            factors.append(p)
            temp //= p
    if temp > 1:
        factors.append(temp)
    remaining_inside = temp if temp > 1 else 1
    outside = 1
    inside = n
    for f in [4, 9, 16, 25, 36, 49, 64, 81, 100]:
        while inside % f == 0:
            outside *= int(f ** 0.5)
            inside //= f
    inside = inside if inside > 1 else 1

    return problem(
        problem_tex=f"\\sqrt{{{n}}}",
        answer_tex=f"{outside}\\sqrt{{{inside}}}" if inside != 1 else str(outside),
        answer_norm=f"{outside}*sqrt({inside})" if inside != 1 else str(outside),
        steps=[
            step("Prime factorization", str(n)),
            step("Group squares", f"{n} = {outside}^2 \\cdot {inside}"),
            step("Simplify", f"\\sqrt{{{n}}} = {outside}\\sqrt{{{inside}}}"),
        ],
    )


def _rationalize_denominator():
    # 1/sqrt(3) = sqrt(3)/3
    return problem(
        problem_tex="\\dfrac{1}{\\sqrt{3}}",
        answer_tex="\\dfrac{\\sqrt{3}}{3}",
        answer_norm="sqrt(3)/3",
        steps=[
            step("Multiply by sqrt(3)/sqrt(3)", "\\dfrac{1}{\\sqrt{3}} \\cdot \\dfrac{\\sqrt{3}}{\\sqrt{3}}"),
            step("Simplify", "\\dfrac{\\sqrt{3}}{3}"),
        ],
    )


# ── radical2 — add/subtract radicals ──────────────────────────────────────────

def _add_radicals():
    # 2sqrt(5) + 3sqrt(5) = 5sqrt(5)
    a = R(2, 8)
    b = R(2, 8)
    return problem(
        problem_tex=f"{a}\\sqrt{{5}} + {b}\\sqrt{{5}}",
        answer_tex=f"{a+b}\\sqrt{{5}}",
        answer_norm=f"{a+b}*sqrt(5)",
        steps=[
            step("Same radical", f"{a}\\sqrt{{5}} + {b}\\sqrt{{5}} = ({a}+{b})\\sqrt{{5}}"),
            step("Simplify", f"= {a+b}\\sqrt{{5}}"),
        ],
    )


def _subtract_radicals():
    # 7sqrt(2) - 3sqrt(2) = 4sqrt(2)
    a = R(4, 10)
    b = R(1, a - 1)
    return problem(
        problem_tex=f"{a}\\sqrt{{3}} - {b}\\sqrt{{3}}",
        answer_tex=f"{a-b}\\sqrt{{3}}",
        answer_norm=f"{a-b}*sqrt(3)",
        steps=[
            step("Same radical, combine coefficients", f"({a} - {b})\\sqrt{{3}}"),
            step("Simplify", f"= {a-b}\\sqrt{{3}}"),
        ],
    )


# ── radical3 — multiply radicals ──────────────────────────────────────────────

def _multiply_radicals():
    # sqrt(3) * sqrt(12) = sqrt(36) = 6
    return problem(
        problem_tex="\\sqrt{3} \\cdot \\sqrt{12}",
        answer_tex="6",
        answer_norm="6",
        steps=[
            step("Use sqrt(a)*sqrt(b) = sqrt(ab)", "\\sqrt{3} \\cdot \\sqrt{12} = \\sqrt{36}"),
            step("Simplify", "6"),
        ],
    )


def _foil_radicals():
    # (sqrt(2) + 3)(sqrt(2) - 1) = 2 + 3sqrt(2) - sqrt(2) - 3 = sqrt(2) - 1
    return problem(
        problem_tex="(\\sqrt{2} + 3)(\\sqrt{2} - 1)",
        answer_tex="\\sqrt{2} - 1",
        answer_norm="sqrt(2)-1",
        steps=[
            step("FOIL", "(\\sqrt{2})^2 + \\sqrt{2}(-1) + 3\\sqrt{2} + 3(-1)"),
            step("Simplify each", "2 - \\sqrt{2} + 3\\sqrt{2} - 3"),
            step("Combine like terms", "-1 + 2\\sqrt{2} = \\sqrt{2} - 1"),
        ],
    )


# ── radical4 — solve radical equations ───────────────────────────────────────

def _solve_radical_basic():
    # sqrt(x) = 5 → x = 25
    a = R(2, 10)
    a2 = a * a
    return problem(
        problem_tex=f"\\sqrt{{x}} = {a}",
        answer_tex=f"x = {a2}",
        answer_norm=f"x={a2}",
        steps=[
            step("Square both sides", "(\\sqrt{x})^2 = {}^2 \\implies x = {a2}"),
            step("Check", f"\\sqrt{{{a2}}} = {a} \\checkmark"),
        ],
    )


def _solve_radical_linear():
    # sqrt(2x + 1) = 3 → 2x + 1 = 9 → x = 4
    b = pick([1, 2, 3])
    c_val = pick([3, 5, 7])
    a = 2
    result = (c_val * c_val - b) / a
    if result == int(result):
        result = int(result)

    return problem(
        problem_tex=f"\\sqrt{{{a}x {sign_str(b)}}} = {c_val}",
        answer_tex=f"x = {result}",
        answer_norm=f"x={result}",
        steps=[
            step("Square both sides", f"{a}x {sign_str(b)} = {c_val}^2 = {c_val*c_val}"),
            step("Isolate x", f"{a}x = {c_val*c_val} {sign_str(-b)} \\implies x = {(c_val*c_val - b)//a}"),
            step("Check", f"\\sqrt{{{a} \\cdot {result} {sign_str(b)}}} = \\sqrt{{{a*result + b}}} = \\sqrt{{{c_val*c_val}}} = {c_val} \\checkmark"),
        ],
    )


# ── radical5 — rational exponents ─────────────────────────────────────────────

def _rational_exponent():
    # 8^(2/3) = (8^(1/3))^2 = 2^2 = 4
    base = pick([8, 27, 16, 64, 125])
    exp_num = pick([2, 3])
    exp_den = pick([3, 2])
    value = round(base ** (exp_num / exp_den))

    return problem(
        problem_tex=f"{base}^{{{exp_num}/{exp_den}}}",
        answer_tex=f"{value}",
        answer_norm=str(value),
        steps=[
            step("Write as root then power", f"{base}^{{{exp_num}/{exp_den}}} = ({base}^{{1/{exp_den}}})^{{{exp_num}}}"),
            step("Compute", f"\\sqrt[{exp_den}]{{{base}}} = {int(round(base ** (1/exp_den)))}, \\quad ({int(round(base ** (1/exp_den)))})^{{{exp_num}}} = {value}"),
        ],
    )


def _radical_to_rational():
    # sqrt(x^4) = x^2 (for x >= 0)
    n = pick([2, 3, 4, 5])
    return problem(
        problem_tex=f"\\sqrt[{n}]{{x^{{{n*2}}}}}",
        answer_tex="x^2",
        answer_norm="x^2",
        steps=[
            step("Apply exponent rule", f"\\sqrt[{n}]{{x^{{{n*2}}}}} = x^{{{n*2}/{n}}}"),
            step("Simplify", "= x^2"),
        ],
    )


radical1 = [_simplify_sqrt, _rationalize_denominator]
radical2 = [_add_radicals, _subtract_radicals]
radical3 = [_multiply_radicals, _foil_radicals]
radical4 = [_solve_radical_basic, _solve_radical_linear]
radical5 = [_rational_exponent, _radical_to_rational]

POOLS = {1: radical1, 2: radical2, 3: radical3, 4: radical4, 5: radical5}