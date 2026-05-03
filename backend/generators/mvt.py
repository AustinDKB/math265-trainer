from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── mvt1 — Mean Value Theorem ─────────────────────────────────────────────────

def _mvt_basic():
    """Verify MVT conditions and find c for f on [a,b]"""
    # f(x) = x² on [1, 3]
    # f'(x) = 2x
    # f(1) = 1, f(3) = 9
    # (f(3)-f(1))/(3-1) = 8/2 = 4
    # f'(c) = 2c = 4 → c = 2
    
    return problem(
        problem_tex="f(x) = x^2 \\text{ on } [1, 3]. \\text{ Find } c \\text{ in } (1, 3) \\text{ such that } f'(c) = \\dfrac{f(3)-f(1)}{3-1}.",
        answer_tex="c = 2",
        answer_norm="c=2",
        steps=[
            step("Compute average rate of change", "\\dfrac{f(3)-f(1)}{3-1} = \\dfrac{9-1}{2} = 4"),
            step("Find f'(x)", "f'(x) = 2x"),
            step("Set f'(c) = average rate", "2c = 4 \\implies c = 2"),
            step("Verify c in (1,3)", "2 \\in (1, 3) \\checkmark"),
        ],
    )


def _mvt_cubic():
    """MVT for cubic on symmetric-ish interval"""
    # f(x) = x³ - 3x on [-1, 2]
    # f'(x) = 3x² - 3
    # f(-1) = -1 + 3 = 2, f(2) = 8 - 6 = 2
    # (f(2)-f(-1))/(2-(-1)) = 0/3 = 0
    # f'(c) = 3c² - 3 = 0 → c = ±1, but c=1 is in (-1,2)
    
    return problem(
        problem_tex="f(x) = x^3 - 3x \\text{ on } [-1, 2]. \\text{ Find all } c \\text{ in } (-1, 2) \\text{ such that } f'(c) = \\dfrac{f(2)-f(-1)}{2-(-1)}.",
        answer_tex="c = 1",
        answer_norm="c=1",
        steps=[
            step("Compute average rate of change", "f(-1) = 2, \\quad f(2) = 2 \\implies \\dfrac{2-2}{3} = 0"),
            step("Find f'(x)", "f'(x) = 3x^2 - 3"),
            step("Set f'(c) = average rate", "3c^2 - 3 = 0 \\implies c^2 = 1 \\implies c = \\pm 1"),
            step("Check interval", "c = 1 \\in (-1, 2); \\quad c = -1 \\text{ is an endpoint, not in } (-1, 2)"),
        ],
    )


# ── mvt2 — Rolle's Theorem ─────────────────────────────────────────────────────

def _rolles_basic():
    """Rolle's Theorem — find c where f'(c)=0"""
    # f(x) = x² - 4x on [0, 4]
    # f(0) = 0, f(4) = 0
    # f'(x) = 2x - 4 = 0 → c = 2
    
    return problem(
        problem_tex="f(x) = x^2 - 4x \\text{ on } [0, 4]. \\text{ Verify Rolle's Theorem and find } c \\text{ such that } f'(c) = 0.",
        answer_tex="c = 2",
        answer_norm="c=2",
        steps=[
            step("Check continuity", "f(x) = x^2 - 4x \\text{ is a polynomial, continuous on } [0, 4] \\checkmark"),
            step("Check differentiability", "f'(x) = 2x - 4 \\text{ exists on } (0, 4) \\checkmark"),
            step("Check endpoints", "f(0) = 0, \\quad f(4) = 16 - 16 = 0 \\implies f(0) = f(4) \\checkmark"),
            step("Find c where f'(c) = 0", "2c - 4 = 0 \\implies c = 2"),
            step("Verify c in (0,4)", "2 \\in (0, 4) \\checkmark"),
        ],
    )


