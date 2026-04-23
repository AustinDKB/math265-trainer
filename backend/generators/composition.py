import random
import math as _math
from math_utils import R, pick

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
    # Wrap inner in parens if complex
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
    return {
        "problemTex": f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Find }} f(g(x)).",
        "answerTex": composed_tex,
        "answerNorm": composed_tex.replace("{","").replace("}","").replace("\\",""),
        "steps": [
            {"label": "Substitute g(x) into f", "math": f"f(g(x)) = {f[2].replace('{u}', 'g(x)')}", "note": "replace x in f with g(x)"},
            {"label": "Result", "math": composed_tex, "note": ""},
        ],
    }


def _compute_gof():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(g[2], f[1])
    return {
        "problemTex": f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Find }} g(f(x)).",
        "answerTex": composed_tex,
        "answerNorm": composed_tex.replace("{","").replace("}","").replace("\\",""),
        "steps": [
            {"label": "Substitute f(x) into g", "math": f"g(f(x)) = {g[2].replace('{u}', 'f(x)')}", "note": "replace x in g with f(x)"},
            {"label": "Result", "math": composed_tex, "note": ""},
        ],
    }


def _evaluate_numeric():
    # f(x) = ax+b, g(x) = x², find f(g(n))
    a = R(1, 5); b = R(-4, 4); n = R(1, 4)
    gn = n**2
    fgn = a * gn + b
    b_tex = f"+{b}" if b > 0 else (str(b) if b < 0 else "")
    return {
        "problemTex": f"f(x)={a}x{b_tex},\\; g(x)=x^2.\\quad \\text{{Find }} f(g({n})).",
        "answerTex": str(fgn),
        "answerNorm": str(fgn),
        "steps": [
            {"label": "Compute g(n) first", "math": f"g({n}) = {n}^2 = {gn}", "note": ""},
            {"label": "Compute f(g(n))", "math": f"f({gn}) = {a}\\cdot{gn}{b_tex} = {fgn}", "note": ""},
        ],
    }


def _identify_outer_inner():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    return {
        "problemTex": f"\\text{{In }} {composed_tex} \\text{{, identify the outer function }} f \\text{{ and inner function }} g.",
        "answerTex": f"f(u)={f[2].replace('{u}','u')},\\; g(x)={g[1]}",
        "answerNorm": f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}",
        "inputHint": f"Type:  f=<outer>, g=<inner>  e.g.  f=sin(x),g=e^x",
        "steps": [
            {"label": "Inner function: what's inside?", "math": f"g(x) = {g[1]}", "note": "applied first"},
            {"label": "Outer function: what wraps it?", "math": f"f(u) = {f[2].replace('{u}','u')}", "note": "applied second"},
        ],
    }


diff1 = [_compute_fog, _compute_fog, _compute_gof, _evaluate_numeric, _identify_outer_inner]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _decompose_two():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    return {
        "problemTex": f"\\text{{Write }} {composed_tex} \\text{{ as }} f(g(x)).",
        "answerTex": f"f(u)={f[2].replace('{u}','u')},\\; g(x)={g[1]}",
        "answerNorm": f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}",
        "validForms": [f"f={f[0].replace('{','').replace('}','').replace('\\','')},g={g[0].replace('{','').replace('}','').replace('\\','')}"],
        "inputHint": f"Type:  f=<outer>, g=<inner>  e.g.  f=sin(x),g=e^x",
        "steps": [
            {"label": "Find inner (what's applied first?)", "math": f"g(x) = {g[1]}", "note": ""},
            {"label": "Find outer (what wraps g?)", "math": f"f(u) = {f[2].replace('{u}','u')}", "note": ""},
            {"label": "Verify: f(g(x))", "math": f"f(g(x)) = {composed_tex}", "note": ""},
        ],
    }


def _decompose_three():
    funcs = random.sample(_FUNCS, 3)
    h_name, h_x, h_u, _ = funcs[0]
    g_name, g_x, g_u, _ = funcs[1]
    f_name, f_x, f_u, _ = funcs[2]
    # Build h(x), then g(h(x)), then f(g(h(x)))
    gh_tex = _compose_tex(g_u, h_x)
    fgh_tex = _compose_tex(f_u, gh_tex)
    return {
        "problemTex": f"\\text{{Decompose }} {fgh_tex} \\text{{ as }} f(g(h(x))).",
        "answerTex": f"f(u)={f_u.replace('{u}','u')},\\; g(u)={g_u.replace('{u}','u')},\\; h(x)={h_x}",
        "answerNorm": f"f={f_name},g={g_name},h={h_name}".replace("{","").replace("}","").replace("\\",""),
        "inputHint": "Type:  f=<outer>, g=<middle>, h=<inner>  e.g.  f=sin(x),g=x^2,h=e^x",
        "steps": [
            {"label": "Innermost (h)", "math": f"h(x)={h_x}", "note": "deepest nested function"},
            {"label": "Middle (g)", "math": f"g(u)={g_u.replace('{u}','u')}", "note": ""},
            {"label": "Outer (f)", "math": f"f(u)={f_u.replace('{u}','u')}", "note": "outermost"},
        ],
    }


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
    return {
        "problemTex": f"\\text{{Build the composite function: \\textquotedblleft{desc}\\textquotedblright}}",
        "answerTex": result_tex,
        "answerNorm": result_norm,
        "steps": [
            {"label": "Start with x, apply first operation", "math": desc.split(",")[0].strip(), "note": ""},
            {"label": "Apply second operation to result", "math": result_tex, "note": ""},
        ],
    }


