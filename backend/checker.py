import re
import math as _math
from math_utils import expand_expression, polys_equal, user_input_to_norm
from checker_registry import get_checker

# ── Safe numeric evaluator ─────────────────────────────────────────────────────

_SAFE_NS = {
    "__builtins__": {},
    "sin": _math.sin, "cos": _math.cos, "tan": _math.tan,
    "cot": lambda v: _math.cos(v) / _math.sin(v),
    "sec": lambda v: 1.0 / _math.cos(v),
    "csc": lambda v: 1.0 / _math.sin(v),
    "ln": _math.log, "log": _math.log10,
    "sqrt": _math.sqrt, "abs": abs,
    "e": _math.e, "pi": _math.pi,
}

_UNSAFE_KW = {
    "import", "exec", "eval", "open", "__", "lambda", "class", "def",
    "for", "while", "yield", "global", "nonlocal", "del", "assert",
    "with", "raise", "return", "pass", "break", "continue",
}

_SAFE_CHARS = set("0123456789abcdefghijklmnopqrstuvwxyz +-*/^().,{}")


def _safe_eval(s: str, x_val: float):
    """Evaluate a math expression at x=x_val in a restricted namespace."""
    s = s.strip().lower()
    if any(kw in s for kw in _UNSAFE_KW):
        return None
    if not all(c in _SAFE_CHARS for c in s):
        return None
    s2 = re.sub(r'\{([^}]*)\}', r'(\1)', s)   # {3x} → (3x)
    s2 = s2.replace('^', '**')
    s2 = s2.replace('x', f'({x_val})')
    s2 = re.sub(r'(\d)\(', r'\1*(', s2)        # 3( → 3*(
    s2 = re.sub(r'\)\(', r')*(', s2)            # )( → )*(
    s2 = re.sub(r'\)([a-z])', r')*\1', s2)      # )s → )*s
    s2 = re.sub(r'(\d)([a-z])', r'\1*\2', s2)   # 4sin → 4*sin, 2e → 2*e
    try:
        return float(eval(s2, _SAFE_NS))        # type: ignore[arg-type]
    except Exception:
        return None


def _numerically_equal(a: str, b: str) -> bool:
    """Check numeric equality of two expression strings at several test points."""
    for xv in (1.3, 2.7, 4.1):
        av = _safe_eval(a, xv)
        bv = _safe_eval(b, xv)
        if av is None or bv is None:
            return False
        if abs(av - bv) > 1e-4:
            return False
    return True


def check_answer(problem: dict, user_input: str) -> dict:
    u = user_input.strip()
    if not u:
        return {"result": "empty"}
    module = problem.get("module")
    checker = get_checker(module)
    if checker is None:
        return {"result": "unknown"}
    return checker(problem, u)


def check_factoring_answer(problem: dict, u: str) -> dict:
    orig = problem.get("originalExpanded", "")
    user_poly = None
    orig_poly = None
    try:
        user_poly = expand_expression(u)
    except Exception:
        pass
    try:
        if isinstance(orig, str):
            orig_poly = expand_expression(orig)
        elif isinstance(orig, dict):
            orig_poly = orig
    except Exception:
        pass

    if user_poly is not None and orig_poly is not None:
        if polys_equal(user_poly, orig_poly):
            factored = "(" in u or problem.get("isGrouping") or problem.get("isQuadDisguise")
            if not factored and not problem.get("isGrouping") and not problem.get("isQuadDisguise"):
                return {"result": "partial", "msg": "Expanded correctly but not factored — keep going"}
            return {"result": "correct"}

    # String fallback
    norm_user = u.lower().replace(" ", "").replace("*", "")
    norm_ans = (problem.get("answerTex", "")
                .lower().replace(" ", "").replace("*", "")
                .replace("\\", "").replace("{", "").replace("}", ""))
    norm_ans = re.sub(r"\\[a-z]*", "", norm_ans)
    if norm_user == norm_ans:
        return {"result": "correct"}
    return {"result": "wrong"}


def check_exponent_answer(problem: dict, u: str) -> dict:
    norm = user_input_to_norm(u)
    ans = problem.get("answerNorm", "").lower().replace(" ", "")

    if norm == ans:
        return {"result": "correct"}

    # x^(a) == x^a for integers
    def strip_int_parens(s):
        return re.sub(r"\((\d+)\)", r"\1", s)
    if strip_int_parens(norm) == strip_int_parens(ans):
        return {"result": "correct"}

    # 1/x^a == x^(-a)
    neg_match = re.search(r"x\^\((-\d+)\)", ans)
    if neg_match:
        pos_exp = abs(int(neg_match.group(1)))
        accepted = {f"1/x^{pos_exp}", f"1/x^({pos_exp})"}
        if pos_exp == 1:
            accepted.add("1/x")
        if norm in accepted:
            return {"result": "correct"}

    # Fractional: x^(3/2) and x^1.5
    frac_match = re.search(r"x\^\((\d+)/(\d+)\)", ans)
    if frac_match:
        decimal = int(frac_match.group(1)) / int(frac_match.group(2))
        dec_str = f"{decimal:.4f}".rstrip("0").rstrip(".")
        if norm in (f"x^{dec_str}", f"x^({dec_str})"):
            return {"result": "correct"}

    # Negative fraction: x^(-a/b) == 1/x^(a/b)
    neg_frac_match = re.search(r"x\^\(-(\d+)/(\d+)\)", ans)
    if neg_frac_match:
        num, den = neg_frac_match.group(1), neg_frac_match.group(2)
        if norm in (f"1/x^({num}/{den})", f"1/x^{num}/{den}"):
            return {"result": "correct"}

    # Numeric fallback — catches any mathematically equivalent form
    if norm and ans and _numerically_equal(norm, ans):
        return {"result": "correct"}

    return {"result": "wrong"}


