# 1 Calculus One Gaps

Plan for all missing Calc 1 problem types. Built after Phase 0 refactor + Phase 1 algebra.



#### Optimization (13-16 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| O1 | Fence along river (3-sided), maximize area | P (perimeter) | OpenStax 4.7, Strang 3.5 |
| O2 | Fence (4-sided, fixed perimeter), maximize area | P | OpenStax 4.7 |
| O3 | Open-top box from sheet, cut corners, max volume | W, L (sheet dims) | OpenStax 4.7, Apex 4.4 |
| O4 | Closed box, fixed volume, min surface area | V | OpenStax 4.7 |
| O5 | Cylinder: min surface for given volume | V | OpenStax 4.7 |
| O6 | Two pens sharing a wall, min fencing | P, n (pens) | OpenStax 4.7 |
| O7 | Printed page: max print area with margins | W, L, margin dims | OpenStax 4.7 |
| O8 | Distance from point to curve, min distance | point coords, curve eq | Strang 3.5 |
| O9 | Revenue maximization (linear demand curve) | price, qty, slope | OpenStax 4.7, Apex 4.4 |
| O10 | Cost minimization (fixed + variable cost) | fixed cost, variable rate | OpenStax 4.7 |
| O11 | Shortest ladder over wall (wall H, gap L) | H, L | OpenStax 4.7 |
| O12 | Cheapest pipeline (cross river + land) | width, dist, cost/m | OpenStax 4.7 |
| O13 | Inscribe rectangle in parabola, max area | parabola params | Strang 3.5 |
| O14 | Inscribe rectangle in circle, max area | radius | OpenStax 4.7 |
| O15 | Inscribe cylinder in sphere, max volume | sphere radius | OpenStax 4.7 |
| O16 | Max/min word problem requiring second derivative test to verify | constraint, objective | OpenStax 4.7 |
| O17 | Inscribe cone in sphere, max volume | sphere radius | OpenStax 4.7 Q342 |
| O18 | Inscribe rectangle in triangle (3-4-5), max area | triangle sides | OpenStax 4.7 Q343 |
| O19 | Inscribe cylinder in cone, max volume | cone R, h | OpenStax 4.7 Q344 |
| O20 | Closed cylinder fixed volume V, min surface area | volume V | OpenStax 4.7 Q345 |
| O21 | Right cone fixed surface area S, max volume | surface area S | OpenStax 4.7 Q346 |
| O22 | Distance from point to curve, min distance (line/parabola) | point coords, curve eq | OpenStax 4.7 Q347–350, Strang 3.5 |
| O23 | Window: semicircle on rectangle, max area given perimeter | perimeter, radius | OpenStax 4.7 Q351 |
| O24 | Discrete optimization (watermelon plants, output drops per extra plant) | initial plants, initial yield, drop rate | OpenStax 4.7 Q352 |
| O25 | Different material costs (bottom vs sides), min cost for given volume | costs per area, volume | OpenStax 4.7 Q353 |
| O26 | Multiple adjacent pens/composite shapes, min fencing | total area, pen count | OpenStax 4.7 Q354 |
| O27 | Apartment rent optimization (price ↑ → occupancy ↓, maintenance cost) | base rent, base units, increment, maintenance | OpenStax 4.7 Q355 |

#### Related Rates (10-12 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| R1 | Conical tank filling/emptying | H, R, flow rate | OpenStax 3.9 |
| R2 | Spherical balloon inflating/deflating | inflation rate | OpenStax 3.9 |
| R3 | Ladder sliding down wall | length, slide rate | OpenStax 3.9 |
| R4 | Shadow length (person walking from lamp) | lamp H, walk speed | OpenStax 3.9 |
| R5 | Two ships diverging (right triangle) | speeds, initial dist | OpenStax 3.9 |
| R6 | Circular oil spill expanding | area growth rate | OpenStax 3.9 |
| R7 | Water draining from inverted cone | H, R, drain rate | OpenStax 3.9 |
| R8 | Angle of elevation (plane approaching) | altitude, speed | OpenStax 3.9 |
| R9 | Expanding rectangle (both dims changing) | dL/dt, dW/dt | OpenStax 3.9 |
| R10 | Spotlight on wall (rotating beacon) | distance, rotation speed | Strang 3.4 |

#### Particle Motion / Kinematics (6-8 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| K1 | Given v(t), find position at time T | v(t) formula, s(0) | OpenStax 5.1 |
| K2 | Given a(t), find velocity at time T | a(t) formula, v(0) | OpenStax 5.1 |
| K3 | Given a(t), find net displacement over [t0, t1] | a(t), v(0), s(0) | OpenStax 5.1 |
| K4 | Car decelerating at constant rate, stopping distance | v0, decel rate | OpenStax 5.1 |
| K5 | Particle changes direction — find total distance | v(t), interval | OpenStax 5.1 |
| K6 | Given s(t), find when particle is at rest | s(t) formula | OpenStax 5.1 |
| K7 | Two particles, when do they meet? | s1(t), s2(t) | OpenStax 5.1 |
| K8 | Given s(t), when is particle speeding up vs slowing down? (v·a sign analysis) | s(t), interval | OpenStax 5.1 |

#### FTC / Net Change (5-6 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| F1 | Given v(a) and ∫[a,b] v'(t) dt, find v(b) | v(a), integral value | OpenStax 5.3 |
| F2 | Population growth: given P(a) and ∫P'(t)dt, find P(b) | P(a), rate function | OpenStax 5.3 |
| F3 | Water tank: given initial volume and flow rate, find final volume | V(0), r(t) | OpenStax 5.3 |
| F4 | Net change of quantity given rate function | initial value, r(t) | OpenStax 5.3 |
| F5 | Average value of function on [a, b] | f(x), a, b | OpenStax 5.3 |
| F6 | Mass from linear density ρ(x) over [0, L] | ρ(x), L | OpenStax 5.3 |

#### Area / Volume Applications (6-7 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| AV1 | Area between two curves | f(x), g(x) | OpenStax 6.1 |
| AV2 | Area between curve and x-axis | f(x), roots | OpenStax 6.1 |
| AV3 | Volume by disk method (rotate around x-axis) | f(x), bounds | OpenStax 6.2 |
| AV4 | Volume by washer method (two curves) | f(x), g(x), bounds | OpenStax 6.2 |
| AV5 | Volume by shell method (rotate around y-axis) | f(x), bounds | OpenStax 6.3 |
| AV6 | Known cross-sections (squares on base curve) | base curve | OpenStax 6.2 |
| AV7 | Triangle area from 3 vertices (line equations + definite integrals) | vertex coords | — |
| AV8 | Gabriel's Horn: finite volume vs infinite surface area paradox | y = 1/x rotated [1,∞) | OpenStax 6.4 Q217 |
| AV9 | Catenary arc length & area-to-arc-length ratio | y = a·cosh(x/a) | OpenStax 6.4 Q426–428 |
| AV10 | Surface area of composite solid with flat cutoff (sphere + cylinder) | sphere radius, cylinder dims | OpenStax 6.4 Q208 |
| AV11 | Arc length comparison / scaling arguments (parabola vs line, x^n family) | function family, interval | OpenStax 6.4 Q213–216 |
| AV12 | Surface area of revolution for 1/x (lampshade) | y = 1/x, bounds | OpenStax 6.4 Q209 |

#### Linear Approximation / Differentials (3-4 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| LA1 | Approximate √a near perfect square | a, nearby square | OpenStax 4.2 |
| LA2 | Approximate sin(a) near standard angle | a, nearby angle | OpenStax 4.2 |
| LA3 | Estimate (1+x)^n for small x | x, n | OpenStax 4.2 |
| LA4 | Differential dy for function at point | f(x), x, dx | OpenStax 4.2 |