diff2 = [_decompose_two, _decompose_two, _decompose_three, _build_from_description]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _domain_of_composition():
    # f(x) = √x, g(x) = x - a; domain of f(g(x)) requires x - a >= 0 → x >= a
    a = R(1, 8)
    return {
        "problemTex": f"f(x)=\\sqrt{{x}},\\; g(x)=x-{a}.\\quad \\text{{Find the domain of }} f(g(x)).",
        "answerTex": f"x \\geq {a},\\; \\text{{or}} \\; [{a},\\infty)",
        "answerNorm": f"x>={a}",
        "steps": [
            {"label": "Form the composition", "math": f"f(g(x))=\\sqrt{{x-{a}}}", "note": ""},
            {"label": "Require radicand ≥ 0", "math": f"x-{a}\\geq 0", "note": "√ requires non-negative input"},
            {"label": "Solve", "math": f"x \\geq {a}", "note": f"domain: [{a},\\infty)"},
        ],
    }


def _multi_compose():
    f, g, h = random.sample(_FUNCS, 3)
    gh_tex = _compose_tex(g[2], h[1])
    fgh_tex = _compose_tex(f[2], gh_tex)
    return {
        "problemTex": f"f(x)={f[1]},\\; g(x)={g[1]},\\; h(x)={h[1]}.\\quad \\text{{Find }} f(g(h(x))).",
        "answerTex": fgh_tex,
        "answerNorm": fgh_tex.replace("{","").replace("}","").replace("\\",""),
        "steps": [
            {"label": "Compute h(x)", "math": h[1], "note": "start innermost"},
            {"label": "Compute g(h(x))", "math": gh_tex, "note": ""},
            {"label": "Compute f(g(h(x)))", "math": fgh_tex, "note": ""},
        ],
    }


diff3 = [_domain_of_composition, _domain_of_composition, _multi_compose]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _simplify_fog():
    # Choose pairs where composition simplifies nicely
    pairs = [
        ("(\\sqrt{x}+1)^2", "\\sqrt{x}+1", "x^2", "x+2\\sqrt{x}+1", "x+2sqrt(x)+1"),
        ("\\sqrt{x^2}=|x|",  "x^2",   "\\sqrt{x}",  "|x|",  "|x|"),
        ("e^{\\ln x}=x",     "\\ln x", "e^x",        "x",    "x"),
        ("\\ln(e^x)=x",      "e^x",    "\\ln(x)",    "x",    "x"),
    ]
    desc, g_tex, f_tex, result_tex, result_norm = pick(pairs)
    return {
        "problemTex": f"f(x)={f_tex},\\; g(x)={g_tex}.\\quad \\text{{Fully simplify }} f(g(x)).",
        "answerTex": result_tex,
        "answerNorm": result_norm,
        "steps": [
            {"label": "Substitute", "math": f"f(g(x))={desc.split('=')[0]}", "note": ""},
            {"label": "Simplify", "math": result_tex, "note": desc},
        ],
    }


def _fog_commutativity():
    f, g = _safe_pick_pair()
    fog_tex = _compose_tex(f[2], g[1])
    gof_tex = _compose_tex(g[2], f[1])
    equal = fog_tex == gof_tex
    return {
        "problemTex": f"f(x)={f[1]},\\; g(x)={g[1]}.\\quad \\text{{Does }} f(g(x))=g(f(x))?",
        "answerTex": ("\\text{Yes}" if equal else
                      f"\\text{{No}}: f(g(x))={fog_tex},\\; g(f(x))={gof_tex}"),
        "answerNorm": "yes" if equal else "no",
        "steps": [
            {"label": "Compute f(g(x))", "math": fog_tex, "note": ""},
            {"label": "Compute g(f(x))", "math": gof_tex, "note": ""},
            {"label": "Compare", "math": "\\text{Equal}" if equal else "\\text{Not equal}", "note": "composition is generally NOT commutative"},
        ],
    }


