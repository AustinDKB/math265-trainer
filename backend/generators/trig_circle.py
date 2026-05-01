import random
from math_utils import R, pick, simplify_frac, frac_to_tex
from problem_builder import problem, step

# ── Value normalization helpers ───────────────────────────────────────────────

_VAL_TEX = {
    "0":          "0",
    "1":          "1",
    "-1":         "-1",
    "1/2":        "\\dfrac{1}{2}",
    "-1/2":       "-\\dfrac{1}{2}",
    "2":          "2",
    "-2":         "-2",
    "sqrt(2)":    "\\sqrt{2}",
    "-sqrt(2)":   "-\\sqrt{2}",
    "sqrt(2)/2":  "\\dfrac{\\sqrt{2}}{2}",
    "-sqrt(2)/2": "-\\dfrac{\\sqrt{2}}{2}",
    "sqrt(3)":    "\\sqrt{3}",
    "-sqrt(3)":   "-\\sqrt{3}",
    "sqrt(3)/2":  "\\dfrac{\\sqrt{3}}{2}",
    "-sqrt(3)/2": "-\\dfrac{\\sqrt{3}}{2}",
    "sqrt(3)/3":  "\\dfrac{\\sqrt{3}}{3}",
    "-sqrt(3)/3": "-\\dfrac{\\sqrt{3}}{3}",
    "2sqrt(3)/3": "\\dfrac{2\\sqrt{3}}{3}",
    "-2sqrt(3)/3":"-\\dfrac{2\\sqrt{3}}{3}",
    "undefined":  "\\text{undefined}",
}

_ANGLE_TEX = {
    "0":     "0",
    "pi/6":  "\\dfrac{\\pi}{6}",
    "pi/4":  "\\dfrac{\\pi}{4}",
    "pi/3":  "\\dfrac{\\pi}{3}",
    "pi/2":  "\\dfrac{\\pi}{2}",
    "2pi/3": "\\dfrac{2\\pi}{3}",
    "3pi/4": "\\dfrac{3\\pi}{4}",
    "5pi/6": "\\dfrac{5\\pi}{6}",
    "pi":    "\\pi",
    "7pi/6": "\\dfrac{7\\pi}{6}",
    "5pi/4": "\\dfrac{5\\pi}{4}",
    "4pi/3": "\\dfrac{4\\pi}{3}",
    "3pi/2": "\\dfrac{3\\pi}{2}",
    "5pi/3": "\\dfrac{5\\pi}{3}",
    "7pi/4": "\\dfrac{7\\pi}{4}",
    "11pi/6":"\\dfrac{11\\pi}{6}",
}

_ANGLE_DEG = {
    "0":0,"pi/6":30,"pi/4":45,"pi/3":60,"pi/2":90,
    "2pi/3":120,"3pi/4":135,"5pi/6":150,"pi":180,
    "7pi/6":210,"5pi/4":225,"4pi/3":240,"3pi/2":270,
    "5pi/3":300,"7pi/4":315,"11pi/6":330,
}

def _vt(norm): return _VAL_TEX.get(norm, norm)
def _at(key):  return _ANGLE_TEX.get(key, key)