#### Concavity & Acceleration in Context (4 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| CA1 | Given rate function r(t), find when rate is increasing (r' > 0) vs decreasing (r' < 0) | r(t), interval | OpenStax 3.4 |
| CA2 | Inflection point interpretation: when does growth start decelerating? (logistic, learning curve) | model params | OpenStax 4.3 |
| CA3 | Rate of rate change: how fast is the rate changing at time t? | quantity, rate, time | OpenStax 3.9 |
| CA4 | Given v(t) graph description, determine acceleration sign and concavity of s(t) | v(t) description | OpenStax 5.1 |

#### Work Applications (2 templates)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| W1 | Work to build pyramid (slice-and-sum, variable force) | base, height, density | OpenStax 6.5 |
| W2 | Work to pump fluid from spherical tank | radius, spout height, density | OpenStax 6.5 |
| W3 | Work with angled force (W = F·d·cos θ) | force, distance, angle | OpenStax 6.5 Q221 |
| W4 | Work to lift object (kg → N conversion trap) | mass, height | OpenStax 6.5 Q220 |
| W5 | Work to stretch/compress spring (Hooke's law) | force, displacement | OpenStax 6.5 |

#### Numerical Integration (1 template)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| NI1 | Midpoint rule from discrete measurements | n, data points | OpenStax 5.1 |

#### Trig Equations (1 template)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| TE1 | Solve sin(x) = cos(kx) on interval | k, interval | OpenStax Ch 7 |

#### Trig Integration (1 template)

| ID | Pattern | Variables | Source Sections |
|----|---------|-----------|-----------------|
| TI1 | ∫sec(t)(a·sec(t) + b·tan(t))dt — expand to sec² + sec·tan | a, b | OpenStax 1.3 |

### Context Skins (DOC_COMPARISON §7 — 75 total)

All word problem templates get skins applied at session-build time. No skin is tied to any specific method. This severs surface narrative → method associations.

**Saskatchewan-weighted clusters:** Agriculture, Oil & Gas, Mining, Construction, Government

Full 75-skin list in DOC_COMPARISON §7.

### Anti-Pattern-Matching Layers (DOC_COMPARISON §5, §7)

| Layer | What it kills | Mechanism |
|-------|---------------|-----------|
| 1 — Context skins | Surface narrative → method | 75 skins × all templates, random assignment |
| 2 — Decoys | Mathematical structure → method | 15% of session, 3 tiers, min 4 apart |
| 3 — Interleaving | Blocked-practice automaticity | No two same method adjacent |
| 4 — Justify mode | Execution without understanding | "Why this method, not [foil]?" |
| 5 — Break mode | Memorized scripts | Find error in flawed solution |
| 6 — Backwards mode | Formula-as-answer | Reconstruct setup from answer |
| 7 — Derive mode | Theorem-as-axiom | Prove theorem from first principles |

Mode distribution per session: solve 50%, justify 20%, backwards 15%, break 10%, derive 5%.

---

## SECTION B — SYSTEMATIC GAP FILL

### B1: Already Implemented (can CRUSH now)

| # | Type | Where | Difficulty |
|---|------|-------|------------|
| 2 | Basic Limit | `limits.py` P1-2 | 1-2 |
| 4 | Basic Integration | `integration_basic.py` P1-2 | 1-2 |
| 9 | FTC/IVP: v(3)=34, ∫v' = 25, find v(6) | `integration_basic.py` P3 `_initial_value_problem` | 3 |
| 10 | Trig differentiation | `derivatives.py` P1 `_trig_basic` | 1 |
| 10 | Trig integration | `integration_basic.py` P1 `_basic_trig` | 1 |
| 11 | a(t) = -cos(πt/4), net change 0→2 | `integration_basic.py` P4 `_definite_usub_trig` | 4 |
| 12 | High order polynomial limits | `limits.py` P1 `_inf_rational`, P3 `_lhopital_basic` | 1, 3 |
| 13 | U-sub: (x+4)(4x-3)^(3/4) dx | `integration_basic.py` P2 `_usub_linear` / `_usub_polynomial` | 2 |

### B2: Partially Implemented — Need Extension

#### #3: Derivative at x=a → classify behavior (asymptote, tangent, undefined)

**Current state:** `derivatives.py` has `_implicit_differentiation` (finds dy/dx for circle, xy, sin(xy)) and `_power_rule`, `_trig_basic`, etc. No problem asks "given f'(a), what does the function have?"

**Action:** Add `_classify_derivative_behavior()` to `derivatives.py` P3.

```
Problem pattern:
  "Given f'(x) = [expression]. At x = a, does f(x) have:
   (a) a horizontal tangent  (b) a vertical tangent  (c) a cusp  (d) undefined?"

Generation:
  - Pick function type: rational (vertical asymptote), absolute value (cusp), smooth (horizontal tangent)
  - Compute f'(a) symbolically
  - If f'(a) = 0 → horizontal tangent
  - If f'(a) undefined (denominator = 0, or |x| at x=0) → vertical tangent or cusp
  - Return answerNorm: "horizontal_tangent" | "vertical_tangent" | "cusp" | "undefined"
```

**Checker:** `check_norm_answer` — string match on classification label.

#### #8: Implicit Differentiation — Tangent Line at Point

**Current state:** `derivatives.py` `_implicit_differentiation()` finds dy/dx for x²+y²=r², xy+y²=7, sin(xy)=x. Does NOT compute tangent line equation.

**Action:** Extend `_implicit_differentiation()` or add `_implicit_tangent_line()` to P4.

```
Problem pattern:
  "Find the equation of the tangent line to [implicit curve] at (x,y) = (a,b)."

Example:
  "Find the tangent line to x·sin(xy - y²) = x² - 1 at (1, 1)."

Generation:
  - Implicit diff: solve for dy/dx at (a,b)
  - Tangent line: y - b = m(x - a) where m = dy/dx|(a,b)
  - answerNorm: "y = m*x + (b - m*a)"  (slope-intercept form)
  - validNorms: ["y-b=m*(x-a)", "y=m*x+c"]  (point-slope and slope-intercept)
```

**Checker:** `check_norm_answer` with `validNorms` for multiple accepted forms.

#### #18: Extended U-Sub Patterns (Nested Trig + Parameterized)

**Extend:** `integration_basic.py` — add `_usub_nested_trig()` to P3 and `_usub_parameterized()` to P4.

Nested trig: ∫cos(x)·sin(sin(x))dx → u=sin(x), du=cos(x)dx
Parameterized: ∫(a+bx⁷)/√(8ax+bx⁸)dx → u=8ax+bx⁸, du=(8a+8bx⁷)dx

```python
def _usub_nested_trig():
    """cos(x)·sin(sin(x))dx → u=sin(x)"""
    # u = sin(x), du = cos(x)dx
    # ∫sin(u) du = -cos(u) + C = -cos(sin(x)) + C
    return {
        "problemTex": f"\\int_0^{{\\pi/2}} \\cos(x) \\sin(\\sin(x)) \\, dx",
        "answerNorm": "-cos(sin(pi/2))+cos(sin(0))",
        "steps": [...],
    }

def _usub_parameterized():
    """∫(a+bx)/√(8ax+bx⁸)dx → u=8ax+bx⁸"""
    a = R(1, 5)
    b = R(1, 5)
    # u = 8ax + bx⁸, du = (8a + 8bx⁷)dx = 8(a + bx⁷)dx
    # (a+bx⁷)dx = du/8
    # ∫(1/8)·u^(-1/2) du = (1/4)·√u + C
    return {
        "problemTex": f"\\int \\frac{{{a} + {b}x^7}}{{\\sqrt{{{8*a}x + {b}x^8}}}} \\, dx",
        "answerNorm": "(1/4)*sqrt(8*a*x+b*x^8)",
        "steps": [...],
    }
```

**Checker:** `check_integration_answer` — strips +C, numeric eval at test points.

#### #19: Particle Motion — Speeding Up / Slowing Down (v·a Sign Analysis)

**Extend:** `integration_basic.py` or new `particle_motion.py` — add `_speeding_up_slowing_down()` to P3.

**Pattern:** Given s(t) (degree 3-4 polynomial), find intervals where particle is speeding up (v·a > 0) vs slowing down (v·a < 0).

**Generation:**
- Pick s(t) = cubic or quartic with 2-3 real critical points
- Compute v(t) = s'(t), a(t) = s''(t)
- Find sign chart for v(t) and a(t)
- Speeding up where signs match, slowing down where they differ
- answerNorm: interval notation, e.g., "(-inf,-2)U(1,3)" for speeding up
- requiresDualAnswer: True (speeding up intervals + slowing down intervals)

**Checker:** `check_dual_answer` — two interval notation strings.

**Example:**
```
s(t) = t³ - 6t² + 9t on [0, 5]
v(t) = 3t² - 12t + 9 = 3(t-1)(t-3)
a(t) = 6t - 12 = 6(t-2)
Speeding up: (0,1) U (3,5)  [v>0,a>0 or v<0,a<0]
Slowing down: (1,3)  [v and a opposite signs]
```

### B3: New Generators Required

#### #1: Optimization Word Problems (Max Volume, Constraints)

**Module:** JSONL template (not .py — per architecture decision DOC_COMPARISON §4)

**File:** `backend/jsonl_templates/calc1_optimization.jsonl`

**Templates:** O1-O15 from Section A above.

**Example JSONL (O3 — open-top box):**

```jsonl
{
  "id": "calc1_opt_003",
  "course": "calc1",
  "topic": "optimization",
  "method": "first_derivative_test",
  "template": "A square-based open-top box is made from {area} cm² of material. Find the dimensions that maximize volume.",
  "variables": {
    "area": {"type": "int", "range": [100, 500]}
  },
  "answer_fn": "(area/5)**0.5",
  "solution_steps": [
    {"label": "Define variables", "math": "x = \\text{base side}, h = \\text{height}", "note": ""},
    {"label": "Constraint", "math": "x^2 + 4xh = {area}", "note": "base + 4 sides"},
    {"label": "Solve for h", "math": "h = \\frac{{{area} - x^2}}{{4x}}", "note": ""},
    {"label": "Volume", "math": "V = x^2 h = x^2 \\cdot \\frac{{{area} - x^2}}{{4x}} = \\frac{x({area} - x^2)}{4}", "note": ""},
    {"label": "Differentiate", "math": "V' = \\frac{{{area} - 3x^2}}{{4}}", "note": "Power rule"},
    {"label": "Set to zero", "math": "{area} - 3x^2 = 0 \\implies x = \\sqrt{{area}/3}", "note": "Critical point"},
    {"label": "Second derivative", "math": "V'' = -\\frac{3x}{2} < 0 \\text{ at } x > 0", "note": "Confirms maximum"},
    {"label": "Find h", "math": "h = \\frac{{{area} - {area}/3}}{{4\\sqrt{{area}/3}}} = \\frac{{area}/3}{2\\sqrt{{area}/3}} = \\frac{\\sqrt{{area}/3}}{2}", "note": ""},
    {"label": "Answer", "math": "x = \\sqrt{{area}/3}, \\quad h = \\frac{\\sqrt{{area}/3}}{2}", "note": "Base side and height"}
  ],
  "contexts": [
    {"skin": "manufacturing", "narrative": "A manufacturer has {area} cm² of sheet metal to form an open-top box with a square base."},
    {"skin": "agriculture", "narrative": "A farmer has {area} cm² of galvanized steel to build an open-top grain bin with a square base."},
    {"skin": "construction", "narrative": "A contractor has {area} cm² of drywall to construct an open-top storage closet with a square floor."}
  ],
  "modes_available": ["solve", "justify", "backwards", "break"],
  "justify_foil": "related_rates",
  "backwards_prompt": "An optimization problem yields a square-based open-top box with base side x = √(A/3) and height h = √(A/3)/2 from A cm² of material. Reconstruct the problem setup.",
  "break_errors": [
    {"type": "skipped_second_derivative_test", "explanation": "Critical point found but not verified as maximum."},
    {"type": "constraint_not_substituted", "explanation": "Set up V = x²h but forgot to eliminate h using the surface area constraint."}
  ],
  "tags": ["optimization", "first_derivative", "box", "square_base"],
  "difficulty": 2
}
```

#### #5: Horizontal/Vertical/Slant Asymptotes

**Module:** `asymptotes.py` (new .py generator — computational, not word problem)

**File:** `backend/generators/asymptotes.py`

**Pools:**

| Pool | Problem Type |
|------|-------------|
| 1 | Horizontal asymptote of rational function (deg numerator < deg denominator → y=0) |
| 2 | Horizontal asymptote (deg num = deg denom → y = ratio of leading coeffs) |
| 3 | Horizontal asymptote (deg num > deg denom → no HA; slant asymptote) |
| 4 | Vertical asymptotes (find where denominator = 0, numerator ≠ 0) |
| 5 | Combined: find all asymptotes (HA + VA + slant) for a rational function |

**Generation pattern:**

```python
def _horizontal_asymptote_equal_deg():
    """deg(num) = deg(denom), HA = leading_coeff_num / leading_coeff_denom"""
    a = R(2, 5)    # leading coeff numerator
    b = R(1, 4)    # leading coeff denominator
    n, d = simplify_frac(a, b)
    deg = R(2, 4)
    # f(x) = (a*x^deg + ...) / (b*x^deg + ...)
    # HA: y = n/d
    return {
        "problemTex": f"\\text{{Find the horizontal asymptote of }} f(x) = \\frac{{{a}x^{{{deg}}} + \\dots}}{{{b}x^{{{deg}}} + \\dots}}",
        "answerTex": f"y = \\frac{{{n}}}{{{d}}}" if d != 1 else f"y = {n}",
        "answerNorm": f"y={n}/{d}" if d != 1 else f"y={n}",
        "steps": [...],
    }
```

**Checker:** `check_norm_answer` — string compare on `y=...` form.

#### #6: Integrate (x^6 + 1)(x^5 + 2) — Expand Then Integrate

**Module:** Extend `integration_basic.py` — add `_expand_then_integrate()` to P2 or P3.

```python
def _expand_then_integrate():
    """Multiply polynomials, then integrate term by term."""
    # (x^m + a)(x^n + b) where m, n ∈ {2,3,4,5,6}
    m = R(3, 6)
    n = R(2, m - 1)  # ensure m > n for variety
    a = R(1, 5)
    b = R(1, 5)
    # Expand: x^(m+n) + b*x^m + a*x^n + a*b
    # Integrate: x^(m+n+1)/(m+n+1) + b*x^(m+1)/(m+1) + a*x^(n+1)/(n+1) + a*b*x + C

    # Build answerNorm
    terms = []
    for exp, coeff in [(m+n+1, 1), (m+1, b), (n+1, a), (1, a*b)]:
        if exp == 1:
            terms.append(f"{coeff}*x")
        else:
            sn, sd = simplify_frac(coeff, exp)
            if sd == 1:
                terms.append(f"{sn}*x^{exp}")
            else:
                terms.append(f"{sn}/{sd}*x^{exp}")
    answer_norm = "+".join(terms)

    return {
        "problemTex": f"\\int (x^{{{m}}} + {a})(x^{{{n}}} + {b}) \\, dx",
        "answerTex": f"\\frac{{x^{{{m+n+1}}}}}{{{m+n+1}}} + {b}\\frac{{x^{{{m+1}}}}}{{{m+1}}} + {a}\\frac{{x^{{{n+1}}}}}{{{n+1}}} + {a*b}x + C",
        "answerNorm": answer_norm,
        "steps": [...],
    }
```

**Checker:** `check_integration_answer` — strips +C, then numeric eval at test points.

#### #7: Bisection Method + Newton's Method

**Module:** `numerical_methods.py` (new .py generator)

**File:** `backend/generators/numerical_methods.py`

**Pools:**

| Pool | Problem Type |
|------|-------------|
| 1 | Bisection: given f(x), interval [a,b], find root after N iterations |
| 2 | Bisection: how many iterations needed for tolerance ε? |
| 3 | Newton's method: given f(x), x₀, compute x₁, x₂ |
| 4 | Newton's method: compare convergence to bisection |
| 5 | Newton's method: find root of f(x) = 0 to 4 decimal places |

**Generation pattern:**

```python
def _bisection_iterations():
    """Apply bisection method for N iterations, report midpoint."""
    # f(x) = x^2 - k (root = sqrt(k))
    k = pick([2, 3, 5, 6, 7, 8, 10])
    a, b = R(0, 2), R(3, 5)  # ensure f(a)*f(b) < 0
    n = R(3, 5)

    # Compute bisection manually
    for _ in range(n):
        mid = (a + b) / 2
        if (mid**2 - k) * (a**2 - k) < 0:
            b = mid
        else:
            a = mid
    final_mid = (a + b) / 2

    return {
        "problemTex": f"\\text{{Use bisection on }} f(x) = x^2 - {k} \\text{{ on }} [{a}, {b}] \\text{{ for }} {n} \\text{{ iterations. Find the midpoint.}}",
        "answerTex": f"\\approx {final_mid:.4f}",
        "answerNorm": f"{final_mid:.4f}",
        "steps": [...],
    }
```

**Checker:** `check_norm_answer` — numeric eval with tolerance 0.01 (bisection is approximate).

#### #14: Increasing/Decreasing Intervals from f'(x)

**Module:** `increasing_decreasing.py` (new .py generator)

**File:** `backend/generators/increasing_decreasing.py`

**Pools:**

| Pool | Problem Type |
|------|-------------|
| 1 | Given f'(x) = polynomial, find where f is increasing (f' > 0) |
| 2 | Given f'(x), find where f is decreasing (f' < 0) |
| 3 | Find critical points, then classify intervals |
| 4 | Given f(x), find increasing/decreasing intervals (requires differentiation first) |
| 5 | Combined: increasing, decreasing, and constant intervals |

