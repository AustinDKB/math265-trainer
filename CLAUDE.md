# MATH TRAINER — Claude Reference

Math problem generator + answer checker for MATH 265 (precalc/calc). Flask backend, single HTML frontend, SQLite stats.

## Running

```bash
cd backend && python app.py        # Flask on http://127.0.0.1:5000
# Then open math265-trainer.html in browser (served via http, not file://)
python -m http.server 8000         # serve frontend from project root
```

No requirements.txt. Install: `pip install flask flask-cors sympy`

## Architecture

```
math265-trainer.html   ~2830 lines — full SPA (KaTeX, vanilla JS, Canvas charts)
backend/
  app.py               Flask API (7 endpoints)
  checker.py           Answer validation
  db.py                SQLite wrapper (attempts.db)
  math_utils.py        Polynomial arithmetic + R(), pick(), sign_str()
  sympy_utils.py       SymPy adapter: to_norm(), to_tex() for generators
  generators/
    factoring.py        POOLS 1-5
    exponents.py        POOLS 1-5
    fractions.py        POOLS 1-5
    trig_circle.py      POOLS 1-3
    logs.py             POOLS 1-3
    composition.py      POOLS 1-3
    limits.py           POOLS 1-4
    derivatives.py      POOLS 1-5 (uses sympy_utils.py)
    integration_basic.py    POOLS 1-3
    integration_advanced.py POOLS 2-5
```

## API Endpoints

| Method | Path | Params |
|--------|------|--------|
| GET | `/api/problem` | `module`, `difficulty` |
| POST | `/api/check` | `{problem, input, timeSec}` or `{problem, inputs:[u1,u2], timeSec}` |
| GET | `/api/stats/overview` | — |
| GET | `/api/stats/trend` | `days=30` |
| GET | `/api/stats/problem` | `tex=...` |
| GET | `/api/stats/weak` | `min_attempts=3, limit=10` |
| POST | `/api/report` | `{problem, userAnswer, note, attemptId}` |
| GET | `/api/reports` | `limit=100` |

## Generator Convention

Every generator function returns this shape:

```python
{
    "problemTex":  "LaTeX shown to user",
    "answerTex":   "LaTeX answer (shown on wrong)",
    "answerNorm":  "normalized form for checker",  # no spaces, no LaTeX
    "steps": [
        {"label": "Step title", "math": "LaTeX", "note": "plain text"},
    ],
    # Optional flags:
    "validNorms":         [...],   # alternate accepted forms
    "originalExpanded":   {0: c, 1: c, ...},  # factoring only (poly dict)
    "requiresDualAnswer": True,    # two inputs; also needs answerNorm2/answerTex2
    "answerNorm2":        "...",   # second answer norm (dual only)
    "answerTex2":         "...",   # second answer LaTeX (dual only)
    "isFracExpGcf":       True,    # exponent factoring
    "isGrouping":         True,
    "isQuadDisguise":     True,
    "isTrigFactoring":    True,
    "trigFunc":           "sin"|"cos"|"mixed",
}
```

Each module exports:

```python
POOLS = {
    1: [fn1, fn2, fn3],  # lists of callables
    2: [fn4, fn5],
    ...
}
```

app.py does: `random.choice(POOLS[module][difficulty])()` — no args passed.

## Checker Dispatch

```
factoring  → check_factoring_answer (polynomial equality via expand_expression)
             isFracExpGcf → check_exp_factoring_answer
             isTrigFactoring → check_trig_factoring_answer
exponents  → check_exponent_answer (normalized x^(a), handles negatives/fractions)
fractions  → check_fraction_answer (cross-multiply, float tolerance 0.001)
trig/logs/composition/limits/derivatives → check_norm_answer (generic)
integration/adv_integration → check_integration_answer (strips +C first)
requiresDualAnswer → check_dual_answer (calls check_norm_answer twice, returns wrongSlot)
```

