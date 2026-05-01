import random
import math as _math
from math_utils import R, pick
from problem_builder import problem, step

# ── Function pool ─────────────────────────────────────────────────────────────
# Each entry: (name_tex, formula_x_tex, formula_u_tex, eval_fn)
# formula_x_tex: LaTeX with x, formula_u_tex: LaTeX with {u} placeholder

_FUNCS = [
    ("x^2",       "x^2",             "{u}^2",                     lambda u: u**2),
    ("x^3",       "x^3",             "{u}^3",                     lambda u: u**3),
    ("\\sqrt{x}", "\\sqrt{x}",       "\\sqrt{{{u}}}",             lambda u: u**0.5 if u >= 0 else None),
    ("\\sin(x)",  "\\sin(x)",        "\\sin({u})",                lambda u: _math.sin(u)),
    ("\\cos(x)",  "\\cos(x)",        "\\cos({u})",                lambda u: _math.cos(u)),
    ("e^x",       "e^x",             "e^{{{u}}}",                 lambda u: _math.exp(u)),
    ("\\ln(x)",   "\\ln(x)",         "\\ln({u})",                 lambda u: _math.log(u) if u > 0 else None),
]

def _compose_tex(outer_u_tex, inner_x_tex):
    """Replace {u} in outer's u-template with inner's x-formula."""
    needs_paren = any(c in inner_x_tex for c in ["+", "-", "*", "/", "^"]) and not inner_x_tex.startswith("(")
    inner = f"({inner_x_tex})" if needs_paren and not inner_x_tex.startswith("\\") else inner_x_tex
    return outer_u_tex.replace("{u}", inner)


def _eval_fn(outer_eval, inner_eval):
    def f(x):
        iv = inner_eval(x)
        if iv is None: return None
        return outer_eval(iv)
    return f


def _safe_pick_pair(exclude_same=True):
    """Pick two distinct functions from pool."""
    funcs = list(range(len(_FUNCS)))
    outer_idx = pick(funcs)
    inner_idx = pick([i for i in funcs if i != outer_idx])
    return _FUNCS[outer_idx], _FUNCS[inner_idx]


# ── diff1 ──────────────────────────────────────────────────────────────────────

def _compute_fog():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    return problem(
        problem_tex=f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Find }} f(g(x)).",
        answer_tex=composed_tex,
        answer_norm=composed_tex.replace("{","").replace("}","").replace("\\",""),
        steps=[
            step("Substitute g(x) into f", f"f(g(x)) = {f[2].replace('{u}', 'g(x)')}", "replace x in f with g(x)"),
            step("Result", composed_tex),
        ],
    )


def _compute_gof():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(g[2], f[1])
    return problem(
        problem_tex=f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Find }} g(f(x)).",
        answer_tex=composed_tex,
        answer_norm=composed_tex.replace("{","").replace("}","").replace("\\",""),
        steps=[
            step("Substitute f(x) into g", f"g(f(x)) = {g[2].replace('{u}', 'f(x)')}", "replace x in g with f(x)"),
            step("Result", composed_tex),
        ],
    )


def _evaluate_numeric():
    a = R(1, 5); b = R(-4, 4); n = R(1, 4)
    gn = n**2
    fgn = a * gn + b
    b_tex = f"+{b}" if b > 0 else (str(b) if b < 0 else "")
    return problem(
        problem_tex=f"f(x)={a}x{b_tex},\\; g(x)=x^2.\\quad \\text{{Find }} f(g({n})).",
        answer_tex=str(fgn),
        answer_norm=str(fgn),
        steps=[
            step("Compute g(n) first", f"g({n}) = {n}^2 = {gn}"),
            step("Compute f(g(n))", f"f({gn}) = {a}\\cdot{gn}{b_tex} = {fgn}"),
        ],
    )


def _identify_outer_inner():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    return problem(
        problem_tex=f"\\text{{In }} {composed_tex} \\text{{, identify the outer function }} f \\text{{ and inner function }} g.",
        answer_tex=f"f(u)={f[2].replace('{u}','u')},\\; g(x)={g[1]}",
        answer_norm=f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}",
        steps=[
            step("Inner function: what's inside?", f"g(x) = {g[1]}", "applied first"),
            step("Outer function: what wraps it?", f"f(u) = {f[2].replace('{u}','u')}", "applied second"),
        ],
        inputHint=f"Type:  f=<outer>, g=<inner>  e.g.  f=sin(x),g=e^x",
    )


