from math_utils import R, pick, sign_str
from problem_builder import problem, step

# ── indeterminate_forms1 — L'Hospital's Rule basics ────────────────────────────

def _lhospital_0over0():
    """Basic 0/0 indeterminate form"""
    # lim x→0 sin(x)/x = 1 (by L'Hospital or known limit)
    
    return problem(
        problem_tex="\\lim_{x \\to 0} \\dfrac{\\sin(x)}{x}",
        answer_tex="1",
        answer_norm="1",
        steps=[
            step("Check form", "x \\to 0: \\dfrac{\\sin(0)}{0} = \\dfrac{0}{0} \\text{ (indeterminate)}"),
            step("Apply L'Hospital's Rule", "\\lim_{x \\to 0} \\dfrac{\\sin(x)}{x} = \\lim_{x \\to 0} \\dfrac{\\cos(x)}{1}"),
            step("Evaluate limit", "\\cos(0) = 1"),
        ],
    )


def _lhospital_inf_over_inf():
    """∞/∞ form"""
    # lim x→∞ x²/eˣ = 0 (apply L'Hospital twice)
    
    return problem(
        problem_tex="\\lim_{x \\to \\infty} \\dfrac{x^2}{e^x}",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("Check form", "x \\to \\infty: \\dfrac{\\infty}{\\infty} \\text{ (indeterminate)}"),
            step("Apply L'Hospital's Rule (1st time)", "\\lim_{x \\to \\infty} \\dfrac{x^2}{e^x} = \\lim_{x \\to \\infty} \\dfrac{2x}{e^x}"),
            step("Apply L'Hospital's Rule (2nd time)", "= \\lim_{x \\to \\infty} \\dfrac{2}{e^x}"),
            step("Evaluate", "e^\\infty = \\infty, \\dfrac{2}{\\infty} = 0"),
        ],
    )


# ── indeterminate_forms2 — more L'Hospital ─────────────────────────────────────

def _lhospital_trig():
    """Trig limit requiring L'Hospital"""
    # lim x→0 (1-cos(x))/x² = 1/2
    # = lim (sin(x))/(2x) = lim cos(x)/2 = 1/2
    
    return problem(
        problem_tex="\\lim_{x \\to 0} \\dfrac{1 - \\cos(x)}{x^2}",
        answer_tex="\\dfrac{1}{2}",
        answer_norm="1/2",
        steps=[
            step("Check form", "\\dfrac{1-1}{0} = \\dfrac{0}{0}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to 0} \\dfrac{\\sin(x)}{2x}"),
            step("Apply again (or use sin(x)/x limit)", "= \\lim_{x \\to 0} \\dfrac{\\cos(x)}{2} = \\dfrac{1}{2}"),
        ],
    )


def _lhospital_exp_log():
    """Exp/log indeterminate"""
    # lim x→∞ x/eˣ = 0
    
    return problem(
        problem_tex="\\lim_{x \\to \\infty} \\dfrac{x}{e^x}",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("Check form", "\\dfrac{\\infty}{\\infty}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to \\infty} \\dfrac{1}{e^x}"),
            step("Evaluate", "\\dfrac{1}{\\infty} = 0"),
        ],
    )


# ── indeterminate_forms3 — other indeterminate forms 0·∞, ∞-∞ ─────────────────

def _product_0timesinf():
    """0·∞ form"""
    # lim x→0⁺ x ln(x) = lim ln(x)/(1/x) = lim (-x) = 0
    # Apply L'Hospital to x ln(x) rewritten as ln(x)/(1/x)
    
    return problem(
        problem_tex="\\lim_{x \\to 0^+} x \\ln(x)",
        answer_tex="0",
        answer_norm="0",
        steps=[
            step("Rewrite as quotient", "x \\ln(x) = \\dfrac{\\ln(x)}{1/x} \\text{ as } x \\to 0^+ \\implies \\dfrac{-\\infty}{\\infty}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to 0^+} \\dfrac{1/x}{-1/x^2} = \\lim_{x \\to 0^+} (-x)"),
            step("Evaluate", "= 0"),
        ],
    )