**Generation pattern:**

```python
def _increasing_from_derivative():
    """Given f'(x), find intervals where f is increasing."""
    # f'(x) = (x - a)(x - b) where a < b
    a = R(-3, 0)
    b = R(1, 4)
    # f'(x) > 0 when x < a or x > b (parabola opening up)
    # f'(x) < 0 when a < x < b

    return {
        "problemTex": f"f'(x) = (x - ({a}))(x - {b}). \\text{{ Find where }} f(x) \\text{{ is increasing.}}",
        "answerTex": f"(-\\infty, {a}) \\cup ({b}, \\infty)",
        "answerNorm": f"(-inf,{a})U({b},inf)",
        "steps": [...],
    }
```

**Checker:** `check_norm_answer` — interval notation string compare.

#### #15: Global/Local Min/Max from Graph

**Module:** `extrema.py` (new .py generator)

**File:** `backend/generators/extrema.py`

**Pools:**

| Pool | Problem Type |
|------|-------------|
| 1 | Find local max/min from f'(x) sign chart |
| 2 | Find absolute max/min on closed interval [a, b] |
| 3 | Given graph description, identify local/global extrema |
| 4 | Second derivative test: classify critical points |
| 5 | Word problem: maximize/minimize quantity, find global optimum |

**Generation pattern:**

