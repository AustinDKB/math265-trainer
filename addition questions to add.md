# Algebra trainer spec — addendum: trainers 4-11

Extends `ALGEBRA_TRAINER_SPEC.md`. Same tech stack, design system, UX patterns, and localStorage schema. Each trainer is a new module tab in the same app.

---

## Trainer 4: Trig unit circle values

### Purpose
Instant recall of sin, cos, tan at standard angles. No derivation, no thinking — automatic. This is rote memory, not understanding. Drill until reflexive.

### Problem types

| Type | Prompt | Answer pool | Difficulty |
|---|---|---|---|
| sin(angle) | `sin(π/6) = ?` | 0, 1/2, √2/2, √3/2, 1, and negatives | 1 |
| cos(angle) | `cos(2π/3) = ?` | same pool | 1 |
| tan(angle) | `tan(π/4) = ?` | 0, 1, √3, 1/√3, undefined, and negatives | 2 |
| Inverse: angle from value | `sin(θ) = √3/2, θ in [0,π]. θ = ?` | standard angles | 2 |
| Mixed: identify quadrant sign | `sin(5π/4) is positive/negative?` | positive, negative | 1 |
| Radians ↔ degrees | `Convert 5π/6 to degrees` | multiples of 30° and 45° | 1 |
| Pythagorean identity | `If sin(θ) = 3/5 and θ in Q1, find cos(θ)` | generated via Pythagorean triples | 3 |
| Double angle | `sin(2θ) if sin(θ)=a, cos(θ)=b` | from known angle values | 3 |
| Reciprocal functions | `csc(π/6) = ?` | reciprocals of standard values | 2 |

### Angle pool (all problems draw from this)

```
Radians:  0, π/6, π/4, π/3, π/2, 2π/3, 3π/4, 5π/6, π,
          7π/6, 5π/4, 4π/3, 3π/2, 5π/3, 7π/4, 11π/6, 2π
Degrees:  0, 30, 45, 60, 90, 120, 135, 150, 180,
          210, 225, 240, 270, 300, 315, 330, 360
```

### Generation algorithm

```
1. Pick random angle from pool
2. Pick sin/cos/tan
3. Look up exact value from hardcoded table
4. For difficulty 3: generate Pythagorean triple (3,4,5), (5,12,13), 
   (8,15,17), (7,24,25) → sin = opp/hyp, cos = adj/hyp
```

### Answer validation
- Accept `sqrt(3)/2`, `√3/2`, `\frac{\sqrt{3}}{2}`, `0.866` (with tolerance)
- Accept `pi/6`, `π/6`, `30` (degrees, if mode is degrees)
- For "undefined": accept `undefined`, `undef`, `DNE`, `∞`

### Special UX: visual unit circle
- Show a unit circle diagram alongside the problem
- Highlight the angle being asked about
- After answering, show the point on the circle with coordinates
- Optional toggle: "show reference triangle" overlay

### KaTeX rendering
```latex
\sin\left(\frac{\pi}{6}\right) = \text{?}
```

---

## Trainer 5: Log rules

### Purpose
Mechanical application of logarithm properties. Required for log differentiation, integration of 1/x forms, and growth/decay models.

### Problem types

| Type | Template | Parameters | Difficulty |
|---|---|---|---|
| Product rule | `ln(ab) = ?` | a,b symbolic or numeric | 1 |
| Quotient rule | `ln(a/b) = ?` | a,b symbolic or numeric | 1 |
| Power rule | `ln(x^n) = ?` | n ∈ {2..8} | 1 |
| Expand expression | `ln(x³y²/z)` → `3ln(x) + 2ln(y) − ln(z)` | random exponents | 2 |
| Condense expression | `3ln(x) + 2ln(y) − ln(z)` → `ln(x³y²/z)` | reverse of above | 2 |
| Solve for x | `ln(x) = 3` → `x = e³` | small integers | 2 |
| Solve exponential | `e^(2x) = 7` → `x = ln(7)/2` | random coefficients | 2 |
| Change of base | `log_a(b) = ln(b)/ln(a)` | a ∈ {2,3,5,10}, b random | 2 |
| Nested | `ln(e^(f(x)))` → `f(x)` | f(x) from function pool | 3 |
| Combined with exponents | `e^(3ln(x))` → `x³` | exponent ∈ {1..6} | 3 |
| Log differentiation setup | `Rewrite y = x^x using ln` → `ln(y) = x·ln(x)` | various f(x)^g(x) | 3 |

