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