def _simplify_linear_inverse():
    """f and g are inverses — composition collapses to x."""
    case = pick([1, 2])
    if case == 1:
        a = R(1, 9)
        return problem(
            problem_tex=f"f(x)=x+{a},\\;g(x)=x-{a}.\\quad\\text{{Simplify }}f(g(x)).",
            answer_tex="x",
            answer_norm="x",
            steps=[
                step("Substitute g(x) into f", f"f(g(x))=(x-{a})+{a}"),
                step("Simplify", "=x", f"+{a} and \u2212{a} cancel"),
            ],
        )
    else:
        k = R(2, 7)
        return problem(
            problem_tex=f"f(x)={k}x,\\;g(x)=\\dfrac{{x}}{{{k}}}.\\quad\\text{{Simplify }}f(g(x)).",
            answer_tex="x",
            answer_norm="x",
            steps=[
                step("Substitute", f"f(g(x))={k}\\cdot\\dfrac{{x}}{{{k}}}"),
                step("Cancel", "=x"),
            ],
        )


diff1 = [_compute_fog, _compute_fog, _compute_gof, _evaluate_numeric, _identify_outer_inner, _simplify_linear_inverse]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _decompose_two():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    return problem(
        problem_tex=f"\\text{{Write }} {composed_tex} \\text{{ as }} f(g(x)).",
        answer_tex=f"f(u)={f[2].replace('{u}','u')},\\; g(x)={g[1]}",
        answer_norm=f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}",
        steps=[
            step("Find inner (what's applied first?)", f"g(x) = {g[1]}"),
            step("Find outer (what wraps g?)", f"f(u) = {f[2].replace('{u}','u')}"),
            step("Verify: f(g(x))", f"f(g(x)) = {composed_tex}"),
        ],
        validForms=[f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}"],
        inputHint=f"Type:  f=<outer>, g=<inner>  e.g.  f=sin(x),g=e^x",
    )


def _decompose_three():
    funcs = random.sample(_FUNCS, 3)
    h_name, h_x, h_u, _ = funcs[0]
    g_name, g_x, g_u, _ = funcs[1]
    f_name, f_x, f_u, _ = funcs[2]
    gh_tex = _compose_tex(g_u, h_x)
    fgh_tex = _compose_tex(f_u, gh_tex)
    return problem(
        problem_tex=f"\\text{{Decompose }} {fgh_tex} \\text{{ as }} f(g(h(x))).",
        answer_tex=f"f(u)={f_u.replace('{u}','u')},\\; g(u)={g_u.replace('{u}','u')},\\; h(x)={h_x}",
        answer_norm=f"f={f_name},g={g_name},h={h_name}".replace("{","").replace("}","").replace("\\",""),
        steps=[
            step("Innermost (h)", f"h(x)={h_x}", "deepest nested function"),
            step("Middle (g)", f"g(u)={g_u.replace('{u}','u')}"),
            step("Outer (f)", f"f(u)={f_u.replace('{u}','u')}", "outermost"),
        ],
        inputHint="Type:  f=<outer>, g=<middle>, h=<inner>  e.g.  f=sin(x),g=x^2,h=e^x",
    )


def _build_from_description():
    ops = [
        ("Square it, then take ln",         "\\ln(x^2)",             "ln(x^2)"),
        ("Apply sin, then square it",        "(\\sin x)^2",           "sin^2(x)"),
        ("Apply e^x, then take cos of it",   "\\cos(e^x)",            "cos(e^x)"),
        ("Take sqrt, then cube it",          "(\\sqrt{x})^3 = x^{3/2}","x^(3/2)"),
        ("Take ln, then apply e^x",          "e^{\\ln x} = x",       "x"),
        ("Square it, then apply sin",        "\\sin(x^2)",            "sin(x^2)"),
    ]
    desc, result_tex, result_norm = pick(ops)
    return problem(
        problem_tex=f"\\text{{Build the composite function: \\textquotedblleft{desc}\\textquotedblright}}",
        answer_tex=result_tex,
        answer_norm=result_norm,
        steps=[
            step("Start with x, apply first operation", desc.split(",")[0].strip()),
            step("Apply second operation to result", result_tex),
        ],
    )


