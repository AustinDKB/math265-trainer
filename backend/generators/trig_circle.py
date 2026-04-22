import random
from math_utils import R, pick, simplify_frac, frac_to_tex

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
    return {
        "problemTex": f"\\sin\\!\\left({_at(key)}\\right) = \\,?",
        "answerTex": _vt(sn),
        "answerNorm": sn,
        "steps": [{"label": "Unit circle lookup", "math": f"\\sin\\!\\left({_at(key)}\\right) = {_vt(sn)}", "note": ""}],
    }


def _cos_direct():
    key = pick(_UC_KEYS)
    _, cn, *_ = _UC[key]
    return {
        "problemTex": f"\\cos\\!\\left({_at(key)}\\right) = \\,?",
        "answerTex": _vt(cn),
        "answerNorm": cn,
        "steps": [{"label": "Unit circle lookup", "math": f"\\cos\\!\\left({_at(key)}\\right) = {_vt(cn)}", "note": ""}],
    }


def _quadrant_sign():
    key = pick(_UC_KEYS)
    fn_name = pick(["sin", "cos", "tan"])
    idx = {"sin":0,"cos":1,"tan":2}[fn_name]
    val = _UC[key][idx]
    if val == "0":
        return _sin_direct()  # retry — 0 is neither
    answer = "positive" if not val.startswith("-") and val != "undefined" else ("negative" if val.startswith("-") else "undefined")
    if answer == "undefined":
        return _sin_direct()
    fn_tex = {"sin":"\\sin","cos":"\\cos","tan":"\\tan"}[fn_name]
    return {
        "problemTex": f"\\text{{Is }} {fn_tex}\\!\\left({_at(key)}\\right) \\text{{ positive or negative?}}",
        "answerTex": f"\\text{{{answer}}}",
        "answerNorm": answer,
        "steps": [
            {"label": "Identify quadrant", "math": f"{_at(key)} \\text{{ is in quadrant }} {'I' if _ANGLE_DEG[key]<90 else 'II' if _ANGLE_DEG[key]<180 else 'III' if _ANGLE_DEG[key]<270 else 'IV'}", "note": ""},
            {"label": "Sign rule", "math": f"{fn_tex}\\!\\left({_at(key)}\\right) = {_vt(val)}", "note": f"value is {'negative' if val.startswith('-') else 'positive'}"},
        ],
    }


def _rad_to_deg():
    key = pick([k for k in _UC_KEYS if k != "0"])
    deg = _ANGLE_DEG[key]
    return {
        "problemTex": f"\\text{{Convert }} {_at(key)} \\text{{ to degrees}}",
        "answerTex": f"{deg}^\\circ",
        "answerNorm": str(deg),
        "steps": [
            {"label": "Multiply by 180/π", "math": f"{_at(key)} \\cdot \\dfrac{{180}}{{\\pi}} = {deg}^\\circ", "note": ""},
        ],
    }


diff1 = [_sin_direct, _sin_direct, _cos_direct, _cos_direct, _quadrant_sign, _rad_to_deg]

# ── diff2 ──────────────────────────────────────────────────────────────────────

def _tan_direct():
    key = pick(_UC_KEYS)
    _, _, tn, *_ = _UC[key]
    return {
        "problemTex": f"\\tan\\!\\left({_at(key)}\\right) = \\,?",
        "answerTex": _vt(tn),
        "answerNorm": tn,
        "steps": [{"label": "Unit circle lookup", "math": f"\\tan\\!\\left({_at(key)}\\right) = {_vt(tn)}", "note": "sin/cos"}],
    }


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
    return {
        "problemTex": f"{fn_tex}\\!\\left({_at(key)}\\right) = \\,?",
        "answerTex": _vt(val),
        "answerNorm": val,
        "steps": [
            {"label": f"Reciprocal of {base_fn}", "math": f"{fn_tex}(\\theta)=\\dfrac{{1}}{{{base_tex}(\\theta)}}", "note": ""},
            {"label": "Look up base value", "math": f"{base_tex}\\!\\left({_at(key)}\\right) = {_vt(base_val)}", "note": ""},
            {"label": "Take reciprocal", "math": f"{fn_tex}\\!\\left({_at(key)}\\right) = {_vt(val)}", "note": ""},
        ],
    }


