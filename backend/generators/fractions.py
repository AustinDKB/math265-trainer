from problem_builder import problem, step
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
        step("Find least common denominator", f"\\text{{LCD}}({b},{d})={L}"),
        step("Rewrite with LCD",
             f"\\frac{{{a*(L//b)}}}{{{L}}}+\\frac{{{c*(L//d)}}}{{{L}}}"),
        step("Add numerators", f"\\frac{{{n}}}{{{L}}}"),
    ]
    g = gcd(abs(n), L)
    if g > 1:
        steps.append(step("Simplify", f"\\frac{{{sn}}}{{{sd}}}", f"Greatest common factor = {g}"))
    else:
        steps.append(step("Already simplified", f"\\frac{{{sn}}}{{{sd}}}"))
    return problem(
        problem_tex=f"\\dfrac{{{a}}}{{{b}}}+\\dfrac{{{c}}}{{{d}}}",
        answer_tex=answer_tex,
        answer_norm=str(sn) if sd == 1 else f"{sn}/{sd}",
        steps=steps,
    )


def _divide_fractions():
    df = CONFIG["divFrac_all"]
    a = R(*df); b = R(df[0]+1, df[1])
    c = R(*df); d = R(df[0]+1, df[1])
    sn, sd = simplify_frac(a*d, b*c)
    answer_tex = str(sn) if sd == 1 else f"\\dfrac{{{sn}}}{{{sd}}}"
    done_label = "Simplify" if (sn != a*d or sd != b*c) else "Done"
    return problem(
        problem_tex=f"\\dfrac{{{a}/{b}}}{{{c}/{d}}}",
        answer_tex=answer_tex,
        answer_norm=str(sn) if sd == 1 else f"{sn}/{sd}",
        steps=[
            step("Flip and multiply",
                 f"\\frac{{{a}}}{{{b}}}\\cdot\\frac{{{d}}}{{{c}}}", "Keep-Change-Flip"),
            step("Multiply", f"\\frac{{{a*d}}}{{{b*c}}}"),
            step(done_label, f"\\frac{{{sn}}}{{{sd}}}"),
        ],
    )


diff1 = [_add_fractions, _divide_fractions]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _cancel_frac():
    a = R(*CONFIG["cancelFrac_a"])
    return problem(
        problem_tex=f"\\dfrac{{x^2-{a*a}}}{{x+{a}}}",
        answer_tex=f"x-{a}",
        answer_norm=f"x-{a}",
        steps=[
            step("Factor numerator",
                 f"\\frac{{(x+{a})(x-{a})}}{{x+{a}}}", "Difference of squares"),
            step("Cancel common factor",
                 f"x-{a}", f"Assuming x ≠ {-a}"),
        ],
    )


def _complex_frac():
    return problem(
        problem_tex="\\dfrac{\\dfrac{1}{x+h}-\\dfrac{1}{x}}{h}",
        answer_tex="\\dfrac{-1}{x(x+h)}",
        answer_norm="-1/(x(x+h))",
        steps=[
            step("Common denominator in numerator",
                 "\\frac{\\frac{x-(x+h)}{x(x+h)}}{h}", "Least common denominator = x(x+h)"),
            step("Simplify numerator",
                 "\\frac{\\frac{-h}{x(x+h)}}{h}", "x−(x+h)=−h"),
            step("Divide by h",
                 "\\frac{-h}{x(x+h)} \\cdot \\frac{1}{h}=\\frac{-1}{x(x+h)}", "Cancel h (h≠0)"),
        ],
    )


def _three_term_lcd():
    a = R(*CONFIG["threeTermLCD_a"])
    a2 = a * a
    return problem(
        problem_tex=f"\\dfrac{{1}}{{x-{a}}}+\\dfrac{{1}}{{x+{a}}}+\\dfrac{{1}}{{x^2-{a2}}}",
        answer_tex=f"\\dfrac{{2x+1}}{{x^2-{a2}}}",
        answer_norm=f"(2x+1)/(x^2-{a2})",
        steps=[
            step("Factor last denominator",
                 f"x^2-{a2}=(x-{a})(x+{a})"),
            step("Least common denominator",
                 f"\\text{{LCD}}=(x-{a})(x+{a})"),
            step("Rewrite all fractions",
                 f"\\frac{{(x+{a})+(x-{a})+1}}{{(x-{a})(x+{a})}}"),
            step("Simplify numerator",
                 f"\\frac{{2x+1}}{{x^2-{a2}}}"),
        ],
    )


