import random
from math_utils import R, pick, simplify_frac, frac_to_tex

_VARS = ["x", "y", "z", "a", "b"]

# ── diff1 ──────────────────────────────────────────────────────────────────────

def _product_rule():
    a, b = pick(["x","y"]), pick(["y","z"])
    return {
        "problemTex": f"\\ln({a}\\cdot {b}) = \\,?",
        "answerTex": f"\\ln {a}+\\ln {b}",
        "answerNorm": f"ln({a})+ln({b})",
        "steps": [{"label": "Product rule", "math": f"\\ln({a}\\cdot {b})=\\ln {a}+\\ln {b}", "note": ""}],
    }


def _quotient_rule():
    a, b = "x", pick(["y","z","a"])
    return {
        "problemTex": f"\\ln\\!\\left(\\dfrac{{{a}}}{{{b}}}\\right) = \\,?",
        "answerTex": f"\\ln {a}-\\ln {b}",
        "answerNorm": f"ln({a})-ln({b})",
        "steps": [{"label": "Quotient rule", "math": f"\\ln\\!\\left(\\dfrac{{{a}}}{{{b}}}\\right)=\\ln {a}-\\ln {b}", "note": ""}],
    }


def _power_rule():
    n = R(2, 8)
    return {
        "problemTex": f"\\ln(x^{{{n}}}) = \\,?",
        "answerTex": f"{n}\\ln x",
        "answerNorm": f"{n}*ln(x)",
        "steps": [{"label": "Power rule", "math": f"\\ln(x^{{{n}}})={n}\\ln x", "note": ""}],
    }


diff1 = [_product_rule, _quotient_rule, _power_rule]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _expand_expression():
    vars_num = random.sample(["x","y","z"], R(1,3))
    vars_den = random.sample([v for v in ["x","y","z"] if v not in vars_num], R(0, min(1, 3-len(vars_num))))
    exps_num = [R(1,5) for _ in vars_num]
    exps_den = [R(1,3) for _ in vars_den]

    # Build compact LaTeX
    num_parts = "".join(
        f"{v}^{{{e}}}" if e > 1 else v
        for v, e in zip(vars_num, exps_num)
    )
    if vars_den:
        den_parts = "".join(
            f"{v}^{{{e}}}" if e > 1 else v
            for v, e in zip(vars_den, exps_den)
        )
        compact = f"\\dfrac{{{num_parts}}}{{{den_parts}}}"
    else:
        compact = num_parts

    # Build expanded form
    expanded_parts = []
    for v, e in zip(vars_num, exps_num):
        expanded_parts.append(f"{e}\\ln {v}" if e > 1 else f"\\ln {v}")
    for v, e in zip(vars_den, exps_den):
        expanded_parts.append(f"-{e}\\ln {v}" if e > 1 else f"-\\ln {v}")
    expanded_tex = "+".join(expanded_parts).replace("+-", "-")

    # Norm
    norm_parts = []
    for v, e in zip(vars_num, exps_num):
        norm_parts.append(f"{e}*ln({v})" if e > 1 else f"ln({v})")
    for v, e in zip(vars_den, exps_den):
        norm_parts.append(f"-{e}*ln({v})" if e > 1 else f"-ln({v})")
    norm = "+".join(norm_parts).replace("+-", "-")

    return {
        "problemTex": f"\\ln\\!\\left({compact}\\right) = \\,?",
        "answerTex": expanded_tex,
        "answerNorm": norm,
        "steps": [
            {"label": "Apply product/quotient rules", "math": "+".join(
                f"\\ln({v}^{{{e}}})" if e > 1 else f"\\ln {v}"
                for v, e in zip(vars_num, exps_num)
            ) + "".join(f"-\\ln({v}^{{{e}}})" if e > 1 else f"-\\ln {v}" for v, e in zip(vars_den, exps_den)), "note": ""},
            {"label": "Apply power rule", "math": expanded_tex, "note": ""},
        ],
    }