def _difference_inf_minus_inf():
    """∞ - ∞ form"""
    # lim x→0 (1/x² - 1/sin²(x))
    # = lim x→0 (sin²(x) - x²)/(x² sin²(x))
    # This is 0/0, apply Taylor: sin(x) = x - x³/6 + ...
    # sin²(x) = x² - x⁴/3 + ... so sin²(x) - x² ≈ -x⁴/3
    # denominator ≈ x⁴, so limit = -1/3
    
    return problem(
        problem_tex="\\lim_{x \\to 0} \\left(\\dfrac{1}{x^2} - \\dfrac{1}{\\sin^2(x)}\\right)",
        answer_tex="-\\dfrac{1}{3}",
        answer_norm="-1/3",
        steps=[
            step("Combine fractions", "= \\lim_{x \\to 0} \\dfrac{\\sin^2(x) - x^2}{x^2 \\sin^2(x)}"),
            step("Leading terms (Taylor)", "\\sin(x) = x - x^3/6 + O(x^5) \\implies \\sin^2(x) = x^2 - x^4/3 + O(x^6)"),
            step("Numerator", "\\sin^2(x) - x^2 = -x^4/3 + O(x^6)"),
            step("Denominator", "x^2 \\sin^2(x) = x^4 + O(x^6)"),
            step("Limit", "\\dfrac{-x^4/3}{x^4} = -\\dfrac{1}{3}"),
        ],
    )


# ── indeterminate_forms4 — 0⁰, ∞⁰, 1^∞ ──────────────────────────────────────────

def _power_indeterminate():
    """1^∞ form — use ln trick"""
    # lim x→0 (1+x)^{1/x} = e
    # ln: (1/x)·ln(1+x) → ln(1+x)/x → 1
    
    return problem(
        problem_tex="\\lim_{x \\to 0} (1 + x)^{1/x}",
        answer_tex="e",
        answer_norm="e",
        steps=[
            step("Take natural log", "L = \\lim_{x \\to 0} \\frac{1}{x} \\ln(1+x)"),
            step("Rewrite", "= \\lim_{x \\to 0} \\dfrac{\\ln(1+x)}{x}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to 0} \\dfrac{1/(1+x)}{1} = 1"),
            step("Exponentiate", "L = e^1 = e"),
        ],
    )


def _power_inf_0():
    """∞⁰ form"""
    # lim x→∞ x^{1/x} = 1
    # ln: (ln x)/x → 0
    
    return problem(
        problem_tex="\\lim_{x \\to \\infty} x^{1/x}",
        answer_tex="1",
        answer_norm="1",
        steps=[
            step("Take natural log", "L = \\lim_{x \\to \\infty} \\frac{\\ln(x)}{x}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to \\infty} \\frac{1/x}{1} = 0"),
            step("Exponentiate", "L = e^0 = 1"),
        ],
    )


# ── indeterminate_forms5 — combined / advanced ──────────────────────────────────

def _repeated_lhospital():
    """Apply L'Hospital multiple times"""
    # lim x→0 (x - sin(x))/x³ = 1/6
    # = lim (1-cos(x))/(3x²) = lim sin(x)/(6x) = 1/6
    
    return problem(
        problem_tex="\\lim_{x \\to 0} \\dfrac{x - \\sin(x)}{x^3}",
        answer_tex="\\dfrac{1}{6}",
        answer_norm="1/6",
        steps=[
            step("Check form", "\\dfrac{0-0}{0} = \\dfrac{0}{0}"),
            step("Apply L'Hospital's Rule (1st)", "= \\lim_{x \\to 0} \\dfrac{1 - \\cos(x)}{3x^2}"),
            step("Apply L'Hospital's Rule (2nd)", "= \\lim_{x \\to 0} \\dfrac{\\sin(x)}{6x}"),
            step("Use known limit sin(x)/x → 1", "= \\dfrac{1}{6}"),
        ],
    )


def _hospital_with_param():
    """L'Hospital with parameter"""
    a = pick([2, 3])
    sa = str(a)

    return problem(
        problem_tex="\\lim_{x \\to 0} \\dfrac{e^{" + sa + "x} - 1}{x}",
        answer_tex=sa,
        answer_norm=sa,
        steps=[
            step("Check form", "e^{0} - 1 = 0, \\dfrac{0}{0}"),
            step("Apply L'Hospital's Rule", "= \\lim_{x \\to 0} \\dfrac{" + sa + " e^{" + sa + "x}}{1}"),
            step("Evaluate at x=0", "= " + sa + " e^0 = " + sa),
        ],
    )


indeterminate_forms1 = [_lhospital_0over0, _lhospital_inf_over_inf]
indeterminate_forms2 = [_lhospital_trig, _lhospital_exp_log]
indeterminate_forms3 = [_product_0timesinf, _difference_inf_minus_inf]
indeterminate_forms4 = [_power_indeterminate, _power_inf_0]
indeterminate_forms5 = [_repeated_lhospital, _hospital_with_param]

POOLS = {1: indeterminate_forms1, 2: indeterminate_forms2, 3: indeterminate_forms3, 4: indeterminate_forms4, 5: indeterminate_forms5}