diff2 = [_cancel_frac, _complex_frac, _three_term_lcd]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _quotient_rule():
    n = R(*CONFIG["quotientRule_n"])
    a = R(*CONFIG["quotientRule_a"])
    a_str = sign_str(a)
    return problem(
        problem_tex=(
            f"\\dfrac{{{n}x^{{{n-1}}}(x{a_str})-x^{{{n}}}}}{{(x{a_str})^2}}"
        ),
        answer_tex=(
            f"\\dfrac{{x^{{{n-1}}}({n-1}x{a_str})}}{{(x{a_str})^2}}"
        ),
        answer_norm=f"x^{n-1}*(({n-1})x+{a})/(x{a_str})^2",
        steps=[
            step("Factor numerator: pull out x^(n-1)",
                 f"\\frac{{x^{{{n-1}}}[{n}(x{a_str})-x]}}{{(x{a_str})^2}}"),
            step("Expand bracket",
                 f"\\frac{{x^{{{n-1}}}[{n-1}x{a_str}]}}{{(x{a_str})^2}}",
                 f"{n}(x{a_str})−x = {n-1}x+{n*a}"),
            step("Final form",
                 f"\\frac{{x^{{{n-1}}}({n-1}x+{n*a})}}{{(x{a_str})^2}}"),
        ],
        isQuotientRule=True,
        n=n,
        a=a,
    )


def _frac_exp_cleanup():
    a = R(2, 5); b = R(2, 5); c = R(1, 4)
    pq = pick([[3, 2], [1, 2], [2, 3], [5, 2]])
    rs = pick([[1, 2], [1, 3], [3, 2]])
    p, q = pq; r, s = rs
    sn1, sd1 = simplify_frac(p - q, q)
    sn2, sd2 = simplify_frac(r - s, s)
    frac1 = str(sn1) if sd1 == 1 else f"{sn1}/{sd1}"
    frac2 = str(sn2) if sd2 == 1 else f"{sn2}/{sd2}"
    return problem(
        problem_tex=f"\\dfrac{{{a}x^{{{p}/{q}}} - {b}x^{{{r}/{s}}}}}{{{c}x}}",
        answer_tex=f"\\dfrac{{{a}x^{{{frac1}}} - {b}x^{{{frac2}}}}}{{{c}}}",
        answer_norm=f"({a}x^({sn1}/{sd1})-{b}x^({sn2}/{sd2}))/{c}",
        steps=[
            step("Divide each term by cx",
                 f"\\frac{{{a}x^{{{p}/{q}}}}}{{{c}x}} - \\frac{{{b}x^{{{r}/{s}}}}}{{{c}x}}"),
            step("Subtract exponent 1 from each",
                 f"\\frac{{{a}}}{{{c}}}x^{{{p}/{q}-1}} - \\frac{{{b}}}{{{c}}}x^{{{r}/{s}-1}}",
                 "Dividing by x = subtracting 1 from exp"),
            step("Simplify exponents",
                 f"\\frac{{{a}}}{{{c}}}x^{{{frac1}}} - \\frac{{{b}}}{{{c}}}x^{{{frac2}}}"),
        ],
    )


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
    return problem(
        problem_tex=f"\\dfrac{{x^2{B_str}x{C_str}}}{{x{p_str}}}",
        answer_tex=f"x{q_str}",
        answer_norm=f"x{q_str}",
        steps=[
            step("Factor numerator",
                 f"\\dfrac{{(x{p_str})(x{q_str})}}{{x{p_str}}}"),
            step("Cancel common factor",
                 f"x{q_str}"),
        ],
    )


