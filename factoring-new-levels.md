# Factoring — New Difficulty Levels

## Difficulty 4 — Exponent Factoring

| Type | Example | Factored Form |
|------|---------|---------------|
| Fractional exponent GCF | `x^(5/2) - x^(1/2)` | `x^(1/2)(x² - 1)` |
| Negative exponent GCF | `x^(-1) + x^(-3)` | `x^(-3)(x² + 1)` |
| Mixed fractional/negative | `3x^(2/3) - 6x^(-1/3)` | `3x^(-1/3)(x - 2)` |
| Fractional + diff of squares | `x^(5/2) - x^(1/2)` | `x^(1/2)(x+1)(x-1)` |

**Skill:** Identify lowest exponent as GCF, factor out, simplify remaining.

---

## Difficulty 5 — Trigonometric Factoring

Treat trig function as a variable, apply standard factoring techniques.

| Type | Example | Factored Form |
|------|---------|---------------|
| Simple trinomial (trig) | `sin²x + 2sin x - 3` | `(sin x + 3)(sin x - 1)` |
| Leading coeff ≠ 1 (trig) | `2sin²x - sin x - 1` | `(2sin x + 1)(sin x - 1)` |
| Diff of squares (trig) | `tan²x - 4` | `(tan x + 2)(tan x - 2)` |
| Pythagorean identity combo | `1 - cos²x` | `(1 + cos x)(1 - cos x)` → `sin²x` |
| GCF (trig) | `sin²x cos x - cos x` | `cos x(sin x + 1)(sin x - 1)` |

**Skill:** Substitute `u = sin x` (or cos/tan), factor in u, rewrite.

---

## Difficulty 5 (alt) — Rational Roots + Synthetic Division

| Type | Example | Factored Form |
|------|---------|---------------|
| Cubic, 3 real roots | `x³ - 6x² + 11x - 6` | `(x-1)(x-2)(x-3)` |
| Cubic, 1 real + irreducible quad | `x³ - x² + x - 1` | `(x-1)(x²+1)` |
| Quartic via rational roots | `x⁴ - 5x² + 4` | `(x-1)(x+1)(x-2)(x+2)` |

**Skill:** List `±factors(const)/factors(leading)`, test via synthetic division, divide out root, repeat.

---

## Difficulty 5 — Multi-Variable Factoring

| Type | Example | Factored Form |
|------|---------|---------------|
| GCF multi-var | `x²y - y³` | `y(x+y)(x-y)` |
| Perfect square trinomial | `a²b - 2ab² + b³` | `b(a-b)²` |
| Grouping multi-var | `x³y + x²y² - xy - y²` | `y(xy+1)(x²-1)` → `y(xy+1)(x+1)(x-1)` |
| Diff of squares multi-var | `4x² - 9y²` | `(2x+3y)(2x-3y)` |

**Skill:** Factor out common variable terms first, then apply standard patterns.

---

## Difficulty 6 — Advanced / Complex

| Type | Example | Factored Form |
|------|---------|---------------|
| Sum of squares (complex) | `x² + 9` | `(x + 3i)(x - 3i)` |
| Sophie Germain identity | `a⁴ + 4b⁴` | `(a²+2b²+2ab)(a²+2b²-2ab)` |
| Cyclotomic-style | `x⁴ + x² + 1` | `(x²+x+1)(x²-x+1)` |
| Higher odd powers | `x⁵ - a⁵` | `(x-a)(x⁴+ax³+a²x²+a³x+a⁴)` |
| Sum of 5th powers | `x⁵ + a⁵` | `(x+a)(x⁴-ax³+a²x²-a³x+a⁴)` |

**Skill:** Recognize non-obvious patterns, apply advanced identities.

---

## Recommended Build Order

1. **Diff 4** — Exponent GCF (most adjacent to current diff 3)
2. **Diff 5a** — Trig factoring (apply known techniques, new substitution)
3. **Diff 5b** — Rational roots + synthetic division (new algorithm)
4. **Diff 5c** — Multi-variable (extend known techniques)
5. **Diff 6** — Complex / Sophie Germain / cyclotomic (advanced identity recognition)
