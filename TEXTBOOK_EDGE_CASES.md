# Edge Case & Weird Questions from OpenStax Calculus Volume 1

Scanned 31 text chunks (769 pages). Below are genuinely unusual, edge-case, or non-standard exercises that would make good advanced problem-generator targets.

---

## 1. LIMITS — Precise Definition / Epsilon-Delta (Chapter 2)

**Q200** (p.180) — Prove a limit does **not** exist using the precise definition.
> *Edge case: Most exercises ask to prove a limit exists; this asks for a formal non-existence proof.*

**Q201** (p.180) — Using precise definitions, prove that `lim f(x)` DNE, given `f(x)` is the **ceiling function**.
> *Edge case: Discontinuous everywhere (jump discontinuities). Requires choosing epsilon strategically. Explicitly mentions ceiling function — rare in standard textbooks.*

**Q202** (p.180) — Prove `lim f(x)` DNE for a function where you can **always choose a rational number**...
> *Edge case: Rational/irrational argument construction.*

**Q203** (p.180) — Determine `lim f(x)` for `f(x) = { ... }` (hint: break into x rational and x irrational).
> *Edge case: Dirichlet-like piecewise function. Two different formulas depending on rationality.*

**Q204** (p.181) — Using the function from Q203, use the precise definition to show `lim f(x)` DNE for `a ≠ 0`.
> *Edge case: Same rational/irrational function, now proving non-existence at arbitrary non-zero points.*

---

## 2. LIMITS / CONTINUITY — Piecewise & Unusual Discontinuities

**Q226–227** (p.185) — Determine value of `c` such that piecewise function remains continuous; **draw** resulting function.
> *Edge case: Requires matching one-sided limits at the boundary and visual verification.*

**Q173–175** (p.168) — Prove functions are continuous everywhere. Q175: `Where is f(x) = ... continuous?`
> *Edge case: One question asks "where" instead of "prove everywhere" — domain-restriction thinking.*

---

## 3. DERIVATIVES — Non-Differentiable Points / Cusps

**Section 4.6 Example 4.31** (p.377) — Sketch `f(x) = x^(2/3)`; show it has a **cusp** at `x = 0`.
> *Edge case: One-sided derivatives are infinite with opposite signs. Vertical tangent vs cusp distinction.*

**Q41–44** (Section 3.1) — Use limit definition to show derivative **does not exist** at `x = 0` for given functions.
> *Edge case: Standard generator usually produces "find the derivative"; these require proving non-differentiability.*

---

## 4. OPTIMIZATION — Unusual Geometric Constraints (Chapter 4.7)

**Q341** (p.393) — Find volume of largest right circular **cylinder that fits in a sphere** of radius r.
> *Edge case: Constraint is an inscribed solid, not a perimeter/fencing problem.*

**Q342** (p.393) — Find volume of largest right **cone that fits in a sphere**.
> *Edge case: Similar inscribed-solid constraint, but cone geometry changes the algebra significantly.*

**Q343** (p.393) — Find area of largest **rectangle that fits into a triangle** with sides a=4, b=3, c=5.
> *Edge case: Right-triangle inscribed rectangle; requires similar-triangle setup before calculus.*

**Q344** (p.393) — Find largest volume of a **cylinder that fits into a cone** with base radius R and height h.
> *Edge case: Nested solids with linear scaling constraint via similar triangles.*

**Q345** (p.393) — Find dimensions of closed cylinder with **volume V that has least surface area**.
> *Edge case: Fixed volume, minimize surface area — classic, but the closed-top constraint changes the formula.*

**Q346** (p.393) — Find dimensions of a right **cone with surface area S that has the largest volume**.
> *Edge case: Inverted optimization (fixed surface area, maximize volume) with cone geometry and slant height.*

**Q347–350** (p.393) — Distance from point to curve minimization:
- `y = 4x + 7` closest to origin
- `y = 4x + 7` closest to point `(1, 2)`
- `y = x²` closest to point `(2, 1)`
- `y = x²` closest to point `(1, 3)`
> *Edge case: Minimizing distance (square-root constraint) rather than simple function value. Requires distance formula setup.*

**Q351** (p.394) — Window composed of **semicircle on top of rectangle**; maximize window area given perimeter constraint.
> *Edge case: Composite shape optimization. Two variables linked by perimeter, area involves circle + rectangle.*

**Q352** (p.394) — Watermelon plants: 30 plants produce 25 watermelons each. For each **additional plant**, output per plant drops by 1. How many extra to plant?
> *Edge case: Discrete optimization disguised as calculus problem. Product `(30+x)(25-x)` is quadratic, but x must be integer.*

**Q353** (p.394) — Cat box: square bottom costs $5/ft², sides cost $2/ft²; need volume 8 ft³. Minimize cost.
> *Edge case: **Different costs for different surfaces** — not uniform material price.*

**Q354** (p.394) — Five **identical pens adjacent to each other** with total area 1000 m². Minimize fencing.
> *Edge case: Multiple adjacent rectangles create a non-standard perimeter formula (6 widths + 2 lengths).* 

