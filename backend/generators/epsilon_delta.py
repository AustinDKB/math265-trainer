from math_utils import R, pick
from problem_builder import problem, step

# ── epsilon_delta1 — basic epsilon-delta ───────────────────────────────────────

def _epsilon_delta_basic():
    """Prove lim f(x) = L using epsilon-delta definition"""
    # lim x→2 (3x-1) = 5
    # Need |3x-1 - 5| = |3x-6| = 3|x-2| < ε
    # So if |x-2| < ε/3, then choose δ = ε/3
    
    return problem(
        problem_tex="\\text{Prove } \\lim_{{x \\to 2}} (3x - 1) = 5 \\text{ using the } \\varepsilon-\\delta \\text{ definition.}",
        answer_tex="\\text{Given } \\varepsilon > 0, \\text{ choose } \\delta = \\varepsilon/3. \\text{ Then } |x-2| < \\delta \\implies |3x-1-5| = 3|x-2| < 3\\delta = \\varepsilon.",
        answer_norm="delta=epsilon/3",
        steps=[
            step("Start with target", "|3x-1-5| = |3x-6| = 3|x-2|"),
            step("Relate to epsilon", "3|x-2| < \\varepsilon \\iff |x-2| < \\varepsilon/3"),
            step("Choose delta", "\\delta = \\varepsilon/3"),
            step("Verify", "|x-2| < \\delta \\implies 3|x-2| < 3\\delta = \\varepsilon"),
        ],
    )


def _epsilon_delta_quadratic():
    """Epsilon-delta for quadratic"""
    # lim x→1 (x²+2) = 3
    # |x²+2-3| = |x²-1| = |x-1||x+1|
    # If |x-1| < 1, then |x+1| < 3
    # So |x-1||x+1| < 3|x-1| < ε → |x-1| < min(1, ε/3)
    
    return problem(
        problem_tex="\\text{Prove } \\lim_{{x \\to 1}} (x^2 + 2) = 3 \\text{ using } \\varepsilon-\\delta.",
        answer_tex="|x^2-1| = |x-1||x+1|. \\text{ If } |x-1| < 1, \\text{ then } |x+1| < 3. \\text{ Choose } \\delta = \\min\\{{1, \\varepsilon/3\\}}.",
        answer_norm="delta=min(1,epsilon/3)",
        steps=[
            step("Set up", "|x^2+2-3| = |x^2-1| = |x-1||x+1|"),
            step("Bound |x+1|", "|x-1| < 1 \\implies -1 < x-1 < 1 \\implies 1 < x < 2 \\implies 2 < x+1 < 3 \\implies |x+1| < 3"),
            step("Choose delta", "\\delta = \\min(1, \\varepsilon/3) \\implies |x-1||x+1| < 3|x-1| < \\varepsilon"),
        ],
    )


# ── epsilon_delta2 — finding delta given epsilon ────────────────────────────────

def _find_delta():
    """Find delta for given epsilon"""
    # For lim x→3 (2x+1)=7, given ε=0.1
    # |2x+1-7| = 2|x-3| < 0.1 → |x-3| < 0.05, so δ = 0.05
    
    return problem(
        problem_tex="\\text{Find } \\delta > 0 \\text{ such that } |2x+1-7| < 0.1 \\text{ whenever } 0 < |x-3| < \\delta.",
        answer_tex="\\delta = 0.05",
        answer_norm="delta=0.05",
        steps=[
            step("Start", "|2x+1-7| = 2|x-3|"),
            step("Set less than epsilon", "2|x-3| < 0.1 \\implies |x-3| < 0.05"),
            step("Conclusion", "\\delta = 0.05"),
        ],
    )


# ── epsilon_delta3 — one-sided limits ──────────────────────────────────────────

def _one_sided_epsilon_delta():
    """Epsilon-delta for one-sided limit"""
    # lim x→0⁺ √x = 0
    # |√x - 0| = √x < ε → x < ε²
    # Also need x < δ, so choose δ = ε²
    
    return problem(
        problem_tex="\\text{Prove } \\lim_{{x \\to 0^+}} \\sqrt{x} = 0 \\text{ using } \\varepsilon-\\delta.",
        answer_tex="\\text{Choose } \\delta = \\varepsilon^2. \\text{ Then } 0 < x < \\delta \\implies \\sqrt{x} < \\sqrt{\\delta} = \\varepsilon.",
        answer_norm="delta=epsilon^2",
        steps=[
            step("Set up", "|\\sqrt{x} - 0| = \\sqrt{x}"),
            step("Require", "\\sqrt{x} < \\varepsilon \\iff x < \\varepsilon^2"),
            step("Choose delta", "\\delta = \\varepsilon^2"),
            step("Verify", "0 < x < \\delta \\implies \\sqrt{x} < \\sqrt{\\delta} = \\varepsilon"),
        ],
    )


