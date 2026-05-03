from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── sequences1 — arithmetic sequences ─────────────────────────────────────────

def _nth_arithmetic():
    # a_n = a_1 + (n-1)d
    a1 = R(1, 10)
    d = R(1, 8)
    n = pick([5, 8, 10, 12, 15])
    an = a1 + (n - 1) * d
    return problem(
        problem_tex=f"\\text{{Arithmetic sequence with }} a_1 = {a1}, d = {d}. \\text{{ Find }} a_{n}.",
        answer_tex=f"a_{n} = {a1} + ({n}-1)({d}) = {an}",
        answer_norm=f"a{n}={an}",
        steps=[
            step("Arithmetic formula", f"a_n = a_1 + (n-1)d"),
            step("Substitute", f"a_{n} = {a1} + ({n}-1)({d})"),
            step("Simplify", f"= {a1} + {(n-1)*d} = {an}"),
        ],
    )


def _sum_arithmetic():
    # S_n = n(a_1 + a_n)/2
    a1 = R(1, 8)
    d = R(1, 5)
    n = pick([5, 8, 10, 12])
    an = a1 + (n - 1) * d
    s_n = n * (a1 + an) // 2
    return problem(
        problem_tex=f"\\text{{Arithmetic sequence: }} a_1 = {a1}, d = {d}, n = {n}. \\text{{ Find the sum of the first {n} terms.}}",
        answer_tex=f"S_{n} = \\frac{{{n}({a1} + {an})}}{{2}} = {s_n}",
        answer_norm=f"S{n}={s_n}",
        steps=[
            step("Sum formula", f"S_n = \\frac{{n(a_1 + a_n)}}{{2}}"),
            step("Find a_n", f"a_n = {a1} + ({n}-1)({d}) = {an}"),
            step("Substitute", f"S_{n} = \\frac{{{n}({a1} + {an})}}{{2}} = {s_n}"),
        ],
    )


# ── sequences2 — geometric sequences ─────────────────────────────────────────

def _nth_geometric():
    # a_n = a_1 * r^(n-1)
    a1 = R(1, 5)
    r = pick([2, 3, 4, 5])
    n = pick([4, 5, 6, 7])
    an = a1 * r ** (n - 1)
    return problem(
        problem_tex=f"\\text{{Geometric sequence with }} a_1 = {a1}, r = {r}. \\text{{ Find }} a_{n}.",
        answer_tex=f"a_{n} = {a1} \\cdot {r}^{{{n}-1}} = {an}",
        answer_norm=f"a{n}={an}",
        steps=[
            step("Geometric formula", f"a_n = a_1 \\cdot r^{{n-1}}"),
            step("Substitute", f"a_{n} = {a1} \\cdot {r}^{{{n}-1}}"),
            step("Simplify", f"= {an}"),
        ],
    )


def _sum_geometric():
    # S_n = a_1(1 - r^n)/(1 - r)
    a1 = R(1, 4)
    r = pick([2, 3])
    n = pick([4, 5, 6])
    s_n = a1 * (r ** n - 1) // (r - 1)
    return problem(
        problem_tex=f"\\text{{Geometric sequence: }} a_1 = {a1}, r = {r}, n = {n}. \\text{{ Find sum of first {n} terms.}}",
        answer_tex=f"S_{n} = {a1}\\dfrac{{{r}^{n} - 1}}{{{r} - 1}} = {s_n}",
        answer_norm=f"S{n}={s_n}",
        steps=[
            step("Geometric sum formula", f"S_n = a_1 \\dfrac{{1 - r^n}}{{1 - r}} = a_1 \\dfrac{{r^n - 1}}{{r - 1}}"),
            step("Substitute", f"S_{n} = {a1} \\cdot \\dfrac{{{r}^{n} - 1}}{{{r} - 1}}"),
            step("Compute", f"= {a1} \\cdot \\dfrac{{{r**n} - 1}}{{{r-1}}} = {s_n}"),
        ],
    )


# ── sequences3 — infinite geometric series ───────────────────────────────────

def _infinite_geometric():
    # S_inf = a_1/(1 - r), for |r| < 1
    a1 = R(1, 5)
    r_num = pick([1, 2])
    r_den = pick([3, 4, 5])
    r = r_num / r_den
    s_inf = a1 / (1 - r)
    return problem(
        problem_tex=f"\\text{{Infinite geometric series: }} a_1 = {a1}, r = {r_num}/{r_den}. \\text{{ Find the sum.}}",
        answer_tex=f"S_\\infty = \\dfrac{{{a1}}}{{1 - {r}}} = {a1 * r_den // (r_den - r_num)}",
        answer_norm=f"Sinf={a1 * r_den // (r_den - r_num)}",
        steps=[
            step("Check |r| < 1", f"|r| = {r_num}/{r_den} < 1 \\checkmark"),
            step("Infinite sum formula", f"S_\\infty = \\dfrac{{a_1}}{{1-r}}"),
            step("Substitute", f"= \\dfrac{{{a1}}}{{1 - {r}}} = {a1 * r_den // (r_den - r_num)}"),
        ],
    )


# ── sequences4 — word problems ───────────────────────────────────────────────

def _arithmetic_word():
    # "A clock tower has 20 bells. The largest weighs 500kg and each subsequent weighs 15kg less."
    a1 = pick([300, 400, 500])
    d = -pick([10, 15, 20])
    n = pick([10, 12, 15, 20])
    an = a1 + (n - 1) * d
    s_n = n * (a1 + an) // 2
    return problem(
        problem_tex=f"\\text{{A clock tower has {n} bells. Largest = {a1}kg, each lower weighs {abs(d)}kg less. Find weight of smallest bell and total weight.}}",
        answer_tex=f"\\text{{Smallest: }} {an} \\text{{ kg}}; \\quad \\text{{Total: }} {s_n} \\text{{ kg}}",
        answer_norm=f"smallest={an},total={s_n}",
        steps=[
            step("Arithmetic sequence", f"a_1 = {a1}, d = {d}"),
            step("Find a_n", f"a_{n} = {a1} + ({n}-1)({d}) = {an}"),
            step("Sum", f"S_{n} = \\frac{{{n}({a1} + {an})}}{{2}} = {s_n}"),
        ],
    )


# ── sequences5 — identify sequence type ──────────────────────────────────────

def _identify_arithmetic_or_geometric():
    # 2, 6, 18, 54, ... → geometric, r=3
    a1 = pick([1, 2, 3])
    r = pick([2, 3, 4])
    terms = [a1 * r ** i for i in range(4)]
    return problem(
        problem_tex=f"{terms[0]}, {terms[1]}, {terms[2]}, {terms[3]}, \\dots. \\text{{ What type of sequence is this?}}",
        answer_tex=f"\\text{{Geometric with }} r = {r}",
        answer_norm=f"geometric:r={r}",
        steps=[
            step("Check ratio", f"\\dfrac{{{terms[1]}}}{{{terms[0]}}} = {r}, \\quad \\dfrac{{{terms[2]}}}{{{terms[1]}}} = {r}"),
            step("Constant ratio", f"\\text{{Geometric sequence with }} r = {r}"),
        ],
    )


sequences1 = [_nth_arithmetic, _sum_arithmetic]
sequences2 = [_nth_geometric, _sum_geometric]
sequences3 = [_infinite_geometric]
sequences4 = [_arithmetic_word]
sequences5 = [_identify_arithmetic_or_geometric]

POOLS = {1: sequences1, 2: sequences2, 3: sequences3, 4: sequences4, 5: sequences5}