# ── Unit circle lookup table ──────────────────────────────────────────────────
# Each key: (sin_norm, cos_norm, tan_norm, csc_norm, sec_norm, cot_norm)
_UC = {
    "0":     ("0",          "1",          "0",          "undefined",   "1",           "undefined"),
    "pi/6":  ("1/2",        "sqrt(3)/2",  "sqrt(3)/3",  "2",           "2sqrt(3)/3",  "sqrt(3)"),
    "pi/4":  ("sqrt(2)/2",  "sqrt(2)/2",  "1",          "sqrt(2)",     "sqrt(2)",     "1"),
    "pi/3":  ("sqrt(3)/2",  "1/2",        "sqrt(3)",    "2sqrt(3)/3",  "2",           "sqrt(3)/3"),
    "pi/2":  ("1",          "0",          "undefined",  "1",           "undefined",   "0"),
    "2pi/3": ("sqrt(3)/2",  "-1/2",       "-sqrt(3)",   "2sqrt(3)/3",  "-2",          "-sqrt(3)/3"),
    "3pi/4": ("sqrt(2)/2",  "-sqrt(2)/2", "-1",         "sqrt(2)",     "-sqrt(2)",    "-1"),
    "5pi/6": ("1/2",        "-sqrt(3)/2", "-sqrt(3)/3", "2",           "-2sqrt(3)/3", "-sqrt(3)"),
    "pi":    ("0",          "-1",         "0",          "undefined",   "-1",          "undefined"),
    "7pi/6": ("-1/2",       "-sqrt(3)/2", "sqrt(3)/3",  "-2",          "-2sqrt(3)/3", "sqrt(3)"),
    "5pi/4": ("-sqrt(2)/2", "-sqrt(2)/2", "1",          "-sqrt(2)",    "-sqrt(2)",    "1"),
    "4pi/3": ("-sqrt(3)/2", "-1/2",       "sqrt(3)",    "-2sqrt(3)/3", "-2",          "sqrt(3)/3"),
    "3pi/2": ("-1",         "0",          "undefined",  "-1",          "undefined",   "0"),
    "5pi/3": ("-sqrt(3)/2", "1/2",        "-sqrt(3)",   "-2sqrt(3)/3", "2",           "-sqrt(3)/3"),
    "7pi/4": ("-sqrt(2)/2", "sqrt(2)/2",  "-1",         "-sqrt(2)",    "sqrt(2)",     "-1"),
    "11pi/6":("-1/2",       "sqrt(3)/2",  "-sqrt(3)/3", "-2",          "2sqrt(3)/3",  "-sqrt(3)"),
}
_UC_KEYS = list(_UC.keys())

# First-quadrant + axes only (easiest angles)
_EASY_KEYS = ["0", "pi/6", "pi/4", "pi/3", "pi/2", "pi", "3pi/2"]

_PYTH_TRIPLES = [(3,4,5),(5,12,13),(8,15,17),(7,24,25)]

# ── diff1 ──────────────────────────────────────────────────────────────────────

def _sin_direct():
    key = pick(_UC_KEYS)
    sn, *_ = _UC[key]
    return problem(
        problem_tex=f"\\sin\\!\\left({_at(key)}\\right) = \\,?",
        answer_tex=_vt(sn),
        answer_norm=sn,
        steps=[step("Unit circle lookup", f"\\sin\\!\\left({_at(key)}\\right) = {_vt(sn)}")],
    )


def _cos_direct():
    key = pick(_UC_KEYS)
    _, cn, *_ = _UC[key]
    return problem(
        problem_tex=f"\\cos\\!\\left({_at(key)}\\right) = \\,?",
        answer_tex=_vt(cn),
        answer_norm=cn,
        steps=[step("Unit circle lookup", f"\\cos\\!\\left({_at(key)}\\right) = {_vt(cn)}")],
    )


def _quadrant_sign():
    key = pick(_UC_KEYS)
    fn_name = pick(["sin", "cos", "tan"])
    idx = {"sin":0,"cos":1,"tan":2}[fn_name]
    val = _UC[key][idx]
    if val == "0":
        return _sin_direct()
    answer = "positive" if not val.startswith("-") and val != "undefined" else ("negative" if val.startswith("-") else "undefined")
    if answer == "undefined":
        return _sin_direct()
    fn_tex = {"sin":"\\sin","cos":"\\cos","tan":"\\tan"}[fn_name]
    return problem(
        problem_tex=f"\\text{{Is }} {fn_tex}\\!\\left({_at(key)}\\right) \\text{{ positive or negative?}}",
        answer_tex=f"\\text{{{answer}}}",
        answer_norm=answer,
        steps=[
            step("Identify quadrant", f"{_at(key)} \\text{{ is in quadrant }} {'I' if _ANGLE_DEG[key]<90 else 'II' if _ANGLE_DEG[key]<180 else 'III' if _ANGLE_DEG[key]<270 else 'IV'}"),
            step("Sign rule", f"{fn_tex}\\!\\left({_at(key)}\\right) = {_vt(val)}", f"value is {'negative' if val.startswith('-') else 'positive'}"),
        ],
    )


def _rad_to_deg():
    key = pick([k for k in _UC_KEYS if k != "0"])
    deg = _ANGLE_DEG[key]
    return problem(
        problem_tex=f"\\text{{Convert }} {_at(key)} \\text{{ to degrees}}",
        answer_tex=f"{deg}^\\circ",
        answer_norm=str(deg),
        steps=[
            step("Multiply by 180/π", f"{_at(key)} \\cdot \\dfrac{{180}}{{\\pi}} = {deg}^\\circ"),
        ],
    )


