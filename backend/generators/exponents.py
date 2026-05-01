from math_utils import R, pick, lcm, simplify_frac, frac_to_tex, exp_frac_to_norm, sign_str
from problem_builder import problem, step

CONFIG = {
    "sameBase_ab":        (1, 12),
    "divideBase_b":       (1, 12),
    "divideBase_aExtra":  (1, 8),
    "powerPower_ab":      (2, 5),
    "negExp_a":           (1, 5),
    "radicalToExp_m":     (1, 5),
    "radicalToExp_n":     [2, 3, 4],
    "fracExpArith_den":   [2, 3, 4, 5, 6],
    "coeffRewrite_k":     (2, 15),
    "coeffRewrite_a":     (1, 5),
    "higherRadical_n":    [3, 4, 5],
    "higherRadical_m":    (2, 13),
}


# ─── diff1 ───

def _same_base_product():
    a = R(*CONFIG["sameBase_ab"])
    b = R(*CONFIG["sameBase_ab"])
    return problem(
        problem_tex=f"x^{{{a}}} \\cdot x^{{{b}}}",
        answer_tex=f"x^{{{a+b}}}",
        answer_norm=f"x^{a+b}",
        steps=[step("Product rule", f"x^{{{a}+{b}}}=x^{{{a+b}}}", "x^a·x^b = x^(a+b)")],
    )


def _quotient_same_base():
    b = R(*CONFIG["divideBase_b"])
    extra = R(*CONFIG["divideBase_aExtra"])
    a = b + extra
    diff = a - b
    return problem(
        problem_tex=f"\\dfrac{{x^{{{a}}}}}{{x^{{{b}}}}}",
        answer_tex=f"x^{{{diff}}}",
        answer_norm=f"x^{diff}",
        steps=[step("Quotient rule", f"x^{{{a}-{b}}}=x^{{{diff}}}", "x^a/x^b = x^(a-b)")],
    )


def _power_of_power():
    a = R(*CONFIG["powerPower_ab"])
    b = R(*CONFIG["powerPower_ab"])
    return problem(
        problem_tex=f"(x^{{{a}}})^{{{b}}}",
        answer_tex=f"x^{{{a*b}}}",
        answer_norm=f"x^{a*b}",
        steps=[step("Power rule", f"x^{{{a}\\cdot{b}}}=x^{{{a*b}}}", "(x^a)^b = x^(ab)")],
    )


def _neg_exp():
    a = R(*CONFIG["negExp_a"])
    return problem(
        problem_tex=f"x^{{-{a}}}",
        answer_tex=f"\\dfrac{{1}}{{x^{{{a}}}}}",
        answer_norm=f"1/x^{a}",
        steps=[step("Negative exponent rule", f"x^{{-{a}}}=\\frac{{1}}{{x^{{{a}}}}}", "x^(-a) = 1/x^a")],
    )


diff1 = [_same_base_product, _quotient_same_base, _power_of_power, _neg_exp]


# ─── diff2 ───

def _radical_to_exp():
    m = R(*CONFIG["radicalToExp_m"])
    n = pick(CONFIG["radicalToExp_n"])
    sn, sd = simplify_frac(m, n)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"\\sqrt[{n}]{{x^{{{m}}}}}",
        answer_tex=f"x^{{{frac_tex}}}",
        answer_norm=f"x^({sn}/{sd})",
        steps=[
            step("Radical to exponent", f"\\sqrt[n]{{x^m}}=x^{{m/n}}"),
            step("Apply", f"x^{{{m}/{n}}}=x^{{{frac_tex}}}", f"Simplified: {m}/{n} = {sn}/{sd}" if sn != m else ""),
        ],
    )


def _frac_exp_arith():
    den = CONFIG["fracExpArith_den"]
    d1 = pick(den); d2 = pick(den)
    n1 = R(1, 3); n2 = R(1, 3)
    L = lcm(d1, d2)
    total = n1 * (L // d1) + n2 * (L // d2)
    sn, sd = simplify_frac(total, L)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"x^{{{n1}/{d1}}} \\cdot x^{{{n2}/{d2}}}",
        answer_tex=f"x^{{{frac_tex}}}",
        answer_norm=exp_frac_to_norm(sn, sd),
        steps=[
            step("Product rule: add exponents", f"x^{{\\frac{{{n1}}}{{{d1}}}+\\frac{{{n2}}}{{{d2}}}}}=x^{{\\frac{{{total}}}{{{L}}}}}", f"LCD={L}"),
            step("Simplify", f"x^{{{frac_tex}}}"),
        ],
    )


diff2 = [_radical_to_exp, _frac_exp_arith]


# ─── diff3 ───

def _rewrite_inv_sqrt():
    return problem(
        problem_tex="\\dfrac{1}{\\sqrt{x}}",
        answer_tex="x^{-1/2}",
        answer_norm="x^(-1/2)",
        steps=[
            step("Rewrite √x", "\\dfrac{1}{x^{1/2}}"),
            step("Negative exponent", "x^{-1/2}"),
        ],
    )


