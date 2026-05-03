# Linear Algebra 1 — Implementation Reference

> Preserved from planning docs. Question types, JSONL templates, checkers, and frontend notes for future LA implementation.

---

## Question Types & Templates

### 1. Matrix Operations (`matrix_ops`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| M1 | 2×2 matrix addition/subtraction | scalar per cell |
| M2 | Scalar multiplication (2×2, 3×3) | matrix |
| M3 | 2×2 matrix multiplication | matrix |
| M4 | 3×3 matrix multiplication | matrix |
| M5 | Linear transformation (rotate/reflect) | vector |

### 2. Determinants (`determinants`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| D1 | 2×2 determinant ad-bc | scalar |
| D2 | 3×3 Sarrus rule | scalar |
| D3 | 3×3 cofactor expansion | scalar |
| D4 | Determinant properties (row swap, etc.) | property identification |
| D5 | Area of parallelogram via determinant | scalar |

### 3. Vectors (`vectors`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| V1 | 2D vector add/subtract/scalar mult | vector |
| V2 | 3D dot product + magnitude | scalar |
| V3 | 3D cross product | vector |
| V4 | Unit vector + vector projection | vector |
| V5 | Angle between vectors | scalar |

### 4. Linear Systems (`linear_systems`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| S1 | 2-variable system (elimination) | scalar pair |
| S2 | 2×2 augmented matrix → row reduce | solution |
| S3 | 3×3 Gaussian elimination | unique solution |
| S4 | 3×3 Gauss-Jordan → RREF | solution type + answer |
| S5 | Cramer's rule 3×3 | scalar answers |

### 5. Matrix Inverse (`matrix_inverse`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| I1 | 2×2 inverse via formula (1/det)[[d,-b],[-c,a]] | matrix |
| I2 | Check invertibility (det ≠ 0) | true/false |
| I3 | 3×3 inverse via row reduction [A|I] | matrix |
| I4 | Solve AX=B using inverse | vector |
| I5 | Adjugate/cofactor method | matrix |

### 6. Eigenvalues & Eigenvectors (`eigenvalues`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| E1 | Characteristic polynomial of 2×2 | polynomial expression |
| E2 | Eigenvalues of 2×2 | λ1, λ2 |
| E3 | Eigenvectors of 2×2 | vectors per eigenvalue |
| E4 | Characteristic polynomial of 3×3 | polynomial |
| E5 | Eigenvalues + eigenvectors of 3×3 | λ1,λ2,λ3 + vectors |

### 7. Vector Spaces (`vector_spaces`) — 5 templates

| ID | Problem | Answer Type |
|----|---------|-------------|
| S1 | Linear combination (find scalar) | scalar |
| S2 | Linear independence check | independent/dependent |
| S3 | Span membership test | in span/not in span |
| S4 | Find basis + dimension | basis set + dim |
| S5 | Row-reduce to find row/column/null space | bases |

---

## LA Word Problems — 10 Templates

| ID | Context | LA Technique |
|----|---------|--------------|
| W1 | Traffic flow network | Gaussian elimination |
| W2 | Chemical equation balancing | Linear system |
| W3 | Economic input-output / Leontief | Matrix inverse |
| W4 | Cryptography encoding/decoding | Matrix multiplication |
| W5 | Triangle area via determinant | Geometry |
| W6 | Collinearity test via determinant | Geometry |
| W7 | Dynamical system iteration | Eigenvalue stability |
| W8 | Markov chain steady-state | Eigenvectors |
| W9 | Computer graphics 2D transformation | Linear transform |
| W10 | Population growth (Leslie matrix) | Eigenvalue application |

---

## Checker Functions Needed

```python
def check_matrix_answer(problem, user_matrix):
    """Compare user 2D list vs problem['answerMatrix'] element-wise.
    Tolerance: 0.001 for float answers.
    Returns: {result: 'correct'|'wrong', slotWise: [...]}"""
    answer = problem["answerMatrix"]
    if len(user_matrix) != len(answer):
        return {"result": "wrong", "reason": "dimension_mismatch"}
    for i, row in enumerate(answer):
        for j, val in enumerate(row):
            if abs(float(user_matrix[i][j]) - float(val)) > 0.001:
                return {"result": "wrong", "reason": "element_mismatch"}
    return {"result": "correct"}

def check_vector_answer(problem, user_vector):
    """Compare user list vs answerVector element-wise."""
    answer = problem["answerVector"]
    for i, val in enumerate(answer):
        if abs(float(user_vector[i]) - float(val)) > 0.001:
            return {"result": "wrong", "reason": "element_mismatch"}
    return {"result": "correct"}

def check_solution_type(problem, user_input):
    """Check 'unique' / 'infinite' / 'inconsistent' matches."""
    return {"result": "correct" if user_input == problem["solutionType"] else "wrong"}
```

