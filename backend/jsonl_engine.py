import json
import math
import os
import random
import re
from pathlib import Path

# ── Safe eval namespace ──
_SAFE_MATH = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "ln": math.log,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "pow": pow,
    "int": int,
    "float": float,
    "round": round,
    "max": max,
    "min": min,
}


def safe_eval(expr, variables):
    """Evaluate an answer_fn expression with a sandboxed namespace."""
    if not expr or not isinstance(expr, str):
        return None
    # Disallow anything that looks like a name outside our safe set
    # Allow: numbers, operators, parentheses, dots, math names, variable names
    allowed_names = set(_SAFE_MATH.keys()) | set(variables.keys())
    # Quick safety check: reject double underscores and attribute access
    if "__" in expr or any(bad in expr for bad in ["import", "eval", "exec", "compile", "open"]):
        raise ValueError(f"Unsafe expression: {expr}")
    ns = dict(_SAFE_MATH)
    ns.update(variables)
    try:
        return eval(expr, {"__builtins__": {}}, ns)
    except Exception as exc:
        raise ValueError(f"Error evaluating '{expr}': {exc}")


# ── Template loading ──

TEMPLATE_DIR = Path(__file__).parent / "jsonl_templates"


def load_templates(course=None, path=None):
    """Load all .jsonl files from the template directory.

    If *course* is given, only files whose stem starts with that course prefix
    are returned (e.g. course='calc1' loads calc1_*.jsonl).
    If *path* is given, load a single file directly.
    """
    templates = []
    if path:
        target = Path(path) if isinstance(path, (str, os.PathLike)) else path
        with target.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                templates.append(json.loads(line))
        return templates

    if not TEMPLATE_DIR.exists():
        return []

    for f in sorted(TEMPLATE_DIR.iterdir()):
        if f.suffix != ".jsonl":
            continue
        if course and not f.stem.startswith(f"{course}_"):
            continue
        with f.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                templates.append(json.loads(line))
    return templates


# ── Variable filling ──

def _sample_variable(spec):
    """Sample a single variable from its spec dict."""
    vtype = spec.get("type", "int")
    lo, hi = spec.get("range", [0, 10])
    step = spec.get("step", 1)
    if vtype == "int":
        vals = list(range(lo, hi + 1, step))
        return random.choice(vals)
    if vtype == "float":
        # Generate a random float in [lo, hi] respecting step if provided
        if step == 1:
            return round(random.uniform(lo, hi), 3)
        # step-based float: e.g. range [0.1, 0.5] step 0.1
        n_steps = int((hi - lo) / step)
        return round(lo + random.randint(0, n_steps) * step, 6)
    if vtype == "pick":
        return random.choice(spec["values"])
    raise ValueError(f"Unknown variable type: {vtype}")


def fill_template(template, max_retries=20):
    """Sample variables, evaluate answer_fn, substitute into text fields.

    Returns a fully-realised problem dict ready for the frontend.
    """
    variables = template.get("variables", {})
    answer_fn = template.get("answer_fn")
    answer_fn2 = template.get("answer_fn2")
    computed = template.get("computed_values", {})

    for _ in range(max_retries):
        # 1. Sample variables
        params = {}
        for name, spec in variables.items():
            params[name] = _sample_variable(spec)

        # 2. Evaluate computed values
        derived = {}
        for name, formula in computed.items():
            try:
                derived[name] = safe_eval(formula, {**params, **derived})
            except ValueError:
                break
        else:
            # All computed values succeeded
            params.update(derived)

            # 3. Evaluate answer
            try:
                answer_val = safe_eval(answer_fn, params) if answer_fn else None
                answer_val2 = safe_eval(answer_fn2, params) if answer_fn2 else None
            except ValueError:
                continue

            # 4. Build substituted strings
            def sub(text):
                if not isinstance(text, str):
                    return text
                # Only replace known variable names; leave literal braces alone
                import re
                pattern = re.compile(r"\{(" + "|".join(re.escape(k) for k in params.keys()) + r")\}")
                return pattern.sub(lambda m: str(params[m.group(1)]), text)

            filled = {
                "id": template.get("id"),
                "course": template.get("course", "calc1"),
                "topic": template.get("topic"),
                "method": template.get("method"),
                "difficulty": template.get("difficulty", 1),
                "problemTex": sub(template.get("template", "")),
                "answerTex": sub(template.get("answerTex", "")) if template.get("answerTex") else (str(answer_val) if answer_val is not None else ""),
                "answerNorm": sub(template.get("answerNorm", "")) if template.get("answerNorm") else (str(answer_val) if answer_val is not None else ""),
                "steps": [
                    {"label": sub(s.get("label", "")), "math": sub(s.get("math", "")), "note": sub(s.get("note", ""))}
                    for s in template.get("solution_steps", [])
                ],
                "tags": template.get("tags", []),
                "isWordProblem": True,
                "modes_available": template.get("modes_available", ["solve"]),
                "justify_foil": template.get("justify_foil"),
                "backwards_prompt": template.get("backwards_prompt"),
                "break_errors": template.get("break_errors", []),
                "requiresDualAnswer": template.get("requiresDualAnswer", False),
            }

            if filled["requiresDualAnswer"] or answer_val2 is not None:
                filled["answerTex2"] = sub(template.get("answerTex2", "")) if template.get("answerTex2") else (str(answer_val2) if answer_val2 is not None else "")
                filled["answerNorm2"] = sub(template.get("answerNorm2", "")) if template.get("answerNorm2") else (str(answer_val2) if answer_val2 is not None else "")
                filled["requiresDualAnswer"] = True

            # 5. Apply validNorms if present
            if "validNorms" in template:
                filled["validNorms"] = [sub(v) for v in template["validNorms"]]

            # 6. Context skin (placeholder; apply_skin does the real work)
            filled["_params"] = params
            filled["_template"] = template
            return filled

    raise RuntimeError(f"Could not fill template {template.get('id')} after {max_retries} retries")