# ── epsilon_delta4 — limit does not exist ──────────────────────────────────────

def _limit_dne_epsilon_delta():
    """Show limit DNE via epsilon-delta"""
    # Show lim x→0 (1 if x>0 else -1) DNE
    # For L=1: ε=0.5 → no δ works because near 0 from left, f(x)=-1
    # |f(x)-1| = 2 ≥ 0.5 = ε for x<0 near 0
    
    return problem(
        problem_tex="\\text{Show that } \\lim_{{x \\to 0}} f(x) \\text{ DNE where } f(x) = 1 \\text{ if } x > 0, f(x) = -1 \\text{ if } x \\leq 0.",
        answer_tex="\\text{For any } L, \\text{ choose } \\varepsilon = 0.5. \\text{ For any } \\delta > 0, \\text{ take } x = -\\delta/2 \\text{ and } x = \\delta/2. \\text{ Values differ by 2, can't both be within } 0.5.",
        answer_norm="dne",
        steps=[
            step("Strategy", "\\text{Show two sequences approach 0 giving different limits}"),
            step("x_n = -1/n", "\\lim_{n \\to \\infty} f(x_n) = -1"),
            step("y_n = 1/n", "\\lim_{n \\to \\infty} f(y_n) = 1"),
            step("Conclusion", "-1 \\neq 1, \\text{ so limit DNE}"),
        ],
    )


# ── epsilon_delta5 — advanced/combined ────────────────────────────────────────

def _epsilon_delta_squeeze():
    """Use squeeze theorem with epsilon-delta"""
    # lim x→0 x² sin(1/x) = 0
    # |x² sin(1/x) - 0| = x²|sin(1/x)| ≤ x²
    # If |x| < δ = √ε, then x² < ε
    
    return problem(
        problem_tex="\\text{Prove } \\lim_{{x \\to 0}} x^2 \\sin(1/x) = 0 \\text{ using } \\varepsilon-\\delta \\text{ and the squeeze theorem.}",
        answer_tex="|x^2 \\sin(1/x)| \\leq x^2. \\text{ Choose } \\delta = \\sqrt{\\varepsilon}. \\text{ Then } |x| < \\delta \\implies |x^2 \\sin(1/x)| \\leq x^2 < \\varepsilon.",
        answer_norm="delta=sqrt(epsilon)",
        steps=[
            step("Bound the function", "|x^2 \\sin(1/x)| \\leq x^2 \\cdot 1 = x^2"),
            step("Make x² < ε", "x^2 < \\varepsilon \\iff |x| < \\sqrt{\\varepsilon}"),
            step("Choose delta", "\\delta = \\sqrt{\\varepsilon}"),
            step("Verify", "|x| < \\delta \\implies x^2 < \\varepsilon \\implies |x^2 \\sin(1/x)| < \\varepsilon"),
        ],
    )


def _epsilon_delta_limit_of_difference():
    """Limit of difference"""
    # Show lim [x] (floor) limit DNE at integer
    # lim x→0⁺ [x] = 0, lim x→0⁻ [x] = -1
    
    return problem(
        problem_tex="\\text{Show that } \\lim_{{x \\to 0}} \\lfloor x \\rfloor \\text{ does not exist.}",
        answer_tex="\\lim_{x \\to 0^+} \\lfloor x \\rfloor = 0, \\quad \\lim_{x \\to 0^-} \\lfloor x \\rfloor = -1 \\implies \\text{limit DNE}",
        answer_norm="dne",
        steps=[
            step("Right-hand limit", "x \\to 0^+, \\lfloor x \\rfloor = 0 \\implies \\lim_{{x \\to 0^+}} = 0"),
            step("Left-hand limit", "x \\to 0^-, \\lfloor x \\rfloor = -1 \\implies \\lim_{{x \\to 0^-}} = -1"),
            step("Conclusion", "0 \\neq -1 \\implies \\text{limit DNE}"),
        ],
    )


epsilon_delta1 = [_epsilon_delta_basic, _epsilon_delta_quadratic]
epsilon_delta2 = [_find_delta]
epsilon_delta3 = [_one_sided_epsilon_delta]
epsilon_delta4 = [_limit_dne_epsilon_delta]
epsilon_delta5 = [_epsilon_delta_squeeze, _epsilon_delta_limit_of_difference]

POOLS = {1: epsilon_delta1, 2: epsilon_delta2, 3: epsilon_delta3, 4: epsilon_delta4, 5: epsilon_delta5}