### Generation algorithm

```
For expand/condense:
  1. Pick 2-3 variables from {x, y, z, a, b}
  2. Assign random exponents ∈ {1..5}
  3. Randomly assign to numerator or denominator
  4. Build the compact form (answer for condense, problem for expand)
  5. Build the expanded form (answer for expand, problem for condense)

For solve problems:
  1. Pick the answer first: x = e^(a/b) or x = ln(a)/b
  2. Build the equation backward
```

### Answer validation
- Accept `ln(x)`, `log(x)` (treated as natural log in calc context), `log_e(x)`
- Accept `e^3`, `e³`, `exp(3)`
- For condensed forms: expand both user answer and stored answer, compare

---

## Trainer 6: Function composition

### Purpose
Decompose nested functions into outer/inner for chain rule. If you can't see f(g(x)) structure on sight, chain rule can't start.

### Problem types

| Type | Prompt | Parameters | Difficulty |
|---|---|---|---|
| Identify outer/inner | Given `sin(x²)`, name f and g | function pool | 1 |
| Compute f(g(x)) | Given f(x)=x², g(x)=sin(x), find f(g(x)) | function pool | 1 |
| Compute g(f(x)) | Same functions, reversed | function pool | 1 |
| Decompose | Given `e^(cos(x))`, write as f(g(x)) | function pool | 2 |
| Three-layer decompose | Given `sin(ln(x²))`, write as f(g(h(x))) | function pool | 2 |
| Evaluate | f(x)=2x+1, g(x)=x², find f(g(3)) | numeric | 1 |
| Build from description | "Square it, then take sin" → sin(x²) | word descriptions | 2 |
| Domain of composition | f(x)=√x, g(x)=x−3, domain of f(g(x))? | requires solving inequality | 3 |
| Multi-compose | f∘g∘h with three functions | function pool | 3 |

### Function pool (all compositions draw from this)

```python
FUNCTIONS = [
    ("x²", lambda x: x**2),
    ("x³", lambda x: x**3),
    ("√x", lambda x: sqrt(x)),
    ("sin(x)", lambda x: sin(x)),
    ("cos(x)", lambda x: cos(x)),
    ("tan(x)", lambda x: tan(x)),
    ("eˣ", lambda x: exp(x)),
    ("ln(x)", lambda x: log(x)),
    ("1/x", lambda x: 1/x),
    ("x+a", lambda x: x+a),  # a = random int
    ("ax", lambda x: a*x),    # a = random int
    ("|x|", lambda x: abs(x)),
]
```

### Answer validation
- For decomposition: multiple valid answers exist. 
  - `sin(x²)`: f=sin(u), g=x² OR f=sin(u²), g=x — accept any valid decomposition
  - Verify by composing user's f and g, comparing to original
- For evaluation: exact numeric match

---

## Trainer 7: Limits

### Purpose
Pattern match limit technique, execute it cleanly. The midterm tested this directly.

### Problem types

| Type | Template | Generation | Difficulty |
|---|---|---|---|
| Direct substitution | `lim(x→a) polynomial` | random poly, a ∈ {-5..5} | 1 |
| 0/0 factor cancel | `lim(x→a) (x²−a²)/(x−a)` | a ∈ {1..8}, extend to cubics | 1 |
| 0/0 rationalize | `lim(x→a) (√x−√a)/(x−a)` | a ∈ perfect squares {1,4,9,16} | 2 |
| x→∞ rational | `lim(x→∞) (ax^n+...)/(bx^m+...)` | random coeffs, vary n vs m | 1 |
| sin(kx)/(mx) | `lim(x→0) sin(kx)/(mx)` | k,m ∈ {1..7} | 2 |
| (1−cos(kx))/x² | `lim(x→0) (1−cos(kx))/x²` | k ∈ {1..5} | 2 |
| tan(kx)/sin(mx) | `lim(x→0) tan(kx)/sin(mx)` | k,m ∈ {1..7} | 2 |
| Difference quotient | `lim(h→0) [f(x+h)−f(x)]/h` | f from function pool | 3 |
| L'Hôpital basic | `lim(x→0) (eˣ−1−x)/x²` | generated e/ln/trig combos | 3 |
| L'Hôpital repeated | problems requiring 2 applications | carefully constructed | 3 |
| Piecewise continuity | is f continuous at x=a? | random piecewise definitions | 3 |
| Squeeze theorem | bound f between known limits | template-based | 3 |

