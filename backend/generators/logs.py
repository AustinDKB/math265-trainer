import random
from math_utils import R, pick, simplify_frac, frac_to_tex
from problem_builder import problem, step

_VARS = ["x", "y", "z", "a", "b"]

# ── diff1 ──────────────────────────────────────────────────────────────────────

def _product_rule():
    a, b = pick(["x","y"]), pick(["y","z"])
    return problem(
        problem_tex=f"\\ln({a}\\cdot {b}) = \\,?",
        answer_tex=f"\\ln {a}+\\ln {b}",
        answer_norm=f"ln({a})+ln({b})",
        steps=[step("Product rule", f"\\ln({a}\\cdot {b})=\\ln {a}+\\ln {b}")],
    )


def _quotient_rule():
    a, b = "x", pick(["y","z","a"])
    return problem(
        problem_tex=f"\\ln\\!\\left(\\dfrac{{{a}}}{{{b}}}\\right) = \\,?",
        answer_tex=f"\\ln {a}-\\ln {b}",
        answer_norm=f"ln({a})-ln({b})",
        steps=[step("Quotient rule", f"\\ln\\!\\left(\\dfrac{{{a}}}{{{b}}}\\right)=\\ln {a}-\\ln {b}")],
    )


def _power_rule():
    n = R(2, 8)
    return problem(
        problem_tex=f"\\ln(x^{{{n}}}) = \\,?",
        answer_tex=f"{n}\\ln x",
        answer_norm=f"{n}*ln(x)",
        steps=[step("Power rule", f"\\ln(x^{{{n}}})={n}\\ln x")],
    )


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

    return problem(
        problem_tex=f"\\ln\\!\\left({compact}\\right) = \\,?",
        answer_tex=expanded_tex,
        answer_norm=norm,
        steps=[
            step("Apply product/quotient rules", "+".join(
                f"\\ln({v}^{{{e}}})" if e > 1 else f"\\ln {v}"
                for v, e in zip(vars_num, exps_num)
            ) + "".join(f"-\\ln({v}^{{{e}}})" if e > 1 else f"-\\ln {v}" for v, e in zip(vars_den, exps_den))),
            step("Apply power rule", expanded_tex),
        ],
    )


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
    return problem(
        problem_tex=f"\\text{{Condense: }}\\; {expanded} = \\,?",
        answer_tex=f"\\ln\\!\\left({orig_compact_inner}\\right)",
        answer_norm=f"ln({orig_compact_inner.replace('{','').replace('}','').replace('\\dfrac','').replace('dfrac','')})",
        steps=[
            step("Power rule (reverse)", f"{expanded} \\to \\ln(\\ldots^n)", "coefficient → exponent"),
            step("Product/quotient rule (reverse)", f"\\ln(\\ldots) \\to \\ln\\!\\left({orig_compact_inner}\\right)", "+ means multiply, − means divide"),
        ],
    )


def _solve_ln():
    # ln(x) = k → x = e^k; pick k ∈ {1..5}
    k = R(1, 5)
    return problem(
        problem_tex=f"\\ln(x) = {k} \\quad \\Rightarrow \\quad x = \\,?",
        answer_tex=f"e^{{{k}}}",
        answer_norm=f"e^{k}",
        steps=[
            step("Exponentiate both sides", f"e^{{\\ln(x)}} = e^{{{k}}}"),
            step("Simplify", f"x = e^{{{k}}}", "e^ln(x) = x"),
        ],
    )


def _solve_exponential():
    # e^(ax) = k → x = ln(k)/a
    a = R(1, 4)
    k = R(2, 12)
    a_tex = "" if a == 1 else str(a)
    return problem(
        problem_tex=f"e^{{{a_tex}x}} = {k} \\quad \\Rightarrow \\quad x = \\,?",
        answer_tex=f"\\dfrac{{\\ln {k}}}{{{a}}}",
        answer_norm=f"ln({k})/{a}",
        steps=[
            step("Take ln of both sides", f"\\ln(e^{{{a_tex}x}}) = \\ln {k}"),
            step("Simplify left side", f"{a_tex}x = \\ln {k}", "ln(e^u) = u"),
            step("Solve for x", f"x = \\dfrac{{\\ln {k}}}{{{a}}}"),
        ],
    )