def _inverse_sin():
    # sin(θ) = val, θ ∈ [0,π] → unique answer
    valid = {k: _UC[k][0] for k in ["0","pi/6","pi/4","pi/3","pi/2","5pi/6","3pi/4","pi"]}
    key = pick(list(valid.keys()))
    val = valid[key]
    return {
        "problemTex": f"\\sin(\\theta) = {_vt(val)},\\; \\theta \\in [0,\\pi]. \\quad \\theta = \\,?",
        "answerTex": _at(key),
        "answerNorm": key,
        "steps": [
            {"label": "Identify range", "math": "\\theta \\in [0,\\pi] \\text{ (first two quadrants)}", "note": ""},
            {"label": "Lookup angle", "math": f"\\sin\\!\\left({_at(key)}\\right) = {_vt(val)}", "note": ""},
        ],
    }


def _deg_to_rad():
    key = pick([k for k in _UC_KEYS if k != "0"])
    deg = _ANGLE_DEG[key]
    return {
        "problemTex": f"\\text{{Convert }} {deg}^\\circ \\text{{ to radians}}",
        "answerTex": _at(key),
        "answerNorm": key,
        "steps": [
            {"label": "Multiply by π/180", "math": f"{deg}^\\circ \\cdot \\dfrac{{\\pi}}{{180}} = {_at(key)}", "note": ""},
        ],
    }


diff2 = [_tan_direct, _tan_direct, _reciprocal_trig, _inverse_sin, _deg_to_rad]

# ── diff3 ──────────────────────────────────────────────────────────────────────

def _pythagorean_identity():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    # Randomly swap opp/adj
    if pick([True, False]):
        opp, adj = adj, opp
    q = pick([1, 2])  # quadrant
    sin_n = f"{opp}/{hyp}"
    cos_n = f"{adj}/{hyp}" if q == 1 else f"-{adj}/{hyp}"
    q_tex = "\\text{Q1}" if q == 1 else "\\text{Q2}"
    return {
        "problemTex": f"\\sin(\\theta)=\\dfrac{{{opp}}}{{{hyp}}},\\; \\theta \\in {q_tex}.\\quad \\cos(\\theta) = \\,?",
        "answerTex": f"\\dfrac{{{adj}}}{{{hyp}}}" if q == 1 else f"-\\dfrac{{{adj}}}{{{hyp}}}",
        "answerNorm": cos_n,
        "steps": [
            {"label": "Pythagorean identity", "math": "\\sin^2\\theta+\\cos^2\\theta=1", "note": ""},
            {"label": "Solve for cos²θ", "math": f"\\cos^2\\theta=1-\\left(\\dfrac{{{opp}}}{{{hyp}}}\\right)^2=\\dfrac{{{hyp**2-opp**2}}}{{{hyp**2}}}", "note": ""},
            {"label": "Take square root", "math": f"\\cos\\theta=\\pm\\dfrac{{{adj}}}{{{hyp}}}", "note": ""},
            {"label": "Apply quadrant sign", "math": f"\\cos\\theta={'+'  if q==1 else '-'}\\dfrac{{{adj}}}{{{hyp}}}", "note": f"cos is {'positive' if q==1 else 'negative'} in Q{q}"},
        ],
    }


