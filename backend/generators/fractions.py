import random
from math_utils import R, pick, gcd, lcm, simplify_frac, sign_str, frac_to_tex

CONFIG = {
    "addFrac_num":    [1, 25],
    "addFrac_den":    [2, 25],
    "divFrac_all":    [1, 15],
    "cancelFrac_a":   [1, 12],
    "threeTermLCD_a": [1, 12],
    "quotientRule_n": [2, 8],
    "quotientRule_a": [1, 8],
    "polyCancel_pq":  [-6, 6],
    "rationalAdd_ab": [1, 5],
    "threeTermSub_a": [2, 6],
    "factorBoth_a":   [2, 8],
}

# ── diff1 ──────────────────────────────────────────────────────────────────────

def _add_fractions():
    af_num = CONFIG["addFrac_num"]
    af_den = CONFIG["addFrac_den"]
    a = R(*af_num); b = R(*af_den)
    c = R(*af_num); d = R(*af_den)
    L = lcm(b, d)
    n = a * (L // b) + c * (L // d)
    sn, sd = simplify_frac(n, L)
    answer_tex = str(sn) if sd == 1 else f"\\dfrac{{{sn}}}{{{sd}}}"
    steps = [
        {"label": "Find least common denominator", "math": f"\\text{{LCD}}({b},{d})={L}", "note": ""},
        {"label": "Rewrite with LCD",
         "math": f"\\frac{{{a*(L//b)}}}{{{L}}}+\\frac{{{c*(L//d)}}}{{{L}}}", "note": ""},
        {"label": "Add numerators", "math": f"\\frac{{{n}}}{{{L}}}", "note": ""},
    ]
    g = gcd(abs(n), L)
    if g > 1:
        steps.append({"label": "Simplify", "math": f"\\frac{{{sn}}}{{{sd}}}", "note": f"Greatest common factor = {g}"})
    else:
        steps.append({"label": "Already simplified", "math": f"\\frac{{{sn}}}{{{sd}}}", "note": ""})
    return {
        "problemTex": f"\\dfrac{{{a}}}{{{b}}}+\\dfrac{{{c}}}{{{d}}}",
        "answerTex": answer_tex,
        "answerNorm": str(sn) if sd == 1 else f"{sn}/{sd}",
        "steps": steps,
    }


def _divide_fractions():
    df = CONFIG["divFrac_all"]
    a = R(*df); b = R(df[0]+1, df[1])
    c = R(*df); d = R(df[0]+1, df[1])
    sn, sd = simplify_frac(a*d, b*c)
    answer_tex = str(sn) if sd == 1 else f"\\dfrac{{{sn}}}{{{sd}}}"
    done_label = "Simplify" if (sn != a*d or sd != b*c) else "Done"
    return {
        "problemTex": f"\\dfrac{{{a}/{b}}}{{{c}/{d}}}",
        "answerTex": answer_tex,
        "answerNorm": str(sn) if sd == 1 else f"{sn}/{sd}",
        "steps": [
            {"label": "Flip and multiply",
             "math": f"\\frac{{{a}}}{{{b}}}\\cdot\\frac{{{d}}}{{{c}}}", "note": "Keep-Change-Flip"},
            {"label": "Multiply", "math": f"\\frac{{{a*d}}}{{{b*c}}}", "note": ""},
            {"label": done_label, "math": f"\\frac{{{sn}}}{{{sd}}}", "note": ""},
        ],
    }


diff1 = [_add_fractions, _divide_fractions]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _cancel_frac():
    a = R(*CONFIG["cancelFrac_a"])
    return {
        "problemTex": f"\\dfrac{{x^2-{a*a}}}{{x+{a}}}",
        "answerTex": f"x-{a}",
        "answerNorm": f"x-{a}",
        "steps": [
            {"label": "Factor numerator",
             "math": f"\\frac{{(x+{a})(x-{a})}}{{x+{a}}}", "note": "Difference of squares"},
            {"label": "Cancel common factor",
             "math": f"x-{a}", "note": f"Assuming x ≠ {-a}"},
        ],
    }


def _complex_frac():
    return {
        "problemTex": "\\dfrac{\\dfrac{1}{x+h}-\\dfrac{1}{x}}{h}",
        "answerTex": "\\dfrac{-1}{x(x+h)}",
        "answerNorm": "-1/(x(x+h))",
        "steps": [
            {"label": "Common denominator in numerator",
             "math": "\\frac{\\frac{x-(x+h)}{x(x+h)}}{h}", "note": "Least common denominator = x(x+h)"},
            {"label": "Simplify numerator",
             "math": "\\frac{\\frac{-h}{x(x+h)}}{h}", "note": "x−(x+h)=−h"},
            {"label": "Divide by h",
             "math": "\\frac{-h}{x(x+h)} \\cdot \\frac{1}{h}=\\frac{-1}{x(x+h)}", "note": "Cancel h (h≠0)"},
        ],
    }


def _three_term_lcd():
    a = R(*CONFIG["threeTermLCD_a"])
    a2 = a * a
    return {
        "problemTex": f"\\dfrac{{1}}{{x-{a}}}+\\dfrac{{1}}{{x+{a}}}+\\dfrac{{1}}{{x^2-{a2}}}",
        "answerTex": f"\\dfrac{{2x+1}}{{x^2-{a2}}}",
        "answerNorm": f"(2x+1)/(x^2-{a2})",
        "steps": [
            {"label": "Factor last denominator",
             "math": f"x^2-{a2}=(x-{a})(x+{a})", "note": ""},
            {"label": "Least common denominator",
             "math": f"\\text{{LCD}}=(x-{a})(x+{a})", "note": ""},
            {"label": "Rewrite all fractions",
             "math": f"\\frac{{(x+{a})+(x-{a})+1}}{{(x-{a})(x+{a})}}", "note": ""},
            {"label": "Simplify numerator",
             "math": f"\\frac{{2x+1}}{{x^2-{a2}}}", "note": ""},
        ],
    }


diff2 = [_cancel_frac, _complex_frac, _three_term_lcd]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _quotient_rule():
    n = R(*CONFIG["quotientRule_n"])
    a = R(*CONFIG["quotientRule_a"])
    a_str = sign_str(a)
    # answerNorm mirrors JS: x^(n-1)*((n-1)x+a)/(x+a)^2
    return {
        "problemTex": (
            f"\\dfrac{{{n}x^{{{n-1}}}(x{a_str})-x^{{{n}}}}}{{(x{a_str})^2}}"
        ),
        "answerTex": (
            f"\\dfrac{{x^{{{n-1}}}({n-1}x{a_str})}}{{(x{a_str})^2}}"
        ),
        "answerNorm": f"x^{n-1}*(({n-1})x+{a})/(x{a_str})^2",
        "isQuotientRule": True,
        "n": n,
        "a": a,
        "steps": [
            {"label": "Factor numerator: pull out x^(n-1)",
             "math": f"\\frac{{x^{{{n-1}}}[{n}(x{a_str})-x]}}{{(x{a_str})^2}}", "note": ""},
            {"label": "Expand bracket",
             "math": f"\\frac{{x^{{{n-1}}}[{n-1}x{a_str}]}}{{(x{a_str})^2}}",
             "note": f"{n}(x{a_str})−x = {n-1}x+{n*a}"},
            {"label": "Final form",
             "math": f"\\frac{{x^{{{n-1}}}({n-1}x+{n*a})}}{{(x{a_str})^2}}", "note": ""},
        ],
    }


def _frac_exp_cleanup():
    a = R(2, 5); b = R(2, 5); c = R(1, 4)
    pq = pick([[3, 2], [1, 2], [2, 3], [5, 2]])
    rs = pick([[1, 2], [1, 3], [3, 2]])
    p, q = pq; r, s = rs
    sn1, sd1 = simplify_frac(p - q, q)
    sn2, sd2 = simplify_frac(r - s, s)
    frac1 = str(sn1) if sd1 == 1 else f"{sn1}/{sd1}"
    frac2 = str(sn2) if sd2 == 1 else f"{sn2}/{sd2}"
    return {
        "problemTex": f"\\dfrac{{{a}x^{{{p}/{q}}} - {b}x^{{{r}/{s}}}}}{{{c}x}}",
        "answerTex": f"\\dfrac{{{a}x^{{{frac1}}} - {b}x^{{{frac2}}}}}{{{c}}}",
        "answerNorm": f"({a}x^({sn1}/{sd1})-{b}x^({sn2}/{sd2}))/{c}",
        "steps": [
            {"label": "Divide each term by cx",
             "math": f"\\frac{{{a}x^{{{p}/{q}}}}}{{{c}x}} - \\frac{{{b}x^{{{r}/{s}}}}}{{{c}x}}", "note": ""},
            {"label": "Subtract exponent 1 from each",
             "math": f"\\frac{{{a}}}{{{c}}}x^{{{p}/{q}-1}} - \\frac{{{b}}}{{{c}}}x^{{{r}/{s}-1}}",
             "note": "Dividing by x = subtracting 1 from exp"},
            {"label": "Simplify exponents",
             "math": f"\\frac{{{a}}}{{{c}}}x^{{{frac1}}} - \\frac{{{b}}}{{{c}}}x^{{{frac2}}}", "note": ""},
        ],
    }


diff3 = [_quotient_rule, _frac_exp_cleanup]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _poly_cancel():
    pq_min, pq_max = CONFIG["polyCancel_pq"]
    p, q, attempts = 0, 0, 0
    while attempts < 50:
        p = R(pq_min, pq_max); q = R(pq_min, pq_max); attempts += 1
        if p != 0 and q != 0:
            break
    B = p + q; C = p * q
    p_str = sign_str(p); q_str = sign_str(q)
    B_str = sign_str(B); C_str = sign_str(C)
    return {
        "problemTex": f"\\dfrac{{x^2{B_str}x{C_str}}}{{x{p_str}}}",
        "answerTex": f"x{q_str}",
        "answerNorm": f"x{q_str}",
        "steps": [
            {"label": "Factor numerator",
             "math": f"\\dfrac{{(x{p_str})(x{q_str})}}{{x{p_str}}}", "note": ""},
            {"label": "Cancel common factor",
             "math": f"x{q_str}", "note": ""},
        ],
    }


def _rational_add():
    r_min, r_max = CONFIG["rationalAdd_ab"]
    a, b, attempts = 0, 0, 0
    while attempts < 50:
        a = R(r_min, r_max); b = R(r_min, r_max); attempts += 1
        if a != b:
            break
    S = a + b; P = a * b
    S_str = sign_str(S); P_str = sign_str(P)
    return {
        "problemTex": f"\\dfrac{{1}}{{x+{a}}}+\\dfrac{{1}}{{x+{b}}}",
        "answerTex": f"\\dfrac{{2x{S_str}}}{{x^2{S_str}x{P_str}}}",
        "answerNorm": f"(2x{S_str})/(x^2{S_str}x{P_str})",
        "steps": [
            {"label": "Least common denominator",
             "math": f"(x+{a})(x+{b})=x^2{S_str}x{P_str}", "note": ""},
            {"label": "Rewrite with LCD",
             "math": f"\\dfrac{{x+{b}+(x+{a})}}{{x^2{S_str}x{P_str}}}", "note": ""},
            {"label": "Combine numerator",
             "math": f"\\dfrac{{2x{S_str}}}{{x^2{S_str}x{P_str}}}", "note": ""},
        ],
    }


def _diff_quotient_x2():
    return {
        "problemTex": "\\dfrac{(x+h)^2 - x^2}{h}",
        "answerTex": "2x+h",
        "answerNorm": "2x+h",
        "steps": [
            {"label": "Expand numerator",
             "math": "\\dfrac{x^2+2xh+h^2-x^2}{h}", "note": ""},
            {"label": "Cancel x²",
             "math": "\\dfrac{2xh+h^2}{h}", "note": ""},
            {"label": "Factor and cancel h",
             "math": "\\dfrac{h(2x+h)}{h}=2x+h", "note": ""},
        ],
    }


diff4 = [_poly_cancel, _rational_add, _diff_quotient_x2]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _diff_quotient_x3():
    return {
        "problemTex": "\\dfrac{(x+h)^3 - x^3}{h}",
        "answerTex": "3x^2+3xh+h^2",
        "answerNorm": "3x^2+3xh+h^2",
        "steps": [
            {"label": "Expand (x+h)³",
             "math": "\\dfrac{x^3+3x^2h+3xh^2+h^3-x^3}{h}", "note": "binomial expansion"},
            {"label": "Cancel x³",
             "math": "\\dfrac{3x^2h+3xh^2+h^3}{h}", "note": ""},
            {"label": "Factor and cancel h",
             "math": "\\dfrac{h(3x^2+3xh+h^2)}{h}=3x^2+3xh+h^2", "note": ""},
        ],
    }


def _three_term_sub():
    a = R(*CONFIG["threeTermSub_a"])
    a2 = a * a
    return {
        "problemTex": f"\\dfrac{{1}}{{x+{a}}}-\\dfrac{{{2*a}}}{{x^2-{a2}}}+\\dfrac{{1}}{{x-{a}}}",
        "answerTex": f"\\dfrac{{2}}{{x+{a}}}",
        "answerNorm": f"2/(x+{a})",
        "steps": [
            {"label": "Factor denominator",
             "math": f"x^2-{a2}=(x+{a})(x-{a})", "note": ""},
            {"label": "Combine over common denominator",
             "math": f"\\dfrac{{x-{a}-{2*a}+x+{a}}}{{x^2-{a2}}}", "note": ""},
            {"label": "Simplify numerator",
             "math": f"\\dfrac{{2x-{2*a}}}{{x^2-{a2}}}=\\dfrac{{2(x-{a})}}{{(x+{a})(x-{a})}}", "note": ""},
            {"label": f"Cancel (x−{a})",
             "math": f"\\dfrac{{2}}{{x+{a}}}", "note": ""},
        ],
    }


def _factor_both_cancel():
    a = R(*CONFIG["factorBoth_a"])
    a2 = a * a; two_a = 2 * a
    return {
        "problemTex": f"\\dfrac{{x^2-{a2}}}{{x^2+{two_a}x+{a2}}}",
        "answerTex": f"\\dfrac{{x-{a}}}{{x+{a}}}",
        "answerNorm": f"(x-{a})/(x+{a})",
        "steps": [
            {"label": "Factor numerator",
             "math": f"\\dfrac{{(x-{a})(x+{a})}}{{x^2+{two_a}x+{a2}}}",
             "note": "difference of squares"},
            {"label": "Factor denominator",
             "math": f"\\dfrac{{(x-{a})(x+{a})}}{{(x+{a})^2}}",
             "note": "perfect square trinomial"},
            {"label": f"Cancel (x+{a})",
             "math": f"\\dfrac{{x-{a}}}{{x+{a}}}", "note": ""},
        ],
    }


diff5 = [_diff_quotient_x3, _three_term_sub, _factor_both_cancel]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