def _expand_linear_compose():
    """f(x)=ax+b, g(x)=cx+d — expand f(g(x)) to slope-intercept form."""
    a = pick([2, 3, 4, 5])
    b = R(-5, 5)
    c = pick([2, 3, 4])
    d = R(-4, 4)
    ac = a * c
    adb = a * d + b

    def sgn(n):
        return (f"+{n}" if n > 0 else str(n)) if n != 0 else ""

    f_tex = f"{a}x{sgn(b)}"
    g_tex = f"{c}x{sgn(d)}"
    result_tex = f"{ac}x{sgn(adb)}"
    result_norm = f"{ac}*x" + (f"+{adb}" if adb > 0 else (str(adb) if adb < 0 else ""))
    return problem(
        problem_tex=f"f(x)={f_tex},\\;g(x)={g_tex}.\\quad\\text{{Simplify }}f(g(x)).",
        answer_tex=result_tex,
        answer_norm=result_norm,
        steps=[
            step("Substitute g(x) into f", f"f(g(x))={a}({g_tex}){sgn(b)}"),
            step("Distribute", f"{ac}x{sgn(a*d)}{sgn(b)}"),
            step("Combine constants", result_tex),
        ],
    )


diff2 = [_decompose_two, _decompose_two, _decompose_three, _build_from_description, _expand_linear_compose]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _domain_of_composition():
    a = R(1, 8)
    return problem(
        problem_tex=f"f(x)=\\sqrt{{x}},\\; g(x)=x-{a}.\\quad \\text{{Find the domain of }} f(g(x)).",
        answer_tex=f"x \\geq {a},\\; \\text{{or}} \\; [{a},\\infty)",
        answer_norm=f"x>={a}",
        steps=[
            step("Form the composition", f"f(g(x))=\\sqrt{{x-{a}}}"),
            step("Require radicand \u2265 0", f"x-{a}\\geq 0", "\u221a requires non-negative input"),
            step("Solve", f"x \\geq {a}", f"domain: [{a},\\infty)"),
        ],
    )


def _multi_compose():
    f, g, h = random.sample(_FUNCS, 3)
    gh_tex = _compose_tex(g[2], h[1])
    fgh_tex = _compose_tex(f[2], gh_tex)
    return problem(
        problem_tex=f"f(x)={f[1]},\\; g(x)={g[1]},\\; h(x)={h[1]}.\\quad \\text{{Find }} f(g(h(x))).",
        answer_tex=fgh_tex,
        answer_norm=fgh_tex.replace("{","").replace("}","").replace("\\",""),
        steps=[
            step("Compute h(x)", h[1], "start innermost"),
            step("Compute g(h(x))", gh_tex),
            step("Compute f(g(h(x)))", fgh_tex),
        ],
    )


def _simplify_log_exp_compose():
    """Simplify f(g(x)) using e/ln inverse identities."""
    k = R(2, 4)
    cases = [
        problem(
            problem_tex=f"f(x)=e^x,\\;g(x)={k}\\ln x.\\quad\\text{{Simplify }}f(g(x)).",
            answer_tex=f"x^{{{k}}}",
            answer_norm=f"x^{k}",
            steps=[
                step("Substitute", f"e^{{{k}\\ln x}}"),
                step("Use a\u00b7ln x = ln(x^a)", f"e^{{\\ln(x^{{{k}}})}}=x^{{{k}}}", "e and ln cancel"),
            ],
        ),
        problem(
            problem_tex=f"f(x)=\\ln x,\\;g(x)=e^{{{k}x}}.\\quad\\text{{Simplify }}f(g(x)).",
            answer_tex=f"{k}x",
            answer_norm=f"{k}*x",
            steps=[
                step("Substitute", f"\\ln(e^{{{k}x}})"),
                step("Use ln(e^u)=u", f"={k}x"),
            ],
        ),
    ]
    return pick(cases)