def _rolles_verify_conditions():
    """Verify Rolle's conditions are met"""
    # f(x) = sin(x) on [0, π]
    # f(0) = 0, f(π) = 0
    # f'(x) = cos(x) = 0 → c = π/2
    
    return problem(
        problem_tex="f(x) = \\sin(x) \\text{ on } [0, \\pi]. \\text{ Verify Rolle's Theorem conditions and find } c.",
        answer_tex="c = \\dfrac{\\pi}{2}",
        answer_norm="c=pi/2",
        steps=[
            step("Continuity", "\\sin(x) \\text{ is continuous on } [0, \\pi] \\checkmark"),
            step("Differentiability", "\\sin(x) \\text{ is differentiable on } (0, \\pi) \\checkmark"),
            step("Endpoint values", "f(0) = 0, \\quad f(\\pi) = 0 \\implies f(0) = f(\\pi) \\checkmark"),
            step("Find c", "f'(x) = \\cos(x) = 0 \\implies x = \\dfrac{\\pi}{2}"),
        ],
    )


# ── mvt3 — apply MVT to show relationship ─────────────────────────────────────

def _mvt_show_unique():
    """Show there is exactly one c satisfying MVT"""
    # f(x) = √x on [0, 4]
    # f'(x) = 1/(2√x)
    # (f(4)-f(0))/4 = 2/4 = 0.5
    # 1/(2√c) = 0.5 → √c = 1 → c = 1
    
    return problem(
        problem_tex="f(x) = \\sqrt{x} \\text{ on } [0, 4]. \\text{ Find the value } c \\text{ guaranteed by the Mean Value Theorem.}",
        answer_tex="c = 1",
        answer_norm="c=1",
        steps=[
            step("Average rate of change", "\\dfrac{f(4)-f(0)}{4-0} = \\dfrac{2-0}{4} = \\dfrac{1}{2}"),
            step("Find f'(x)", "f'(x) = \\dfrac{1}{2\\sqrt{x}}"),
            step("Set f'(c) = average rate", "\\dfrac{1}{2\\sqrt{c}} = \\dfrac{1}{2} \\implies \\sqrt{c} = 1 \\implies c = 1"),
            step("Verify c in (0,4)", "1 \\in (0, 4) \\checkmark"),
        ],
    )


def _mvt_comparison():
    """Use MVT to compare two function values"""
    # f(x) = x³ on [1, 2]
    # f'(x) = 3x² ≥ 3 on [1, 2]
    # by MVT, f(2) - f(1) = f'(c)(2-1) = f'(c) ≥ 3
    # so f(2) ≥ f(1) + 3 = 1 + 3 = 4, and indeed f(2) = 8
    
    return problem(
        problem_tex="f(x) = x^3. \\text{ Use the Mean Value Theorem to show } f(2) > f(1) + 2.",
        answer_tex="f(2) - f(1) = f'(c)(2-1) = 3c^2 \\geq 3 \\text{ for some } c \\in (1, 2) \\implies f(2) - f(1) > 2",
        answer_norm="f(2)-f(1)>2",
        steps=[
            step("Apply MVT on [1, 2]", f"f(2) - f(1) = f'(c)(2-1) = 3c^2 \\text{{ for some }} c \\in (1, 2)"),
            step("Lower bound on f'(c)", "c > 1 \\implies c^2 > 1 \\implies 3c^2 > 3 > 2"),
            step("Conclusion", "f(2) - f(1) > 2 \\implies f(2) > f(1) + 2"),
        ],
    )


# ── mvt4 — MVT corollary problems ─────────────────────────────────────────────