**Q355** (p.394) — Apartment complex: 50 units, rent $1000 → all rented. Each $50 increase → 1 fewer rented. Maintenance $100/occupied unit. Maximize profit.
> *Edge case: Revenue and cost both depend on occupancy, which depends on price. Non-objective quadratic.*

---

## 5. L'HÔPITAL'S RULE — Indeterminate Forms & Growth Rates (Chapter 4.8)

**Q289–293** (p.380) — Graph and estimate horizontal asymptote / limit, then calculate actual limit.
> *Edge case: Technology + analytical confirmation. Functions include `x^(1/x)`, `x^(1/x²)`, `x·ln(x)`, etc.*

**Q285–288** (p.379) — **Construct a function** that has given asymptotes.
> *Edge case: Reverse engineering a rational function from asymptote specifications. Non-unique answer, requires structural understanding.*

**Section 4.8 Examples 4.41–4.44** — Indeterminate forms `0·∞`, `∞−∞`, `1^∞`, `∞^0`.
> *Edge case: Not just 0/0 or ∞/∞. Requires rewriting before applying L'Hôpital. Good generator candidates.*

---

## 6. NEWTON'S METHOD — Edge Cases & Extensions (Chapter 4.9)

**Q446–448** (p.430) — Use Newton's method to find **fixed points** of `f(x) = cos(x)`, `sin(x)`, `e^x − 2`.
> *Edge case: Finding fixed points (where `f(x) = x`) rather than roots (where `f(x) = 0`).*

**Q449–454** (p.430) — Use Newton's method to find **local minima/maxima** by applying it to `f'(x)`.
> *Edge case: Newton on the derivative, not the original function. Requires student to set up `f'(x)=0` first.*

**Q455–458** (p.430) — **Secant method** exercises (alternative to Newton's method).
> *Edge case: Different iterative formula. Requires two initial guesses instead of one.*

**Q460–463** (p.430) — "Use Newton's method to find the first two iterations, given the starting point."
> *Edge case: Some starting points lead to divergence, cycles, or convergence to unexpected roots. Good for "predict the behavior" questions.*

---

## 7. INTEGRATION APPLICATIONS — Gabriel's Horn & Paradoxes (Chapter 6.4)

**Q217** (p.593) — Explain why the **surface area is infinite** when `y = 1/x` is rotated around the x-axis for `[1, ∞)`, **but the volume is finite**.
> *Edge case: **Gabriel's Horn** (Torricelli's trumpet). Classic paradox. Requires improper integrals and comparison. Answer key explicitly says "look up Gabriel's Horn."*

**Q212** (p.593) — Find exact arc length of `y = ln(cos x)` from `0` to `π/4`.
> *Edge case: Trig identity required inside the arc-length integral (`sec x`).*

**Q213** (p.593) — Draw graphs of `y = x^n` for `n = 1, 2, 3`. Predict arc length from `(0,0)` to `(1,1)` as n increases. Compute and check.
> *Edge case: Comparative arc length. Counterintuitive that higher power curves can be shorter or longer depending on region.*

**Q214** (p.593) — Compare lengths of parabola `y = x²` and line `y = x` from `0` to `1` as parameter changes.
> *Edge case: Parametric comparison — which curve is longer?*

**Q215** (p.593) — Solve arc length of `y = (x−1)^(3/2)` from `1` to `2`. Show `y = x^(3/2)` from `0` to `1` is twice as long. Explain why.
> *Edge case: Same curve shape, different interval scaling produces exact factor of 2. Requires insight about arc-length scaling.*

**Q216** (p.593) — Which is longer between `(1,1)` and `(2,2)`: hyperbola `y = 1/x` or graph of `y = ln x`?
> *Edge case: Comparing arc lengths of two different transcendental functions over same interval.*

---

## 8. PHYSICAL APPLICATIONS — Non-Standard Geometry (Chapter 6.5)

**Q207** (p.592) — Base of lamp: revolve quarter-circle `y = √(r² − x²)` around x-axis. Create integral and compute surface area.
> *Edge case: Surface area of a spherical cap / hemisphere from explicit formula.*

**Q208** (p.592) — Light bulb is sphere radius 2 in with bottom sliced off to fit onto cylinder radius 1 in, length 3 in. Find surface area (not including cylinder top/bottom).
> *Edge case: Composite solid of revolution with a **flat cutoff** — requires finding the exact circle-rectangle intersection before revolving.*

**Q209** (p.593) — Lampshade: rotate `y = 1/x` around x-axis from `x=1` to `x=2`. Find surface area.
> *Edge case: Surface area of revolution for `1/x` — leads to messy but integrable form.*

**Q210** (p.593) — Anchor drags according to `y = 24·cosh(x/24) − 24`. Anchor is 18 ft below boat; how much rope to pull?
> *Edge case: **Catenary** (hyperbolic cosine) in a real-world context. Arc length of catenary.*

