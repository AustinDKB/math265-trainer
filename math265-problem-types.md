# MATH 265 Algebra Trainer — Problem Types & Difficulty Guide

> Last updated to match source code CONFIG block.

---

## How Difficulty Works

Every problem is pre-assigned to difficulty tier **1, 2, or 3** based on the number of
distinct algebraic techniques required to solve it.

| Tier | Meaning | Rule of thumb |
|------|---------|---------------|
| **1** | Single technique, direct application | One formula, one step |
| **2** | Two techniques, or a formula requiring recognizing a non-obvious pattern | Factor then apply, or multi-step rewrite |
| **3** | Three or more chained techniques, multi-degree expressions, or require a substitution | Nested factoring, u-sub, compound exponent rewriting |

In **Auto** mode the app tracks your last 5 attempts per module per difficulty level:
- **5/5 correct** → bumps difficulty up by 1 (`CONFIG.adaptive.bumpUpStreak = 5`)
- **3+ wrong in last 5** → drops difficulty down by 1 (`CONFIG.adaptive.dropDownWrong = 3`)
- Otherwise stays put
- Per-module tracking: you can be Diff 3 in Exponents and Diff 1 in Fractions simultaneously

---

## CONFIG — Parameter Ranges (edit in source)

All ranges live in one `CONFIG` object at the top of the `<script>` block.

```js
CONFIG.factoring.diffSquares_a      = [2, 15]    // x² − a²: root range
CONFIG.factoring.simpleTrinomial_pq = [-12, 12]  // trinomial roots p,q
CONFIG.factoring.gcf_k              = [2, 7]     // GCF coefficient
CONFIG.factoring.gcf_pq             = [-8, 8]    // GCF inner roots
CONFIG.factoring.leadCoeff_a        = [2,3,5,6]  // leading coeff choices
CONFIG.factoring.leadCoeff_pq       = [-8, 8]    // (ax+p)(x+q) inner values
CONFIG.factoring.cubes_a            = [2, 6]     // x³±a³ root
CONFIG.factoring.quartic_a          = [2, 4]     // x⁴−a⁴ root
CONFIG.factoring.grouping_ab        = [-8, 8]    // grouping a,b
CONFIG.factoring.quadDisguise_pq    = [-8, 8]    // u-sub roots
CONFIG.factoring.allXterms_k        = [2, 6]     // k in kx(x+p)(x+q)
CONFIG.factoring.allXterms_pq       = [-8, 8]    // inner trinomial roots

CONFIG.exponents.sameBase_ab        = [1, 8]     // x^a · x^b exponents
CONFIG.exponents.divideBase_b       = [1, 8]     // denominator exponent
CONFIG.exponents.divideBase_aExtra  = [1, 4]     // numerator = b + this
CONFIG.exponents.powerPower_ab      = [2, 5]     // (x^a)^b
CONFIG.exponents.negExp_a           = [1, 5]     // x^(-a)
CONFIG.exponents.radicalToExp_m     = [1, 5]     // power under radical
CONFIG.exponents.radicalToExp_n     = [2,3,4]    // radical index
CONFIG.exponents.fracExpArith_num   = [1, 3]     // fractional exp numerators
CONFIG.exponents.fracExpArith_den   = [2,3,4]    // fractional exp denominators
CONFIG.exponents.coeffRewrite_k     = [2, 10]    // coefficient in k/(x^a√x)
CONFIG.exponents.coeffRewrite_a     = [1, 3]     // x^a in denominator
CONFIG.exponents.higherRadical_n    = [3,4,5]    // higher radical index
CONFIG.exponents.higherRadical_m    = [2, 7]     // power under higher radical

CONFIG.fractions.addFrac_num        = [1, 5]     // a/b + c/d numerators
CONFIG.fractions.addFrac_den        = [2, 9]     // denominators
CONFIG.fractions.divFrac_all        = [1, 9]     // (a/b)÷(c/d) all values
CONFIG.fractions.cancelFrac_a       = [1, 8]     // (x²−a²)/(x+a) root
CONFIG.fractions.threeTermLCD_a     = [1, 5]     // 1/(x±a)+… root
CONFIG.fractions.quotientRule_n     = [2, 4]     // derivative degree
CONFIG.fractions.quotientRule_a     = [1, 5]     // (x+a) denominator

CONFIG.adaptive.bumpUpStreak        = 5          // consecutive correct → harder
CONFIG.adaptive.dropDownWrong       = 3          // wrongs in last 5 → easier
CONFIG.adaptive.dedupWindow         = 30         // no repeat within last N problems
```

