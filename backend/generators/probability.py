from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── probability1 — basic probability ─────────────────────────────────────────

def _basic_prob():
    # P(E) = favorable / total outcomes
    # "Roll a die. What is P(rolling a 3 or 5)?"
    total = 6
    favorable = 2
    return problem(
        problem_tex="\\text{Roll a fair six-sided die. What is } P(\\text{rolling a 3 or 5})?",
        answer_tex=f"\\dfrac{{{favorable}}}{{{total}}}",
        answer_norm=f"{favorable}/{total}",
        steps=[
            step("Count favorable outcomes", "{3, 5} = 2 outcomes"),
            step("Count total outcomes", "{1,2,3,4,5,6} = 6 outcomes"),
            step("Compute probability", f"P = \\dfrac{{2}}{{6}} = \\dfrac{{{favorable}}}{{{total}}}"),
        ],
    )


def _complement_prob():
    # P(E') = 1 - P(E)
    p_num = pick([1, 2, 3, 4, 5])
    p_den = pick([p_num+1, p_num+2, p_num+3, p_num+4])
    p_e = f"\\dfrac{{{p_num}}}{{{p_den}}}"
    p_not_e = f"\\dfrac{{{p_den - p_num}}}{{{p_den}}}"
    return problem(
        problem_tex=f"\\text{{If }} P(E) = {p_e}, \\text{{ find }} P(E')",
        answer_tex=p_not_e,
        answer_norm=f"({p_den-p_num})/{p_den}",
        steps=[
            step("Complement rule", "P(E') = 1 - P(E)"),
            step("Substitute", f"= 1 - \\dfrac{{{p_num}}}{{{p_den}}} = \\dfrac{{{p_den} - {p_num}}}{{{p_den}}}"),
        ],
    )


# ── probability2 — independent/dependent ─────────────────────────────────────

def _independent_prob():
    # P(A and B) = P(A) * P(B) for independent events
    # Coin flip and die roll
    return problem(
        problem_tex="\\text{Flip a coin and roll a die. What is } P(\\text{heads and 4})?",
        answer_tex="\\dfrac{1}{12}",
        answer_norm="1/12",
        steps=[
            step("P(heads)", "\\dfrac{1}{2}"),
            step("P(4)", "\\dfrac{1}{6}"),
            step("Multiply (independence)", "\\dfrac{1}{2} \\cdot \\dfrac{1}{6} = \\dfrac{1}{12}"),
        ],
    )


def _dependent_prob():
    # P(A and B) = P(A) * P(B|A) for dependent events
    # "Draw 2 aces from a deck without replacement"
    return problem(
        problem_tex="\\text{Draw 2 aces from a standard 52-card deck without replacement. Find } P(\\text{both aces}).",
        answer_tex="\\dfrac{4}{52} \\cdot \\dfrac{3}{51} = \\dfrac{1}{221}",
        answer_norm="1/221",
        steps=[
            step("P(first ace)", "\\dfrac{4}{52}"),
            step("P(second ace | first ace)", "\\dfrac{3}{51} \\quad (\\text{one ace already removed})"),
            step("Multiply", "\\dfrac{4}{52} \\cdot \\dfrac{3}{51} = \\dfrac{12}{2652} = \\dfrac{1}{221}"),
        ],
    )


# ── probability3 — conditional probability ────────────────────────────────────

def _conditional_prob():
    # P(B|A) = P(A and B) / P(A)
    # Table problem: P(disease|positive test)
    return problem(
        problem_tex="\\text{Given } P(A) = 0.3, P(B) = 0.5, P(A \\cap B) = 0.15. \\text{ Find } P(B|A).",
        answer_tex="\\dfrac{0.15}{0.3} = 0.5",
        answer_norm="0.5",
        steps=[
            step("Conditional formula", "P(B|A) = \\dfrac{P(A \\cap B)}{P(A)}"),
            step("Substitute", "= \\dfrac{0.15}{0.3}"),
            step("Simplify", "= 0.5"),
        ],
    )


# ── probability4 — permutations/combinations ────────────────────────────────

def _permutation():
    # P(n,r) = n!/(n-r)!
    n = pick([5, 6, 7, 8])
    r = pick([2, 3])
    val = 1
    for i in range(r):
        val *= (n - i)
    return problem(
        problem_tex=f"\\text{{How many ways to arrange {r} books from {n} different books?}}",
        answer_tex=f"P({n},{r}) = \\dfrac{{{n}!}}{{({n}-{r})!}} = {val}",
        answer_norm=str(val),
        steps=[
            step("Permutation formula", f"P(n,r) = \\dfrac{{n!}}{{(n-r)!}}"),
            step("Substitute", f"P({n},{r}) = \\dfrac{{{n}!}}{{({n}-{r})!}}"),
            step("Compute", f"= {n} \\cdot {n-1}" + (f" \\cdot {n-2}" if r == 3 else "") + f" = {val}"),
        ],
    )


def _combination():
    # C(n,r) = n!/(r!(n-r)!)
    n = pick([6, 7, 8, 9, 10])
    r = pick([2, 3, 4])
    val = 1
    for i in range(r):
        val *= (n - i)
    for i in range(r):
        val //= (r - i)
    return problem(
        problem_tex=f"\\text{{How many ways to choose {r} people from {n}?}}",
        answer_tex=f"C({n},{r}) = \\dfrac{{{n}!}}{{{r}!({n}-{r})!}} = {val}",
        answer_norm=str(val),
        steps=[
            step("Combination formula", f"C(n,r) = \\dfrac{{n!}}{{r!(n-r)!}}"),
            step("Substitute", f"C({n},{r}) = \\dfrac{{{n}!}}{{{r}!({n}-{r})!}}"),
            step("Compute", f"= {val}"),
        ],
    )


# ── probability5 — expected value ─────────────────────────────────────────────

def _expected_value():
    # E(X) = sum of x * P(x)
    # Fair game: E = 0
    values = [1, 2, 3, 4, 5, 6]
    probs = [1/6] * 6
    ev = sum(v * p for v, p in zip(values, probs))
    return problem(
        problem_tex="\\text{A fair die: each number 1-6 has probability } 1/6. \\text{ Find the expected value.}",
        answer_tex=f"E(X) = {ev:.1f}",
        answer_norm=str(ev),
        steps=[
            step("Formula", "E(X) = \\sum x \\cdot P(x)"),
            step("Compute", f"= 1(1/6) + 2(1/6) + 3(1/6) + 4(1/6) + 5(1/6) + 6(1/6)"),
            step("Simplify", f"= (1+2+3+4+5+6)/6 = {21}/6 = {ev:.1f}"),
        ],
    )


probability1 = [_basic_prob, _complement_prob]
probability2 = [_independent_prob, _dependent_prob]
probability3 = [_conditional_prob]
probability4 = [_permutation, _combination]
probability5 = [_expected_value]

POOLS = {1: probability1, 2: probability2, 3: probability3, 4: probability4, 5: probability5}