# ── Skin application ──

def load_skins(path=None):
    """Load skins from skins.json."""
    p = Path(path) if path else Path(__file__).parent / "skins.json"
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    # Support both dict-of-lists and list-of-dicts
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return {s["skin"]: s for s in data}
    return {}


def apply_skin(filled, skin_name=None, skins_data=None):
    """Inject a skin narrative into a filled problem dict."""
    if skins_data is None:
        skins_data = load_skins()

    template = filled.get("_template", {})
    contexts = template.get("contexts", [])
    if not contexts and not skins_data:
        filled["skin"] = "general"
        return filled

    # Prefer a context entry from the template; fall back to skins.json
    if contexts:
        ctx = random.choice(contexts)
        narrative = ctx.get("narrative", filled["problemTex"])
        params = filled.get("_params", {})
        try:
            filled["problemTex"] = narrative.format(**params)
        except KeyError:
            pass
        filled["skin"] = ctx.get("skin", "general")
        return filled

    if skins_data and skin_name in skins_data:
        skin = skins_data[skin_name]
        narratives = skin.get("narratives", [skin.get("narrative", filled["problemTex"])])
        narrative = random.choice(narratives)
        params = filled.get("_params", {})
        try:
            filled["problemTex"] = narrative.format(**params)
        except KeyError:
            pass
        filled["skin"] = skin_name
        return filled

    filled["skin"] = "general"
    return filled


# ── Session building ──

