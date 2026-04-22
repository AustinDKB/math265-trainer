import re
from math_utils import expand_expression, polys_equal, user_input_to_norm


def check_answer(problem: dict, user_input: str) -> dict:
    u = user_input.strip()
    if not u:
        return {"result": "empty"}
    module = problem.get("module")
    if module == "factoring":
        if problem.get("isFracExpGcf"):
            return check_exp_factoring_answer(problem, u)
        if problem.get("isTrigFactoring"):
            return check_trig_factoring_answer(problem, u)
        return check_factoring_answer(problem, u)
    if module == "exponents":
        return check_exponent_answer(problem, u)
    if module == "fractions":
        return check_fraction_answer(problem, u)
    if module == "trig":
        return check_norm_answer(problem, u)
    if module == "logs":
        return check_norm_answer(problem, u)
    if module == "composition":
        return check_norm_answer(problem, u)
    if module == "limits":
        return check_norm_answer(problem, u)
    if module == "derivatives":
        return check_norm_answer(problem, u)
    if module == "integration":
        return check_integration_answer(problem, u)
    if module == "adv_integration":
        return check_integration_answer(problem, u)
    return {"result": "unknown"}


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
        if norm in (f"1/x^{pos_exp}", f"1/x^({pos_exp})"):
            return {"result": "correct"}

    # Fractional: x^(3/2) and x^1.5
    frac_match = re.search(r"x\^\((\d+)/(\d+)\)", ans)
    if frac_match:
        decimal = int(frac_match.group(1)) / int(frac_match.group(2))
        dec_str = f"{decimal:.4f}".rstrip("0").rstrip(".")
        if norm in (f"x^{dec_str}", f"x^({dec_str})"):
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
    s = re.sub(r"\bsinx\b", "x", s)
    s = re.sub(r"\bcosx\b", "x", s)
    s = re.sub(r"\btanx\b", "x", s)
    s = re.sub(r"\bsin\s+x\b", "x", s)
    s = re.sub(r"\bcos\s+x\b", "x", s)
    s = re.sub(r"\btan\s+x\b", "x", s)
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
    # collapse multiple parens
    s = s.replace("()", "")
    return s


def check_norm_answer(problem: dict, u: str) -> dict:
    """Generic checker: compare against answerNorm with lightweight normalization.
    Falls back to string-cleaned answerTex comparison."""
    ans_norm = problem.get("answerNorm", "")
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

    return {"result": "wrong"}


def check_integration_answer(problem: dict, u: str) -> dict:
    """Integration checker: strip trailing +C variants, then norm compare."""
    def strip_c(s):
        s = _norm_generic(s)
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

    return {"result": "wrong"}