def _double_angle_sin():
    # sin(2θ) = 2·sin(θ)·cos(θ), use known values
    key = pick(["pi/6","pi/4","pi/3"])
    sn, cn, *_ = _UC[key]
    # Compute sin(2θ) by finding 2θ in table
    two_key_map = {"pi/6":"pi/3","pi/4":"pi/2","pi/3":"2pi/3"}
    two_key = two_key_map[key]
    result = _UC[two_key][0]
    return {
        "problemTex": f"\\text{{If }} \\sin(\\theta)={_vt(sn)},\\; \\cos(\\theta)={_vt(cn)},\\text{{ find }} \\sin(2\\theta)",
        "answerTex": _vt(result),
        "answerNorm": result,
        "steps": [
            {"label": "Double angle formula", "math": "\\sin(2\\theta)=2\\sin(\\theta)\\cos(\\theta)", "note": ""},
            {"label": "Substitute", "math": f"2 \\cdot {_vt(sn)} \\cdot {_vt(cn)}", "note": ""},
            {"label": "Compute", "math": _vt(result), "note": ""},
        ],
    }


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
    return {
        "problemTex": f"\\sin(\\theta)={_vt_frac(sin_sign*opp, hyp)},\\; \\theta \\in {q_labels[q]}.\\quad \\text{{Find all 6 trig values.}}",
        "answerTex": (
            f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)},\\; \\tan={_vt_frac(sin_sign*cos_sign*opp,adj)},\\;"
            f"\\csc={_vt_frac(sin_sign*hyp,opp)},\\; \\sec={_vt_frac(cos_sign*hyp,adj)},\\; \\cot={_vt_frac(sin_sign*cos_sign*adj,opp)}"
        ),
        "answerNorm": f"sin={s_n},cos={c_n},tan={t_n}",
        "validForms": [f"sin={s_n},cos={c_n},tan={t_n}"],
        "steps": [
            {"label": "Find hypotenuse", "math": f"{opp}^2+{adj}^2={hyp}^2 \\;\\checkmark", "note": "Pythagorean triple"},
            {"label": "sin & cos from quadrant", "math": f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)}", "note": f"Q{q} sign rules"},
            {"label": "tan = sin/cos", "math": f"\\tan={_vt_frac(sin_sign*cos_sign*opp,adj)}", "note": ""},
            {"label": "Reciprocals", "math": f"\\csc={_vt_frac(sin_sign*hyp,opp)},\\; \\sec={_vt_frac(cos_sign*hyp,adj)},\\; \\cot={_vt_frac(sin_sign*cos_sign*adj,opp)}", "note": ""},
        ],
        "isAllSix": True,
    }


def _vt_frac(num, den):
    if den == 1: return str(num)
    if num < 0:
        return f"-\\dfrac{{{-num}}}{{{den}}}"
    return f"\\dfrac{{{num}}}{{{den}}}"


def _cofunction_identity():
    # sin(π/2 − θ) = cos(θ), cos(π/2 − θ) = sin(θ)
    key = pick(["pi/6","pi/4","pi/3"])
    fn = pick(["sin","cos"])
    comp_key = {"pi/6":"pi/3","pi/4":"pi/4","pi/3":"pi/6"}[key]
    result_fn = "cos" if fn == "sin" else "sin"
    idx = 0 if result_fn == "sin" else 1
    result = _UC[comp_key][idx]
    fn_tex = {"sin":"\\sin","cos":"\\cos"}[fn]
    result_fn_tex = {"sin":"\\sin","cos":"\\cos"}[result_fn]
    return {
        "problemTex": f"{fn_tex}\\!\\left(\\dfrac{{\\pi}}{{2}}-{_at(key)}\\right) = \\,?",
        "answerTex": _vt(result),
        "answerNorm": result,
        "steps": [
            {"label": "Cofunction identity", "math": f"\\sin\\!\\left(\\dfrac{{\\pi}}{{2}}-\\theta\\right)=\\cos(\\theta),\\quad \\cos\\!\\left(\\dfrac{{\\pi}}{{2}}-\\theta\\right)=\\sin(\\theta)", "note": ""},
            {"label": "Apply", "math": f"{fn_tex}\\!\\left(\\dfrac{{\\pi}}{{2}}-{_at(key)}\\right) = {result_fn_tex}\\!\\left({_at(key)}\\right) = {_vt(result)}", "note": ""},
        ],
    }