def _change_of_base():
    b = pick([2, 3, 5, 10])
    n = R(2, 20)
    return problem(
        problem_tex=f"\\log_{{{b}}}({n}) = \\,?",
        answer_tex=f"\\dfrac{{\\ln {n}}}{{\\ln {b}}}",
        answer_norm=f"ln({n})/ln({b})",
        steps=[
            step("Change of base formula", f"\\log_{{{b}}}({n}) = \\dfrac{{\\ln {n}}}{{\\ln {b}}}"),
        ],
    )


diff2 = [_expand_expression, _expand_expression, _condense_expression, _solve_ln, _solve_exponential, _change_of_base]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _nested_log():
    # ln(e^(f(x))) = f(x)
    fns = [("2x","2x"), ("x^2","x^2"), ("3x+1","3x+1"), ("x+5","x+5")]
    fx, fx_norm = pick(fns)
    return problem(
        problem_tex=f"\\ln\\!\\left(e^{{{fx}}}\\right) = \\,?",
        answer_tex=fx,
        answer_norm=fx_norm,
        steps=[
            step("ln and e are inverse functions", "\\ln(e^u) = u"),
            step("Apply", f"\\ln(e^{{{fx}}}) = {fx}"),
        ],
    )


def _combined_exp_log():
    # e^(n·ln(x)) = x^n
    n = R(2, 6)
    return problem(
        problem_tex=f"e^{{{n}\\ln x}} = \\,?",
        answer_tex=f"x^{{{n}}}",
        answer_norm=f"x^{n}",
        steps=[
            step("Power rule of ln", f"{n}\\ln x = \\ln(x^{{{n}}})"),
            step("Then e^ln(...) cancels", f"e^{{\\ln(x^{{{n}}})}} = x^{{{n}}}"),
        ],
    )


def _log_diff_setup():
    # y = x^x → ln(y) = x·ln(x)
    fns = [
        ("x^x", "x\\ln x"),
        ("x^{\\sin x}", "\\sin(x)\\cdot\\ln x"),
        ("(x+1)^{2x}", "2x\\ln(x+1)"),
    ]
    y_tex, rhs_tex = pick(fns)
    return problem(
        problem_tex=f"\\text{{Rewrite }} y={y_tex} \\text{{ using }} \\ln \\text{{: }} \\ln y = \\,?",
        answer_tex=rhs_tex,
        answer_norm=rhs_tex.replace("{","").replace("}","").replace("\\","").replace("cdot","*"),
        steps=[
            step("Take ln of both sides", f"\\ln y = \\ln\\!\\left({y_tex}\\right)"),
            step("Apply power rule of ln", f"\\ln y = {rhs_tex}", "ln(f^g) = g·ln(f)"),
        ],
    )


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
    return problem(
        problem_tex=f"\\ln(x)+\\ln(x-{r2}) = \\ln({b}) \\quad \\Rightarrow \\quad x = \\,?",
        answer_tex=str(r1),
        answer_norm=str(r1),
        steps=[
            step("Condense left side", f"\\ln(x(x-{r2})) = \\ln({b})", "product rule"),
            step("Since ln is 1-1", f"x(x-{r2}) = {b}"),
            step("Expand and rearrange", f"x^2-{r2}x-{b}=0"),
            step("Factor", f"(x-{r1})(x+{r2}) = 0", "" if r1 != r2 else ""),
            step("Reject negative root", f"x = {r1}", f"x must be positive (ln domain)"),
        ],
    )


def _expand_complex():
    # ln(x^a * sqrt(x+1) / (x-b)^c)
    a = R(2, 4); c = R(2, 3); b = R(1, 4)
    compact = f"\\dfrac{{x^{{{a}}}\\sqrt{{x+{b}}}}}{{(x-{b})^{{{c}}}}}"
    expanded = f"{a}\\ln x + \\dfrac{{1}}{{2}}\\ln(x+{b}) - {c}\\ln(x-{b})"
    norm = f"{a}*ln(x)+0.5*ln(x+{b})-{c}*ln(x-{b})"
    return problem(
        problem_tex=f"\\ln\\!\\left({compact}\\right) = \\,?",
        answer_tex=expanded,
        answer_norm=norm,
        steps=[
            step("Product/quotient rules", f"\\ln(x^{{{a}}})+\\ln\\!\\sqrt{{x+{b}}}-\\ln(x-{b})^{{{c}}}"),
            step("Power rule: sqrt = power 1/2", f"{a}\\ln x+\\dfrac{{1}}{{2}}\\ln(x+{b})-{c}\\ln(x-{b})"),
        ],
    )


