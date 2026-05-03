from math_utils import R, pick
from problem_builder import problem, step

# ── center_of_mass1 — 1D discrete ──────────────────────────────────────────────

def _cm_discrete_basic():
    """Center of mass of discrete point masses"""
    # masses at x=1 (m=2), x=3 (m=4), x=7 (m=6)
    # x_cm = (2·1 + 4·3 + 6·7)/(2+4+6) = (2+12+42)/12 = 56/12 = 14/3 ≈ 4.67
    
    return problem(
        problem_tex="\\text{Find the center of mass of masses } m_1=2 \\text{ at } x_1=1, m_2=4 \\text{ at } x_2=3, m_3=6 \\text{ at } x_3=7.",
        answer_tex="x_{\\text{cm}} = \\dfrac{14}{3} \\approx 4.67",
        answer_norm="14/3",
        steps=[
            step("Total mass", "M = 2 + 4 + 6 = 12"),
            step("Weighted sum", "2 \\cdot 1 + 4 \\cdot 3 + 6 \\cdot 7 = 2 + 12 + 42 = 56"),
            step("Compute x_cm", "x_{\\text{cm}} = 56/12 = 14/3"),
        ],
    )


def _cm_discrete_two_mass():
    """Two mass system"""
    m1 = pick([3, 4, 5])
    m2 = pick([1, 2, 3])
    x1 = pick([0, 1])
    x2 = pick([4, 5, 6])
    
    return problem(
        problem_tex=f"\\text{{Masses }} m_1={m1} \\text{{ at }} x_1={x1}, m_2={m2} \\text{{ at }} x_2={x2}. \\text{{ Find center of mass.}}",
        answer_tex=f"x_{{\\text{{cm}}}} = \\dfrac{{{m1*x1 + m2*x2}}}{{{m1+m2}}} = \\dfrac{{{m1*x1 + m2*x2}}}{{{m1+m2}}}",
        answer_norm=f"{(m1*x1 + m2*x2)/(m1+m2)}",
        steps=[
            step("Total mass", f"M = {m1} + {m2} = {m1+m2}"),
            step("Weighted position", f"{m1}\\cdot{x1} + {m2}\\cdot{x2} = {m1*x1 + m2*x2}"),
            step("Center of mass", f"x_{{cm}} = \\dfrac{{{m1*x1 + m2*x2}}}{{{m1+m2}}}"),
        ],
    )


# ── center_of_mass2 — 1D continuous rod ───────────────────────────────────────

def _cm_rod_variable_density():
    """Rod with variable density"""
    # Rod on [0, 4] with density δ(x) = x (mass per unit length)
    # mass = ∫₀⁴ x dx = 16/2 = 8
    # moment = ∫₀⁴ x·x dx = ∫₀⁴ x² dx = 64/3
    # x_cm = (64/3)/8 = 8/3
    
    return problem(
        problem_tex="\\text{A rod on } [0, 4] \\text{ has density } \\delta(x) = x. \\text{ Find its center of mass.}",
        answer_tex="x_{\\text{cm}} = \\dfrac{8}{3}",
        answer_norm="8/3",
        steps=[
            step("Total mass", "M = \\int_0^4 x \\, dx = \\frac{x^2}{2}\\bigg|_0^4 = 8"),
            step("First moment", "M_x = \\int_0^4 x \\cdot x \\, dx = \\int_0^4 x^2 \\, dx = \\frac{x^3}{3}\\bigg|_0^4 = \\frac{64}{3}"),
            step("Center of mass", "x_{\\text{cm}} = M_x/M = \\frac{64/3}{8} = \\frac{8}{3}"),
        ],
    )


def _cm_rod_constant_density():
    """Rod with constant density"""
    # Rod [0, L] with constant density ρ
    # mass = ρL, moment = ρ∫₀ᴸ x dx = ρL²/2
    # x_cm = (ρL²/2)/(ρL) = L/2
    
    L = pick([2, 3, 4, 5])
    
    return problem(
        problem_tex=f"\\text{{Rod on }} [0, {L}] \\text{{ with constant density }} \\delta(x) = 3. \\text{{ Find center of mass.}}",
        answer_tex=f"x_{{\\text{{cm}}}} = \\dfrac{{{L}}}{{2}}",
        answer_norm=f"{L}/2",
        steps=[
            step("Total mass", f"M = \\int_0^{L} 3 \\, dx = 3{L}"),
            step("First moment", f"M_x = \\int_0^{L} 3x \\, dx = 3 \\cdot \\frac{{L^2}}{{2}} = \\frac{{3L^2}}{{2}}"),
            step("Center of mass", f"x_{{cm}} = \\frac{{3L^2/2}}{{3L}} = \\frac{{L}}{{2}}"),
        ],
    )


# ── center_of_mass3 — 2D lamina ────────────────────────────────────────────────