### Generation algorithm

```
For factor/cancel (the most important type):
  1. Pick a ∈ {1..8}
  2. Pick the CANCELLED form: e.g., (x + a) = answer
  3. Multiply top and bottom by (x − a) to create 0/0
  4. Problem: [(x+a)(x−a)] / (x−a) = (x²−a²)/(x−a)
  5. Limit value: 2a

For trig limits:
  1. Pick k, m
  2. Answer is always k/m (for sin(kx)/(mx)) or k²/2 (for (1−cos(kx))/x²)
  3. Build problem from template

For L'Hôpital:
  1. Pick f(x) and g(x) such that f(a)=0 and g(a)=0
  2. Compute f'(a)/g'(a) — that's the answer
  3. If still 0/0, compute f''(a)/g''(a)
  4. Store number of L'Hôpital applications needed
```

### Step templates

```
Direct sub: [Try plugging in] → [Compute] → [Answer]
Factor:     [Try plugging in → 0/0] → [Factor numerator] → [Cancel] → [Sub] → [Answer]
Rationalize:[Try → 0/0] → [Multiply conjugate] → [Simplify] → [Cancel] → [Sub] → [Answer]
Trig:       [Try → 0/0] → [Rewrite toward sin(u)/u] → [Apply known limit] → [Answer]
L'Hôpital:  [Try → 0/0] → [Differentiate top] → [Differentiate bottom] → [Try again] → [Answer]
```

---

## Trainer 8: Derivative computation

### Purpose
Apply all derivative rules at speed. This is the mechanical core of the final exam.

### Problem types

| Type | Template | Generation | Difficulty |
|---|---|---|---|
| Power rule | `d/dx [ax^n]` | a ∈ {1..10}, n ∈ {-3..8}, including fractions | 1 |
| Trig basic | `d/dx [sin(x)]`, `d/dx [cos(x)]`, `d/dx [tan(x)]` | pick from 6 trig functions | 1 |
| Exponential | `d/dx [e^x]`, `d/dx [a^x]` | a ∈ {2,3,5,10} | 1 |
| Logarithmic | `d/dx [ln(x)]`, `d/dx [log_a(x)]` | a ∈ {2,3,10} | 1 |
| Sum/difference | `d/dx [f(x) ± g(x)]` | f,g from basic pool | 1 |
| Product rule | `d/dx [f(x)·g(x)]` | f,g from function pool | 2 |
| Quotient rule | `d/dx [f(x)/g(x)]` | f,g from function pool | 2 |
| Chain rule (single) | `d/dx [f(g(x))]` | f,g from function pool | 2 |
| Chain rule (nested) | `d/dx [f(g(h(x)))]` | three functions composed | 3 |
| Product + chain | `d/dx [x²·sin(3x)]` | combos | 3 |
| Quotient + chain | `d/dx [e^(2x)/(x²+1)]` | combos | 3 |
| Implicit differentiation | `x² + y² = r²`, find dy/dx | various implicit curves | 3 |
| Logarithmic differentiation | `y = x^x`, find dy/dx | f(x)^g(x) forms | 3 |
| Higher-order | `find f''(x)` | differentiate twice | 3 |

### Generation algorithm

```
1. Pick difficulty → pick type
2. Draw functions from pool (same pool as composition trainer)
3. Apply symbolic differentiation rules to compute answer:
   - Power: ax^n → anx^(n-1)
   - Product: fg → f'g + fg'
   - Quotient: f/g → (f'g - fg')/g²
   - Chain: f(g(x)) → f'(g(x))·g'(x)
4. Store unsimplified and simplified forms
5. Generate step-by-step showing which rule at each stage
```

### Symbolic differentiation engine

The generator needs a basic symbolic math system. Represent expressions as trees:

```
Expression types:
  Const(n)          → derivative = 0
  Var("x")          → derivative = 1
  Add(a, b)         → derivative = a' + b'
  Mul(a, b)         → derivative = a'b + ab'
  Div(a, b)         → derivative = (a'b - ab') / b²
  Pow(base, exp)    → derivative = exp · base^(exp-1) · base' (if exp is const)
  Sin(a)            → derivative = cos(a) · a'
  Cos(a)            → derivative = -sin(a) · a'
  Exp(a)            → derivative = exp(a) · a'
  Ln(a)             → derivative = a'/a
```

This is the most complex engineering in the app. Build it as a separate module. Test it independently against known derivatives before integrating.

### Answer validation
- For derivatives: expand and compare both user answer and computed answer
- Accept equivalent forms: `2x·cos(x²)` = `cos(x²)·2x`
- Accept unsimplified if mathematically correct
- Flag "correct but simplify further" when appropriate

---

## Trainer 9: Basic integration

### Purpose
Reverse the derivative. Power rule antiderivatives + u-substitution.

### Problem types

| Type | Template | Generation | Difficulty |
|---|---|---|---|
| Power rule | `∫ ax^n dx` | a ∈ {1..8}, n ∈ {-3..6} (n≠-1) | 1 |
| 1/x | `∫ 1/x dx` | always ln|x| + C | 1 |
| e^x | `∫ e^(ax) dx` | a ∈ {1..5} | 1 |
| Basic trig | `∫ sin(x) dx`, `∫ cos(x) dx` | 6 standard trig | 1 |
| Sum/difference | `∫ [f(x) ± g(x)] dx` | basic terms | 1 |
| U-sub (linear) | `∫ f(ax+b) dx` | a,b random | 2 |
| U-sub (polynomial) | `∫ x·f(x²) dx` | inner = x², x³, etc | 2 |
| U-sub (trig) | `∫ sin(x)·cos(x) dx` | various trig combos | 2 |
| U-sub (exp) | `∫ x·e^(x²) dx` | inner = x², 2x+1, etc | 2 |
| Definite integrals | `∫ from a to b of f(x) dx` | compute numeric answer | 3 |
| Rewrite then integrate | `∫ √x dx`, `∫ 1/x³ dx` | needs exponent rewriting | 2 |
| Initial value problem | `f'(x) = ..., f(a) = b, find f(x)` | basic + solve for C | 3 |

### Generation algorithm — THE BACKWARD TRICK

```
This is the key insight: generate integration problems BACKWARD.

1. Pick a function F(x) — this is the ANSWER
2. Differentiate F(x) to get f(x) — this is the PROBLEM
3. The problem is: ∫ f(x) dx
4. The answer is: F(x) + C

This guarantees every problem has a clean antiderivative.

Example:
  Pick F(x) = (2x+1)⁵ / 10
  Differentiate: f(x) = (2x+1)⁴ · 2 / 10 = (2x+1)⁴ / 5
  Problem: ∫ (2x+1)⁴/5 dx → but present as: (1/5)∫(2x+1)⁴ dx
  Answer: (2x+1)⁵/10 + C ← guaranteed clean
```

### U-substitution step template

```
Step 1: "Identify u"         → u = [inner function]
Step 2: "Compute du"         → du = [inner derivative] dx
Step 3: "Rewrite integral"   → ∫ [expression in u] du
Step 4: "Integrate"          → [antiderivative in u] + C
Step 5: "Substitute back"    → [answer in x] + C
```

### Answer validation
- Must include `+ C` for indefinite integrals (warn if missing)
- Accept equivalent forms after expansion
- For definite integrals: numeric comparison with tolerance ε = 0.001

---

## Trainer 10: Integration techniques (advanced)

### Purpose
Integration by parts, trig substitution, partial fractions. Typically 20-30% of a Calc II final, but some appear in late Calc I.

### Problem types

| Type | Template | Generation | Difficulty |
|---|---|---|---|
| By parts (basic) | `∫ x·e^x dx`, `∫ x·sin(x) dx` | pick u and dv from pools | 1 |
| By parts (repeated) | `∫ x²·e^x dx` | requires 2 applications | 2 |
| By parts (circular) | `∫ e^x·sin(x) dx` | solve-for-I technique | 3 |
| Trig identity | `∫ sin²(x) dx`, `∫ cos²(x) dx` | half-angle formula | 2 |
| Trig powers | `∫ sin^m(x)·cos^n(x) dx` | m,n ∈ {1..4} | 2 |
| Partial fractions (distinct) | `∫ 1/[(x−a)(x−b)] dx` | a,b distinct integers | 2 |
| Partial fractions (repeated) | `∫ 1/(x−a)² dx` | a random | 2 |
| Partial fractions (quadratic) | `∫ 1/(x²+a²) dx` | a ∈ {1..5} → arctan | 3 |
| Trig substitution | `∫ √(a²−x²) dx` | a ∈ {1..6} | 3 |
| Combination | requires recognizing which technique to use | mixed | 3 |

