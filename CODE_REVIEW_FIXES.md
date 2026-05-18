# Code Review — Required Fixes

## app.py

### 1. Duplicate import (`L19`, `L33`)
`UNLOCK_TIERS` imported twice.
```python
# Remove L33 — keep only:
from module_config import UNLOCK_TIERS
```

### 2. ZeroDivisionError in `_get_unlocked_modules` (`L88–92`)
`mod_totals[m]["correct"] / mod_totals[m]["attempts"]` crashes if `attempts == 0`.
```python
tier_ready = all(
    mod_totals.get(m, {}).get("attempts", 0) >= 5
    and mod_totals.get(m, {}).get("attempts", 0) > 0
    and mod_totals[m]["correct"] / mod_totals[m]["attempts"] >= 0.8
    for m in tier
)
```

### 3. Duplicated unlock logic (`L344–364`)
`get_unlock_status()` re-implements `_get_unlocked_modules` inline. Extract and reuse.
```python
@app.get("/api/unlock-status")
def get_unlock_status():
    pair_stats = stats_overview()
    unlocked = _get_unlocked_modules(pair_stats)
    # ... build response using `unlocked` — don't re-implement the loop
```

### 4. Missing `difficulty` param validation (`L126`)
`?difficulty=abc` → unhandled `ValueError` → 500.
```python
try:
    diff = int(request.args.get("difficulty", 1))
except ValueError:
    return jsonify({"error": "difficulty must be an integer"}), 400
```

### 5. Unbounded `stats_trend` days param (`L285`)
`?days=99999` causes full table scan.
```python
days = max(1, min(int(request.args.get("days", 30)), 365))
```

### 6. Unbounded `list_bug_reports` limit (`L332`)
`?limit=9999999` returns uncapped rows.
```python
limit = max(1, min(int(request.args.get("limit", 100)), 500))
```

---

## checker.py

### 7. Double-negative factoring logic (`L89–91`)
`factored` is set, then immediately re-checked with the same conditions.
```python
# Before:
factored = "(" in u or problem.get("isGrouping") or problem.get("isQuadDisguise")
if not factored and not problem.get("isGrouping") and not problem.get("isQuadDisguise"):
    return {"result": "partial", ...}

# After:
factored = "(" in u or problem.get("isGrouping") or problem.get("isQuadDisguise")
if not factored:
    return {"result": "partial", "msg": "Expanded correctly but not factored — keep going"}
```

### 8. String fallback uses `answerTex` not `answerNorm` (`L96–101`)
When polynomial parse fails, fallback compares against LaTeX-stripped `answerTex`. Should prefer `answerNorm` first if available.
```python
# Try answerNorm first
norm_ans_direct = problem.get("answerNorm", "").lower().replace(" ", "").replace("*", "")
if norm_user == norm_ans_direct:
    return {"result": "correct"}
# Then fall back to stripped answerTex
```

### 9. `_normalize_inequality` misses `<=` / `<` with constant on left (`L332–340`)
`4<x` is not flipped to `x>4`. Only `>=` / `>` cases handled.
```python
for op_a, op_b in [(">=", "<="), (">", "<"), ("<=", ">="), ("<", ">")]:
    if op_a in s:
        parts = s.split(op_a)
        if len(parts) == 2:
            left, right = parts
            if re.match(r'^-?\d+(\.\d+)?$', left) and re.match(r'^[a-z]$', right):
                return f"{right}{op_b}{left}"
```

### 10. Double-normalization in `check_inequality_answer` (`L358–361`)
`nu` and `na` are pre-normalized, then passed to `check_norm_answer` which normalizes again via `_norm_generic`. Harmless now but will break if normalization ever has side effects. Pass the already-normalized values or skip the `check_norm_answer` fallback.

---

## db.py

### 11. Dead SM-2 code (`L217–275`, `L327–348`)
`time_to_quality`, `_sm2_update`, `update_srs_card`, `get_srs_due` — none called by `app.py` (FSRS replaced them). Delete to avoid confusion about which SRS system is active.

### 12. Silent migration errors (`L37–60`)
`except Exception: pass` on `ALTER TABLE` swallows real errors (disk full, permissions).
```python
try:
    conn.execute("ALTER TABLE attempts ADD COLUMN disputed INTEGER DEFAULT 0")
except Exception as e:
    if "duplicate column" not in str(e).lower():
        app.logger.warning("Migration warning: %s", e)
```
*(or use `sqlite3.OperationalError` specifically)*

### 13. f-string SQL in `get_fsrs_due_skills` (`L313`)
Inputs are internal module keys — not user-controlled — so injection risk is low. Add a comment explicitly documenting this assumption so a future maintainer doesn't introduce a vulnerability:
```python
# module names come from GENERATORS keys — not user input — safe to interpolate
placeholders = ",".join("?" * len(unlocked_modules))
```

---

## math_utils.py

### 14. Silent wrong result for negative exponents in `poly_pow` (`L104–108`)
`poly_pow(p, -1)` silently returns `{0: 1}` (loops 0 times) instead of raising.
```python
def poly_pow(p, n):
    if n < 0:
        raise ValueError(f"poly_pow does not support negative exponents (got {n})")
    result = {0: 1}
    for _ in range(n):
        result = poly_mul(result, p)
    return result
```

### 15. `expand_expression` silently mangling non-polynomial input (`L190–203`)
`\sqrt{x}` → LaTeX stripped → `{x}` → `(x)` → treated as `x`. User submitting `sqrt(x+1)` would produce a wrong polynomial silently. Detect and reject:
```python
if re.search(r'sqrt|log|sin|cos|tan|exp', s, re.IGNORECASE):
    raise ValueError("Non-polynomial expression — cannot expand")
```

---

## Cross-Cutting

### 16. `_numerically_equal` — 3 test points insufficient for degree ≥ 3 polynomials
Three fixed points `{1.3, 2.7, 4.1}` cannot distinguish all polynomials of degree ≥ 3 (two distinct degree-3 polys can agree at exactly 3 points by Lagrange interpolation). For factoring/integration modules that produce high-degree outputs, add a 4th test point:
```python
for xv in (1.3, 2.7, 4.1, 5.9):  # 4 points catches degree-3 imposters
```