def _cm_lamina_rectangle():
    """CM of uniform rectangle"""
    # Rectangle [0,a]×[0,b] with constant density ρ
    # By symmetry, CM is at the center: (a/2, b/2)
    
    a = pick([2, 3, 4])
    b = pick([1, 3, 5])
    
    return problem(
        problem_tex=f"\\text{{Uniform rectangle }} [0, {a}] \\times [0, {b}] \\text{{ with density }}\\delta = 2. \\text{{ Find center of mass.}}",
        answer_tex=f"(\\dfrac{{{a}}}{{2}}, \\dfrac{{{b}}}{{2}})",
        answer_norm=f"({a}/2,{b}/2)",
        steps=[
            step("By symmetry", "\\text{Both x and y coordinates are at the centroid of the region}"),
            step("x_cm", f"\\dfrac{{1}}{{Area}} \\int_0^{a} \\int_0^{b} x \\, dy \\, dx = \\dfrac{{1}}{{{a}{b}}} \\cdot {a}^2{b}/2 = {a}/2"),
            step("y_cm", f"\\dfrac{{1}}{{Area}} \\int_0^{a} \\int_0^{b} y \\, dy \\, dx = {b}/2"),
        ],
    )


def _cm_lamina_triangular():
    """CM of triangular lamina"""
    # Triangle with vertices (0,0), (b,0), (0,h) constant density
    # x_cm = b/3, y_cm = h/3
    
    b = pick([3, 4])
    h = pick([2, 3, 4])
    
    return problem(
        problem_tex=f"\\text{{Triangle with vertices (0,0), ({b},0), (0,{h}) and constant density. Find center of mass.}}",
        answer_tex=f"(\\dfrac{{{b}}}{{3}}, \\dfrac{{{h}}}{{3}})",
        answer_norm=f"({b}/3,{h}/3)",
        steps=[
            step("Area of triangle", f"A = \\frac{{1}}{{2}}{b}{h}"),
            step("x_cm formula", f"x_cm = \\frac{{1}}{{A}} \\int_0^{b} \\int_0^{{h(1-x/{b})}} x \\, dy \\, dx = \\frac{{b}}{{3}}"),
            step("y_cm formula", f"y_cm = \\frac{{1}}{{A}} \\int_0^{b} \\int_0^{{h(1-x/{b})}} y \\, dy \\, dx = \\frac{{h}}{{3}}"),
        ],
    )


# ── center_of_mass4 — with gravitation ────────────────────────────────────────

def _cm_with_tension():
    """Find balance point with lever"""
    # Mass m1 at distance d1 from fulcrum, m2 at d2
    # m1·d1 = m2·d2 → balance
    
    m1 = pick([4, 6, 8])
    m2 = pick([2, 3, 4])
    d1 = pick([2, 3])
    # m2*d2 = m1*d1 → d2 = m1*d1/m2
    
    d2 = m1 * d1 / m2
    
    return problem(
        problem_tex=f"\\text{{Mass }} {m1} \\text{{ kg at distance }} {d1} \\text{{ m from fulcrum. Where should mass }} {m2} \\text{{ kg be placed to balance?}}",
        answer_tex=f"d_2 = \\dfrac{{{m1*d1}}}{{{m2}}} = {d2} \\text{{ m}}",
        answer_norm=f"d2={d2}",
        steps=[
            step("Torque balance condition", f"\\tau_1 = \\tau_2 \\implies {m1} \\cdot {d1} = {m2} \\cdot d_2"),
            step("Solve for d_2", f"d_2 = \\dfrac{{{m1*d1}}}{{{m2}}} = {d2}"),
            step("Check", f"{m1}({d1}) = {m2}({d2}) = {m1*d1}"),
        ],
    )


# ── center_of_mass5 — Pappus's theorem ────────────────────────────────────────

def _pappus_centroid():
    """Use Pappus's centroid theorem for volume of revolution"""
    # Rectangle [a,b]×[0,h] rotated about x-axis
    # Volume = (area)·(distance traveled by centroid) = (b-a)·h · 2π·(h/2)
    # = (b-a)·h²·π
    
    b = pick([3, 4])
    h = pick([2, 3])
    a = 0
    
    return problem(
        problem_tex=f"\\text{{Region }} [{a},{b}] \\times [0,{h}] \\text{{ rotated about x-axis. Find volume using Pappus.}}",
        answer_tex=f"V = \\pi {h} \\cdot ({b}-{a}) \\cdot {h} = \\pi ({b}-{a}){h}^2",
        answer_norm=f"V=pi*({b}-{a})*{h}^2",
        steps=[
            step("Area of region", f"A = ({b}-{a}) \\cdot {h}"),
            step("Centroid y-coordinate", f"\\bar{{y}} = {h}/2"),
            step("Distance traveled by centroid", f"2\\pi \\bar{{y}} = 2\\pi \\cdot {h}/2 = \\pi{h}"),
            step("Pappus's theorem", f"V = A \\cdot 2\\pi\\bar{{y}} = ({b}-{a}){h} \\cdot \\pi{h} = \\pi({b}-{a}){h}^2"),
        ],
    )


center_of_mass1 = [_cm_discrete_basic, _cm_discrete_two_mass]
center_of_mass2 = [_cm_rod_variable_density, _cm_rod_constant_density]
center_of_mass3 = [_cm_lamina_rectangle, _cm_lamina_triangular]
center_of_mass4 = [_cm_with_tension]
center_of_mass5 = [_pappus_centroid]

POOLS = {1: center_of_mass1, 2: center_of_mass2, 3: center_of_mass3, 4: center_of_mass4, 5: center_of_mass5}