diff3 = [_domain_of_composition, _domain_of_composition, _multi_compose, _simplify_log_exp_compose]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _simplify_fog():
    pairs = [
        ("(\\sqrt{x}+1)^2", "\\sqrt{x}+1", "x^2", "x+2\\sqrt{x}+1", "x+2sqrt(x)+1"),
        ("\\sqrt{x^2}=|x|",  "x^2",   "\\sqrt{x}",  "|x|",  "|x|"),
        ("e^{\\ln x}=x",     "\\ln x", "e^x",        "x",    "x"),
        ("\\ln(e^x)=x",      "e^x",    "\\ln(x)",    "x",    "x"),
    ]
    desc, g_tex, f_tex, result_tex, result_norm = pick(pairs)
    return problem(
        problem_tex=f"f(x)={f_tex},\\; g(x)={g_tex}.\\quad \\text{{Fully simplify }} f(g(x)).",
        answer_tex=result_tex,
        answer_norm=result_norm,
        steps=[
            step("Substitute", f"f(g(x))={desc.split('=')[0]}"),
            step("Simplify", result_tex, desc),
        ],
    )


def _fog_commutativity():
    f, g = _safe_pick_pair()
    fog_tex = _compose_tex(f[2], g[1])
    gof_tex = _compose_tex(g[2], f[1])
    equal = fog_tex == gof_tex
    return problem(
        problem_tex=f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Does }} f(g(x))=g(f(x))?",
        answer_tex=("\\text{Yes}" if equal else
                    f"\\text{{No}}: f(g(x))={fog_tex},\\; g(f(x))={gof_tex}"),
        answer_norm="yes" if equal else "no",
        steps=[
            step("Compute f(g(x))", fog_tex),
            step("Compute g(f(x))", gof_tex),
            step("Compare", "\\text{Equal}" if equal else "\\text{Not equal}", "composition is generally NOT commutative"),
        ],
    )


def _solve_fog():
    a = R(2, 5); b = R(1, 4); c = a + b
    x_sol = (c - b) // a if (c - b) % a == 0 else None
    if x_sol is None:
        a = 2; b = 1; c = 5; x_sol = 2
    return problem(
        problem_tex=f"f(x)=x+{b},\\; g(x)={a}x.\\quad \\text{{Solve }} f(g(x))={c}.",
        answer_tex=f"x = {x_sol}",
        answer_norm=str(x_sol),
        steps=[
            step("Form composition", f"f(g(x))={a}x+{b}"),
            step("Set equal to c", f"{a}x+{b}={c}"),
            step("Solve", f"x={x_sol}"),
        ],
    )


def _simplify_quadratic_compose():
    """f(x)=x²+bx, g(x)=x+a — expand f(g(x)) fully, collect terms."""
    a = R(1, 5)
    b = pick([-4, -3, -2, -1, 1, 2, 3, 4])
    lin = 2 * a + b
    const = a * a + b * a

    def sgn(n):
        return (f"+{n}" if n > 0 else str(n)) if n != 0 else ""

    b_term = f"+{b}x" if b > 0 else f"{b}x"
    f_tex = f"x^2{b_term}"
    g_tex = f"x+{a}"

    lin_part = (f"+{lin}x" if lin > 0 else (f"{lin}x" if lin < 0 else ""))
    result_tex = f"x^2{lin_part}{sgn(const)}"

    parts = ["x^2"]
    if lin: parts.append(f"{lin}*x")
    if const: parts.append(str(const))
    result_norm = "+".join(parts).replace("+-", "-")

    return problem(
        problem_tex=f"f(x)={f_tex},\\;g(x)={g_tex}.\\quad\\text{{Expand and simplify }}f(g(x)).",
        answer_tex=result_tex,
        answer_norm=result_norm,
        steps=[
            step("Substitute", f"(x+{a})^2+{b}(x+{a})"),
            step("Expand (x+a)\u00b2", f"x^2+{2*a}x+{a*a}+{b}x+{b*a}"),
            step("Collect like terms", result_tex),
        ],
    )


