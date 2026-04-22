import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from math_utils import R, pick, lcm, simplify_frac, frac_to_tex, exp_frac_to_norm, sign_str

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
    return {
        "problemTex": f"x^{{{a}}} \\cdot x^{{{b}}}",
        "answerTex": f"x^{{{a+b}}}",
        "answerNorm": f"x^{a+b}",
        "steps": [
            {"label": "Product rule", "math": f"x^{{{a}+{b}}}=x^{{{a+b}}}", "note": "x^a·x^b = x^(a+b)"},
        ],
    }


def _quotient_same_base():
    b = R(*CONFIG["divideBase_b"])
    extra = R(*CONFIG["divideBase_aExtra"])
    a = b + extra
    diff = a - b
    return {
        "problemTex": f"\\dfrac{{x^{{{a}}}}}{{x^{{{b}}}}}",
        "answerTex": f"x^{{{diff}}}",
        "answerNorm": f"x^{diff}",
        "steps": [
            {"label": "Quotient rule", "math": f"x^{{{a}-{b}}}=x^{{{diff}}}", "note": "x^a/x^b = x^(a-b)"},
        ],
    }


def _power_of_power():
    a = R(*CONFIG["powerPower_ab"])
    b = R(*CONFIG["powerPower_ab"])
    return {
        "problemTex": f"(x^{{{a}}})^{{{b}}}",
        "answerTex": f"x^{{{a*b}}}",
        "answerNorm": f"x^{a*b}",
        "steps": [
            {"label": "Power rule", "math": f"x^{{{a}\\cdot{b}}}=x^{{{a*b}}}", "note": "(x^a)^b = x^(ab)"},
        ],
    }


def _neg_exp():
    a = R(*CONFIG["negExp_a"])
    return {
        "problemTex": f"x^{{-{a}}}",
        "answerTex": f"\\dfrac{{1}}{{x^{{{a}}}}}",
        "answerNorm": f"1/x^{a}",
        "steps": [
            {"label": "Negative exponent rule", "math": f"x^{{-{a}}}=\\frac{{1}}{{x^{{{a}}}}}", "note": "x^(-a) = 1/x^a"},
        ],
    }


diff1 = [_same_base_product, _quotient_same_base, _power_of_power, _neg_exp]


# ─── diff2 ───

def _radical_to_exp():
    m = R(*CONFIG["radicalToExp_m"])
    n = pick(CONFIG["radicalToExp_n"])
    sn, sd = simplify_frac(m, n)
    frac_tex = frac_to_tex(sn, sd)
    return {
        "problemTex": f"\\sqrt[{n}]{{x^{{{m}}}}}",
        "answerTex": f"x^{{{frac_tex}}}",
        "answerNorm": f"x^({sn}/{sd})",
        "steps": [
            {"label": "Radical to exponent", "math": f"\\sqrt[n]{{x^m}}=x^{{m/n}}", "note": ""},
            {"label": "Apply", "math": f"x^{{{m}/{n}}}=x^{{{frac_tex}}}", "note": f"Simplified: {m}/{n} = {sn}/{sd}" if sn != m else ""},
        ],
    }