diff1 = [_sin_direct, _sin_direct, _cos_direct, _cos_direct, _quadrant_sign, _rad_to_deg]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _tan_direct():
    key = pick(_UC_KEYS)
    _, _, tn, *_ = _UC[key]
    return problem(
        problem_tex=f"\\tan\\!\\left({_at(key)}\\right) = \\,?",
        answer_tex=_vt(tn),
        answer_norm=tn,
        steps=[step("Unit circle lookup", f"\\tan\\!\\left({_at(key)}\\right) = {_vt(tn)}", "sin/cos")],
    )


def _reciprocal_trig():
    fn_name = pick(["csc", "sec", "cot"])
    key = pick([k for k in _UC_KEYS if _UC[k][{"csc":3,"sec":4,"cot":5}[fn_name]] != "undefined"])
    idx = {"csc":3,"sec":4,"cot":5}[fn_name]
    val = _UC[key][idx]
    fn_tex = {"csc":"\\csc","sec":"\\sec","cot":"\\cot"}[fn_name]
    base_fn = {"csc":"sin","sec":"cos","cot":"tan"}[fn_name]
    base_idx = {"csc":0,"sec":1,"cot":2}[fn_name]
    base_val = _UC[key][base_idx]
    base_tex = {"csc":"\\sin","sec":"\\cos","cot":"\\tan"}[fn_name]
    return problem(
        problem_tex=f"{fn_tex}\\!\\left({_at(key)}\\right) = \\,?",
        answer_tex=_vt(val),
        answer_norm=val,
        steps=[
            step(f"Reciprocal of {base_fn}", f"{fn_tex}(\\theta)=\\dfrac{{1}}{{{base_tex}(\\theta)}}"),
            step("Look up base value", f"{base_tex}\\!\\left({_at(key)}\\right) = {_vt(base_val)}"),
            step("Take reciprocal", f"{fn_tex}\\!\\left({_at(key)}\\right) = {_vt(val)}"),
        ],
    )


def _inverse_sin():
    valid = {k: _UC[k][0] for k in ["0","pi/6","pi/4","pi/3","pi/2","5pi/6","3pi/4","pi"]}
    key = pick(list(valid.keys()))
    val = valid[key]
    return problem(
        problem_tex=f"\\sin(\\theta) = {_vt(val)},\\; \\theta \\in [0,\\pi]. \\quad \\theta = \\,?",
        answer_tex=_at(key),
        answer_norm=key,
        steps=[
            step("Identify range", "\\theta \\in [0,\\pi] \\text{ (first two quadrants)}"),
            step("Lookup angle", f"\\sin\\!\\left({_at(key)}\\right) = {_vt(val)}"),
        ],
    )


def _deg_to_rad():
    key = pick([k for k in _UC_KEYS if k != "0"])
    deg = _ANGLE_DEG[key]
    return problem(
        problem_tex=f"\\text{{Convert }} {deg}^\\circ \\text{{ to radians}}",
        answer_tex=_at(key),
        answer_norm=key,
        steps=[
            step("Multiply by π/180", f"{deg}^\\circ \\cdot \\dfrac{{\\pi}}{{180}} = {_at(key)}"),
        ],
    )


diff2 = [_tan_direct, _tan_direct, _reciprocal_trig, _inverse_sin, _deg_to_rad]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _pythagorean_identity():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    if pick([True, False]):
        opp, adj = adj, opp
    q = pick([1, 2])
    sin_n = f"{opp}/{hyp}"
    cos_n = f"{adj}/{hyp}" if q == 1 else f"-{adj}/{hyp}"
    q_tex = "\\text{Q1}" if q == 1 else "\\text{Q2}"
    return problem(
        problem_tex=f"\\sin(\\theta)=\\dfrac{{{opp}}}{{{hyp}}},\\; \\theta \\in {q_tex}.\\quad \\cos(\\theta) = \\,?",
        answer_tex=f"\\dfrac{{{adj}}}{{{hyp}}}" if q == 1 else f"-\\dfrac{{{adj}}}{{{hyp}}}",
        answer_norm=cos_n,
        steps=[
            step("Pythagorean identity", "\\sin^2\\theta+\\cos^2\\theta=1"),
            step("Solve for cos²θ", f"\\cos^2\\theta=1-\\left(\\dfrac{{{opp}}}{{{hyp}}}\\right)^2=\\dfrac{{{hyp**2-opp**2}}}{{{hyp**2}}}"),
            step("Take square root", f"\\cos\\theta=\\pm\\dfrac{{{adj}}}{{{hyp}}}"),
            step("Apply quadrant sign", f"\\cos\\theta={'+'  if q==1 else '-'}\\dfrac{{{adj}}}{{{hyp}}}", f"cos is {'positive' if q==1 else 'negative'} in Q{q}"),
        ],
    )