def _mvt_corollary_constant():
    """If f'=0 on interval then f is constant"""
    # Show f(x) = e^{x} - x² has f'(x) > something → not constant
    
    return problem(
        problem_tex="f(x) = e^x - x^2. \\text{ Show that } f'(x) > 0 \\text{ for all } x > 0.",
        answer_tex="f'(x) = e^x - 2x. \\text{ For } x > 0, e^x > 1 + x + x^2/2 > 2x \\text{ (by expansion)}",
        answer_norm="f'(x)>0",
        steps=[
            step("Differentiate", "f'(x) = e^x - 2x"),
            step("Use Taylor expansion", "e^x = 1 + x + x^2/2 + x^3/6 + \\dots > 1 + x + x^2/2"),
            step("Compare to 2x", "1 + x + x^2/2 > 2x \\iff 1 + x^2/2 > x \\iff x^2 - 2x + 2 > 0"),
            step("Discriminant check", "(x-1)^2 + 1 > 0 \\text{ always true}"),
            step("Conclusion", "f'(x) > 0 \\text{ for all } x > 0"),
        ],
    )


# ── mvt5 — combined / advanced ────────────────────────────────────────────────

def _mvt_trig():
    """MVT with trig function"""
    # f(x) = sin(x) on [0, π/6]
    # f'(x) = cos(x)
    # (f(π/6)-f(0))/(π/6-0) = (1/2-0)/(π/6) = 3/π
    # cos(c) = 3/π → c = arccos(3/π)
    
    return problem(
        problem_tex="f(x) = \\sin(x) \\text{ on } [0, \\frac{\\pi}{6}]. \\text{ Find } c \\text{ satisfying MVT.}",
        answer_tex="c = \\arccos\\left(\\dfrac{3}{\\pi}\\right)",
        answer_norm="c=arccos(3/pi)",
        steps=[
            step("Average rate of change", "\\dfrac{f(\\pi/6)-f(0)}{\\pi/6} = \\dfrac{1/2}{\\pi/6} = \\dfrac{3}{\\pi}"),
            step("Find f'(x)", "f'(x) = \\cos(x)"),
            step("Set f'(c) = average rate", "\\cos(c) = \\dfrac{3}{\\pi} \\implies c = \\arccos\\left(\\dfrac{3}{\\pi}\\right)"),
            step("Verify c in (0, π/6)", "3/π ≈ 0.955, so c ≈ 0.31 ∈ (0, π/6 ≈ 0.524) ✓"),
        ],
    )


def _mvt_ivt_combo():
    """Ivy/MVT combination: show there's a point with a specific derivative"""
    # f(x) = x³ on [-2, 2]
    # Average rate = (8-(-8))/4 = 16/4 = 4
    # f'(x) = 3x² = 4 → x = ±2/√3
    # Only c = 2/√3 is in (-2, 2)
    
    return problem(
        problem_tex="f(x) = x^3 \\text{ on } [-2, 2]. \\text{ Find } c \\text{ satisfying } f'(c) = \\dfrac{f(2)-f(-2)}{4}.",
        answer_tex="c = \\pm \\dfrac{2}{\\sqrt{3}}, \\quad c = \\dfrac{2}{\\sqrt{3}} \\text{ is in } (-2, 2)",
        answer_norm="c=2/sqrt(3)",
        steps=[
            step("Compute average rate of change", "f(2) = 8, f(-2) = -8 \\implies \\dfrac{8-(-8)}{4} = 4"),
            step("Find f'(x)", "f'(x) = 3x^2"),
            step("Set f'(c) = 4", "3c^2 = 4 \\implies c^2 = \\dfrac{4}{3} \\implies c = \\pm \\dfrac{2}{\\sqrt{3}}"),
            step("Check interval", "2/√3 ≈ 1.15 \\in (-2, 2) \\checkmark; \\quad -2/√3 \\approx -1.15 \\in (-2, 2) \\checkmark"),
        ],
    )


mvt1 = [_mvt_basic, _mvt_cubic]
mvt2 = [_rolles_basic, _rolles_verify_conditions]
mvt3 = [_mvt_show_unique, _mvt_comparison]
mvt4 = [_mvt_corollary_constant]
mvt5 = [_mvt_trig, _mvt_ivt_combo]

POOLS = {1: mvt1, 2: mvt2, 3: mvt3, 4: mvt4, 5: mvt5}