---

## Module 1: Factoring

### Difficulty 1  *(3 problem types)*

#### 1a. Difference of Squares
**Form:** `x² − a²`
**Config:** `diffSquares_a = [2, 15]`
**Answer:** `(x + a)(x − a)`
**Why Diff 1:** One pattern, one formula. No search needed.
**Example:** `x² − 49` → `(x + 7)(x − 7)`

---

#### 1b. Simple Trinomial (leading coeff = 1)
**Form:** `x² + bx + c`
**Config:** `simpleTrinomial_pq = [-12, 12]` — roots p, q; `b = p+q`, `c = p·q`
**Answer:** `(x + p)(x + q)`
**Why Diff 1:** Find two integers summing to b and multiplying to c. Single technique.
**Example:** `x² − 3x − 28` → `(x − 7)(x + 4)`

---

#### 1c. All-X-Terms (GCF contains x)
**Form:** `kx³ + kbx² + kcx` — every term divisible by x
**Config:** `allXterms_k = [2, 6]`, `allXterms_pq = [-8, 8]`
**Answer:** `kx(x + p)(x + q)`
**Why Diff 1:** Extends basic GCF factoring — the catch is recognizing `x` itself is part of the GCF. Two mechanical steps but both are Diff 1 individually.
**Example:** `3x³ − 6x² − 24x` → `3x(x − 4)(x + 2)`

---

### Difficulty 2  *(4 problem types)*

#### 2a. GCF Extraction + Trinomial
**Form:** `kx² + kbx + kc`
**Config:** `gcf_k = [2, 7]`, `gcf_pq = [-8, 8]`
**Answer:** `k(x + p)(x + q)`
**Why Diff 2:** Two steps — pull GCF, then factor the remaining trinomial. Missing either is wrong.
**Example:** `3x² + 9x − 30` → `3(x + 5)(x − 2)`

---

#### 2b. Leading Coefficient ≠ 1
**Form:** `ax² + Bx + C`
**Config:** `leadCoeff_a = [2,3,5,6]`, `leadCoeff_pq = [-8, 8]`; built from `(ax+p)(x+q)`
**Answer:** `(ax + p)(x + q)`
**Why Diff 2:** AC method required — find factors of `a·c` summing to `b`, then split and group.
**Example:** `2x² + 7x + 3` → `(2x + 1)(x + 3)`

---

#### 2c. Difference of Cubes
**Form:** `x³ − a³`
**Config:** `cubes_a = [2, 6]`
**Answer:** `(x − a)(x² + ax + a²)`
**Why Diff 2:** Must recall and apply the cubes identity correctly. The trinomial factor is fixed, not found by guessing.
**Example:** `x³ − 27` → `(x − 3)(x² + 3x + 9)`

---

#### 2d. Sum of Cubes
**Form:** `x³ + a³`
**Config:** `cubes_a = [2, 6]`
**Answer:** `(x + a)(x² − ax + a²)`
**Why Diff 2:** Same as difference of cubes — the sign pattern in the trinomial flips, which is the common error.
**Example:** `x³ + 8` → `(x + 2)(x² − 2x + 4)`

---

### Difficulty 3  *(3 problem types)*

#### 3a. Quartic — Nested Difference of Squares
**Form:** `x⁴ − a⁴`
**Config:** `quartic_a = [2, 4]`
**Answer:** `(x² + a²)(x + a)(x − a)`
**Why Diff 3:** Two-stage factoring — `(x²)² − (a²)²` then `x² − a²` again. Three factors total, must go all the way.
**Example:** `x⁴ − 16` → `(x² + 4)(x + 2)(x − 2)`

---

#### 3b. Factoring by Grouping (4 terms)
**Form:** `x³ + ax² + bx + ab`
**Config:** `grouping_ab = [-8, 8]`
**Answer:** `(x² + b)(x + a)`
**Why Diff 3:** No single formula — must spot the grouping structure, factor each pair, then pull the common binomial.
**Example:** `x³ + 3x² − 5x − 15` → `(x² − 5)(x + 3)`

---