def _solve_fog():
    # f(g(x)) = c; pick f and g so equation is solvable
    a = R(2, 5); b = R(1, 4); c = a + b
    # f(x) = x + b, g(x) = ax; f(g(x)) = ax + b = c → x = (c-b)/a
    x_sol = (c - b) // a if (c - b) % a == 0 else None
    if x_sol is None:
        # retry with clean numbers
        a = 2; b = 1; c = 5; x_sol = 2
    return {
        "problemTex": f"f(x)=x+{b},\\; g(x)={a}x.\\quad \\text{{Solve }} f(g(x))={c}.",
        "answerTex": f"x = {x_sol}",
        "answerNorm": str(x_sol),
        "steps": [
            {"label": "Form composition", "math": f"f(g(x))={a}x+{b}", "note": ""},
            {"label": "Set equal to c", "math": f"{a}x+{b}={c}", "note": ""},
            {"label": "Solve", "math": f"x={x_sol}", "note": ""},
        ],
    }


diff4 = [_simplify_fog, _fog_commutativity, _solve_fog]

# ── diff5 ──────────────────────────────────────────────────────────────────────

def _chain_rule_setup():
    f, g = _safe_pick_pair()
    composed_tex = _compose_tex(f[2], g[1])
    rules = {
        "x^2":      "power rule",
        "x^3":      "power rule",
        "\\sin(x)": "derivative of sin",
        "\\cos(x)": "derivative of cos",
        "e^x":      "derivative of eˣ",
        "\\ln(x)":  "derivative of ln",
    }
    f_rule = rules.get(f[1], "standard rule")
    g_rule = rules.get(g[1], "standard rule")
    return {
        "problemTex": f"\\text{{Identify all derivative rules needed to differentiate }} {composed_tex}.",
        "answerTex": f"\\text{{Chain rule: outer=}}\\,{f[1]},\\text{{ inner=}}\\,{g[1]}",
        "answerNorm": f"chain,outer={f[0]},inner={g[0]}".replace("{","").replace("}","").replace("\\",""),
        "steps": [
            {"label": "Identify inner function", "math": f"g(x)={g[1]}", "note": f"requires: {g_rule}"},
            {"label": "Identify outer function", "math": f"f(u)={f[2].replace('{u}','u')}", "note": f"requires: {f_rule}"},
            {"label": "Chain rule: d/dx[f(g(x))] = f'(g(x))·g'(x)", "math": "\\text{will need both rules}", "note": ""},
        ],
    }


def _inverse_composition_verify():
    # f and f^{-1}: verify f(f^{-1}(x)) = x
    pairs = [
        ("e^x",          "\\ln(x)",     "e^{\\ln x}=x"),
        ("\\ln(x)",      "e^x",         "\\ln(e^x)=x"),
        ("x^3",          "x^{1/3}",     "(x^{1/3})^3=x"),
        ("2x+1",         "(x-1)/2",     "2\\cdot\\frac{x-1}{2}+1=x"),
    ]
    f_tex, fi_tex, verify = pick(pairs)
    return {
        "problemTex": f"f(x)={f_tex},\\; f^{{-1}}(x)={fi_tex}.\\quad \\text{{Verify }} f(f^{{-1}}(x))=x.",
        "answerTex": f"{verify}\\;\\checkmark",
        "answerNorm": "x",
        "steps": [
            {"label": "Substitute f⁻¹ into f", "math": f"f(f^{{-1}}(x))={verify.split('=')[0]}", "note": ""},
            {"label": "Simplify", "math": "= x\\;\\checkmark", "note": "confirms f and f⁻¹ are inverses"},
        ],
    }


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
    return {
        "problemTex": (
            f"f(x)={h4[1]},\\;g(x)={h3[1]},\\;h(x)={h2[1]},\\;k(x)={h1[1]}."
            f"\\quad\\text{{Find }}(f\\circ g\\circ h\\circ k)({x_val})."
        ),
        "answerTex": str(v4_rounded),
        "answerNorm": str(v4_rounded),
        "steps": [
            {"label": f"k({x_val})", "math": f"k({x_val})={round(v1,4)}", "note": ""},
            {"label": f"h(k({x_val}))", "math": f"h({round(v1,4)})={round(v2,4) if v2 else '?'}", "note": ""},
            {"label": f"g(h(...))", "math": f"g({round(v2,4) if v2 else '?'})={round(v3,4) if v3 else '?'}", "note": ""},
            {"label": f"f(g(...))", "math": f"f({round(v3,4) if v3 else '?'})={v4_rounded}", "note": ""},
        ],
    }


diff5 = [_chain_rule_setup, _inverse_composition_verify, _four_layer_compose]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