def _double_angle_cos():
    key = pick(["pi/6","pi/4","pi/3"])
    sn, cn, *_ = _UC[key]
    two_key_map = {"pi/6":"pi/3","pi/4":"pi/2","pi/3":"2pi/3"}
    two_key = two_key_map[key]
    result = _UC[two_key][1]  # cos(2θ)
    form = pick([1,2,3])
    if form == 1:
        formula = "\\cos(2\\theta)=\\cos^2\\theta-\\sin^2\\theta"
    elif form == 2:
        formula = "\\cos(2\\theta)=1-2\\sin^2\\theta"
    else:
        formula = "\\cos(2\\theta)=2\\cos^2\\theta-1"
    return {
        "problemTex": f"\\text{{Using }} {formula.split('=')[0]}={formula.split('=')[1]},\\; \\text{{find }} \\cos(2\\theta) \\text{{ if }} \\cos\\theta={_vt(cn)},\\; \\sin\\theta={_vt(sn)}.",
        "answerTex": _vt(result),
        "answerNorm": result,
        "steps": [
            {"label": "Formula", "math": formula, "note": ""},
            {"label": "Substitute", "math": f"\\cos(2\\cdot{_at(key)}) = {formula.split('=')[1].replace('\\theta', f'({_at(key)})')}", "note": ""},
            {"label": "Result", "math": f"\\cos\\!\\left({_at(two_key)}\\right) = {_vt(result)}", "note": ""},
        ],
    }


diff4 = [_all_six_from_triple, _all_six_from_triple, _cofunction_identity, _double_angle_cos]

# ── diff5 ──────────────────────────────────────────────────────────────────────

_COMPOUND_PAIRS = [
    ("pi/6","pi/3","pi/2","sin"),   # sin(π/6+π/3)=sin(π/2)
    ("pi/4","pi/4","pi/2","sin"),   # sin(π/4+π/4)=sin(π/2)
    ("pi/3","pi/6","pi/2","sin"),   # sin(π/3+π/6)=sin(π/2)
    ("pi/3","pi/6","pi/6","sin"),   # sin(π/3-π/6)=sin(π/6)
    ("pi/3","pi/6","pi/2","cos"),   # cos(π/3+π/6)=cos(π/2)
    ("pi/4","pi/4","pi/2","cos"),   # cos(π/4+π/4)=cos(π/2)
]

def _compound_angle_eval():
    a_key, b_key, result_key, fn = pick(_COMPOUND_PAIRS)
    sa, ca, *_ = _UC[a_key]
    sb, cb, *_ = _UC[b_key]
    if fn == "sin":
        # sin(a+b) = sin(a)cos(b) + cos(a)sin(b)
        result = _UC[result_key][0]
        expr = f"\\sin\\!\\left({_at(a_key)}\\right)\\cos\\!\\left({_at(b_key)}\\right)+\\cos\\!\\left({_at(a_key)}\\right)\\sin\\!\\left({_at(b_key)}\\right)"
        formula = "\\sin(A+B)=\\sin A\\cos B+\\cos A\\sin B"
    else:
        # cos(a+b) = cos(a)cos(b) - sin(a)sin(b)
        result = _UC[result_key][1]
        expr = f"\\cos\\!\\left({_at(a_key)}\\right)\\cos\\!\\left({_at(b_key)}\\right)-\\sin\\!\\left({_at(a_key)}\\right)\\sin\\!\\left({_at(b_key)}\\right)"
        formula = "\\cos(A+B)=\\cos A\\cos B-\\sin A\\sin B"
    return {
        "problemTex": f"\\text{{Evaluate: }} {expr}",
        "answerTex": _vt(result),
        "answerNorm": result,
        "steps": [
            {"label": "Recognize sum formula", "math": formula, "note": ""},
            {"label": "This equals", "math": f"{'\\sin' if fn=='sin' else '\\cos'}\\!\\left({_at(a_key)}+{_at(b_key)}\\right)={'\\sin' if fn=='sin' else '\\cos'}\\!\\left({_at(result_key)}\\right)", "note": ""},
            {"label": "Look up value", "math": f"= {_vt(result)}", "note": ""},
        ],
    }