def _double_angle_sin():
    key = pick(["pi/6","pi/4","pi/3"])
    sn, cn, *_ = _UC[key]
    two_key_map = {"pi/6":"pi/3","pi/4":"pi/2","pi/3":"2pi/3"}
    two_key = two_key_map[key]
    result = _UC[two_key][0]
    return problem(
        problem_tex=f"\\text{{If }} \\sin(\\theta)={_vt(sn)},\\; \\cos(\\theta)={_vt(cn)},\\text{{ find }} \\sin(2\\theta)",
        answer_tex=_vt(result),
        answer_norm=result,
        steps=[
            step("Double angle formula", "\\sin(2\\theta)=2\\sin(\\theta)\\cos(\\theta)"),
            step("Substitute", f"2 \\cdot {_vt(sn)} \\cdot {_vt(cn)}"),
            step("Compute", _vt(result)),
        ],
    )


diff3 = [_pythagorean_identity, _pythagorean_identity, _double_angle_sin]

# ── diff4 ──────────────────────────────────────────────────────────────────────

def _all_six_from_triple():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    q = pick([1, 2, 3, 4])
    sin_sign = 1 if q in [1, 2] else -1
    cos_sign = 1 if q in [1, 4] else -1
    s_n = f"{opp}/{hyp}" if sin_sign == 1 else f"-{opp}/{hyp}"
    c_n = f"{adj}/{hyp}" if cos_sign == 1 else f"-{adj}/{hyp}"
    t_n = f"{opp}/{adj}" if sin_sign * cos_sign == 1 else f"-{opp}/{adj}"
    csc_n = f"{hyp}/{opp}" if sin_sign == 1 else f"-{hyp}/{opp}"
    sec_n = f"{hyp}/{adj}" if cos_sign == 1 else f"-{hyp}/{adj}"
    cot_n = f"{adj}/{opp}" if sin_sign * cos_sign == 1 else f"-{adj}/{opp}"
    q_labels = {1:"\\text{Q1}",2:"\\text{Q2}",3:"\\text{Q3}",4:"\\text{Q4}"}
    return problem(
        problem_tex=f"\\sin(\\theta)={_vt_frac(sin_sign*opp, hyp)},\\; \\theta \\in {q_labels[q]}.\\quad \\text{{Find all 6 trig values.}}",
        answer_tex=(
            f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)},\\; \\tan={_vt_frac(sin_sign*cos_sign*opp,adj)},\\;"
            f"\\csc={_vt_frac(sin_sign*hyp,opp)},\\; \\sec={_vt_frac(cos_sign*hyp,adj)},\\; \\cot={_vt_frac(sin_sign*cos_sign*adj,opp)}"
        ),
        answer_norm=f"sin={s_n},cos={c_n},tan={t_n}",
        steps=[
            step("Find hypotenuse", f"{opp}^2+{adj}^2={hyp}^2 \\;\\checkmark", "Pythagorean triple"),
            step("sin & cos from quadrant", f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)}", f"Q{q} sign rules"),
            step("tan = sin/cos", f"\\tan={_vt_frac(sin_sign*cos_sign*opp,adj)}"),
            step("Reciprocals", f"\\csc={_vt_frac(sin_sign*hyp,opp)},\\; \\sec={_vt_frac(cos_sign*hyp,adj)},\\; \\cot={_vt_frac(sin_sign*cos_sign*adj,opp)}"),
        ],
        validForms=[f"sin={s_n},cos={c_n},tan={t_n}"],
        isAllSix=True,
    )


def _vt_frac(num, den):
    if den == 1: return str(num)
    if num < 0:
        return f"-\\dfrac{{{-num}}}{{{den}}}"
    return f"\\dfrac{{{num}}}{{{den}}}"