def _frac_exp_arith():
    den = CONFIG["fracExpArith_den"]
    d1 = pick(den); d2 = pick(den)
    n1 = R(1, 3); n2 = R(1, 3)
    L = lcm(d1, d2)
    total = n1 * (L // d1) + n2 * (L // d2)
    sn, sd = simplify_frac(total, L)
    frac_tex = frac_to_tex(sn, sd)
    return {
        "problemTex": f"x^{{{n1}/{d1}}} \\cdot x^{{{n2}/{d2}}}",
        "answerTex": f"x^{{{frac_tex}}}",
        "answerNorm": exp_frac_to_norm(sn, sd),
        "steps": [
            {"label": "Product rule: add exponents", "math": f"x^{{\\frac{{{n1}}}{{{d1}}}+\\frac{{{n2}}}{{{d2}}}}}=x^{{\\frac{{{total}}}{{{L}}}}}", "note": f"LCD={L}"},
            {"label": "Simplify", "math": f"x^{{{frac_tex}}}", "note": ""},
        ],
    }


diff2 = [_radical_to_exp, _frac_exp_arith]


# ─── diff3 ───

def _rewrite_inv_sqrt():
    return {
        "problemTex": "\\dfrac{1}{\\sqrt{x}}",
        "answerTex": "x^{-1/2}",
        "answerNorm": "x^(-1/2)",
        "steps": [
            {"label": "Rewrite √x", "math": "\\dfrac{1}{x^{1/2}}", "note": ""},
            {"label": "Negative exponent", "math": "x^{-1/2}", "note": ""},
        ],
    }


def _rewrite_x2_sqrt():
    return {
        "problemTex": "\\dfrac{1}{x^2\\sqrt{x}}",
        "answerTex": "x^{-5/2}",
        "answerNorm": "x^(-5/2)",
        "steps": [
            {"label": "Rewrite √x", "math": "\\dfrac{1}{x^2 \\cdot x^{1/2}}", "note": ""},
            {"label": "Combine", "math": "\\dfrac{1}{x^{5/2}}", "note": "2+1/2=5/2"},
            {"label": "Negative exponent", "math": "x^{-5/2}", "note": ""},
        ],
    }


def _coeff_rewrite():
    k = R(*CONFIG["coeffRewrite_k"])
    a = R(*CONFIG["coeffRewrite_a"])
    num = 2 * a + 1
    sn, sd = simplify_frac(-num, 2)
    frac_tex = frac_to_tex(abs(sn), sd)
    return {
        "problemTex": f"\\dfrac{{{k}}}{{x^{{{a}}}\\sqrt{{x}}}}",
        "answerTex": f"{k}x^{{-{frac_tex}}}",
        "answerNorm": f"{k}x^({sn}/{sd})",
        "steps": [
            {"label": "Rewrite √x", "math": f"\\frac{{{k}}}{{x^{{{a}}} \\cdot x^{{1/2}}}}", "note": ""},
            {"label": "Combine base", "math": f"\\frac{{{k}}}{{x^{{{a}+1/2}}}}=\\frac{{{k}}}{{x^{{{num}/2}}}}", "note": ""},
            {"label": "Apply negative exponent", "math": f"{k}x^{{-{frac_tex}}}", "note": ""},
        ],
    }


def _higher_radical():
    n = pick(CONFIG["higherRadical_n"])
    m = R(*CONFIG["higherRadical_m"])
    sn, sd = simplify_frac(m, n)
    frac_tex = frac_to_tex(sn, sd)
    return {
        "problemTex": f"\\sqrt[{n}]{{x^{{{m}}}}}",
        "answerTex": f"x^{{{frac_tex}}}",
        "answerNorm": f"x^({sn}/{sd})",
        "steps": [
            {"label": "Radical to exponent", "math": f"x^{{{m}/{n}}}", "note": ""},
            {"label": "Simplify", "math": f"x^{{{frac_tex}}}", "note": ""},
        ],
    }


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
    return {
        "problemTex": f"\\dfrac{{\\sqrt[{n}]{{x^{{{m}}}}}}}{{x^{{{p}}}}}",
        "answerTex": f"x^{{{frac_tex}}}",
        "answerNorm": exp_frac_to_norm(sn, sd),
        "steps": [
            {"label": "Rewrite radical", "math": f"\\dfrac{{x^{{{m}/{n}}}}}{{x^{{{p}}}}}", "note": f"\\sqrt[{n}]{{x^m}}=x^{{m/{n}}}"},
            {"label": "Quotient rule", "math": f"x^{{{m}/{n}-{p}}}=x^{{\\frac{{{m}-{p*n}}}{{{n}}}}}", "note": "subtract exponents"},
            {"label": "Simplify", "math": f"x^{{{frac_tex}}}", "note": ""},
        ],
    }


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
    return {
        "problemTex": f"\\dfrac{{x^{{{a1}/{b1}}}\\cdot x^{{{a2}/{b2}}}}}{{x^{{{e}}}}}",
        "answerTex": f"x^{{{frac_to_tex(sn, sd)}}}",
        "answerNorm": exp_frac_to_norm(sn, sd),
        "steps": [
            {"label": "Product rule: add top exponents", "math": f"x^{{\\frac{{{a1}}}{{{b1}}}+\\frac{{{a2}}}{{{b2}}}}}=x^{{{interm_tex}}}", "note": f"LCD={L}"},
            {"label": "Quotient rule: subtract bottom", "math": f"x^{{{interm_tex}-{e}}}=x^{{\\frac{{{total_num}}}{{{L}}}}}", "note": ""},
            {"label": "Simplify", "math": f"x^{{{frac_to_tex(sn, sd)}}}", "note": ""},
        ],
    }


def _neg_frac_coeff():
    k = R(2, 8)
    pq_choices = [[1,2],[2,3],[3,4],[1,3]]
    p, q = pick(pq_choices)
    n = pick([3, 4])
    total_num = p * n + q
    total_den = q * n
    sn, sd = simplify_frac(total_num, total_den)
    frac_tex = frac_to_tex(sn, sd)
    return {
        "problemTex": f"\\dfrac{{{k}}}{{x^{{{p}/{q}}}\\cdot\\sqrt[{n}]{{x}}}}",
        "answerTex": f"{k}x^{{-{frac_tex}}}",
        "answerNorm": f"{k}x^(-{sn}/{sd})",
        "steps": [
            {"label": "Rewrite radical", "math": f"\\dfrac{{{k}}}{{x^{{{p}/{q}}}\\cdot x^{{1/{n}}}}}", "note": ""},
            {"label": "Product rule in denominator", "math": f"\\dfrac{{{k}}}{{x^{{{p}/{q}+1/{n}}}}}=\\dfrac{{{k}}}{{x^{{{frac_tex}}}}}", "note": f"LCD={q*n}"},
            {"label": "Negative exponent", "math": f"{k}x^{{-{frac_tex}}}", "note": "1/x^a=x^{-a}"},
        ],
    }


diff4 = [_radical_over_power, _three_factor_combine, _neg_frac_coeff]


# ─── diff5 ───

def _power_of_quotient():
    a = R(4, 8); b = R(1, 3)
    pq_choices = [[1,2],[2,3],[3,2],[1,3]]
    p, q = pick(pq_choices)
    inner = a - b
    sn, sd = simplify_frac(inner * p, q)
    frac_tex = frac_to_tex(sn, sd)
    return {
        "problemTex": f"\\left(\\dfrac{{x^{{{a}}}}}{{x^{{{b}}}}}\\right)^{{{p}/{q}}}",
        "answerTex": f"x^{{{frac_tex}}}",
        "answerNorm": exp_frac_to_norm(sn, sd),
        "steps": [
            {"label": "Quotient rule inside", "math": f"\\left(x^{{{a}-{b}}}\\right)^{{{p}/{q}}}=\\left(x^{{{inner}}}\\right)^{{{p}/{q}}}", "note": ""},
            {"label": "Power rule", "math": f"x^{{{inner}\\cdot\\frac{{{p}}}{{{q}}}}}=x^{{\\frac{{{inner*p}}}{{{q}}}}}", "note": "multiply exponents"},
            {"label": "Simplify", "math": f"x^{{{frac_tex}}}", "note": ""},
        ],
    }


def _power_of_product():
    a1 = R(1, 3); b1 = pick([2, 3])
    a2 = R(1, 3); b2 = pick([2, 3])
    n = R(2, 3)
    L = lcm(b1, b2)
    sum_num = a1 * (L // b1) + a2 * (L // b2)
    sn, sd = simplify_frac(sum_num * n, L)
    isn, isd = simplify_frac(sum_num, L)
    interm_tex = frac_to_tex(isn, isd)
    return {
        "problemTex": f"\\left(x^{{{a1}/{b1}}}\\cdot x^{{{a2}/{b2}}}\\right)^{{{n}}}",
        "answerTex": f"x^{{{frac_to_tex(sn, sd)}}}",
        "answerNorm": exp_frac_to_norm(sn, sd),
        "steps": [
            {"label": "Product rule inside", "math": f"\\left(x^{{{interm_tex}}}\\right)^{{{n}}}", "note": f"LCD={L}"},
            {"label": "Power rule", "math": f"x^{{{interm_tex}\\cdot {n}}}=x^{{\\frac{{{sum_num*n}}}{{{L}}}}}", "note": ""},
            {"label": "Simplify", "math": f"x^{{{frac_to_tex(sn, sd)}}}", "note": ""},
        ],
    }


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
    return {
        "problemTex": f"\\left(x^{{{a}/{b}}}\\cdot\\sqrt[{n}]{{x}}\\right)^{{-{m}}}",
        "answerTex": f"x^{{-{frac_tex}}}",
        "answerNorm": f"x^({sn}/{sd})",
        "steps": [
            {"label": "Rewrite radical", "math": f"\\left(x^{{{a}/{b}}}\\cdot x^{{1/{n}}}\\right)^{{-{m}}}", "note": ""},
            {"label": "Product rule inside", "math": f"\\left(x^{{\\frac{{{inner_num}}}{{{inner_den}}}}}\\right)^{{-{m}}}", "note": f"LCD={b*n}"},
            {"label": "Power rule", "math": f"x^{{-{m}\\cdot\\frac{{{inner_num}}}{{{inner_den}}}}}=x^{{-\\frac{{{inner_num*m}}}{{{inner_den}}}}}", "note": ""},
            {"label": "Simplify", "math": f"x^{{-{frac_tex}}}", "note": ""},
        ],
    }


diff5 = [_power_of_quotient, _power_of_product, _neg_power_of_product]


POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