### Generation algorithm

```
Integration by parts:
  1. Pick u from {x, x², x³, ln(x), arctan(x)}
  2. Pick dv from {e^(ax)dx, sin(bx)dx, cos(bx)dx}
  3. Compute du and v
  4. Apply ∫u·dv = u·v − ∫v·du
  5. If ∫v·du requires another by-parts, recurse (max depth 2)
  6. Store all steps

Partial fractions (backward generation):
  1. Pick the DECOMPOSITION: A/(x−a) + B/(x−b)
  2. Choose A, B ∈ {1..5}, a,b ∈ {-5..5}, a≠b
  3. Combine into single fraction — that's the problem
  4. Answer: A·ln|x−a| + B·ln|x−b| + C
```

---

## Trainer 11: Application word problems (template system)

### Architecture

```
┌─────────────────────────┐
│ Template JSON file       │ ← generated by LLM once, stored forever
│ 50-70 templates          │
├─────────────────────────┤
│ Parameter generator      │ ← runtime, picks valid random numbers
├─────────────────────────┤
│ Symbolic answer computer │ ← computes answer from formula + params
├─────────────────────────┤
│ KaTeX renderer           │ ← displays problem + step-by-step
└─────────────────────────┘
```

### Template schema

```json
{
  "id": "string",
  "category": "optimization | related_rates | area_between | volume_revolution | linear_approx | mean_value",
  "difficulty": 1 | 2 | 3,
  "title": "Fence around a field",
  "narrative": "A farmer has {P} meters of fencing to enclose a rectangular field along a river (no fence on the river side). Find the dimensions that maximize the enclosed area.",
  "params": {
    "P": {
      "min": 40,
      "max": 200,
      "step": 10,
      "type": "int",
      "unit": "meters"
    }
  },
  "constraints": {
    "description": "P must be divisible by 4 for clean answer"
  },
  "variables": {
    "x": "width of field (perpendicular to river)",
    "y": "length of field (parallel to river)"
  },
  "setup_equations": [
    "2x + y = {P}",
    "A = x · y"
  ],
  "solution_steps": [
    {
      "label": "Express y in terms of x",
      "math": "y = {P} - 2x",
      "note": "From the constraint equation"
    },
    {
      "label": "Write area as function of x",
      "math": "A(x) = x({P} - 2x) = {P}x - 2x^2",
      "note": "Substitute y"
    },
    {
      "label": "Differentiate",
      "math": "A'(x) = {P} - 4x",
      "note": "Power rule"
    },
    {
      "label": "Set derivative to zero",
      "math": "{P} - 4x = 0 \\implies x = {P}/4 = {P_div_4}",
      "note": "Critical point"
    },
    {
      "label": "Find y",
      "math": "y = {P} - 2({P_div_4}) = {P_div_2}",
      "note": ""
    },
    {
      "label": "Verify maximum",
      "math": "A''(x) = -4 < 0 \\implies \\text{maximum}",
      "note": "Second derivative test"
    },
    {
      "label": "Answer",
      "math": "x = {P_div_4}\\text{ m}, \\quad y = {P_div_2}\\text{ m}, \\quad A = {A_max}\\text{ m}^2",
      "note": ""
    }
  ],
  "computed_values": {
    "P_div_4": "P / 4",
    "P_div_2": "P / 2",
    "A_max": "P * P / 8"
  },
  "answer_formula": "x = P/4, y = P/2, A = P²/8",
  "answer_display": "Dimensions: {P_div_4} m × {P_div_2} m, Maximum area: {A_max} m²",
  "diagram_type": "rectangle_river",
  "tags": ["optimization", "quadratic", "second_derivative_test"]
}
```

### Template categories and counts

#### Optimization (20 templates)