**Q211** (p.593) — Bridge rope in shape of `y = 10·sin(πx/50)`. Span 50 ft. Find rope length; round up to whole feet.
> *Edge case: Sinusoidal arc length. Requires numerical approximation (or elliptic integral in general, though this one simplifies).* 

**Q220** (p.597) — Work done **lifting a 20 kg child from the floor to 0.4 m**.
> *Edge case: Basic work, but note says "a mass of 1 kg weighs 9.8 N" — units confusion trap.*

**Q221** (p.597) — Work done pushing box along floor 2 m with constant force of 25 N at 30° angle.
> *Edge case: Work with **angled force** (`W = F·d·cos θ`). Most textbook problems use force parallel to motion.*

---

## 9. CENTERS OF MASS / PAPPUS — Generalized & Unusual Regions (Chapter 6.6)

**Q290** (p.625) — Find **generalized center of mass** in the sliver between `y = x^a` and `y = x^b` with `a > b`. Then use Pappus theorem to find volume of solid generated revolving around y-axis.
> *Edge case: **Symbolic / parameterized** center of mass. Requires general formula in terms of exponents a and b. Then Pappus application.*

**Q291–292** (p.625) — Similar generalized center of mass between `y = x^a` and `y = x^b` for specific exponent pairs, then Pappus volume.
> *Edge case: Same as above with specific values. Tests symbolic integration and Pappus theorem together.*

**Q293** (p.625) — Use theorem of Pappus to find volume of a **torus**. Disk radius r positioned with left end at `x = R` rotated around y-axis.
> *Edge case: Classic torus via Pappus. Good for verifying shell-method result by a different path.*

**Q294** (p.625) — Find center of mass for a **thin wire along the semicircle** `y = √(1−x²)` with unit mass. Hint: use Pappus.
> *Edge case: Center of mass of a **curve** (wire), not a region. Requires arc-length density or Pappus insight.*

**Student Project: Grand Canyon Skywalk** (p.621–622) — Multi-part center-of-mass project with three sub-regions (semicircular annulus + two rectangular legs). Recalculate when visitor center and tourists are included.
> *Edge case: Real-world engineering application. Composite region with constant density. Requires breaking into subregions, computing each centroid, then weighted average.*

---

## 10. HYPERBOLIC / TRANSCENDENTAL — Inverse & Special Functions (Chapter 6.9)

**Q426** (p.651) — Chain hangs between posts 4 m apart forming catenary `y = 4·cosh(x/4)`. Find total length.
> *Edge case: Arc length of catenary. Hyperbolic function integral (`∫ cosh dx = sinh`).)*

**Q427** (p.651) — High-voltage line is catenary `y = a·cosh(x/a)`. Find ratio of area under catenary to its arc length. What do you notice?
> *Edge case: **Ratio invariant** discovery. Area and arc length of catenary scale proportionally. Pattern-recognition question.*

**Q428** (p.651) — Telephone line catenary `y = b·cosh(x/b)`. Same ratio question. Does it confirm previous answer?
> *Edge case: Confirming the invariant ratio holds for any parameter.*

---

## 11. MISCELLANEOUS WEIRD / FUN

**Q298** (p.96) — Rewrite expressions in terms of exponentials and simplify: `sinh(ln x)`, `cosh(ln x)`, etc.
> *Edge case: Logarithm inside hyperbolic function. Requires substituting definitions and simplifying algebraic fractions.*

**Q217 (Answer Key p.758)** — "For more information, look up **Gabriel's Horn**."
> *Meta edge case: The textbook itself directs students to research a famous paradox. This could inspire a "explain the paradox" problem type.*

---

## SUMMARY: Recommended New Problem Types for MATH TRAINER

Based on this scan, here are categories worth adding to the generator that are **not** currently in the app's problem list:

1. **Epsilon-delta proofs** (prove limit does/doesn't exist)
2. **Ceiling/floor function limits & continuity**
3. **Rational vs irrational piecewise functions**
4. **Cusp / vertical tangent analysis**
5. **Inscribed solids optimization** (cylinder in sphere, cone in sphere, etc.)
6. **Distance-to-curve minimization**
7. **Different material costs optimization**
8. **Newton's method for fixed points / extrema**
9. **Secant method iterations**
10. **Indeterminate forms beyond 0/0 and ∞/∞** (`0·∞`, `∞−∞`, `1^∞`, `∞^0`)
11. **Gabriel's Horn / finite volume vs infinite surface area**
12. **Arc length comparison / scaling arguments**
13. **Catenary arc length & area/arc-length ratio**
14. **Work with angled forces**
15. **Generalized center of mass (symbolic exponents) + Pappus**
16. **Center of mass of a wire / curve**
17. **Composite region center of mass (multiple subregions)**
18. **Surface area of revolution with flat cutoffs**
19. **Construct a function with given asymptotes**
20. **Discrete optimization (watermelon/plant problems)**

---

*Scan generated from: `C:\Users\austi\Downloads\calculus-volume-1_-_WEB.pdf`*
*Chunked into 25-page segments; 31 chunks total; 1,030,000+ chars extracted.*
