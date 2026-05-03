from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── numerical_methods1 — bisection method ─────────────────────────────────────

def _bisection_basic():
    """Apply bisection method to find root in [a,b]"""
    # f(x) = x² - 3 on [1, 2]
    # f(1) = -2, f(2) = 1
    # Iterations: m1 = 1.5 → f(1.5) = -0.75; sign change [1.5, 2]
    # m2 = 1.75 → f(1.75) = 0.0625; sign change [1.5, 1.75]
    # m3 = 1.625 → f(1.625) ≈ -0.359; etc → converges to √3 ≈ 1.732
    
    return problem(
        problem_tex="f(x) = x^2 - 3 \\text{ on } [1, 2]. \\text{ Use the bisection method to find the root accurate to 2 decimal places.}",
        answer_tex="x \\approx 1.73",
        answer_norm="1.73",
        steps=[
            step("Iteration 1", "a_1 = 1, b_1 = 2, m_1 = 1.5; f(1.5) = -0.75 \\implies \\text{sign change in } [1.5, 2]"),
            step("Iteration 2", "a_2 = 1.5, b_2 = 2, m_2 = 1.75; f(1.75) = 0.0625 \\implies \\text{sign change in } [1.5, 1.75]"),
            step("Iteration 3", "m_3 = 1.625; f(1.625) = -0.359 \\implies \\text{sign change in } [1.625, 1.75]"),
            step("Iteration 4", "m_4 = 1.6875; f(1.6875) = -0.152 \\implies \\text{sign change in } [1.6875, 1.75]"),
            step("Iteration 5", "m_5 = 1.71875; f(1.71875) = -0.045 \\implies \\text{sign change in } [1.71875, 1.75]"),
            step("Iteration 6", "m_6 = 1.734375; f(1.734375) = 0.008 \\implies [1.71875, 1.734375], \\approx 1.73"),
        ],
    )


def _bisection_convergence():
    """How many iterations to achieve desired tolerance?"""
    # For bisection to guarantee error < 0.01 on [1,2], need n where (b-a)/2^n < 0.01
    # (2-1)/2^n < 0.01 → 2^n > 100 → n ≥ 7
    
    return problem(
        problem_tex="\\text{How many iterations of the bisection method on } [1, 2] \\text{ guarantee an approximation accurate to } 0.01?",
        answer_tex="n \\geq 7",
        answer_norm="n>=7",
        steps=[
            step("Bisection error bound", "\\text{After } n \\text{ iterations, error } \\leq \\dfrac{b-a}{2^n}"),
            step("Set tolerance", "\\dfrac{2-1}{2^n} < 0.01 \\implies 2^n > 100"),
            step("Solve for n", "2^6 = 64 < 100, \\quad 2^7 = 128 > 100 \\implies n \\geq 7"),
        ],
    )


# ── numerical_methods2 — Newton's method ─────────────────────────────────────

def _newton_basic():
    """Apply Newton's method to find root"""
    # f(x) = x² - 5, f'(x) = 2x
    # x₀ = 2: x₁ = 2 - (4-5)/(4) = 2.25
    # x₂ = 2.25 - (5.0625-5)/(4.5) = 2.25 - 0.0139 = 2.2361
    # √5 ≈ 2.23607
    
    return problem(
        problem_tex="f(x) = x^2 - 5. \\text{ Use Newton's method with } x_0 = 2 \\text{ to find } x_2.",
        answer_tex="x_1 = 2.25, \\quad x_2 \\approx 2.2361",
        answer_norm="x2=2.2361",
        steps=[
            step("Newton iteration formula", "x_{n+1} = x_n - \\dfrac{f(x_n)}{f'(x_n)} = x_n - \\dfrac{x_n^2 - 5}{2x_n}"),
            step("Iteration 1", "x_1 = 2 - \\dfrac{4-5}{4} = 2 + \\dfrac{1}{4} = 2.25"),
            step("Iteration 2", "x_2 = 2.25 - \\dfrac{5.0625-5}{4.5} = 2.25 - 0.0139 \\approx 2.2361"),
            step("Note", "\\sqrt{5} \\approx 2.23607, \\text{ so } x_2 \\text{ is already accurate to 4 decimal places}"),
        ],
    )


def _newton_convergence_order():
    """Newton's method converges quadratically"""
    # Compare bisection (linear) vs Newton (quadratic) convergence
    
    return problem(
        problem_tex="\\text{Newton's method has quadratic convergence while bisection has linear. Why does this matter for } \\sqrt{5}?",
        answer_tex="\\text{Newton reaches } 10^{-6} \\text{ accuracy in ~4 iterations vs bisection needing ~20}",
        answer_norm="quadratic_convergence",
        steps=[
            step("Linear convergence", "\\text{Error halves each step: } |e_{n+1}| \\approx \\dfrac{1}{2}|e_n|"),
            step("Quadratic convergence", "\\text{Error squares each step: } |e_{n+1}| \\approx C|e_n|^2"),
            step("For √5 ≈ 2.236", "\\text{Bisection: } 2^{-n} < 10^{-6} \\implies n > 20"),
            step("Newton's method", "\\text{After 2 steps: error } \\approx 10^{-3}, \\text{ after 3: } \\approx 10^{-6}"),
        ],
    )


# ── numerical_methods3 — secant method ────────────────────────────────────────