def _given_tan_find_sin_cos():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    q = pick([1, 2, 3, 4])
    sin_sign = 1 if q in [1, 2] else -1
    cos_sign = 1 if q in [1, 4] else -1
    tan_sign = sin_sign * cos_sign
    tan_n = f"{opp}/{adj}" if tan_sign == 1 else f"-{opp}/{adj}"
    q_labels = {1:"\\text{Q1}",2:"\\text{Q2}",3:"\\text{Q3}",4:"\\text{Q4}"}
    return {
        "problemTex": (
            f"\\tan(\\theta)={_vt_frac(tan_sign*opp,adj)},\\; \\theta \\in {q_labels[q]}."
            f"\\quad \\text{{Find }} \\sin(\\theta) \\text{{ and }} \\cos(\\theta)."
        ),
        "answerTex": f"\\sin={_vt_frac(sin_sign*opp,hyp)},\\; \\cos={_vt_frac(cos_sign*adj,hyp)}",
        "answerNorm": f"sin={sin_sign*opp}/{hyp},cos={cos_sign*adj}/{hyp}",
        "steps": [
            {"label": "tan = opp/adj, so build triangle", "math": f"\\text{{opp}}={opp},\\; \\text{{adj}}={adj},\\; \\text{{hyp}}=\\sqrt{{{opp}^2+{adj}^2}}={hyp}", "note": ""},
            {"label": "sin = opp/hyp", "math": f"\\sin\\theta={_vt_frac(sin_sign*opp,hyp)}", "note": f"positive in Q{q}" if sin_sign == 1 else f"negative in Q{q}"},
            {"label": "cos = adj/hyp", "math": f"\\cos\\theta={_vt_frac(cos_sign*adj,hyp)}", "note": f"positive in Q{q}" if cos_sign == 1 else f"negative in Q{q}"},
        ],
        "isGivenTan": True,
    }


def _full_set_q3():
    opp, adj, hyp = pick(_PYTH_TRIPLES)
    # Q3: sin<0, cos<0, tan>0
    sin_n = f"-{opp}/{hyp}"; cos_n = f"-{adj}/{hyp}"; tan_n = f"{opp}/{adj}"
    csc_n = f"-{hyp}/{opp}"; sec_n = f"-{hyp}/{adj}"; cot_n = f"{adj}/{opp}"
    return {
        "problemTex": f"\\sin(\\theta)=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\theta \\in \\text{{Q3}}.\\quad \\text{{Find all 6 trig values.}}",
        "answerTex": (
            f"\\sin=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\cos=-\\dfrac{{{adj}}}{{{hyp}}},\\; \\tan=\\dfrac{{{opp}}}{{{adj}}},\\;"
            f"\\csc=-\\dfrac{{{hyp}}}{{{opp}}},\\; \\sec=-\\dfrac{{{hyp}}}{{{adj}}},\\; \\cot=\\dfrac{{{adj}}}{{{opp}}}"
        ),
        "answerNorm": f"sin={sin_n},cos={cos_n},tan={tan_n}",
        "validForms": [f"sin={sin_n},cos={cos_n},tan={tan_n}"],
        "steps": [
            {"label": "Build reference triangle", "math": f"\\text{{opp}}={opp},\\; \\text{{adj}}={adj},\\; \\text{{hyp}}={hyp}", "note": ""},
            {"label": "Q3 signs: sin−, cos−, tan+", "math": "\\sin<0,\\; \\cos<0,\\; \\tan>0 \\text{{ in Q3}}", "note": ""},
            {"label": "Primary values", "math": f"\\sin=-\\dfrac{{{opp}}}{{{hyp}}},\\; \\cos=-\\dfrac{{{adj}}}{{{hyp}}},\\; \\tan=\\dfrac{{{opp}}}{{{adj}}}", "note": ""},
            {"label": "Reciprocals", "math": f"\\csc=-\\dfrac{{{hyp}}}{{{opp}}},\\; \\sec=-\\dfrac{{{hyp}}}{{{adj}}},\\; \\cot=\\dfrac{{{adj}}}{{{opp}}}", "note": ""},
        ],
        "isAllSix": True,
    }


diff5 = [_compound_angle_eval, _given_tan_find_sin_cos, _full_set_q3]

POOLS = {1: diff1, 2: diff2, 3: diff3, 4: diff4, 5: diff5}