def _base_conversion_solve():
    # log_2(x) + log_4(x) = k → convert log_4(x) = log_2(x)/2 → (3/2)log_2(x) = k
    k = pick([3, 4, 6])
    # (3/2)log_2(x) = k → log_2(x) = 2k/3 → x = 2^(2k/3)
    # Choose k divisible by 3
    k = 6
    return problem(
        problem_tex=f"\\log_2(x)+\\log_4(x)={k} \\quad \\Rightarrow \\quad x = \\,?",
        answer_tex=f"2^{{4}} = 16",
        answer_norm="16",
        steps=[
            step("Convert log_4 to log_2", f"\\log_4(x)=\\dfrac{{\\log_2(x)}}{{\\log_2(4)}}=\\dfrac{{\\log_2(x)}}{{2}}", "change of base"),
            step("Substitute", f"\\log_2(x)+\\dfrac{{\\log_2(x)}}{{2}}={k}"),
            step("Combine", f"\\dfrac{{3}}{{2}}\\log_2(x)={k} \\Rightarrow \\log_2(x)=4"),
            step("Solve", "x=2^4=16"),
        ],
    )


diff4 = [_solve_log_equation, _expand_complex, _base_conversion_solve]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _exponential_growth_setup():
    # A = A0 * e^(kt); given two data points, find k
    A0 = pick([100, 200, 500, 1000])
    t1 = pick([1, 2, 3])
    mult = pick([2, 3, 4])
    A1 = A0 * mult
    return problem(
        problem_tex=(
            f"A population starts at {A0} and grows to {A1} after {t1} {'hour' if t1==1 else 'hours'}."
            f"\\quad \\text{{Find }} k \\text{{ in }} A=A_0 e^{{kt}}."
        ),
        answer_tex=f"k=\\dfrac{{\\ln {mult}}}{{{t1}}}",
        answer_norm=f"ln({mult})/{t1}",
        steps=[
            step("Set up equation", f"{A1}={A0}e^{{k\\cdot{t1}}}"),
            step("Divide by A₀", f"{mult}=e^{{{t1}k}}"),
            step("Take ln both sides", f"\\ln {mult}={t1}k"),
            step("Solve for k", f"k=\\dfrac{{\\ln {mult}}}{{{t1}}}"),
        ],
    )


def _nested_solve():
    # ln(ln(x)) = a → solve step by step
    a = R(1, 2)
    return problem(
        problem_tex=f"\\ln(\\ln(x)) = {a} \\quad \\Rightarrow \\quad x = \\,?",
        answer_tex=f"e^{{e^{{{a}}}}}",
        answer_norm=f"e^(e^{a})",
        steps=[
            step("Exponentiate both sides", f"e^{{\\ln(\\ln x)}}=e^{{{a}}}"),
            step("Simplify", f"\\ln x = e^{{{a}}}"),
            step("Exponentiate again", f"x = e^{{e^{{{a}}}}}"),
        ],
    )


def _full_log_diff_setup():
    # y = (x^2+1)^3 * sin(x) / sqrt(x+2) → ln form
    return problem(
        problem_tex="\\text{Rewrite using }\\ln: \\quad y=\\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}}",
        answer_tex="\\ln y = 3\\ln(x^2+1)+\\ln(\\sin x)-\\tfrac{1}{2}\\ln(x+2)",
        answer_norm="3*ln(x^2+1)+ln(sin(x))-0.5*ln(x+2)",
        steps=[
            step("ln both sides", "\\ln y = \\ln\\!\\left[\\dfrac{(x^2+1)^3 \\sin x}{\\sqrt{x+2}}\\right]"),
            step("Product/quotient rules", "= \\ln(x^2+1)^3+\\ln(\\sin x)-\\ln\\sqrt{x+2}"),
            step("Power rule", "= 3\\ln(x^2+1)+\\ln(\\sin x)-\\tfrac{1}{2}\\ln(x+2)"),
        ],
    )


diff5 = [_exponential_growth_setup, _nested_solve, _full_log_diff_setup]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}