```
ID   Scenario                                    Params
───  ──────────────────────────────────────────  ──────────────────
O1   Fence along river (3-sided rectangle)       P = perimeter
O2   Fence (4-sided rectangle, fixed perimeter)  P
O3   Open-top box from sheet (cut corners)       W, L of sheet
O4   Closed box, fixed volume, min surface area  V
O5   Cylinder: min surface for given volume      V
O6   Two pens sharing a wall                     P, num pens
O7   Printed page: max print area with margins   W, L, margin size
O8   Distance from point to curve                point coords, curve
O9   Revenue maximization (linear demand)        base price, base qty, slope
O10  Cost minimization (production)              fixed, variable, demand
O11  Shortest ladder over wall                   wall height, gap distance
O12  Cheapest pipeline (cross river + along)     river width, land dist, water/land cost
O13  Inscribe rectangle in parabola              parabola params
O14  Inscribe rectangle in circle                radius
O15  Inscribe cylinder in sphere                 sphere radius
O16  Cone with max volume inscribed in sphere    sphere radius
O17  Window: rectangle + semicircle, max area    perimeter
O18  Poster: fixed print area, min total area    print area, margins
O19  Fold corner of page to opposite edge        page dims
O20  Minimum travel time (swim + walk)           distances, speeds
```

#### Related rates (15 templates)

```
ID   Scenario                                    Params
───  ──────────────────────────────────────────  ──────────────────
R1   Conical tank filling                        H, R, flow rate
R2   Spherical balloon inflating                 inflation rate
R3   Ladder sliding down wall                    ladder length, slide rate
R4   Shadow length (walking away from lamp)      lamp height, walk speed
R5   Two ships diverging                         speeds, initial distances
R6   Circular oil spill expanding                area growth rate
R7   Water draining from inverted cone           H, R, drain rate
R8   Angle of elevation (approaching plane)      altitude, ground speed
R9   Expanding rectangle                         length rate, width rate
R10  Spotlight on wall (rotating beacon)         distance, rotation speed
R11  Filling trough (triangular cross-section)   dims, flow rate
R12  Kite flying (string angle)                  wind speed, string length
R13  Expanding ripple (circular wave)            radius rate
R14  Person walking on circle, shadow on wall    circle radius, walk speed
R15  Draining hemisphere                         radius, drain rate
```

#### Area between curves (10 templates)

```
ID   Scenario                                    Params
───  ──────────────────────────────────────────  ──────────────────
A1   Two polynomials (linear + quadratic)        coefficients
A2   Polynomial and x-axis                       roots
A3   Two quadratics                              coefficients
A4   Trig + horizontal line                      trig func, line height
A5   Exponential + horizontal line               exp params, line
A6   Two trig functions                          sin/cos combos
A7   Polynomial + abs value                      simple polynomial, abs
A8   Between cubic and linear                    coefficients
A9   √x and x² (standard)                       scaling params
A10  Enclosed region requiring 2 integrals       generated from crossings
```

#### Volume of revolution (10 templates)

```
ID   Scenario                                    Params
───  ──────────────────────────────────────────  ──────────────────
V1   Disk method: y=f(x) around x-axis           simple f(x), bounds
V2   Disk method: x=f(y) around y-axis           simple f(y), bounds
V3   Washer method: two curves around x-axis     two functions, bounds
V4   Washer method: around y-axis                two functions
V5   Shell method: around y-axis                 f(x), bounds
V6   Shell method: around x-axis                 f(y), bounds
V7   Around line y=k (not axis)                  f(x), k, bounds
V8   Around line x=k (not axis)                  f(x), k, bounds
V9   Known cross-sections (squares)              base curve, bounds
V10  Known cross-sections (semicircles)          base curve, bounds
```

#### Linear approximation (5 templates)

```
ID   Scenario                                    Params
───  ──────────────────────────────────────────  ──────────────────
L1   √(a) near perfect square                    a near 1,4,9,16,25
L2   ³√(a) near perfect cube                     a near 1,8,27,64
L3   sin(a) near standard angle                  a near 0,π/6,π/4,π/3
L4   e^a near 0                                  small a
L5   (1+x)^n near x=0                            n rational, small x
```

### Template parameter filling