```python
def _absolute_extrema_closed_interval():
    """Find absolute max/min of f(x) on [a, b]."""
    # f(x) = x^3 - 3x on [-2, 2]
    # f'(x) = 3x^2 - 3 = 0 → x = ±1
    # Evaluate f(-2), f(-1), f(1), f(2)

    a = R(-3, -1)
    b = R(1, 3)
    # f(x) = x^3 - 3x
    vals = {
        a: a**3 - 3*a,
        -1: 2,
        1: -2,
        b: b**3 - 3*b,
    }
    abs_max = max(vals.values())
    abs_min = min(vals.values())

    return {
        "problemTex": f"\\text{{Find the absolute maximum and minimum of }} f(x) = x^3 - 3x \\text{{ on }} [{a}, {b}].",
        "answerTex": f"\\text{{max}} = {abs_max}, \\quad \\text{{min}} = {abs_min}",
        "answerNorm": f"max={abs_max},min={abs_min}",
        "requiresDualAnswer": True,
        "answerNorm2": f"{abs_min}",
        "answerTex2": f"{abs_min}",
        "steps": [...],
    }
```

**Checker:** `check_norm_answer` with `requiresDualAnswer` → `check_dual_answer`.

#### #16: Car Deceleration / Distance Traveled

**Module:** JSONL template (word problem) or extend `integration_basic.py`

**File:** `backend/generators/integration_basic.py` — add `_constant_acceleration_distance()` to P3

```python
def _constant_acceleration_distance():
    """Car decelerating at rate a, initial velocity v0. Find stopping distance."""
    v0 = R(20, 60)  # m/s
    a = R(2, 8)     # m/s² deceleration

    # v(t) = v0 - a*t
    # Stop when v(t) = 0 → t = v0/a
    # Distance = ∫₀^(v0/a) (v0 - a*t) dt = v0²/(2a)
    dist = v0**2 / (2 * a)
    sn, sd = simplify_frac(int(v0**2), 2 * a)

    return {
        "problemTex": f"\\text{{A car traveling at }} {v0} \\text{{ m/s decelerates at }} {a} \\text{{ m/s². Find the stopping distance.}}",
        "answerTex": f"\\frac{{{sn}}}{{{sd}}} \\text{{ m}}" if sd != 1 else f"{sn} \\text{{ m}}",
        "answerNorm": f"{sn}/{sd}" if sd != 1 else f"{sn}",
        "steps": [
            {"label": "Velocity function", "math": f"v(t) = {v0} - {a}t", "note": ""},
            {"label": "Time to stop", "math": f"v(t) = 0 \\implies t = \\frac{{{v0}}}{{{a}}}", "note": ""},
            {"label": "Distance", "math": f"d = \\int_0^{{{v0}/{a}}} ({v0} - {a}t) \\, dt", "note": ""},
            {"label": "Integrate", "math": f"d = \\left[{v0}t - \\frac{{{a}}}{{2}}t^2\\right]_0^{{{v0}/{a}}}", "note": ""},
            {"label": "Evaluate", "math": f"d = {v0}\\cdot\\frac{{{v0}}}{{{a}}} - \\frac{{{a}}}{{2}}\\cdot\\frac{{{v0}^2}}{{{a}^2}} = \\frac{{{v0}^2}}{{2{a}}}", "note": ""},
            {"label": "Answer", "math": f"d = \\frac{{{sn}}}{{{sd}}} \\text{{ m}}", "note": ""}
        ],
    }
```

**Checker:** `check_norm_answer` — numeric eval at test points.

#### #17: Mean Value Theorem

**Module:** `mvt.py` (new .py generator)

**File:** `backend/generators/mvt.py`