def _cofunction_identity():
    key = pick(["pi/6","pi/4","pi/3"])
    fn = pick(["sin","cos"])
    comp_key = {"pi/6":"pi/3","pi/4":"pi/4","pi/3":"pi/6"}[key]
    result_fn = "cos" if fn == "sin" else "sin"
    idx = 0 if result_fn == "sin" else 1
    result = _UC[comp_key][idx]
    fn_tex = {"sin":"\\sin","cos":"\\cos"}[fn]
    result_fn_tex = {"sin":"\\sin","cos":"\\cos"}[result_fn]
    return problem(
        problem_tex=f"{fn_tex}\\!\\left(\\dfrac{{\\pi}}{{2}}-{_at(key)}\\right) = \\,?",
        answer_tex=_vt(result),
        answer_norm=result,
        steps=[
            step("Cofunction identity", "\\sin\\!\\left(\\dfrac{\\pi}{2}-\\theta\\right)=\\cos(\\theta),\\quad \\cos\\!\\left(\\dfrac{\\pi}{2}-\\theta\\right)=\\sin(\\theta)"),
            step("Apply", f"{fn_tex}\\!\\left(\\dfrac{{\\pi}}{{2}}-{_at(key)}\\right) = {result_fn_tex}\\!\\left({_at(key)}\\right) = {_vt(result)}"),
        ],
    )


def _double_angle_cos():
    key = pick(["pi/6","pi/4","pi/3"])
    sn, cn, *_ = _UC[key]
    two_key_map = {"pi/6":"pi/3","pi/4":"pi/2","pi/3":"2pi/3"}
    two_key = two_key_map[key]
    result = _UC[two_key][1]
    form = pick([1,2,3])
    if form == 1:
        formula = "\\cos(2\\theta)=\\cos^2\\theta-\\sin^2\\theta"
    elif form == 2:
        formula = "\\cos(2\\theta)=1-2\\sin^2\\theta"
    else:
        formula = "\\cos(2\\theta)=2\\cos^2\\theta-1"
    return problem(
        problem_tex=f"\\text{{Using }} {formula.split('=')[0]}={formula.split('=')[1]},\\; \\text{{find }} \\cos(2\\theta) \\text{{ if }} \\cos\\theta={_vt(cn)},\\; \\sin\\theta={_vt(sn)}.",
        answer_tex=_vt(result),
        answer_norm=result,
        steps=[
            step("Formula", formula),
            step("Substitute", f"\\cos(2\\cdot{_at(key)}) = {formula.split('=')[1].replace('\\theta', f'({_at(key)})')}"),
            step("Result", f"\\cos\\!\\left({_at(two_key)}\\right) = {_vt(result)}"),
        ],
    )


diff4 = [_all_six_from_triple, _all_six_from_triple, _cofunction_identity, _double_angle_cos]

# ── diff5 ──────────────────────────────────────────────────────────────────────

_COMPOUND_PAIRS = [
    ("pi/6","pi/3","pi/2","sin"),
    ("pi/4","pi/4","pi/2","sin"),
    ("pi/3","pi/6","pi/2","sin"),
    ("pi/3","pi/6","pi/6","sin"),
    ("pi/3","pi/6","pi/2","cos"),
    ("pi/4","pi/4","pi/2","cos"),
]

def _compound_angle_eval():
    a_key, b_key, result_key, fn = pick(_COMPOUND_PAIRS)
    sa, ca, *_ = _UC[a_key]
    sb, cb, *_ = _UC[b_key]
    if fn == "sin":
        result = _UC[result_key][0]
        expr = f"\\sin\\!\\left({_at(a_key)}\\right)\\cos\\!\\left({_at(b_key)}\\right)+\\cos\\!\\left({_at(a_key)}\\right)\\sin\\!\\left({_at(b_key)}\\right)"
        formula = "\\sin(A+B)=\\sin A\\cos B+\\cos A\\sin B"
    else:
        result = _UC[result_key][1]
        expr = f"\\cos\\!\\left({_at(a_key)}\\right)\\cos\\!\\left({_at(b_key)}\\right)-\\sin\\!\\left({_at(a_key)}\\right)\\sin\\!\\left({_at(b_key)}\\right)"
        formula = "\\cos(A+B)=\\cos A\\cos B-\\sin A\\sin B"
    return problem(
        problem_tex=f"\\text{{Evaluate: }} {expr}",
        answer_tex=_vt(result),
        answer_norm=result,
        steps=[
            step("Recognize sum formula", formula),
            step("This equals", f"{'\\sin' if fn=='sin' else '\\cos'}\\!\\left({_at(a_key)}+{_at(b_key)}\\right)={'\\sin' if fn=='sin' else '\\cos'}\\!\\left({_at(result_key)}\\right)"),
            step("Look up value", f"= {_vt(result)}"),
        ],
    )


