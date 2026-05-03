# MATH TRAINER — Project Progress

> Last updated: 2026-05-02

---

## What Exists Now

### Backend (30 modules, 412 tests passing)

**Algebra (13 modules):**
- `factoring`, `exponents`, `fractions` — original
- `linear_equations`, `quadratic`, `polynomials`, `rational_expressions`, `systems`, `absolute_value`, `radicals`, `inequalities`, `sequences`, `probability` — WP5

**Precalculus (3 modules):**
- `trig`, `logs`, `composition` — original

**Calculus 1 (10 modules):**
- `limits`, `derivatives`, `integration` — original
- `asymptotes`, `increasing_decreasing`, `extrema`, `mvt`, `numerical_methods`, `indeterminate_forms`, `epsilon_delta`, `hyperbolic_apps`, `center_of_mass`, `function_construction` — WP4

**Calculus 2 (1 module):**
- `adv_integration` — original

### JSONL Engine (50 templates, 6 files)

- `calc1_optimization.jsonl` — 10 templates
- `calc1_deriv_app.jsonl` — 10 templates
- `calc1_integ_app.jsonl` — 10 templates
- `calc1_trig_exp.jsonl` — 10 templates
- `calc2_and_precalc.jsonl` — 5 templates
- `algebra_exp.jsonl` — 5 templates

**Features:** variable sampling, computed answers, dual answers, 4 mode wrappers (justify/backwards/break/derive), decoy injection, mode assignment, skin application, session builder, schema validation.

### Frontend

- `math265-shared.css` — shared styles (276 lines)
- `math265-trainer.html` — main trainer SPA (3042 lines)
- `math265-modes.html` — JSONL mode picker (798 lines)

### API Endpoints

- `GET /api/problem?module=&difficulty=` — computational problems
- `GET /api/problem/jsonl?course=` — JSONL word problems
- `POST /api/check` — standard answer checking
- `POST /api/check/mode` — mode-specific checking (justify/backwards/break/derive)
- `GET /api/modules` — module list
- `GET /api/xp` — XP stats
- `POST /api/report` — bug reports
- `GET /api/problem/auto` — adaptive problem selection
- `GET /api/stats/*` — overview, trend, weak spots

### Checkers

- `check_factoring_answer` — polynomial equality via expansion
- `check_exponent_answer` — exponent normalization
- `check_fraction_answer` — cross-multiply, float tolerance
- `check_norm_answer` — generic string compare + numeric fallback
- `check_integration_answer` — +C stripping
- `check_dual_answer` — two-slot checking with wrongSlot
- `check_exp_factoring_answer` — fractional exponent GCF
- `check_trig_factoring_answer` — trig polynomial equality

### Database

- SQLite (`attempts.db`) — auto-created, auto-migrated
- FSRS integration for spaced repetition
- Stats tracking per module/difficulty

---

## Test Coverage

**412 tests passing** across 13 test files:

| File | Tests | What |
|------|-------|------|
| `test_app.py` | 14 | Flask endpoints (problem, check, auto, stats, XP) |
| `test_app_extra.py` | 5 | Extra endpoints (modules, report, auto) |
| `test_checkers.py` | 22 | All checker functions |
| `test_dual_answers.py` | 5 | Dual-answer flow |
| `test_edge_cases.py` | 5 | Trig flags, validNorms, dne/und, tolerance |
| `test_generators.py` | 66 | Shape tests for all 30 modules |
| `test_jsonl_engine.py` | 21 | JSONL engine core |
| `test_math_utils.py` | 12 | math_utils helpers |
| `test_mode_endpoints.py` | 10 | `/api/check/mode` endpoint |
| `test_mode_wrappers.py` | 14 | Mode wrapper functions |
| `test_new_checkers.py` | 105 | New module checker registration |
| `test_wp4_generators.py` | 17 | WP4 generator + checker validation |
| `test_wp5_generators.py` | 17 | WP5 generator + checker validation |

---

## What Comes Next

### Near-term (next session)

1. **More JSONL templates** — current 50 is a good start; target ~150 for calc1 alone
2. **Break mode improvements** — currently minimal; needs actual flawed steps per template
3. **Derive library** — `derive_library.py` exists but is thin; needs ~20 entries
4. **FOIL tables** — `foil_table.py` exists but is thin; needs expansion

### Medium-term

1. **Linear Algebra 1** — 7 modules, ~35 templates, matrix grid input, new checkers
   - See `LINEAR_ALGEBRA_REFERENCE.md` for full spec
2. **Calc 2 expansion** — only `adv_integration` exists; need series, parametric, polar, etc.
3. **Frontend polish** — dark mode, keyboard shortcuts, progress visualization
4. **Stats dashboard** — charts, weak spot drill-down, study recommendations

### Long-term

1. **Calc 3** — multivariable, vectors, multiple integrals
2. **LA 2 & LA 3** — proof-based, abstract vector spaces
3. **Mobile app** — PWA or React Native wrapper
4. **User accounts** — persistent progress across devices

---

## Files to Keep

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent instructions for this project |
| `CLAUDE.md` | Claude-specific context |
| `PROBLEM_GENERATOR_METHODOLOGY.md` | How generators are built |
| `LINEAR_ALGEBRA_REFERENCE.md` | LA question types & implementation notes |
| `PROGRESS.md` | This file |

## Deleted Planning Files

The following were deleted after extracting useful content:

- `MASTER_BUILD_PLAN.md` — day-by-day plan (superseded by implemented code)
- `EXPANSION_PLAN.md` — expansion roadmap (now in PROGRESS.md)
- `1 Calculus One Gaps.md` — gap analysis (now filled)
- `addition questions to add.md` — question list (now implemented)
- `check implemented.md` — implementation checklist (now done)
- `factoring-new-levels.md` — factoring levels (now in code)
- `LINEAR 123 CALC 123.md` — broad reference (LA content extracted to `LINEAR_ALGEBRA_REFERENCE.md`)
- `TEXTBOOK_ANALYSIS.md` — textbook analysis (used during build)
- `DOCUMENT_COMPARISON.md` — doc comparison (used during build)
- `TEXTBOOK_EDGE_CASES.md` — edge cases (tested in `test_edge_cases.py`)
- `edge_case_exercises.md` — edge case list (tested)
- `edge_case_scan.md` — edge case scan (tested)
- `ENGAGEMENT_ALGORITHMS.md` — engagement ideas (implemented in JSONL engine)
- `math265-problem-types.md` — old problem type doc (superseded by module_config.py)