#### 3c. Quadratic in Disguise (u-substitution)
**Form:** `x⁴ + bx² + c`
**Config:** `quadDisguise_pq = [-8, 8]`; built from `(x²+p)(x²+q)`
**Answer:** `(x² + p)(x² + q)`
**Why Diff 3:** Must recognize this as quadratic in `u = x²`, factor it, then substitute back.
**Example:** `x⁴ − 5x² + 6` → `(x² − 2)(x² − 3)`

---

## Module 2: Exponents & Radicals

### Difficulty 1  *(4 problem types)*

#### 1a. Multiply Same Base
**Form:** `xᵃ · xᵇ`
**Config:** `sameBase_ab = [1, 8]`
**Answer:** `x^(a+b)`
**Why Diff 1:** One rule, one addition.
**Example:** `x³ · x⁵` → `x⁸`

---

#### 1b. Divide Same Base
**Form:** `xᵃ / xᵇ` where a > b
**Config:** `divideBase_b = [1, 8]`, numerator = b + `divideBase_aExtra = [1, 4]`
**Answer:** `x^(a−b)` (always positive)
**Why Diff 1:** One rule, one subtraction.
**Example:** `x⁷ / x³` → `x⁴`

---

#### 1c. Power of a Power
**Form:** `(xᵃ)ᵇ`
**Config:** `powerPower_ab = [2, 5]`
**Answer:** `x^(ab)`
**Why Diff 1:** One rule, one multiplication.
**Example:** `(x³)⁴` → `x¹²`

---

#### 1d. Negative Exponent
**Form:** `x^(−a)`
**Config:** `negExp_a = [1, 5]`
**Answer:** `1/xᵃ`
**Why Diff 1:** One rule, direct rewrite.
**Example:** `x⁻³` → `1/x³`

---

### Difficulty 2  *(2 problem types)*

#### 2a. Radical to Fractional Exponent
**Form:** `ⁿ√(xᵐ)`
**Config:** `radicalToExp_m = [1, 5]`, `radicalToExp_n = [2, 3, 4]`
**Answer:** `x^(m/n)` (fraction simplified)
**Why Diff 2:** Must convert radical form AND simplify the resulting fraction.
**Example:** `⁴√(x³)` → `x^(3/4)`

---

#### 2b. Fractional Exponent Arithmetic
**Form:** `x^(a/b) · x^(c/d)`
**Config:** `fracExpArith_num = [1, 3]`, `fracExpArith_den = [2, 3, 4]`
**Answer:** `x^((ad+bc)/(bd))` simplified
**Why Diff 2:** Product rule applies, but adding unlike fractions adds an LCD step.
**Example:** `x^(1/2) · x^(1/3)` → `x^(5/6)`

---

### Difficulty 3  *(4 problem types)*

#### 3a. Rewrite `1/√x`
**Form:** Fixed: `1/√x`
**Answer:** `x^(−1/2)`
**Why Diff 3:** Chain: √x = x^(1/2) → 1/x^(1/2) = x^(−1/2). Two rules in one rewrite.

---

#### 3b. Rewrite `1/(x²√x)`
**Form:** Fixed: `1/(x²√x)`
**Answer:** `x^(−5/2)`
**Why Diff 3:** Combine x² · x^(1/2) = x^(5/2) in denominator first (Product rule), then flip sign. Three operations.

---

#### 3c. Rewrite with Coefficient `k/(xᵃ√x)`
**Form:** `k/(xᵃ√x)`
**Config:** `coeffRewrite_k = [2, 10]`, `coeffRewrite_a = [1, 3]`
**Answer:** `k · x^(−(2a+1)/2)`
**Why Diff 3:** Same chain as 3b but exponent `(2a+1)/2` must be computed, not looked up.
**Example:** `5/(x²√x)` → `5x^(−5/2)`

---

#### 3d. Higher-Index Radical `ⁿ√(xᵐ)` — with Required Simplification
**Form:** `ⁿ√(xᵐ)`
**Config:** `higherRadical_n = [3, 4, 5]`, `higherRadical_m = [2, 7]`
**Answer:** `x^(m/n)` reduced
**Why Diff 3:** Cube/fourth/fifth roots are less automatic than square roots; fraction reduction is non-trivial.
**Example:** `⁵√(x⁴)` → `x^(4/5)`

---

## Module 3: Fraction Manipulation

### Difficulty 1  *(2 problem types)*