def check_fraction_answer(problem: dict, u: str) -> dict:
    norm = user_input_to_norm(u)
    ans = user_input_to_norm(str(problem.get("answerNorm", "")))

    if norm == ans:
        return {"result": "correct"}

    # Numeric fraction cross-multiply
    num_frac = re.match(r"^(\d+)/(\d+)$", ans)
    user_frac = re.match(r"^(\d+)/(\d+)$", norm)
    if num_frac and user_frac:
        an, ad = int(num_frac.group(1)), int(num_frac.group(2))
        un, ud = int(user_frac.group(1)), int(user_frac.group(2))
        if an * ud == un * ad:
            return {"result": "correct"}

    # Integer comparison
    try:
        if abs(float(norm) - float(ans)) < 0.001:
            return {"result": "correct"}
    except ValueError:
        pass

    # Algebraic expression fallback (e.g. (x-3)/(x+3))
    u_eval = norm.strip().lower().replace(" ", "")
    an_eval = ans.strip().lower().replace(" ", "")
    if u_eval and an_eval and _numerically_equal(u_eval, an_eval):
        return {"result": "correct"}

    return {"result": "wrong"}


def _normalize_exp_frac_form(s: str) -> str:
    s = s.strip().lower().replace(" ", "")
    s = re.sub(r"x\^\{([^}]+)\}", r"x^(\1)", s)
    s = re.sub(r"x\^(-?\d+/\d+)(?!\))", r"x^(\1)", s)
    s = re.sub(r"x\^(-\d+)(?!\))", r"x^(\1)", s)
    return s.replace("*", "")


def check_exp_factoring_answer(problem: dict, u: str) -> dict:
    norm = _normalize_exp_frac_form(u)
    for f in problem.get("validForms", []):
        if norm == _normalize_exp_frac_form(f):
            return {"result": "correct"}

    def strip(s):
        return re.sub(r"\\[a-z]+", "", s).replace("{", "").replace("}", "").replace(" ", "").lower()
    if strip(norm) == strip(problem.get("answerTex", "")):
        return {"result": "correct"}
    return {"result": "wrong"}


def _strip_trig_to_x(s: str) -> str:
    s = re.sub(r"\\sin\^2\s*x", "x^2", s)
    s = re.sub(r"\\cos\^2\s*x", "x^2", s)
    s = re.sub(r"\\tan\^2\s*x", "x^2", s)
    s = re.sub(r"\(sinx\)\^2", "x^2", s)
    s = re.sub(r"\(cosx\)\^2", "x^2", s)
    s = re.sub(r"\(tanx\)\^2", "x^2", s)
    s = re.sub(r"sin\^2\s*x", "x^2", s)
    s = re.sub(r"cos\^2\s*x", "x^2", s)
    s = re.sub(r"tan\^2\s*x", "x^2", s)
    s = re.sub(r"\\sin\s*x", "x", s)
    s = re.sub(r"\\cos\s*x", "x", s)
    s = re.sub(r"\\tan\s*x", "x", s)
    s = re.sub(r"(?<![a-z])sinx(?![a-z])", "x", s)
    s = re.sub(r"(?<![a-z])cosx(?![a-z])", "x", s)
    s = re.sub(r"(?<![a-z])tanx(?![a-z])", "x", s)
    s = re.sub(r"(?<![a-z])sin\s+x(?![a-z])", "x", s)
    s = re.sub(r"(?<![a-z])cos\s+x(?![a-z])", "x", s)
    s = re.sub(r"(?<![a-z])tan\s+x(?![a-z])", "x", s)
    return s


def check_trig_factoring_answer(problem: dict, u: str) -> dict:
    if problem.get("trigFunc") == "mixed":
        def norms(s):
            s = s.lower().replace(" ", "")
            s = re.sub(r"\\sin\s*x", "sinx", s)
            s = re.sub(r"\\cos\s*x", "cosx", s)
            s = re.sub(r"\\tan\s*x", "tanx", s)
            return s.replace("\\", "").replace("{", "").replace("}", "").replace("*", "")
        nu = norms(u)
        for f in problem.get("validForms", []):
            if nu == norms(f):
                return {"result": "correct"}
        return {"result": "wrong"}

    substituted = _strip_trig_to_x(u)
    synthetic = {
        "module": "factoring",
        "originalExpanded": problem.get("originalExpandedPoly", ""),
        "isGrouping": False,
        "isQuadDisguise": False,
        "answerTex": "",
    }
    return check_factoring_answer(synthetic, substituted)