**Pools:**

| Pool | Problem Type |
|------|-------------|
| 1 | Verify MVT conditions for f(x) on [a, b] |
| 2 | Find c such that f'(c) = (f(b) - f(a))/(b - a) |
| 3 | MVT for specific function (polynomial, trig, exponential) |
| 4 | Rolle's Theorem: find c where f'(c) = 0 given f(a) = f(b) |
| 5 | Word problem: MVT interpretation (average vs instantaneous rate) |

**Generation pattern:**

```python
def _find_c_mvt_polynomial():
    """Find c satisfying MVT for a polynomial on [a, b]."""
    a = R(0, 2)
    b = R(3, 5)
    # f(x) = x^2
    # f'(x) = 2x
    # MVT: f'(c) = (f(b) - f(a))/(b - a) = (b² - a²)/(b - a) = b + a
    # 2c = b + a → c = (b + a)/2
    c = (b + a) / 2

    return {
        "problemTex": f"\\text{{Find }} c \\text{{ satisfying the Mean Value Theorem for }} f(x) = x^2 \\text{{ on }} [{a}, {b}].",
        "answerTex": f"c = {c}",
        "answerNorm": f"{c}",
        "steps": [
            {"label": "Compute f(b) - f(a)", "math": f"f({b}) - f({a}) = {b}^2 - {a}^2 = {b**2 - a**2}", "note": ""},
            {"label": "Average rate", "math": f"\\frac{{f({b}) - f({a})}}{{{b} - {a}}} = \\frac{{{b**2 - a**2}}}{{{b - a}}} = {b + a}", "note": ""},
            {"label": "Set f'(c) equal", "math": f"f'(c) = 2c = {b + a}", "note": ""},
            {"label": "Solve", "math": f"c = \\frac{{{b + a}}}{{2}} = {c}", "note": ""}
        ],
    }
```

**Checker:** `check_norm_answer` — numeric eval with tolerance 0.001.

#### #18: Newton's Method — Fixed Points, Extrema, Secant Method

**Module:** Extend `numerical_methods.py` or create `newton_extensions.py`

**New patterns discovered from OpenStax 4.9:

| Pool | Problem Type |
|------|-------------|
| 1 | Newton's method to find **fixed points** (f(x) = x, not f(x)=0) — e.g. cos(x), sin(x), e^x − 2 |
| 2 | Apply Newton to **f'(x)** to locate local minima/maxima |
| 3 | **Secant method** iterations (alternative to Newton, requires two guesses) |
| 4 | Compare Newton vs secant convergence on same root |
| 5 | Starting-point sensitivity: predict behavior (divergence, cycle, unexpected root) |

**Checker:** `check_norm_answer` with float tolerance 0.01 for iterations; string match for behavior prediction.

#### #19: Indeterminate Forms Beyond 0/0 and ∞/∞

**Module:** Extend `limits.py` — add `_indeterminate_forms()` to P4/P5, or new `indeterminate_forms.py`

**Patterns from OpenStax 4.8:

| Pool | Problem Type |
|------|-------------|
| 1 | `0 · ∞` form — rewrite as quotient, then L'Hôpital |
| 2 | `∞ − ∞` form — combine fractions, then L'Hôpital |
| 3 | `1^∞` form — let y = f(x)^g(x), take ln, rewrite as `∞·0` |
| 4 | `∞^0` form — same logarithmic rewrite technique |
| 5 | `0^0` form — same logarithmic rewrite technique |

**Checker:** `check_norm_answer` — numeric eval after rewriting.

#### #20: Epsilon-Delta Proofs — Limit Existence AND Non-Existence

**Module:** `epsilon_delta.py` (new .py generator, fill-in-the-blank / proof mode)

**Patterns from OpenStax 2.5:

| Pool | Problem Type |
|------|-------------|
| 1 | Find δ given ε for linear function (straightforward algebra) |
| 2 | Find δ given ε for quadratic (geometric + algebraic approach) |
| 3 | Prove limit **does not exist** using negation of ε-δ definition |
| 4 | Prove limit DNE for **ceiling/floor function** at integer points |
| 5 | Rational vs irrational piecewise — prove limit DNE at non-zero points |

**Checker:** `check_norm_answer` per blank slot; `validNorms` for equivalent algebraic expressions.

#### #21: Special / Transcendental Functions — Catenary, Hyperbolic, Arc Length

**Module:** `hyperbolic_apps.py` (new .py generator)

**Patterns from OpenStax 6.4, 6.9:

| Pool | Problem Type |
|------|-------------|
| 1 | Arc length of catenary `y = a·cosh(x/a)` over given interval |
| 2 | Area under catenary / arc length ratio (invariant discovery) |
| 3 | Surface area of revolution for `y = 1/x` (Gabriel's Horn setup) |
| 4 | Work with catenary rope / anchor drag (real-world hyperbolic context) |
| 5 | Simplify expressions like `sinh(ln x)`, `cosh(ln x)` into algebraic form |

**Checker:** `check_norm_answer` for algebraic simplifications; `check_integration_answer` for +C strip on arc-length antiderivatives.

#### #22: Center of Mass — Generalized, Wire, Pappus, Composite Regions

**Module:** `center_of_mass.py` (new .py generator)

**Patterns from OpenStax 6.6:

| Pool | Problem Type |
|------|-------------|
| 1 | Generalized COM between `y = x^a` and `y = x^b` (symbolic exponents), then Pappus volume |
| 2 | COM of a **thin wire along a curve** (e.g. semicircle `y = √(1−x²)`) |
| 3 | Composite region COM (multiple subregions: rectangles + semicircular annulus) |
| 4 | Pappus theorem: volume of torus from revolving a disk |
| 5 | Variable density rod / disk (linear or radial density function) |

**Checker:** `check_norm_answer` for coordinate pairs; `check_dual_answer` for `(x̄, ȳ)`.

#### #23: Construct-a-Function / Reverse Engineering

**Module:** `function_construction.py` (new .py generator)

**Patterns from OpenStax 4.6:

| Pool | Problem Type |
|------|-------------|
| 1 | Construct rational function with given horizontal and vertical asymptotes |
| 2 | Construct function with given slant (oblique) asymptote |
| 3 | Given graph features (roots, asymptotes, critical points), write possible formula |
| 4 | Build logistic growth model from carrying capacity and initial condition |

**Checker:** `check_norm_answer` with `validNorms` (non-unique answers).

### B4: Proof / Derive Mode (Fill-in-the-Blank)

#### #25: Riemann Sum Proof — ∫ₐ x dx from Definition

**Type:** Fill-in-the-blank proof, not computational generator.

**Pattern:** Prove ∫ₐ x dx = (b²-a²)/2 by expanding the Riemann sum definition step-by-step. 7 blank slots.

**Implementation:** Static template with fill-in-the-blank slots. Frontend renders as multi-input problem (like WebAssign proof mode).

**Example structure:**
```
∫ₐᵇ x dx = lim(n→∞) (b-a)/n · Σ[a + (b-a)/n · i]
         = lim(n→∞) [ a(b-a)/n · Σ(1) + (b-a)²/n² · Σ(i) ]
         = lim(n→∞) [ a(b-a)/n · n + (b-a)²/n² · n(n+1)/2 ]
         = a(b-a) + lim(n→∞) [ (b-a)²/2 · (n+1)/n ]
         = a(b-a) + (b-a)²/2
         = (b-a)(a + (b-a)/2)
         = (b-a)(a + b/2 - a/2)
         = (b-a)(a/2 + b/2)
         = (b-a)·(a+b)/2
         = (b² - a²)/2
```

**Checker:** `check_norm_answer` per slot — string match on expected algebraic expression. `validNorms` for equivalent forms.

#### #27: Concavity & Rate-of-Rate Word Problems

**Module:** JSONL templates (per architecture decision DOC_COMPARISON §4)

**File:** `backend/jsonl_templates/calc1_concavity.jsonl`

**Templates:** CA1-CA4 from Section A above.

**Example JSONL (CA1 — rate increasing/decreasing):**
```jsonl
{
  "id": "calc1_conc_001",
  "course": "calc1",
  "topic": "concavity",
  "method": "second_derivative_sign_analysis",
  "template": "The {context} is modeled by r(t) = {coeff1}t³ + {coeff2}t² + {coeff3}t + {const}. On the interval [{a}, {b}], when is the rate increasing and when is it decreasing?",
  "variables": {
    "coeff1": {"type": "int", "range": [-2, 2]},
    "coeff2": {"type": "int", "range": [-5, 5]},
    "coeff3": {"type": "int", "range": [-10, 10]},
    "const": {"type": "int", "range": [0, 100]},
    "a": {"type": "int", "range": [0, 2]},
    "b": {"type": "int", "range": [5, 10]}
  },
  "answer_fn_increasing": "solve(r'(t) > 0 on [a,b])",
  "answer_fn_decreasing": "solve(r'(t) < 0 on [a,b])",
  "solution_steps": [
    {"label": "Define rate function", "math": "r(t) = {coeff1}t^3 + {coeff2}t^2 + {coeff3}t + {const}", "note": ""},
    {"label": "Differentiate", "math": "r'(t) = {3*coeff1}t^2 + {2*coeff2}t + {coeff3}", "note": "Power rule"},
    {"label": "Find critical points", "math": "r'(t) = 0 \\implies t = \\text{[solve quadratic]}", "note": "Quadratic formula"},
    {"label": "Sign chart", "math": "Test r'(t) in each interval", "note": "Pick test points"},
    {"label": "Increasing intervals", "math": "r'(t) > 0 \\text{ on } \\text{[interval notation]}", "note": ""},
    {"label": "Decreasing intervals", "math": "r'(t) < 0 \\text{ on } \\text{[interval notation]}", "note": ""},
    {"label": "Interpret", "math": "\\text{Rate is increasing on } \\text{[inc]}, \\text{ decreasing on } \\text{[dec]}", "note": "Context interpretation"}
  ],
  "contexts": [
    {"skin": "manufacturing", "narrative": "A factory's production rate"},
    {"skin": "agriculture", "narrative": "A crop's growth rate"},
    {"skin": "oil_gas", "narrative": "An oil well's output rate"},
    {"skin": "government", "narrative": "A city's population growth rate"},
    {"skin": "mining", "narrative": "A mine's ore extraction rate"}
  ],
  "requiresDualAnswer": true,
  "answerNorm2_slot": "decreasing_intervals",
  "modes_available": ["solve", "justify", "backwards"],
  "justify_foil": "optimization",
  "tags": ["concavity", "second_derivative", "rate_analysis", "interval_notation"],
  "difficulty": 3
}
```

**Example JSONL (CA2 — inflection point):**
```jsonl
{
  "id": "calc1_conc_002",
  "course": "calc1",
  "topic": "concavity",
  "method": "inflection_point",
  "template": "The {context} follows the model P(t) = \\frac{{{L}}}{{1 + {A}e^{{-{k}t}}}}. When does the growth rate start to decelerate? (Find the inflection point.)",
  "variables": {
    "L": {"type": "int", "range": [1000, 10000]},
    "A": {"type": "int", "range": [5, 50]},
    "k": {"type": "float", "range": [0.1, 0.5]}
  },
  "answer_fn": "ln(A)/k",
  "solution_steps": [
    {"label": "Model", "math": "P(t) = \\frac{{{L}}}{{1 + {A}e^{{-{k}t}}}}", "note": "Logistic growth"},
    {"label": "First derivative", "math": "P'(t) = \\frac{{{L}{A}{k}e^{{-{k}t}}}}{{(1 + {A}e^{{-{k}t}})^2}}", "note": "Chain + quotient rule"},
    {"label": "Second derivative", "math": "P''(t) = \\frac{{{L}{A}{k}^2 e^{{-{k}t}}({A}e^{{-{k}t}} - 1)}}{{(1 + {A}e^{{-{k}t}})^3}}", "note": "Quotient rule again"},
    {"label": "Set to zero", "math": "P''(t) = 0 \\implies {A}e^{{-{k}t}} = 1", "note": "Numerator = 0"},
    {"label": "Solve", "math": "e^{{-{k}t}} = \\frac{{1}}{{{A}}} \\implies -{k}t = \\ln\\left(\\frac{{1}}{{{A}}}\\right) \\implies t = \\frac{{\\ln({A})}}{{{k}}}", "note": ""},
    {"label": "Interpret", "math": "\\text{Growth rate is highest at } t = \\frac{{\\ln({A})}}{{{k}}}", "note": "Before this point, growth accelerates; after, it decelerates"}
  ],
  "contexts": [
    {"skin": "agriculture", "narrative": "A bacterial culture in a petri dish"},
    {"skin": "government", "narrative": "A city's population"},
    {"skin": "oil_gas", "narrative": "Oil extraction from a new well"},
    {"skin": "manufacturing", "narrative": "Adoption of a new manufacturing technology"}
  ],
  "modes_available": ["solve", "justify", "derive"],
  "tags": ["inflection", "logistic", "second_derivative", "concavity"],
  "difficulty": 4
}
```

**Checker:** `check_dual_answer` for CA1 (two interval strings). `check_norm_answer` for CA2/CA3/CA4 (scalar or interval).

---

## SECTION C — IMPLEMENTATION ORDER

### Phase 0: Refactor (Days 1-2)
1. Remove `/api/problem/smart` dead alias
2. Create `backend/module_config.py` — single source for MODULES dict + UNLOCK_CHAIN
3. Create `backend/checker_registry.py` — module→checker map
4. Create `backend/problem_builder.py` — `problem()`, `dual_problem()`, `step()` factories
5. Create test suite: `backend/tests/`
6. Migrate 10 existing generators to use `problem()`/`step()` builders

### Phase 1: Algebra Modules (Days 3-7)
9 new modules, all .py generators with POOLS 1-5:

| Module | Topics | Tier |
|--------|--------|------|
| `linear_eqns` | ax+b=c, multi-step, word problems | 0 |
| `graphing` | slope, intercepts, y=mx+b, parallel/perp | 0 |
| `inequalities` | linear, absolute value, quadratic sign | 0 |
| `systems` | 2x2 substitution/elimination, word problems | 0 |
| `poly_ops` | add/sub/mul/div polynomials, synthetic division | 0 |
| `rational_expr` | simplify, multiply, divide, add/sub rational expressions | 0 |
| `radicals` | simplify, add/sub, multiply, divide, rationalize | 0 |
| `quadratics` | solve by factoring, quadratic formula, complete square | 0 |
| `functions` | f(x) notation, evaluate, domain, composition, inverse | 0 |

All tier 0 (immediately unlocked). Each uses `check_norm_answer` except `quadratics` (needs `validNorms` for factored vs formula form).

---

## SECTION C-1 — PHASE 1 ALGEBRA DETAIL

Based on textbook scan of *Beginning and Intermediate Algebra* by Tyler Wallace (489 pages, 10 chapters + Pre-Algebra).

### Module: `linear_eqns`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | One-step equations (addition, subtraction, multiplication, division) | 40 |
| 2 | Two-step equations (ax+b=c, x/a+b=c) | 40 |
| 3 | General linear equations (variables on both sides, distribute, combine like terms) | 50 |
| 4 | Equations with fractions (clear fractions via LCD) | 30 |
| 5 | Special cases — identity (all real numbers) vs contradiction (no solution) | 15 |

**Word problem sub-types:**
- Number/geometry: consecutive integers, triangle angles, rectangle perimeter
- Age: now/future/past table method, sum given now, "how many years until"
- Distance/rate/time: rt=d, opposite directions, catch-up, total time given

**Edge cases:**
- Variables subtract out completely → identity or contradiction
- Equations with no lone variable (must isolate and use fractions)

### Module: `graphing`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Plotting points, coordinate plane, quadrants | 20 |
| 2 | Finding slope from graph or two points | 40 |
| 3 | Slope-intercept form (identify m and b, convert to, graph from) | 42 |
| 4 | Point-slope form (write equation given point and slope, convert to slope-intercept) | 52 |
| 5 | Parallel and perpendicular lines (find slope, write equation through point) | 48 |

**Edge cases:**
- Undefined slope (vertical line) vs zero slope (horizontal line)
- Perpendicular to vertical line → horizontal line (y = constant)

### Module: `inequalities`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Linear inequalities (solve, graph, interval notation) | 38 |
| 2 | Compound OR inequalities | 15 |
| 3 | Compound AND inequalities | 15 |
| 4 | Three-part inequalities (a < x < b) | 15 |
| 5 | Absolute value inequalities (< becomes AND, > becomes OR) | 35 |

**Edge cases:**
- No overlap of intervals → no solution (∅)
- Full overlap of intervals → all real numbers (R)
- Absolute value < negative number → no solution
- Absolute value > negative number → all real numbers

### Module: `systems`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Graphing method (find intersection, identify parallel/same line) | 30 |
| 2 | Substitution method (lone variable, isolate, substitute) | 40 |
| 3 | Addition/elimination (multiply to get opposites, add, solve) | 34 |
| 4 | Three variables (reduce to two, solve ordered triplets) | 32 |
| 5 | Word problems — value (coins, tickets, stamps) and mixture (solutions, investments) | 35 |

**Edge cases:**
- Parallel lines → no solution (∅)
- Same line → infinite solutions
- No lone variable in substitution → must solve for variable with fractions
- Three-variable systems with special cases (true statement = infinite, false = no solution)

### Module: `poly_ops`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Exponent properties (product, quotient, power rules) | 30 |
| 2 | Negative exponents and scientific notation | 45 |
| 3 | Multiply polynomials (monomial × polynomial, FOIL) | 40 |
| 4 | Special products (difference of squares, perfect square trinomials) | 40 |
| 5 | Divide polynomials (by monomial, long division, missing terms) | 44 |

**Edge cases:**
- Long division with missing terms → must add 0x² placeholder
- Division result with fractional coefficients
- Special products: cannot get a² + b² from real multiplication

### Module: `rational_expr`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Reduce rational expressions (factor numerator and denominator, cancel) | 20 |
| 2 | Multiply and divide rational expressions | 44 |
| 3 | Find LCD and build up denominators | 30 |
| 4 | Add and subtract rational expressions | 30 |
| 5 | Complex fractions and solve rational equations | 35 |

**Edge cases:**
- LCD with repeated factors (e.g., (x-5)² and (x-5)(x-9))
- Extraneous solutions when solving rational equations
- Complex fractions with multiple operations requiring full factorization

### Module: `radicals`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Square roots (simplify, perfect squares) | 20 |
| 2 | Higher roots (cube, 4th, nth roots) | 15 |
| 3 | Add/subtract and multiply/divide radicals | 45 |
| 4 | Rationalize denominators (single term, binomial conjugate) | 25 |
| 5 | Rational exponents and complex numbers | 45 |

**Edge cases:**
- Mixed index radicals → convert to rational exponents first
- Complex number division → multiply by conjugate
- Rationalizing binomial denominators with i

### Module: `quadratics`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Solve with square roots (isolate squared term, take ±√) | 20 |
| 2 | Solve with quadratic formula | 25 |
| 3 | Complete the square | 20 |
| 4 | Build quadratic from roots | 15 |
| 5 | Quadratic in form (substitute u = xⁿ, solve, back-substitute) | 20 |

**Word problem sub-types:**
- Rectangles, teamwork, revenue, distance

**Edge cases:**
- Quadratic in form: x⁴ - 5x² + 4 = 0 → u = x²
- Must check all solutions in original equation for rational/radical equations

### Module: `functions`

| Pool | Problem Type | Count Est. |
|------|-------------|-----------|
| 1 | Function notation (f(x), evaluate, domain) | 20 |
| 2 | Operations on functions (add, subtract, multiply, divide) | 15 |
| 3 | Inverse functions (find inverse, verify f(f⁻¹(x)) = x) | 15 |
| 4 | Exponential and logarithmic functions | 30 |
| 5 | Trigonometric and inverse trig functions | 25 |

**Edge cases:**
- Compound interest: solve for time t requires logarithms
- Inverse trig restricted domains

### Algebra Textbook Coverage Summary

| Module | Estimated Problems in Textbook | Templates Needed for Generator |
|--------|-------------------------------|-------------------------------|
| `linear_eqns` | 200+ | 30-40 |
| `graphing` | 150+ | 25-30 |
| `inequalities` | 100+ | 20-25 |
| `systems` | 150+ | 25-30 |
| `poly_ops` | 150+ | 20-25 |
| `rational_expr` | 150+ | 25-30 |
| `radicals` | 100+ | 20-25 |
| `quadratics` | 150+ | 25-30 |
| `functions` | 100+ | 15-20 |
| **Total** | **~1,250+** | **~200-250** |

---

### Phase 2: Calc Gaps + Word Problems (Days 8-14)

#### 2a: Extend existing generators
- `derivatives.py`: add `_classify_derivative_behavior()` (P3), `_implicit_tangent_line()` (P4)
- `integration_basic.py`: add `_expand_then_integrate()` (P2), `_constant_acceleration_distance()` (P3), `_usub_nested_trig()` (P3), `_usub_parameterized()` (P4)
- `integration_basic.py` or `particle_motion.py`: add `_speeding_up_slowing_down()` (P3)

#### 2b: New .py generators
| File | Topics | Pools |
|------|--------|-------|
| `asymptotes.py` | HA, VA, slant asymptotes | 1-5 |
| `increasing_decreasing.py` | f'(x) sign analysis, intervals | 1-5 |
| `extrema.py` | local/global min/max, second derivative test | 1-5 |
| `numerical_methods.py` | bisection, Newton's method | 1-5 |
| `mvt.py` | Mean Value Theorem, Rolle's Theorem | 1-5 |
| `concavity_word.py` or JSONL | rate increasing/decreasing, inflection, rate-of-rate | 1-4 |
| `epsilon_delta.py` | ε-δ proofs (existence + non-existence), ceiling/floor, rational/irrational | 1-5 |
| `indeterminate_forms.py` | L'Hôpital for `0·∞`, `∞−∞`, `1^∞`, `∞^0`, `0^0` | 1-5 |
| `hyperbolic_apps.py` | Catenary arc length, Gabriel's Horn, hyperbolic simplifications | 1-5 |
| `center_of_mass.py` | Generalized COM, wire COM, Pappus, composite regions | 1-5 |
| `function_construction.py` | Build function from asymptotes, slant asymptote, graph features | 1-4 |

#### 2c: JSONL word problem templates
| File | Templates | Topics |
|------|-----------|--------|
| `calc1_optimization.jsonl` | O1-O27 (27 templates) | Optimization |
| `calc1_related_rates.jsonl` | R1-R10 (10 templates) | Related Rates |
| `calc1_particle_motion.jsonl` | K1-K8 (8 templates) | Kinematics |
| `calc1_ftc.jsonl` | F1-F6 (6 templates) | FTC / Net Change |
| `calc1_area_volume.jsonl` | AV1-AV12 (12 templates) | Area / Volume |
| `calc1_linear_approx.jsonl` | LA1-LA4 (4 templates) | Linear Approximation |
| `calc1_work.jsonl` | W1-W5 (5 templates) | Work Applications |
| `calc1_numerical.jsonl` | NI1 (1 template) | Numerical Integration |
| `calc1_trig_eqns.jsonl` | TE1 (1 template) | Trig Equations |
| `calc1_trig_integration.jsonl` | TI1 (1 template) | Trig Integration |
| `calc1_concavity.jsonl` | CA1-CA4 (4 templates) | Concavity & Acceleration |

**Total: 79 word problem templates**

Each template includes:
- `variables` with ranges
- `answer_fn` expression
- `solution_steps` (10+ entries)
- `contexts` (3+ skins from 75-skin bank)
- `modes_available`, `justify_foil`, `backwards_prompt`, `break_errors`
- `tags`, `difficulty`

### Phase 3: JSONL Engine + Frontend (Days 15-18)
1. `backend/jsonl_engine.py` — load, fill, skin, session build, mode wrap
2. `backend/skins.json` — 75 industry narratives
3. `backend/foil_table.py` — justify foil lookup
4. `backend/derive_library.py` — static derive problems
5. Frontend mode UI: `math265-modes.html` (justify/backwards/break/derive inputs)
6. Frontend core changes: skin badge, mode indicator, word problem badge

### Phase 4: Integration + Testing (Days 19-21)
1. All new generators produce valid shapes
2. All checkers dispatch correctly
3. JSONL templates validate through pipeline
4. Full user test session: 20 problems in "All" mode
5. No regression on existing functionality

---

## SECTION D — CHECKER DISPATCH MAP (UPDATED)

After all gaps filled, the full checker registry:

| Module | Checker | Notes |
|--------|---------|-------|
| `factoring` | `check_factoring_answer` | Uses `originalExpanded` |
| `exponents` | `check_exponent_answer` | Handles fractional exponents |
| `fractions` | `check_fraction_answer` | Cross-multiply, float tol |
| `trig` | `check_norm_answer` | Unit circle, identities |
| `logs` | `check_norm_answer` | Expand/condense/solve |
| `composition` | `check_norm_answer` | f(g(x)), domain, inverse |
| `limits` | `check_norm_answer` | Direct sub, L'Hôpital, sequences |
| `derivatives` | `check_norm_answer` | All diff rules, implicit |
| `integration` | `check_integration_answer` | Strips +C |
| `adv_integration` | `check_integration_answer` | Strips +C |
| `linear_eqns` | `check_norm_answer` | Scalar answer |
| `graphing` | `check_norm_answer` | Slope, intercepts |
| `inequalities` | `check_norm_answer` | Interval notation |
| `systems` | `check_norm_answer` | Scalar pair |
| `poly_ops` | `check_norm_answer` | Polynomial result |
| `rational_expr` | `check_norm_answer` | Simplified expression |
| `radicals` | `check_norm_answer` | Simplified radical |
| `quadratics` | `check_norm_answer` | `validNorms` for multiple forms |
| `functions` | `check_norm_answer` | Scalar/string answer |
| `asymptotes` | `check_norm_answer` | `y=...` form |
| `increasing_decreasing` | `check_norm_answer` | Interval notation |
| `extrema` | `check_norm_answer` | Dual answer (max + min) |
| `numerical_methods` | `check_norm_answer` | Float tolerance 0.01 |
| `mvt` | `check_norm_answer` | Float tolerance 0.001 |
| `epsilon_delta` | `check_norm_answer` | `validNorms` per slot; symbolic normalization |
| `indeterminate_forms` | `check_norm_answer` | Numeric eval after rewrite |
| `hyperbolic_apps` | `check_norm_answer` / `check_integration_answer` | `trigsimp()` + `simplify()` |
| `center_of_mass` | `check_dual_answer` | `(x̄, ȳ)` coordinate pair |
| `function_construction` | `check_norm_answer` | `validNorms` for non-unique answers |
| `word_problems` (JSONL) | `check_norm_answer` | Scalar result |

---

## SECTION E — VERIFICATION COMMANDS

For each new generator:

```bash
# Test generator returns valid shape
python -c "from generators.asymptotes import POOLS; import random; print(random.choice(POOLS[2])())"

# Test checker dispatch
python -c "from checker import check_norm_answer; print(check_norm_answer({'answerNorm': 'y=3/2'}, 'y=3/2', 'asymptotes'))"

# Test JSONL template validates
python -c "from jsonl_engine import validate_template; print(validate_template({...}))"

# Full integration test
python -c "
from generators.extrema import POOLS
from checker import check_norm_answer
p = random.choice(POOLS[2])()
result = check_norm_answer(p, p['answerNorm'], 'extrema')
print(result)
"
```

---

## SECTION G — RISK REGISTER

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | JSONL engine complexity (parse, eval, skin, mode, decoy) | High | Build incrementally: parse→fill→skin→mode→decoy. Test each stage. |
| 2 | 79 templates × 5 modes = heavy authoring load | High | LLM batch-generate templates. Human review top 10 per category. Prioritize O22–O27, AV8–AV12, W3–W5 first. |
| 3 | Frontend splitting breaks existing 3318-line SPA | High | Additive split via `<script src>`. Existing code unchanged. Test after each fragment. |
| 4 | Numerical methods checker tolerance too strict/loose | Medium | Test with known bisection/Newton instances. Adjust tolerance per method. |
| 5 | Asymptote answer format ambiguous (y=3 vs 3) | Medium | `validNorms` list covers both forms. |
| 6 | Interval notation parsing fragile | Medium | Standardize: `(-inf,a)U(b,inf)` as answerNorm. Frontend displays LaTeX. |
| 7 | MVT c-value may not be unique (multiple c satisfy) | Medium | Choose functions where c is unique (quadratic on [a,b]). |
| 8 | Extrema dual-answer checker needs both max AND min correct | Medium | `check_dual_answer` calls `check_norm_answer` twice, returns `wrongSlot`. |
| 9 | Speeding up/slowing down interval notation parsing fragile | Medium | Standardize: `(-inf,a)U(b,c)U(d,inf)`. Frontend displays LaTeX union notation. Dual-answer checker handles two interval strings. |
| 10 | Epsilon-delta proof grading fragile (many equivalent algebraic forms) | Medium | `validNorms` per blank slot + symbolic normalization via SymPy (`simplify()`). Allow factored/expanded equivalents. |
| 11 | Function construction answers non-unique (many correct rational functions) | Medium | `validNorms` list or symbolic equivalence check. Accept any function satisfying given asymptotes/features. |
| 12 | Hyperbolic/catenary answer normalization complex (`sinh(ln x)` → `(x²−1)/(2x)`) | Medium | Use SymPy `simplify()` + `trigsimp()` in checker pipeline. Test against multiple equivalent forms. |
| 13 | Gabriel's Horn / improper integral checker needs ∞ handling | Medium | Return `"diverges"` or `"undefined"` as `answerNorm`. Numeric fallback disabled; string match only. |
| 14 | Newton fixed-point / secant method problems have multiple valid iteration paths | Low | Specify exact number of iterations and starting value(s). Checker evaluates final numeric value with tolerance. |

---

*Generated April 30, 2026. Based on DOC_COMPARISON.md §5 (JSONL Schema), §7 (Skins + Anti-Pattern-Matching), MASTER_BUILD_PLAN.md, EXPANSION_PLAN.md, LINEAR 123 CALC 123.md.*