def _condense_expression():
    # Build expanded first, answer is condensed
    result = _expand_expression()
    # Swap problem and answer
    compact_tex = result["problemTex"].replace("\\ln\\!\\left(", "").rstrip("= \\,?").rstrip(")").rstrip("\\right")
    # Rebuild: problem is expanded, answer is condensed
    # Extract from result
    orig_compact_inner = result["problemTex"]
    orig_compact_inner = orig_compact_inner.replace("\\ln\\!\\left(", "").replace("\\right) = \\,?", "").strip()
    expanded = result["answerTex"]
    return {
        "problemTex": f"\\text{{Condense: }}\\; {expanded} = \\,?",
        "answerTex": f"\\ln\\!\\left({orig_compact_inner}\\right)",
        "answerNorm": f"ln({orig_compact_inner.replace('{','').replace('}','').replace('\\dfrac','').replace('dfrac','')})",
        "steps": [
            {"label": "Power rule (reverse)", "math": f"{expanded} \\to \\ln(\\ldots^n)", "note": "coefficient → exponent"},
            {"label": "Product/quotient rule (reverse)", "math": f"\\ln(\\ldots) \\to \\ln\\!\\left({orig_compact_inner}\\right)", "note": "+ means multiply, − means divide"},
        ],
    }


def _solve_ln():
    # ln(x) = k → x = e^k; pick k ∈ {1..5}
    k = R(1, 5)
    return {
        "problemTex": f"\\ln(x) = {k} \\quad \\Rightarrow \\quad x = \\,?",
        "answerTex": f"e^{{{k}}}",
        "answerNorm": f"e^{k}",
        "steps": [
            {"label": "Exponentiate both sides", "math": f"e^{{\\ln(x)}} = e^{{{k}}}", "note": ""},
            {"label": "Simplify", "math": f"x = e^{{{k}}}", "note": "e^ln(x) = x"},
        ],
    }


def _solve_exponential():
    # e^(ax) = k → x = ln(k)/a
    a = R(1, 4)
    k = R(2, 12)
    a_tex = "" if a == 1 else str(a)
    return {
        "problemTex": f"e^{{{a_tex}x}} = {k} \\quad \\Rightarrow \\quad x = \\,?",
        "answerTex": f"\\dfrac{{\\ln {k}}}{{{a}}}",
        "answerNorm": f"ln({k})/{a}",
        "steps": [
            {"label": "Take ln of both sides", "math": f"\\ln(e^{{{a_tex}x}}) = \\ln {k}", "note": ""},
            {"label": "Simplify left side", "math": f"{a_tex}x = \\ln {k}", "note": "ln(e^u) = u"},
            {"label": "Solve for x", "math": f"x = \\dfrac{{\\ln {k}}}{{{a}}}", "note": ""},
        ],
    }


def _change_of_base():
    b = pick([2, 3, 5, 10])
    n = R(2, 20)
    return {
        "problemTex": f"\\log_{{{b}}}({n}) = \\,?",
        "answerTex": f"\\dfrac{{\\ln {n}}}{{\\ln {b}}}",
        "answerNorm": f"ln({n})/ln({b})",
        "steps": [
            {"label": "Change of base formula", "math": f"\\log_{{{b}}}({n}) = \\dfrac{{\\ln {n}}}{{\\ln {b}}}", "note": ""},
        ],
    }


diff2 = [_expand_expression, _expand_expression, _condense_expression, _solve_ln, _solve_exponential, _change_of_base]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _nested_log():
    # ln(e^(f(x))) = f(x)
    fns = [("2x","2x"), ("x^2","x^2"), ("3x+1","3x+1"), ("x+5","x+5")]
    fx, fx_norm = pick(fns)
    return {
        "problemTex": f"\\ln\\!\\left(e^{{{fx}}}\\right) = \\,?",
        "answerTex": fx,
        "answerNorm": fx_norm,
        "steps": [
            {"label": "ln and e are inverse functions", "math": f"\\ln(e^u) = u", "note": ""},
            {"label": "Apply", "math": f"\\ln(e^{{{fx}}}) = {fx}", "note": ""},
        ],
    }