def _rational_add():
    r_min, r_max = CONFIG["rationalAdd_ab"]
    a, b, attempts = 0, 0, 0
    while attempts < 50:
        a = R(r_min, r_max); b = R(r_min, r_max); attempts += 1
        if a != b:
            break
    S = a + b; P = a * b
    S_str = sign_str(S); P_str = sign_str(P)
    return problem(
        problem_tex=f"\\dfrac{{1}}{{x+{a}}}+\\dfrac{{1}}{{x+{b}}}",
        answer_tex=f"\\dfrac{{2x{S_str}}}{{x^2{S_str}x{P_str}}}",
        answer_norm=f"(2x{S_str})/(x^2{S_str}x{P_str})",
        steps=[
            step("Least common denominator",
                 f"(x+{a})(x+{b})=x^2{S_str}x{P_str}"),
            step("Rewrite with LCD",
                 f"\\dfrac{{x+{b}+(x+{a})}}{{x^2{S_str}x{P_str}}}"),
            step("Combine numerator",
                 f"\\dfrac{{2x{S_str}}}{{x^2{S_str}x{P_str}}}"),
        ],
    )


def _diff_quotient_x2():
    return problem(
        problem_tex="\\dfrac{(x+h)^2 - x^2}{h}",
        answer_tex="2x+h",
        answer_norm="2x+h",
        steps=[
            step("Expand numerator",
                 "\\dfrac{x^2+2xh+h^2-x^2}{h}"),
            step("Cancel x²",
                 "\\dfrac{2xh+h^2}{h}"),
            step("Factor and cancel h",
                 "\\dfrac{h(2x+h)}{h}=2x+h"),
        ],
    )


diff4 = [_poly_cancel, _rational_add, _diff_quotient_x2]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _diff_quotient_x3():
    return problem(
        problem_tex="\\dfrac{(x+h)^3 - x^3}{h}",
        answer_tex="3x^2+3xh+h^2",
        answer_norm="3x^2+3xh+h^2",
        steps=[
            step("Expand (x+h)³",
                 "\\dfrac{x^3+3x^2h+3xh^2+h^3-x^3}{h}", "binomial expansion"),
            step("Cancel x³",
                 "\\dfrac{3x^2h+3xh^2+h^3}{h}"),
            step("Factor and cancel h",
                 "\\dfrac{h(3x^2+3xh+h^2)}{h}=3x^2+3xh+h^2"),
        ],
    )


def _three_term_sub():
    a = R(*CONFIG["threeTermSub_a"])
    a2 = a * a
    return problem(
        problem_tex=f"\\dfrac{{1}}{{x+{a}}}-\\dfrac{{{2*a}}}{{x^2-{a2}}}+\\dfrac{{1}}{{x-{a}}}",
        answer_tex=f"\\dfrac{{2}}{{x+{a}}}",
        answer_norm=f"2/(x+{a})",
        steps=[
            step("Factor denominator",
                 f"x^2-{a2}=(x+{a})(x-{a})"),
            step("Combine over common denominator",
                 f"\\dfrac{{x-{a}-{2*a}+x+{a}}}{{x^2-{a2}}}"),
            step("Simplify numerator",
                 f"\\dfrac{{2x-{2*a}}}{{x^2-{a2}}}=\\dfrac{{2(x-{a})}}{{(x+{a})(x-{a})}}"),
            step(f"Cancel (x−{a})",
                 f"\\dfrac{{2}}{{x+{a}}}"),
        ],
    )


def _factor_both_cancel():
    a = R(*CONFIG["factorBoth_a"])
    a2 = a * a; two_a = 2 * a
    return problem(
        problem_tex=f"\\dfrac{{x^2-{a2}}}{{x^2+{two_a}x+{a2}}}",
        answer_tex=f"\\dfrac{{x-{a}}}{{x+{a}}}",
        answer_norm=f"(x-{a})/(x+{a})",
        steps=[
            step("Factor numerator",
                 f"\\dfrac{{(x-{a})(x+{a})}}{{x^2+{two_a}x+{a2}}}",
                 "difference of squares"),
            step("Factor denominator",
                 f"\\dfrac{{(x-{a})(x+{a})}}{{(x+{a})^2}}",
                 "perfect square trinomial"),
            step(f"Cancel (x+{a})",
                 f"\\dfrac{{x-{a}}}{{x+{a}}}"),
        ],
    )


diff5 = [_diff_quotient_x3, _three_term_sub, _factor_both_cancel]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}