def _given_tan_find_sin_cos():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    q = pick([1, 2, 3, 4])
    sin_sign = 1 if q in [1, 2] else -1
    cos_sign = 1 if q in [1, 4] else -1
    tan_sign = sin_sign * cos_sign
    tan_n = f"{opp}/{adj}" if tan_sign == 1 else f"-{opp}/{adj}"
    q_labels = {1:"\\text{Q1}",2:"\\text{Q2}",3:"\\text{Q3}",4:"\\text{Q4}"}
    return problem(
        problem_tex=(
            f"\\tan(\\theta)={_vt_frac(tan_sign*opp,adj)},\\; \\theta \\in {q_labels[q]}."
            f"\\quad \\text{{Find }} \\sin(\\theta) \\text{{ and }} \\cos(\\theta)."
        ),
        answer_tex=f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)}",
        answer_norm=f"sin={sin_sign*opp}/{hyp},cos={cos_sign*adj}/{hyp}",
        steps=[
            step("tan = opp/adj, so build triangle", f"\\text{{opp}}={opp},\\; \\text{{adj}}={adj},\\; \\text{{hyp}}=\\sqrt{{{opp}^2+{adj}^2}}={hyp}"),
            step("sin = opp/hyp", f"\\sin\\theta={_vt_frac(sin_sign*opp,hyp)}", f"positive in Q{q}" if sin_sign == 1 else f"negative in Q{q}"),
            step("cos = adj/hyp", f"\\cos\\theta={_vt_frac(cos_sign*adj,hyp)}", f"positive in Q{q}" if cos_sign == 1 else f"negative in Q{q}"),
        ],
        isGivenTan=True,
    )


def _full_set_q3():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    sin_n = f"-{opp}/{hyp}"; cos_n = f"-{adj}/{hyp}"; tan_n = f"{opp}/{adj}"
    csc_n = f"-{hyp}/{opp}"; sec_n = f"-{hyp}/{adj}"; cot_n = f"{adj}/{opp}"
    return problem(
        problem_tex=f"\\sin(\\theta)=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\theta \\in \\text{{Q3}}.\\quad \\text{{Find all 6 trig values.}}",
        answer_tex=(
            f"\\sin=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\cos=-\\dfrac{{{adj}}}{{{hyp}}},\\; \\tan=\\dfrac{{{opp}}}{{{adj}}},\\;"
            f"\\csc=-\\dfrac{{{hyp}}}{{{opp}}},\\; \\sec=-\\dfrac{{{hyp}}}{{{adj}}},\\; \\cot=\\dfrac{{{adj}}}{{{opp}}}"
        ),
        answer_norm=f"sin={sin_n},cos={cos_n},tan={tan_n}",
        steps=[
            step("Build reference triangle", f"\\text{{opp}}={opp},\\; \\text{{adj}}={adj},\\; \\text{{hyp}}={hyp}"),
            step("Q3 signs: sin−, cos−, tan+", "\\sin<0,\\; \\cos<0,\\; \\tan>0 \\text{{ in Q3}}"),
            step("Primary values", f"\\sin=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\cos=-\\dfrac{{{adj}}}{{{hyp}}},\\; \\tan=\\dfrac{{{opp}}}{{{adj}}}"),
            step("Reciprocals", f"\\csc=-\\dfrac{{{hyp}}}{{{opp}}},\\; \\sec=-\\dfrac{{{hyp}}}{{{adj}}},\\; \\cot=\\dfrac{{{adj}}}{{{opp}}}"),
        ],
        validForms=[f"sin={sin_n},cos={cos_n},tan={tan_n}"],
        isAllSix=True,
    )


diff5 = [_compound_angle_eval, _given_tan_find_sin_cos, _full_set_q3]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}