def _rewrite_x2_sqrt():
    return problem(
        problem_tex="\\dfrac{1}{x^2\\sqrt{x}}",
        answer_tex="x^{-5/2}",
        answer_norm="x^(-5/2)",
        steps=[
            step("Rewrite √x", "\\dfrac{1}{x^2 \\cdot x^{1/2}}"),
            step("Combine", "\\dfrac{1}{x^{5/2}}", "2+1/2=5/2"),
            step("Negative exponent", "x^{-5/2}"),
        ],
    )


def _coeff_rewrite():
    k = R(*CONFIG["coeffRewrite_k"])
    a = R(*CONFIG["coeffRewrite_a"])
    num = 2 * a + 1
    sn, sd = simplify_frac(-num, 2)
    frac_tex = frac_to_tex(abs(sn), sd)
    return problem(
        problem_tex=f"\\dfrac{{{k}}}{{x^{{{a}}}\\sqrt{{x}}}}",
        answer_tex=f"{k}x^{{-{frac_tex}}}",
        answer_norm=f"{k}x^({sn}/{sd})",
        steps=[
            step("Rewrite √x", f"\\frac{{{k}}}{{x^{{{a}}} \\cdot x^{{1/2}}}}"),
            step("Combine base", f"\\frac{{{k}}}{{x^{{{a}+1/2}}}}=\\frac{{{k}}}{{x^{{{num}/2}}}}"),
            step("Apply negative exponent", f"{k}x^{{-{frac_tex}}}"),
        ],
    )


def _higher_radical():
    n = pick(CONFIG["higherRadical_n"])
    m = R(*CONFIG["higherRadical_m"])
    sn, sd = simplify_frac(m, n)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"\\sqrt[{n}]{{x^{{{m}}}}}",
        answer_tex=f"x^{{{frac_tex}}}",
        answer_norm=f"x^({sn}/{sd})",
        steps=[
            step("Radical to exponent", f"x^{{{m}/{n}}}"),
            step("Simplify", f"x^{{{frac_tex}}}"),
        ],
    )


diff3 = [_rewrite_inv_sqrt, _rewrite_x2_sqrt, _coeff_rewrite, _higher_radical]


# ─── diff4 ───

def _radical_over_power():
    n, m, p, num_raw, attempts = None, None, None, 0, 0
    while (num_raw <= 0) and attempts < 50:
        n = pick(CONFIG["higherRadical_n"])
        m = R(*CONFIG["higherRadical_m"])
        p = R(1, 3)
        num_raw = m - p * n
        attempts += 1
    sn, sd = simplify_frac(num_raw, n)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"\\dfrac{{\\sqrt[{n}]{{x^{{{m}}}}}}}{{x^{{{p}}}}}",
        answer_tex=f"x^{{{frac_tex}}}",
        answer_norm=exp_frac_to_norm(sn, sd),
        steps=[
            step("Rewrite radical", f"\\dfrac{{x^{{{m}/{n}}}}}{{x^{{{p}}}}}", f"\\sqrt[{n}]{{x^m}}=x^{{m/{n}}}"),
            step("Quotient rule", f"x^{{{m}/{n}-{p}}}=x^{{\\frac{{{m}-{p*n}}}{{{n}}}}}", "subtract exponents"),
            step("Simplify", f"x^{{{frac_tex}}}"),
        ],
    )