`check_norm_answer` pipeline:
1. Match `validNorms` list if present
2. `_norm_generic()` string compare vs `answerNorm`
3. "undefined" ↔ "dne"/"doesnotexist"
4. Numeric eval at x ∈ {1.3, 2.7, 4.1}, tolerance 1e-4

## SymPy Integration (sympy_utils.py)

Uses SymPy for symbolic differentiation in derivatives.py generators.

```python
from sympy import symbols, diff, simplify
from sympy_utils import to_norm, to_tex

x = symbols('x')
expr = x**2 * exp(x)
y_prime = simplify(diff(expr, x))
print(to_tex(y_prime), to_norm(y_prime))
```

- `to_norm()` converts SymPy expressions to answerNorm format (^ for power, e^() for exp, ln() for log)
- `to_tex()` converts to LaTeX via sympy.latex()
- Used in: derivatives.py (product/quotient rule generators). All others hardcoded.

## math_utils.py

```python
R(a, b)           # random.randint(a, b)
pick(arr)         # random.choice(arr)
sign_str(n)       # "+3" or "-3"
expand_expression("(x+2)(x-3)")  # → {0: -6, 1: -1, 2: 1} (poly dict)
polys_equal(a, b) # True if same polynomial
simplify_frac(n, d)  # → (n//g, d//g)
```

## Database Schema

```sql
attempts(id, ts, module, difficulty, problem_tex, correct, time_sec, disputed)
bug_reports(id, ts, module, difficulty, problem_tex, answer_tex, user_answer, note, attempt_id)
```

Stats track per-(module, difficulty): attempts, correct, accuracy.
`dispute_attempt(id)` marks disputed=1, excluded from stats.

## Frontend Key Points

- State in JS `state` object; localStorage key `math265_v3`
- Per-module store: `store[module][difficulty] = {attempts, correct, streak, best_streak, last10}`
- Adaptive difficulty: streak≥5 → bump up; 3 wrong in last 5 → bump down
- Dual-answer problems: `requiresDualAnswer:true` shows second input, sends `inputs:[u1,u2]`
- `$('element-id')` helper for `document.getElementById`
- `ensureKatex(fn)` for lazy KaTeX loading before rendering

## answerNorm Format Examples

```
"3*(2+sqrt(x))^2/(2*sqrt(x))"    # no spaces, * explicit, ^ for power
"e^x*(1+x)"                       # e^x stays as-is
"2*sin(x)*cos(x)"                 # trig with parens
"-2/x^2"                          # negatives fine
"3/4"                             # fractions
"sqrt(3)/2"                       # not \\sqrt
"undefined"                        # or "dne"
```

## Adding a New Generator (checklist)

1. Write function in appropriate `generators/X.py`
2. Add to `POOLS[difficulty]` list
3. Ensure `answerNorm` passes `_safe_eval` (uses safe char set: `0-9a-z +-*/^().,{}`)
4. Test: `python -c "from generators.X import _fn; print(_fn())"`
5. If multiple valid forms: use `validNorms` list
6. If dual-answer: set `requiresDualAnswer:True`, add `answerNorm2`/`answerTex2`

## Modules List (for `module=` param)

`factoring`, `exponents`, `fractions`, `trig`, `logs`, `composition`, `limits`, `derivatives`, `integration`, `adv_integration`

## Known Gotchas

- `originalExpanded` keys are stringified in JSON transit; app.py converts back to int on receive
- `_safe_eval` allowlist: `0123456789abcdefghijklmnopqrstuvwxyz +-*/^().,{}` — no uppercase, no `|`
- `pick()` and `R()` are in math_utils, not random directly
- Frontend `API_BASE` hardcoded to `http://127.0.0.1:5000` in HTML
- Steps array is optional but should be provided for all non-trivial problems
- KaTeX loaded lazily; always wrap render calls in `ensureKatex(fn)`