### Registry mappings:
- `matrix_ops` → `check_matrix_answer`
- `determinants` → `check_norm_answer` (scalar)
- `vectors` → `check_vector_answer`
- `linear_systems` → `check_solution_type` (varies by problem)
- `matrix_inverse` → `check_matrix_answer`
- `eigenvalues` → `check_norm_answer` (scalar λ)
- `vector_spaces` → `check_norm_answer` (scalar/string)

---

## Frontend: Matrix Grid Input

```javascript
// When problem.answerType === 'matrix':
//   Render matrixRows × matrixCols grid of <input> elements
//   Monospace font, bordered cells
//   Arrow-key navigation between cells
//   On submit: collect values into 2D array → matrixAnswer

// When problem.answerType === 'vector':
//   Render single-column grid (matrixRows × 1)

// Solution type radio:
//   For linear_systems problems with noUniqueSolution: true
//   Radio buttons: "Unique solution" / "Infinitely many" / "No solution"
```

---

## LA-Specific JSONL Schema Extensions

```jsonl
{
  "id": "la1_matrix_inverse_003",
  "course": "la1",
  "topic": "matrix_inverse",
  "method": "adjugate_method",
  "template": "Find A^{-1} for A = [[{a},{b}],[{c},{d}]]. Use the adjugate method.",
  "variables": {
    "a": {"type": "int", "range": [1, 5]},
    "b": {"type": "int", "range": [1, 5]},
    "c": {"type": "int", "range": [1, 5]},
    "d": {"type": "int", "range": [1, 5]}
  },
  "answer_fn": "[[d/(a*d-b*c), -b/(a*d-b*c)], [-c/(a*d-b*c), a/(a*d-b*c)]]",
  "answerType": "matrix",
  "matrixRows": 2,
  "matrixCols": 2,
  "solution_steps": [
    {"label": "Compute determinant", "math": "det(A) = {a}({d}) - {b}({c}) = {det}", "note": "ad - bc"},
    {"label": "Verify invertible", "math": "det(A) = {det} \\neq 0 \\implies A \\text{ is invertible}", "note": ""},
    {"label": "Apply formula", "math": "A^{-1} = \\frac{1}{{det}}\\begin{{pmatrix}} {d} & {-b} \\\\ {-c} & {a} \\end{{pmatrix}}", "note": "Swap a,d; negate b,c"}
  ],
  "modes_available": ["solve"],
  "difficulty": 1,
  "tags": ["matrix_inverse", "2x2", "adjugate"]
}
```

---

## Source Books

| Book | Level | Link |
|------|-------|------|
| Hefferon — *Linear Algebra* | Intro (LA 1–2) | joshua.smcvt.edu/linearalgebra |
| Treil — *Linear Algebra Done Wrong* | Intermediate (LA 2) | math.brown.edu/streil/papers/LADW |
| Axler — *Linear Algebra Done Right* (free since 2024) | Proof-based (LA 2–3) | linear.axler.net |
| Strang — *Introduction to Linear Algebra* | Applied (LA 1–2) | math.mit.edu |
| Beezer — *A First Course in Linear Algebra* | Intro, very thorough | linear.ups.edu |

**Recommended stack for Applied Math + ML:**
- LA 1: Hefferon or Beezer
- LA 2: Treil
- LA 3: Axler
- Strang's MIT OCW lectures pair with any of the above

---

## Module Config (Tiers 8-14)

```python
"matrix_ops":      {"tier": 8,  "label": "Matrix Operations",      "group": "la1"},
"determinants":    {"tier": 9,  "label": "Determinants",           "group": "la1"},
"vectors":         {"tier": 10, "label": "Vectors",                "group": "la1"},
"linear_systems":  {"tier": 11, "label": "Linear Systems",         "group": "la1"},
"matrix_inverse":  {"tier": 12, "label": "Matrix Inverse",         "group": "la1"},
"eigenvalues":     {"tier": 13, "label": "Eigenvalues",            "group": "la1"},
"vector_spaces":   {"tier": 14, "label": "Vector Spaces",          "group": "la1"},
```

---

## Volume Estimate

| Course | Sub-topics | Templates | ~Problems |
|--------|-----------|-----------|-----------|
| LA 1 | ~7 | ~35 | 140 |
| LA 2 | ~7 | ~35 | 140 |
| LA 3 | ~8 | ~40 | 160 |

---

## Mixed Mode UI Notes

```
┌─────────────────────────────────────────────────────────┐
│ ○ Calc Only    ○ Linear Algebra Only    ● Mixed         │
│                                                         │
│ Calculus [═══════════░░░] 70%                           │
│ Linear Algebra [════░░░░░░░] 30%                        │
└─────────────────────────────────────────────────────────┘
```

- `state.mixedMode = 'calc' | 'la' | 'mixed'`
- `state.subjectWeights = { calc: 0.7, la: 0.3 }`
- Calc Only: picks from unlocked calc modules
- LA Only: picks from unlocked LA modules
- Mixed: weighted random based on subjectWeights