def _combined_exp_log():
    # e^(n·ln(x)) = x^n
    n = R(2, 6)
    return {
        "problemTex": f"e^{{{n}\\ln x}} = \\,?",
        "answerTex": f"x^{{{n}}}",
        "answerNorm": f"x^{n}",
        "steps": [
            {"label": "Power rule of ln", "math": f"{n}\\ln x = \\ln(x^{{{n}}})", "note": ""},
            {"label": "Then e^ln(...) cancels", "math": f"e^{{\\ln(x^{{{n}}})}} = x^{{{n}}}", "note": ""},
        ],
    }


def _log_diff_setup():
    # y = x^x → ln(y) = x·ln(x)
    fns = [
        ("x^x", "x\\ln x"),
        ("x^{\\sin x}", "\\sin(x)\\cdot\\ln x"),
        ("(x+1)^{2x}", "2x\\ln(x+1)"),
    ]
    y_tex, rhs_tex = pick(fns)
    return {
        "problemTex": f"\\text{{Rewrite }} y={y_tex} \\text{{ using }} \\ln \\text{{: }} \\ln y = \\,?",
        "answerTex": rhs_tex,
        "answerNorm": rhs_tex.replace("{","").replace("}","").replace("\\","").replace("cdot","*"),
        "steps": [
            {"label": "Take ln of both sides", "math": f"\\ln y = \\ln\\!\\left({y_tex}\\right)", "note": ""},
            {"label": "Apply power rule of ln", "math": f"\\ln y = {rhs_tex}", "note": "ln(f^g) = g·ln(f)"},
        ],
    }


diff3 = [_nested_log, _combined_exp_log, _log_diff_setup]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _solve_log_equation():
    # 2·ln(x) + ln(x+1) = ln(k): condense left → ln(x²(x+1)) = ln(k)
    # Use simple case: ln(x) + ln(x-a) = ln(b) → x² - ax - b = 0
    # Pick a and b such that roots are integers
    r1, r2 = R(2, 6), R(1, 5)
    b = r1 * r2
    a = r1 + r2
    if a <= 0 or b <= 0:
        return _solve_ln()
    return {
        "problemTex": f"\\ln(x)+\\ln(x-{r2}) = \\ln({b}) \\quad \\Rightarrow \\quad x = \\,?",
        "answerTex": str(r1),
        "answerNorm": str(r1),
        "steps": [
            {"label": "Condense left side", "math": f"\\ln(x(x-{r2})) = \\ln({b})", "note": "product rule"},
            {"label": "Since ln is 1-1", "math": f"x(x-{r2}) = {b}", "note": ""},
            {"label": "Expand and rearrange", "math": f"x^2-{r2}x-{b}=0", "note": ""},
            {"label": "Factor", "math": f"(x-{r1})(x+{r2}) = 0", "note": "" if r1 != r2 else ""},
            {"label": "Reject negative root", "math": f"x = {r1}", "note": f"x must be positive (ln domain)"},
        ],
    }


def _expand_complex():
    # ln(x^a * sqrt(x+1) / (x-b)^c)
    a = R(2, 4); c = R(2, 3); b = R(1, 4)
    compact = f"\\dfrac{{x^{{{a}}}\\sqrt{{x+{b}}}}}{{(x-{b})^{{{c}}}}}"
    expanded = f"{a}\\ln x + \\dfrac{{1}}{{2}}\\ln(x+{b}) - {c}\\ln(x-{b})"
    norm = f"{a}*ln(x)+0.5*ln(x+{b})-{c}*ln(x-{b})"
    return {
        "problemTex": f"\\ln\\!\\left({compact}\\right) = \\,?",
        "answerTex": expanded,
        "answerNorm": norm,
        "steps": [
            {"label": "Product/quotient rules", "math": f"\\ln(x^{{{a}}})+\\ln\\!\\sqrt{{x+{b}}}-\\ln(x-{b})^{{{c}}}", "note": ""},
            {"label": "Power rule: sqrt = power 1/2", "math": f"{a}\\ln x+\\dfrac{{1}}{{2}}\\ln(x+{b})-{c}\\ln(x-{b})", "note": ""},
        ],
    }