def interleave(templates, n):
    """Return up to *n* templates shuffled so no two adjacent share the same method.

    Falls back to simple shuffle if strict interleaving is impossible.
    """
    if not templates:
        return []
    if len(templates) < n:
        # Allow repetition with cycling
        pool = list(templates) * ((n // len(templates)) + 1)
    else:
        pool = list(templates)

    # Greedy interleave by method
    result = []
    remaining = list(pool)
    random.shuffle(remaining)
    attempts = 0
    while len(result) < n and remaining and attempts < n * 100:
        attempts += 1
        last_method = result[-1].get("method") if result else None
        # Find a candidate with different method
        candidates = [t for t in remaining if t.get("method") != last_method]
        if not candidates:
            # Relax constraint
            candidates = remaining
        choice = random.choice(candidates)
        result.append(choice)
        remaining.remove(choice)

    # If we still need more, fill from pool randomly
    while len(result) < n:
        result.append(random.choice(pool))

    return result[:n]


def inject_decoys(session, all_templates, rate=0.15, min_gap=4):
    """Replace ~rate fraction of session problems with decoy variants.

    A decoy is a problem whose surface cues suggest one method but whose actual
    solution requires another.  For v1 we implement this by picking a template
    whose method differs from the victim's method and swapping it in.
    """
    if not session or not all_templates:
        return session

    n_decoys = max(1, int(len(session) * rate))
    eligible_indices = list(range(len(session)))
    random.shuffle(eligible_indices)

    decoyed = 0
    used_indices = set()
    for idx in eligible_indices:
        if decoyed >= n_decoys:
            break
        # Respect min_gap from previous decoy
        if any(abs(idx - used_idx) < min_gap for used_idx in used_indices):
            continue
        victim = session[idx]
        victim_method = victim.get("method")
        # Pick a decoy template with a different method
        decoy_pool = [t for t in all_templates if t.get("method") != victim_method]
        if not decoy_pool:
            continue
        decoy = random.choice(decoy_pool)
        session[idx] = {**decoy, "_is_decoy": True, "_victim_method": victim_method}
        used_indices.add(idx)
        decoyed += 1

    return session


def assign_modes(session, weights=None):
    """Assign a mode to each problem in the session.

    Default distribution: solve 50%, justify 20%, backwards 15%, break 10%, derive 5%.
    Constraints:
      - derive: max 1 per session, difficulty >= 2, never on decoy
      - no three identical modes adjacent
    """
    if weights is None:
        weights = {"solve": 0.50, "justify": 0.20, "backwards": 0.15, "break": 0.10, "derive": 0.05}

    modes = list(weights.keys())
    probs = [weights[m] for m in modes]

    derive_assigned = False
    result = []
    for prob in session:
        is_decoy = prob.get("_is_decoy", False)
        diff = prob.get("difficulty", 1)
        # Filter modes
        available = list(modes)
        if is_decoy or derive_assigned or diff < 2:
            available = [m for m in available if m != "derive"]
        # Avoid three identical modes adjacent
        if len(result) >= 2:
            last_two = [result[-1].get("mode"), result[-2].get("mode")]
            if last_two[0] == last_two[1]:
                available = [m for m in available if m != last_two[0]]

        # Weighted pick from available
        avail_probs = [weights[m] for m in available]
        total = sum(avail_probs)
        if total == 0:
            mode = "solve"
        else:
            avail_probs = [p / total for p in avail_probs]
            mode = random.choices(available, weights=avail_probs, k=1)[0]

        if mode == "derive":
            derive_assigned = True

        result.append({**prob, "mode": mode})
    return result


# ── Mode wrappers ──

def wrap_justify(filled, foil_table=None, prompt_table=None):
    """Transform a solve template into a justify problem."""
    if foil_table is None:
        try:
            from foil_table import JUSTIFY_FOILS as _foil_table
            foil_table = _foil_table
        except Exception:
            foil_table = {}

    method = filled.get("method", "this method")
    foil = filled.get("justify_foil", "another method")
    if foil_table and method in foil_table:
        foil = foil_table[method]

    prompts = prompt_table or {
        "contrast": "Solve. Then explain why {method} applies here and not {foil}.",
        "condition": "Solve. Then state the condition that makes {method} correct.",
        "pre_solve": "Before solving: identify the method and why. Then solve.",
    }
    style = random.choice(list(prompts.keys()))
    prompt = prompts[style].format(method=method, foil=foil)

    filled["problemTex"] = f"[Justify] {prompt}\\\n\textbf{{Problem:}} {filled['problemTex']}"
    filled["modeData"] = {"style": style, "foil": foil, "prompt": prompt}
    return filled


def wrap_backwards(filled):
    """Transform into a backwards problem (answer shown, reconstruct setup)."""
    prompt = filled.get("backwards_prompt", "Given the answer below, reconstruct the original problem setup.")
    answer_display = filled.get("answerTex", filled.get("answerNorm", ""))
    filled["problemTex"] = (
        f"[Backwards] {prompt}\\\\\n"
        f"\\textbf{{Answer:}} {answer_display}\\\\\n"
        f"\\textbf{{Your task:}} Write the original problem statement and show the key equations."
    )
    filled["modeData"] = {"type": "backwards", "answer": answer_display}
    return filled


def wrap_break(filled):
    """Transform into a break problem (flawed solution, identify error + fix)."""
    errors = filled.get("break_errors", [])
    if not errors:
        # Fall back to a generic break template
        filled["problemTex"] = f"[Break] {filled['problemTex']}"
        filled["modeData"] = {"type": "break", "error": None}
        return filled

    error = random.choice(errors)
    flawed_steps = filled.get("steps", [])
    # v1: just flag the break mode; frontend will render the flawed steps
    filled["problemTex"] = (
        f"[Break] The following solution contains an error. Identify the error and provide the correct solution.\\\n"
        f"\\textbf{{Problem:}} {filled['problemTex']}"
    )
    filled["modeData"] = {"type": "break", "error": error, "flawed_steps": flawed_steps}
    return filled


def wrap_derive(filled, derive_library=None):
    """Replace the problem with a derive-mode problem from the static library.

    If the library has an entry matching the current method, use it;
    otherwise keep the original problem but tag it as derive.
    """
    if derive_library is None:
        try:
            from derive_library import DERIVE_CALC1 as _derive_lib
            derive_library = _derive_lib
        except Exception:
            derive_library = {}

    method = filled.get("method", "")
    if derive_library and method in derive_library:
        entry = random.choice(derive_library[method]) if isinstance(derive_library[method], list) else derive_library[method]
        filled["problemTex"] = f"[Derive] {entry.get('problem', 'Prove the related theorem.')}"
        filled["steps"] = entry.get("steps", [])
        filled["answerNorm"] = "derive_accept_any"
        filled["modeData"] = {"type": "derive", "theorem": entry.get("theorem", method)}
    else:
        filled["problemTex"] = f"[Derive] {filled['problemTex']}"
        filled["modeData"] = {"type": "derive"}
    return filled


# ── Session builder ──

def build_session(templates, n=10, mode_weights=None, decoy_rate=0.15, min_decoy_gap=4, skins_data=None):
    """Build a complete session:

    1. Interleave templates (no adjacent same method)
    2. Inject decoys
    3. Assign modes per weights
    4. Fill templates (sample variables, eval answers)
    5. Apply skins
    6. Wrap problems according to assigned mode

    Returns a list of fully-realised problem dicts.
    """
    # Step 0: wrap raw templates so _template travels through the pipeline
    wrapped = [{**t, "_template": t} for t in templates]

    # Step 1: interleave
    session = interleave(wrapped, n)

    # Step 2: decoys
    session = inject_decoys(session, wrapped, rate=decoy_rate, min_gap=min_decoy_gap)

    # Step 3: modes
    session = assign_modes(session, weights=mode_weights)

    # Step 4: fill + skin + wrap
    result = []
    for prob in session:
        template = prob.pop("_template", None)
        if template is None:
            continue
        try:
            filled = fill_template(template)
        except RuntimeError:
            continue

        # Skin
        filled = apply_skin(filled, skins_data=skins_data)

        # Mode wrap
        mode = prob.get("mode", "solve")
        if mode == "justify":
            filled = wrap_justify(filled)
        elif mode == "backwards":
            filled = wrap_backwards(filled)
        elif mode == "break":
            filled = wrap_break(filled)
        elif mode == "derive":
            filled = wrap_derive(filled)

        # Merge any extra fields from session builder (decoy flags, etc.)
        filled.update({k: v for k, v in prob.items() if k not in filled})
        result.append(filled)

    return result


# ── Validation ──

REQUIRED_TEMPLATE_FIELDS = {"id", "course", "topic", "method", "template", "difficulty"}


def validate_template(template):
    """Check a template dict for required fields and basic sanity."""
    missing = REQUIRED_TEMPLATE_FIELDS - set(template.keys())
    if missing:
        return False, f"Missing required fields: {missing}"

    # Check variables are well-formed
    for name, spec in template.get("variables", {}).items():
        if "range" not in spec and "values" not in spec:
            return False, f"Variable '{name}' missing range or values"
        vtype = spec.get("type", "int")
        if vtype not in {"int", "float", "pick"}:
            return False, f"Variable '{name}' has unknown type '{vtype}'"

    # Try a dry-run fill
    try:
        dry = fill_template(template)
        if not dry.get("answerNorm") and not dry.get("answer_fn"):
            return False, "Template produced empty answer"
    except RuntimeError as exc:
        return False, f"Fill failed: {exc}"
    except Exception as exc:
        return False, f"Fill error: {exc}"

    return True, "ok"


# ── Convenience: get next problem ──

def get_next_problem(course="calc1", topic=None, difficulty=None, mode_weights=None, skins_data=None):
    """Load templates for a course, optionally filter by topic/difficulty, build a single-problem session."""
    templates = load_templates(course=course)
    if topic:
        templates = [t for t in templates if t.get("topic") == topic]
    if difficulty is not None:
        templates = [t for t in templates if t.get("difficulty") == difficulty]
    if not templates:
        return None
    session = build_session(templates, n=1, mode_weights=mode_weights, skins_data=skins_data)
    return session[0] if session else None