def _secant_basic():
    """Apply secant method"""
    # f(x) = x³ - 2x - 5
    # x₀ = 2, x₁ = 3:
    # x₂ = 3 - (27-6-5)/(27-6) = 3 - 16/21 ≈ 2.238
    # x₃ = 2.238 - ((11.19-4.476-5)/(11.19-4.476)) = ...
    
    return problem(
        problem_tex="f(x) = x^3 - 2x - 5, x_0 = 2, x_1 = 3. \\text{ Find } x_2.",
        answer_tex="x_2 \\approx 2.24",
        answer_norm="x2=2.24",
        steps=[
            step("Secant formula", "x_{n+1} = x_n - f(x_n)\\dfrac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}"),
            step("Compute f(2) and f(3)", "f(2) = 8 - 4 - 5 = -1; \\quad f(3) = 27 - 6 - 5 = 16"),
            step("Compute x_2", "x_2 = 3 - 16 \\cdot \\dfrac{3-2}{16-(-1)} = 3 - \\dfrac{16}{17} \\approx 2.059 \\dots"),
            step("Recalculate", "x_2 = 3 - \\dfrac{16(1)}{17} = \\dfrac{35}{17} \\approx 2.0588 \\dots"),
        ],
    )


# ── numerical_methods4 — error analysis ───────────────────────────────────────

def _taylor_error_bound():
    """Taylor polynomial error bound"""
    # f(x) = e^x, T₃(x) at 0, error bound for |x| ≤ 0.1
    # R₄(x) = e^ξ · x⁴/4! for some ξ between 0 and x
    # |R₄(x)| ≤ e^{0.1} · (0.1)⁴/24 < 1.1052 · 10^{-6}
    
    return problem(
        problem_tex="\\text{Use the Taylor remainder theorem to bound the error of } e^x \\approx 1 + x + x^2/2 \\text{ for } |x| \\leq 0.1.",
        answer_tex="|R_3(x)| \\leq \\dfrac{e^{0.1} \\cdot (0.1)^3}{6} \\approx 0.00018",
        answer_norm="R3<=0.00018",
        steps=[
            step("Taylor remainder formula", "R_n(x) = \\dfrac{f^{(n+1)}(\\xi)}{(n+1)!}(x-a)^{n+1} \\text{ for some } \\xi \\in (a, x)"),
            step("For e^x", "f^{(k)}(x) = e^x, \\text{ so } |f^{(4)}(\\xi)| \\leq e^{0.1} < 1.11"),
            step("Error bound", "|R_3(x)| = \\dfrac{|e^\\xi x^3|}{6} \\leq \\dfrac{e^{0.1}(0.1)^3}{6} \\approx 0.00018"),
        ],
    )


def _midpoint_trapezoid_error():
    """Error in numerical integration"""
    # ∫₀¹ x² dx with n=4 subintervals
    # Trapezoid error: -(b-a)³f''(ξ)/(12n²) = -1³·2/(12·16) = -1/96 ≈ -0.0104
    # Actual error: 1/3 - 0.3125 = 0.0210...
    
    return problem(
        problem_tex="\\text{Estimate the error of the Trapezoidal rule with } n=4 \\text{ for } \\int_0^1 x^2 dx.",
        answer_tex="|E_T| \\leq \\dfrac{(1)^3 \\cdot 2}{12 \\cdot 16} = \\dfrac{1}{96} \\approx 0.0104",
        answer_norm="error<=0.0104",
        steps=[
            step("Trapezoidal error bound", "|E_T| \\leq \\dfrac{(b-a)^3 \\max|f''(x)|}{12n^2}"),
            step("For f(x)=x²", "f'(x) = 2x, \\quad f''(x) = 2, \\quad \\max_{[0,1]} |f''| = 2"),
            step("Plug in values", "|E_T| \\leq \\dfrac{1 \\cdot 2}{12 \\cdot 16} = \\dfrac{1}{96} \\approx 0.0104"),
            step("Compare to actual", "\\int_0^1 x^2 dx = 1/3 \\approx 0.3333, T_4 = 0.34375, |E_T| = 0.0104 \\checkmark"),
        ],
    )


# ── numerical_methods5 — combined / advanced ──────────────────────────────────

def _bisection_vs_newton():
    """Compare bisection vs Newton for specific function"""
    # f(x) = x³ - x - 1 has root at ~1.3247
    # Bisection needs ~14 iterations for 0.001 tolerance
    # Newton with x₀=1.5: x₁ = 1.5 - (2.375-1.5-1)/(6.75-1) ≈ 1.3478
    # x₂ = 1.3478 - (0.444-...)/... ≈ ...
    
    return problem(
        problem_tex="\\text{Why might Newton's method diverge for } f(x) = x^3 - 3x + 1 \\text{ with } x_0 = 0.5?",
        answer_tex="f'(0.5) = -2.25, f(0.5) = -0.375 \\implies x_1 = 0.5 - (-0.375)/(-2.25) = 0.333 \\dots \\text{ (oscillates)}",
        answer_norm="oscillatory",
        steps=[
            step("Check Newton iteration", "x_{n+1} = x_n - f(x_n)/f'(x_n) = x_n - (x_n^3-3x_n+1)/(3x_n^2-3)"),
            step("At x_0 = 0.5", "x_1 = 0.5 - (-0.375)/(-2.25) = 0.333"),
            step("At x_1 = 0.333", "f(0.333) \\approx -0.037, f'(0.333) \\approx -2.667 \\implies x_2 = 0.333 - (-0.037)/(-2.667) \\approx 0.319"),
            step("Analysis", "\\text{Near } x=0, f'(x) \\approx -3, f(x) \\approx 1 \\implies \\text{Newton stays near 0 instead of converging}"),
        ],
    )


numerical_methods1 = [_bisection_basic, _bisection_convergence]
numerical_methods2 = [_newton_basic, _newton_convergence_order]
numerical_methods3 = [_secant_basic]
numerical_methods4 = [_taylor_error_bound, _midpoint_trapezoid_error]
numerical_methods5 = [_bisection_vs_newton]

POOLS = {1: numerical_methods1, 2: numerical_methods2, 3: numerical_methods3, 4: numerical_methods4, 5: numerical_methods5}