def _base_conversion_solve():
    # log_2(x) + log_4(x) = k → convert log_4(x) = log_2(x)/2 → (3/2)log_2(x) = k
    k = pick([3, 4, 6])
    # (3/2)log_2(x) = k → log_2(x) = 2k/3 → x = 2^(2k/3)
    # Choose k divisible by 3
    k = 6
    return {
        "problemTex": f"\\log_2(x)+\\log_4(x)={k} \\quad \\Rightarrow \\quad x = \\,?",
        "answerTex": f"2^{{4}} = 16",
        "answerNorm": "16",
        "steps": [
            {"label": "Convert log_4 to log_2", "math": f"\\log_4(x)=\\dfrac{{\\log_2(x)}}{{\\log_2(4)}}=\\dfrac{{\\log_2(x)}}{{2}}", "note": "change of base"},
            {"label": "Substitute", "math": f"\\log_2(x)+\\dfrac{{\\log_2(x)}}{{2}}={k}", "note": ""},
            {"label": "Combine", "math": f"\\dfrac{{3}}{{2}}\\log_2(x)={k} \\Rightarrow \\log_2(x)=4", "note": ""},
            {"label": "Solve", "math": "x=2^4=16", "note": ""},
        ],
    }


diff4 = [_solve_log_equation, _expand_complex, _base_conversion_solve]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _exponential_growth_setup():
    # A = A0 * e^(kt); given two data points, find k
    A0 = pick([100, 200, 500, 1000])
    t1 = pick([1, 2, 3])
    mult = pick([2, 3, 4])
    A1 = A0 * mult
    return {
        "problemTex": (
            f"A population starts at {A0} and grows to {A1} after {t1} {'hour' if t1==1 else 'hours'}."
            f"\\quad \\text{{Find }} k \\text{{ in }} A=A_0 e^{{kt}}."
        ),
        "answerTex": f"k=\\dfrac{{\\ln {mult}}}{{{t1}}}",
        "answerNorm": f"ln({mult})/{t1}",
        "steps": [
            {"label": "Set up equation", "math": f"{A1}={A0}e^{{k\\cdot{t1}}}", "note": ""},
            {"label": "Divide by A₀", "math": f"{mult}=e^{{{t1}k}}", "note": ""},
            {"label": "Take ln both sides", "math": f"\\ln {mult}={t1}k", "note": ""},
            {"label": "Solve for k", "math": f"k=\\dfrac{{\\ln {mult}}}{{{t1}}}", "note": ""},
        ],
    }


def _nested_solve():
    # ln(ln(x)) = a → solve step by step
    a = R(1, 2)
    return {
        "problemTex": f"\\ln(\\ln(x)) = {a} \\quad \\Rightarrow \\quad x = \\,?",
        "answerTex": f"e^{{e^{{{a}}}}}",
        "answerNorm": f"e^(e^{a})",
        "steps": [
            {"label": "Exponentiate both sides", "math": f"e^{{\\ln(\\ln x)}}=e^{{{a}}}", "note": ""},
            {"label": "Simplify", "math": f"\\ln x = e^{{{a}}}", "note": ""},
            {"label": "Exponentiate again", "math": f"x = e^{{e^{{{a}}}}}", "note": ""},
        ],
    }


def _full_log_diff_setup():
    # y = (x^2+1)^3 * sin(x) / sqrt(x+2) → ln form
    return {
        "problemTex": "\\text{Rewrite using }\\ln: \\quad y=\\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}}",
        "answerTex": "\\ln y = 3\\ln(x^2+1)+\\ln(\\sin x)-\\tfrac{1}{2}\\ln(x+2)",
        "answerNorm": "3*ln(x^2+1)+ln(sin(x))-0.5*ln(x+2)",
        "steps": [
            {"label": "ln both sides", "math": "\\ln y = \\ln\\!\\left[\\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}}\\right]", "note": ""},
            {"label": "Product/quotient rules", "math": "= \\ln(x^2+1)^3+\\ln(\\sin x)-\\ln\\sqrt{x+2}", "note": ""},
            {"label": "Power rule", "math": "= 3\\ln(x^2+1)+\\ln(\\sin x)-\\tfrac{1}{2}\\ln(x+2)", "note": ""},
        ],
    }


diff5 = [_exponential_growth_setup, _nested_solve, _full_log_diff_setup]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