def _norm_generic(s: str) -> str:
    """Normalize user input for generic string comparison."""
    s = s.strip().lower()
    s = s.replace(" ", "").replace("*", "").replace("\\", "")
    s = re.sub(r"\{([^}]*)\}", r"\1", s)
    s = s.replace("()", "")
    # normalize bare trig calls: sinx → sin(x), cosx → cos(x), etc.
    for _fn in ("sin", "cos", "tan", "cot", "sec", "csc", "ln", "log"):
        s = re.sub(_fn + r"x(?![a-z0-9(])", _fn + "(x)", s)
    return s


def check_norm_answer(problem: dict, u: str) -> dict:
    """Generic checker: compare against answerNorm with lightweight normalization.
    Falls back to string-cleaned answerTex comparison, then numeric equality."""
    ans_norm = problem.get("answerNorm", "")
    # Check validNorms list if present
    valid_norms = problem.get("validNorms", [])
    if valid_norms:
        nu = _norm_generic(u)
        for vn in valid_norms:
            if nu == _norm_generic(vn):
                return {"result": "correct"}

    if ans_norm:
        nu = _norm_generic(u)
        an = _norm_generic(ans_norm)
        if nu == an:
            return {"result": "correct"}
        # Allow "undefined" spelled out
        if an == "undefined" and nu in ("undefined", "dne", "doesnotexist"):
            return {"result": "correct"}
        # Allow numeric float equality
        try:
            if abs(float(nu) - float(an)) < 1e-4:
                return {"result": "correct"}
        except (ValueError, TypeError):
            pass

    # Fallback: cleaned LaTeX
    ans_tex = _norm_generic(problem.get("answerTex", ""))
    if _norm_generic(u) == ans_tex:
        return {"result": "correct"}

    # Numeric equivalence fallback (handles cot(x), e^(x), fraction forms, etc.)
    u_eval = u.strip().lower().replace(" ", "")
    an_eval = (ans_norm or "").strip().lower().replace(" ", "")
    if u_eval and an_eval and _numerically_equal(u_eval, an_eval):
        return {"result": "correct"}

    return {"result": "wrong"}


def check_dual_answer(problem: dict, input1: str, input2: str) -> dict:
    """Check both answers for requiresDualAnswer problems."""
    r1 = check_norm_answer(problem, input1)
    prob2 = dict(problem)
    prob2["answerNorm"] = problem.get("answerNorm2", "")
    prob2["answerTex"]  = problem.get("answerTex2", "")
    r2 = check_norm_answer(prob2, input2)
    if r1["result"] == "correct" and r2["result"] == "correct":
        return {"result": "correct"}
    wrong = []
    if r1["result"] != "correct": wrong.append(1)
    if r2["result"] != "correct": wrong.append(2)
    return {"result": "wrong", "wrongSlot": wrong}


def check_integration_answer(problem: dict, u: str) -> dict:
    """Integration checker: strip trailing +C variants, then norm compare."""
    def strip_c(s):
        s = _norm_generic(s)
        s = re.sub(r"\+c$", "", s)
        s = re.sub(r"\+constant$", "", s)
        return s.strip("+")

    def strip_c_eval(s):
        """Strip +C without _norm_generic so * is preserved for safe_eval."""
        s = s.strip().lower().replace(" ", "")
        s = re.sub(r"\+c$", "", s)
        s = re.sub(r"\+constant$", "", s)
        return s.strip("+")

    user_stripped = strip_c(u)
    ans_norm = strip_c(problem.get("answerNorm", ""))
    ans_tex = strip_c(problem.get("answerTex", ""))

    if user_stripped == ans_norm or user_stripped == ans_tex:
        return {"result": "correct"}

    # Also check with +C present
    if _norm_generic(u) == _norm_generic(problem.get("answerNorm", "")):
        return {"result": "correct"}

    # "diverges" / "dne" for improper
    if ans_norm in ("diverges", "dne"):
        if _norm_generic(u) in ("diverges", "dne", "divergent"):
            return {"result": "correct"}

    # Numeric fallback for definite integrals / improper
    try:
        if abs(float(user_stripped) - float(ans_norm)) < 1e-4:
            return {"result": "correct"}
    except (ValueError, TypeError):
        pass

    # Numeric polynomial equivalence — handles x^2/2 vs 1/2*x^2, fraction coeffs, etc.
    u_eval = strip_c_eval(u)
    an_eval = strip_c_eval(problem.get("answerNorm", ""))
    if u_eval and an_eval and _numerically_equal(u_eval, an_eval):
        return {"result": "correct"}

    return {"result": "wrong"}