diff4 = [_simplify_fog, _fog_commutativity, _solve_fog, _simplify_quadratic_compose]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _chain_rule_setup():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    rules = {
        "x^2":      "power rule",
        "x^3":      "power rule",
        "\\sin(x)": "derivative of sin",
        "\\cos(x)": "derivative of cos",
        "e^x":      "derivative of e\u02e3",
        "\\ln(x)":  "derivative of ln",
    }
    f_rule = rules.get(f[1], "standard rule")
    g_rule = rules.get(g[1], "standard rule")
    return problem(
        problem_tex=f"\\text{{Identify all derivative rules needed to differentiate }} {composed_tex}.",
        answer_tex=f"\\text{{Chain rule: outer=}}\\,{f[1]},\\text{{ inner=}}\\,{g[1]}",
        answer_norm=f"chain,outer={f[0]},inner={g[0]}".replace("{","").replace("}","").replace("\\",""),
        steps=[
            step("Identify inner function", f"g(x)={g[1]}", f"requires: {g_rule}"),
            step("Identify outer function", f"f(u)={f[2].replace('{u}','u')}", f"requires: {f_rule}"),
            step("Chain rule: d/dx[f(g(x))] = f'(g(x))\u00b7g'(x)", "\\text{will need both rules}"),
        ],
    )


def _inverse_composition_verify():
    pairs = [
        ("e^x",          "\\ln(x)",     "e^{\\ln x}=x"),
        ("\\ln(x)",      "e^x",         "\\ln(e^x)=x"),
        ("x^3",          "x^{1/3}",     "(x^{1/3})^3=x"),
        ("2x+1",         "(x-1)/2",     "2\\cdot\\frac{x-1}{2}+1=x"),
    ]
    f_tex, fi_tex, verify = pick(pairs)
    return problem(
        problem_tex=f"f(x)={f_tex},\\; f^{{-1}}(x)={fi_tex}.\\quad \\text{{Verify }} f(f^{{-1}}(x))=x.",
        answer_tex=f"{verify}\\;\\checkmark",
        answer_norm="x",
        steps=[
            step("Substitute f\u207b\u00b9 into f", f"f(f^{{-1}}(x))={verify.split('=')[0]}"),
            step("Simplify", "= x\\;\\checkmark", "confirms f and f\u207b\u00b9 are inverses"),
        ],
    )


def _four_layer_compose():
    funcs = random.sample([f for f in _FUNCS if f[3] is not None], 4)
    h1, h2, h3, h4 = funcs
    x_val = pick([1, 2])
    try:
        v1 = h1[3](x_val)
        v2 = h2[3](v1) if v1 is not None else None
        v3 = h3[3](v2) if v2 is not None else None
        v4 = h4[3](v3) if v3 is not None else None
    except Exception:
        return _compute_fog()
    if v4 is None:
        return _compute_fog()
    v4_rounded = round(v4, 4)
    return problem(
        problem_tex=(
            f"f(x)={h4[1]},\\;g(x)={h3[1]},\\;h(x)={h2[1]},\\;k(x)={h1[1]}."
            f"\\quad\\text{{Find }}(f\\circ g\\circ h\\circ k)({x_val})."
        ),
        answer_tex=str(v4_rounded),
        answer_norm=str(v4_rounded),
        steps=[
            step(f"k({x_val})", f"k({x_val})={round(v1,4)}"),
            step(f"h(k({x_val}))", f"h({round(v1,4)})={round(v2,4) if v2 else '?'}"),
            step(f"g(h(...))", f"g({round(v2,4) if v2 else '?'})={round(v3,4) if v3 else '?'}"),
            step(f"f(g(...))", f"f({round(v3,4) if v3 else '?'})={v4_rounded}"),
        ],
    )


def _simplify_triple_chain():
    """f(x)=e^x, g(x)=kx, h(x)=ln x → f(g(h(x)))=x^k."""
    k = R(2, 5)
    return problem(
        problem_tex=(
            f"f(x)=e^x,\\;g(x)={k}x,\\;h(x)=\\ln x.\\quad"
            f"\\text{{Simplify }}f(g(h(x)))."
        ),
        answer_tex=f"x^{{{k}}}",
        answer_norm=f"x^{k}",
        steps=[
            step("h(x)", "h(x)=\\ln x"),
            step("g(h(x))", f"g(\\ln x)={k}\\ln x"),
            step("f(g(h(x)))", f"e^{{{k}\\ln x}}"),
            step("Use e^(k\u00b7ln x)=x^k", f"=x^{{{k}}}"),
        ],
    )


diff5 = [_chain_rule_setup, _inverse_composition_verify, _four_layer_compose, _simplify_triple_chain]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}