def _three_factor_combine():
    a1, b1, a2, b2, e, total_num, attempts = 1, 2, 1, 2, 1, 0, 0
    while total_num <= 0 and attempts < 50:
        a1 = R(1, 3); b1 = pick([2, 3, 4])
        a2 = R(1, 3); b2 = pick([2, 3, 4])
        e = R(1, 2)
        L = lcm(b1, b2)
        sum_num = a1 * (L // b1) + a2 * (L // b2)
        total_num = sum_num - e * L
        attempts += 1
    L = lcm(b1, b2)
    sum_num = a1 * (L // b1) + a2 * (L // b2)
    sn, sd = simplify_frac(total_num, L)
    isn, isd = simplify_frac(sum_num, L)
    interm_tex = frac_to_tex(isn, isd)
    return problem(
        problem_tex=f"\\dfrac{{x^{{{a1}/{b1}}}\\cdot x^{{{a2}/{b2}}}}}{{x^{{{e}}}}}",
        answer_tex=f"x^{{{frac_to_tex(sn, sd)}}}",
        answer_norm=exp_frac_to_norm(sn, sd),
        steps=[
            step("Product rule: add top exponents", f"x^{{\\frac{{{a1}}}{{{b1}}}+\\frac{{{a2}}}{{{b2}}}}}=x^{{{interm_tex}}}", f"LCD={L}"),
            step("Quotient rule: subtract bottom", f"x^{{{interm_tex}-{e}}}=x^{{\\frac{{{total_num}}}{{{L}}}}}"),
            step("Simplify", f"x^{{{frac_to_tex(sn, sd)}}}"),
        ],
    )


def _neg_frac_coeff():
    k = R(2, 8)
    pq_choices = [[1,2],[2,3],[3,4],[1,3]]
    p, q = pick(pq_choices)
    n = pick([3, 4])
    total_num = p * n + q
    total_den = q * n
    sn, sd = simplify_frac(total_num, total_den)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"\\dfrac{{{k}}}{{x^{{{p}/{q}}}\\cdot\\sqrt[{n}]{{x}}}}",
        answer_tex=f"{k}x^{{-{frac_tex}}}",
        answer_norm=f"{k}x^(-{sn}/{sd})",
        steps=[
            step("Rewrite radical", f"\\dfrac{{{k}}}{{x^{{{p}/{q}}}\\cdot x^{{1/{n}}}}}"),
            step("Product rule in denominator", f"\\dfrac{{{k}}}{{x^{{{p}/{q}+1/{n}}}}}=\\dfrac{{{k}}}{{x^{{{frac_tex}}}}}", f"LCD={q*n}"),
            step("Negative exponent", f"{k}x^{{-{frac_tex}}}", "1/x^a=x^{-a}"),
        ],
    )


diff4 = [_radical_over_power, _three_factor_combine, _neg_frac_coeff]


# ─── diff5 ───

def _power_of_quotient():
    a = R(4, 8); b = R(1, 3)
    pq_choices = [[1,2],[2,3],[3,2],[1,3]]
    p, q = pick(pq_choices)
    inner = a - b
    sn, sd = simplify_frac(inner * p, q)
    frac_tex = frac_to_tex(sn, sd)
    return problem(
        problem_tex=f"\\left(\\dfrac{{x^{{{a}}}}}{{x^{{{b}}}}}\\right)^{{{p}/{q}}}",
        answer_tex=f"x^{{{frac_tex}}}",
        answer_norm=exp_frac_to_norm(sn, sd),
        steps=[
            step("Quotient rule inside", f"\\left(x^{{{a}-{b}}}\\right)^{{{p}/{q}}}=\\left(x^{{{inner}}}\\right)^{{{p}/{q}}}"),
            step("Power rule", f"x^{{{inner}\\cdot\\frac{{{p}}}{{{q}}}}}=x^{{\\frac{{{inner*p}}}{{{q}}}}}", "multiply exponents"),
            step("Simplify", f"x^{{{frac_tex}}}"),
        ],
    )


def _power_of_product():
    a1 = R(1, 3); b1 = pick([2, 3])
    a2 = R(1, 3); b2 = pick([2, 3])
    n = R(2, 3)
    L = lcm(b1, b2)
    sum_num = a1 * (L // b1) + a2 * (L // b2)
    sn, sd = simplify_frac(sum_num * n, L)
    isn, isd = simplify_frac(sum_num, L)
    interm_tex = frac_to_tex(isn, isd)
    return problem(
        problem_tex=f"\\left(x^{{{a1}/{b1}}}\\cdot x^{{{a2}/{b2}}}\\right)^{{{n}}}",
        answer_tex=f"x^{{{frac_to_tex(sn, sd)}}}",
        answer_norm=exp_frac_to_norm(sn, sd),
        steps=[
            step("Product rule inside", f"\\left(x^{{{interm_tex}}}\\right)^{{{n}}}", f"LCD={L}"),
            step("Power rule", f"x^{{{interm_tex}\\cdot {n}}}=x^{{\\frac{{{sum_num*n}}}{{{L}}}}}"),
            step("Simplify", f"x^{{{frac_to_tex(sn, sd)}}}"),
        ],
    )


def _neg_power_of_product():
    ab_choices = [[1,2],[1,3],[2,3]]
    a, b = pick(ab_choices)
    n = pick([3, 4])
    m = R(1, 2)
    inner_num = a * n + b
    inner_den = b * n
    total_num = -(inner_num * m)
    sn, sd = simplify_frac(total_num, inner_den)
    frac_tex = frac_to_tex(abs(sn), sd)
    return problem(
        problem_tex=f"\\left(x^{{{a}/{b}}}\\cdot\\sqrt[{n}]{{x}}\\right)^{{-{m}}}",
        answer_tex=f"x^{{-{frac_tex}}}",
        answer_norm=f"x^({sn}/{sd})",
        steps=[
            step("Rewrite radical", f"\\left(x^{{{a}/{b}}}\\cdot x^{{1/{n}}}\\right)^{{-{m}}}"),
            step("Product rule inside", f"\\left(x^{{\\frac{{{inner_num}}}{{{inner_den}}}}}\\right)^{{-{m}}}", f"LCD={b*n}"),
            step("Power rule", f"x^{{-{m}\\cdot\\frac{{{inner_num}}}{{{inner_den}}}}}=x^{{-\\frac{{{inner_num*m}}}{{{inner_den}}}}}"),
            step("Simplify", f"x^{{-{frac_tex}}}"),
        ],
    )


diff5 = [_power_of_quotient, _power_of_product, _neg_power_of_product]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}