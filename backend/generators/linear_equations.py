from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── linear1 — solve ax + b = c ─────────────────────────────────────────────────

def _solve_linear_basic():
    # 3x + 7 = 16 → x = 3
    a = R(2, 9)
    b = R(-10, 10)
    c = R(-20, 20)
    # Ensure integer solution
    n = R(-20, 20)
    x = n
    c_val = a * x + b
    return problem(
        problem_tex=f"{a}x + {b} = {c_val}",
        answer_tex=f"x = {x}",
        answer_norm=f"x={x}",
        steps=[
            step("Subtract " + str(b), f"{a}x = {c_val} - ({b}) = {c_val - b}"),
            step("Divide by " + str(a), f"x = \\dfrac{{{c_val - b}}}{{{a}}} = {x}"),
        ],
    )


def _solve_linear_fractions():
    # (x + 3)/4 = 2 → x = 5
    num = R(-8, 8)
    den = R(2, 6)
    x = R(-10, 10)
    rhs = R(1, 10)
    val = den * rhs - num
    return problem(
        problem_tex=f"\\dfrac{{x {sign_str(num)}}}{{{den}}} = {rhs}",
        answer_tex=f"x = {val}",
        answer_norm=f"x={val}",
        steps=[
            step("Multiply both sides by " + str(den), f"x {sign_str(num)} = {den} \\cdot {rhs} = {den * rhs}"),
            step("Isolate x", f"x = {den * rhs} {sign_str(-num)}"),
        ],
    )


# ── linear2 — word problem leading to linear ────────────────────────────────────

def _linear_word_basic():
    # "A number plus 5 equals 12. Find the number."
    # x + 5 = 12 → x = 7
    x = R(1, 20)
    a = R(1, 10)
    b = a * x
    return problem(
        problem_tex=f"\\text{{A number multiplied by }} {a} \\text{{ equals }} {b}. \\text{{ What is the number?}}",
        answer_tex=f"x = {x}",
        answer_norm=f"x={x}",
        steps=[
            step("Set up equation", f"{a}x = {b}"),
            step("Divide by " + str(a), f"x = \\dfrac{{{b}}}{{{a}}} = {x}"),
        ],
    )


def _linear_word_two_step():
    # "If 3 is added to a number and the result is multiplied by 4, you get 20"
    # 4(x + 3) = 20 → x = 2
    a = R(2, 5)
    b = R(1, 8)
    x = R(1, 10)
    result = a * (x + b)
    return problem(
        problem_tex=f"\\text{{If }} {a} \\text{{ is added to a number and multiplied by }} {a}, \\text{{ you get }} {result}. \\text{{ Find the number.}}",
        answer_tex=f"x = {x}",
        answer_norm=f"x={x}",
        steps=[
            step("Set up equation", f"{a}(x + {b}) = {result}"),
            step("Divide by " + str(a), f"x + {b} = \\dfrac{{{result}}}{{{a}}} = {result // a}"),
            step("Subtract " + str(b), f"x = {result // a} - {b} = {x}"),
        ],
    )


# ── linear3 — linear in terms of variable ───────────────────────────────────────

def _solve_for_variable():
    # PV = nRT → solve for T: T = PV/(nR)
    # Use simple numeric substitution: P=2, V=4, n=1, R=3
    P = pick([1, 2, 3])
    V = pick([2, 4])
    n = 1
    R = pick([2, 3, 4])
    T_val = (P * V) / (n * R)
    if T_val == int(T_val):
        T_val = int(T_val)

    return problem(
        problem_tex=f"\\text{{Given }} P = {P}, V = {V}, n = {n}, R = {R}, \\text{{ solve }} PV = nRT \\text{{ for }} T.",
        answer_tex=f"T = \\dfrac{{{P * V}}}{{{n * R}}} = {T_val}",
        answer_norm=f"T={T_val}",
        steps=[
            step("Start with formula", "PV = nRT"),
            step("Divide both sides by nR", f"T = \\dfrac{{PV}}{{nR}} = \\dfrac{{{P} \\cdot {V}}}{{{n} \\cdot {R}}}"),
            step("Compute", f"= \\dfrac{{{P * V}}}{{{n * R}}} = {T_val}"),
        ],
    )


# ── linear4 — linear inequalities ─────────────────────────────────────────────

def _solve_linear_inequality():
    # 2x - 3 < 7 → x < 5
    a = R(2, 6)
    b = R(-8, 8)
    c_val = R(1, 15)
    rhs = a * R(1, 5) + b
    return problem(
        problem_tex=f"{a}x {sign_str(b)} < {rhs}",
        answer_tex=f"x < {rhs - b} \\quad (\\text{{if }} {a} > 0)",
        answer_norm=f"x<{rhs-b}",
        steps=[
            step("Isolate term", f"{a}x {sign_str(b)} < {rhs} \\implies {a}x < {rhs} - ({b}) = {rhs - b}"),
            step("Divide by " + str(a), f"x < \\dfrac{{{rhs - b}}}{{{a}}} = {rhs - b}"),
        ],
    )


# ── linear5 — combined ────────────────────────────────────────────────────────

def _linear_application_consecutive():
    # "Find three consecutive integers that sum to 45"
    # x + (x+1) + (x+2) = 45 → x = 14
    total = pick([30, 45, 54, 63])
    x = (total - 3) // 3
    return problem(
        problem_tex=f"\\text{{Three consecutive integers sum to }} {total}. \\text{{ Find them.}}",
        answer_tex=f"x = {x}, \\quad x+1 = {x+1}, \\quad x+2 = {x+2}",
        answer_norm=f"{x},{x+1},{x+2}",
        steps=[
            step("Set up equation", f"x + (x+1) + (x+2) = {total}"),
            step("Combine like terms", f"3x + 3 = {total} \\implies 3x = {total - 3}"),
            step("Solve", f"x = \\dfrac{{{total - 3}}}{{3}} = {x}"),
            step("Numbers", f"{x}, {x+1}, {x+2}"),
        ],
    )


def _linear_age_problem():
    # "Alice is twice as old as Bob. In 5 years, the sum of their ages will be 40."
    # a = 2b, (a+5)+(b+5)=40 → 2b+5+b+5=40 → 3b=30 → b=10, a=20
    b = R(5, 15)
    a = 2 * b
    years = pick([3, 5, 8])
    future_sum = (a + years) + (b + years)
    return problem(
        problem_tex=f"\\text{{Alice is twice as old as Bob. In {years} years, the sum of their ages will be }} {future_sum}. \\text{{ Find their current ages.}}",
        answer_tex=f"\\text{{Bob: }} {b}, \\quad \\text{{Alice: }} {a}",
        answer_norm=f"bob={b},alice={a}",
        steps=[
            step("Let Bob's age = x", f"\\text{{Alice's age}} = 2x"),
            step("Future ages", f"x + {years} + 2x + {years} = {future_sum}"),
            step("Solve", f"3x + {2*years} = {future_sum} \\implies 3x = {future_sum - 2*years} \\implies x = {b}"),
        ],
    )


linear1 = [_solve_linear_basic, _solve_linear_fractions]
linear2 = [_linear_word_basic, _linear_word_two_step]
linear3 = [_solve_for_variable]
linear4 = [_solve_linear_inequality]
linear5 = [_linear_application_consecutive, _linear_age_problem]

POOLS = {1: linear1, 2: linear2, 3: linear3, 4: linear4, 5: linear5}