#### 1a. Add Simple Numeric Fractions
**Form:** `a/b + c/d` (pure numbers)
**Config:** `addFrac_num = [1, 5]`, `addFrac_den = [2, 9]`
**Answer:** simplified fraction or integer
**Why Diff 1:** Standard LCD procedure on pure numbers. No variables.
**Example:** `2/3 + 3/4` → `17/12`

---

#### 1b. Divide Fractions
**Form:** `(a/b) ÷ (c/d)`
**Config:** `divFrac_all = [1, 9]`
**Answer:** simplified fraction or integer
**Why Diff 1:** Keep-Change-Flip then simplify. Two mechanical steps.
**Example:** `(3/4) ÷ (9/8)` → `2/3`

---

### Difficulty 2  *(3 problem types)*

#### 2a. Factor and Cancel
**Form:** `(x² − a²) / (x + a)`
**Config:** `cancelFrac_a = [1, 8]`
**Answer:** `x − a`
**Why Diff 2:** Must recognize difference of squares in numerator, factor it, then cancel. Bridges factoring and fractions.
**Example:** `(x² − 25)/(x + 5)` → `x − 5`

---

#### 2b. Complex Fraction — Calculus Preview
**Form:** Fixed: `[1/(x+h) − 1/x] / h`
**Answer:** `−1 / [x(x+h)]`
**Why Diff 2:** This is the exact limit definition of the derivative of `1/x`. Requires nested LCD, numerator simplification, and cancellation of `h`.

---

#### 2c. Three-Term LCD
**Form:** `1/(x−a) + 1/(x+a) + 1/(x²−a²)`
**Config:** `threeTermLCD_a = [1, 5]`
**Answer:** `(2x+1)/(x²−a²)`
**Why Diff 2:** Three denominators, one of which factors into the other two. Must spot the relationship before choosing LCD.
**Example:** `1/(x−3) + 1/(x+3) + 1/(x²−9)` → `(2x+1)/(x²−9)`

---

### Difficulty 3  *(2 problem types)*

#### 3a. Quotient Rule Cleanup
**Form:** `[nxⁿ⁻¹(x+a) − xⁿ] / (x+a)²`
**Config:** `quotientRule_n = [2, 4]`, `quotientRule_a = [1, 5]`
**Answer:** `xⁿ⁻¹[(n−1)x + na] / (x+a)²`
**Why Diff 3:** This is the direct output of applying the quotient rule in derivatives. Must factor `xⁿ⁻¹` from numerator then simplify the bracket. Directly targets MATH 265 exam problems.
**Example:** `[3x²(x+2) − x³] / (x+2)²` → `x²(2x+6)/(x+2)²`

---

#### 3b. Fractional Exponent Cleanup
**Form:** `[ax^(p/q) − bx^(r/s)] / (cx)` — fixed exponent pairs from `{(3/2),(1/2),(2/3),(5/2)}`
**Answer:** `(a/c)x^(p/q−1) − (b/c)x^(r/s−1)` simplified
**Why Diff 3:** Dividing each term by `cx` subtracts 1 from each fractional exponent separately while carrying coefficients. Common final step in derivative simplification.
**Example:** `[4x^(3/2) − 2x^(1/2)] / (2x)` → `2x^(1/2) − x^(−1/2)`

---

## Summary Table

| Module | Diff 1 | Diff 2 | Diff 3 | Total types |
|--------|--------|--------|--------|-------------|
| Factoring | 3 (DoS, Trinomial, All-X-Terms) | 4 (GCF, Lead≠1, Diff Cubes, Sum Cubes) | 3 (Quartic, Grouping, Quad Disguise) | **10** |
| Exponents | 4 (×base, ÷base, pow², neg) | 2 (radical→exp, frac arith) | 4 (1/√x, 1/x²√x, k/xᵃ√x, ⁿ√xᵐ) | **10** |
| Fractions | 2 (add, divide) | 3 (cancel, complex, 3-term LCD) | 2 (quotient rule, frac exp cleanup) | **7** |
| **Total** | **9** | **9** | **9** | **27** |

Within each type, parameters are randomized from CONFIG ranges, giving hundreds of distinct surface expressions before any repeat is likely. The dedup window (`CONFIG.adaptive.dedupWindow = 30`) prevents the same expression from appearing twice within any 30-problem run.