```python
def fill_template(template):
    params = {}
    for name, spec in template["params"].items():
        value = random_in_range(spec["min"], spec["max"], spec["step"])
        params[name] = value
    
    # Compute derived values
    for name, formula in template["computed_values"].items():
        params[name] = eval_formula(formula, params)
    
    # Validate constraints
    if not check_constraints(template["constraints"], params):
        return fill_template(template)  # retry
    
    # Fill narrative
    narrative = template["narrative"].format(**params)
    
    # Fill steps
    steps = []
    for step in template["solution_steps"]:
        steps.append({
            "label": step["label"],
            "math": step["math"].format(**params),
            "note": step["note"]
        })
    
    return { "narrative": narrative, "steps": steps, "params": params }
```

### Constraint validation

Every template must specify constraints that prevent degenerate problems:

```json
"constraints": {
  "rules": [
    "P > 0",
    "P % 4 == 0",
    "A_max > 0",
    "P_div_4 is integer"
  ],
  "max_retries": 10
}
```

If 10 random parameter sets all fail constraints, log a warning and skip that template.

### Diagram system (optional, high-value)

Each template specifies a `diagram_type`. The app includes a diagram renderer that draws a schematic for the problem using SVG. Pre-built diagram types:

```
rectangle_river     — rectangle with one side labeled "river"
rectangle_box       — 3D box with labeled dimensions
cylinder            — cylinder with r and h labeled
cone                — cone with r and h labeled
triangle_ladder     — right triangle with ladder, wall, ground
circle_inscribed    — shape inscribed in circle
two_curves_shaded   — two curves with shaded area between
solid_of_revolution — curve with rotation arrow
shadow_lamp         — stick figure, lamp, shadow
ships_diverging     — two arrows from common origin
```

Each diagram type is a parameterized SVG function that takes the problem's params and draws the appropriate figure.

---

## LLM template generation prompt

Use this prompt to batch-generate templates. Run once, save output as JSON, never call LLM again at runtime.

```
Generate [N] word problem templates for calculus students in JSON format.

Category: [optimization / related_rates / area_between / volume_revolution]

Each template must include:
- A realistic narrative with parameter placeholders in {braces}
- Parameter specifications with min, max, step, and type
- Constraints that ensure clean numeric answers
- Solution steps with {placeholder} math expressions
- A computed_values section with formulas for derived quantities
- An answer_formula using the parameter names
- A diagram_type string

Rules:
- Every answer must evaluate to a clean number (integer or simple fraction)
- Parameters must be constrained so no division by zero is possible
- Steps must show the complete solution method
- Narratives must be concise (2-3 sentences max)
- Vary the scenarios — don't repeat the same physical setup

Output only valid JSON array. No explanation.
```

---

## Combined "Exam sim" mode (uses all trainers)

### Configuration
- 20 or 30 problems
- Time limit: 60 or 90 minutes
- Problem distribution mirrors typical Calc I final:

```
Module                    Count (20-problem sim)    Count (30-problem sim)
────────────────────────  ───────────────────────   ─────────────────────
Limits                    3                          4
Derivative computation    6                          9
Integration (basic)       4                          6
Integration (techniques)  2                          3
Application (word)        3                          5
Mixed algebra cleanup     2                          3
```

### Scoring
- Each problem weighted equally
- Partial credit: show step count reached before wrong answer
- Final report: accuracy by module, weakest areas, time per problem

---

## Build order for Claude Code

```
Phase   What to build                              Depends on
─────   ─────────────────────────────────────────   ──────────
  1     Expression tree + symbolic differentiator   Nothing
  2     Problem generators for trainers 4-6         Phase 1
  3     Problem generators for trainers 7-8         Phase 1
  4     Problem generators for trainers 9-10        Phase 1
  5     Template JSON for trainer 11                LLM prompt
  6     Template filler + renderer for trainer 11   Phase 5
  7     Exam sim mode                               All above
  8     Stats dashboard expansion                   Phase 7
```

Phase 1 (expression tree) is the load-bearing wall. Everything else depends on it. Get this right and tested before proceeding.

---

## Testing requirements

For each trainer, before shipping:
1. Generate 50 problems at each difficulty level
2. Verify all KaTeX renders without errors
3. Verify all answers are mathematically correct
4. Verify answer validation accepts equivalent forms
5. Verify no degenerate problems (div by zero, imaginary numbers, unsolvable)
6. For word problems: verify all constraints produce clean answers
7. Time the generation: must be < 100ms per problem