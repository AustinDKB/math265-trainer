# MATH TRAINER — Agent Notes

Math problem generator + answer checker for MATH 265. Flask backend, single-file HTML frontend, SQLite stats.

## Running

```bash
cd backend && python app.py          # Flask on http://127.0.0.1:5000
# In another shell from project root:
python -m http.server 8000           # serve frontend
# Open http://localhost:8000/math265-trainer.html  (not file://)
```

## Dependencies

No `requirements.txt`. Install manually:

```bash
pip install flask flask-cors sympy fsrs pytest
```

## Testing

```bash
cd backend && pytest tests/
```

Tests manually `sys.path.insert(...)` the parent dir — no `pytest.ini` or `setup.py` needed. A quick smoke test for one generator:

```bash
cd backend && python -c "from generators.factoring import _diff_squares; print(_diff_squares())"
```

## Architecture

```
math265-trainer.html      SPA frontend (~2800 lines, KaTeX, vanilla JS, Canvas)
backend/
  app.py                  Flask API (problem, check, stats, XP, SRS)
  checker.py              Answer validation pipeline
  checker_registry.py     Module → checker_fn map. New modules must register here.
  db.py                   SQLite wrapper (auto-creates attempts.db, auto-migrates)
  math_utils.py           Polynomial parser, R(), pick(), sign_str(), simplify_frac()
  module_config.py        MODULES metadata + UNLOCK_TIERS
  problem_builder.py      Helpers: problem(), dual_problem(), step()
  sympy_utils.py          SymPy → to_tex() / to_norm() adapter
  generators/
    __init__.py           Exports ALL_MODULES, GENERATORS, REGISTRY
    *.py                  Each exports POOLS = {1: [fn, ...], 2: [...], ...}
```

## Generator Contract

Every pool function returns:

```python
{
    "problemTex": "LaTeX shown to user",
    "answerTex":  "LaTeX answer (wrong feedback)",
    "answerNorm": "normalized string for checker",  # no spaces
    "steps": [{"label": "...", "math": "LaTeX", "note": "text"}],
    # optional flags:
    "validNorms": [...],           # alternate accepted forms
    "requiresDualAnswer": True,    # needs answerNorm2 / answerTex2
    "originalExpanded": {0: c, ...},  # factoring only (poly dict)
    "isFracExpGcf": True,
    "isTrigFactoring": True,
    "trigFunc": "sin"|"cos"|"mixed",
}
```

Add a new generator:
1. Write function in `generators/X.py`
2. Append to `POOLS[difficulty]` list
3. Register checker in `checker_registry.py` if module is new
4. Ensure `answerNorm` passes `_safe_eval` (see below)

## Checker Dispatch

```
factoring       → check_factoring_answer (polynomial equality via expand_expression)
                  isFracExpGcf     → check_exp_factoring_answer
                  isTrigFactoring  → check_trig_factoring_answer
exponents       → check_exponent_answer
fractions       → check_fraction_answer (cross-multiply, float tol 0.001)
trig/logs/composition/limits/derivatives → check_norm_answer
integration / adv_integration            → check_integration_answer (+C stripped)
dual-answer                              → check_dual_answer (returns wrongSlot)
```

`check_norm_answer` pipeline:
1. `validNorms` list match
2. `_norm_generic()` string compare vs `answerNorm`
3. `"undefined"` ↔ `"dne"` / `"doesnotexist"`
4. Numeric eval at x ∈ {1.3, 2.7, 4.1}, tolerance 1e-4

## Critical Gotchas

- `_safe_eval` allowlist: `0123456789abcdefghijklmnopqrstuvwxyz +-*/^().,{}` — **no uppercase, no `|`, no `=`, no `!`**. If `answerNorm` contains disallowed chars, the numeric fallback will silently fail; rely on `validNorms` or string normalization instead.
- `originalExpanded` keys are stringified in JSON transit; `app.py` converts them back to `int` on receive.
- `pick()` and `R()` live in `math_utils.py`, not `random`.
- Frontend `API_BASE` is hardcoded to `http://127.0.0.1:5000` inside `math265-trainer.html`.
- KaTeX is loaded lazily; always wrap render calls in `ensureKatex(fn)`.
- `problem_builder.py` has helpers — use them instead of hand-rolling dicts.
- `attempts.db` is auto-created in `backend/` and auto-migrated on startup. It is `.gitignore`d.
- `db.py` depends on the `fsrs` library for spaced-repetition scheduling.

## Module Names (for `module=` param)

`factoring`, `exponents`, `fractions`, `trig`, `logs`, `composition`, `limits`, `derivatives`, `integration`, `adv_integration`

## answerNorm Format Examples

```
"3*(2+sqrt(x))^2/(2*sqrt(x))"
"e^x*(1+x)"
"2*sin(x)*cos(x)"
"-2/x^2"
"3/4"
"sqrt(3)/2"
"undefined"
```

No spaces, explicit `*`, `^` for power, `e^()` for exp, `ln()` for log.
