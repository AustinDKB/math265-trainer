from math_utils import R, pick
from problem_builder import problem, step

def _antiderivative_basic():
    return problem(
        problem_tex="f'(x) = 3x^2 + 2x, \\quad f(0) = 1. \\text{ Find } f(x).",
        answer_tex="f(x) = x^3 + x^2 + 1",
        answer_norm="f(x)=x^3+x^2+1",
        steps=[
            step("Integrate f'", "f(x) = \\int (3x^2 + 2x) \\, dx = x^3 + x^2 + C"),
            step("Use initial condition", "f(0) = 0 + 0 + C = 1 \\implies C = 1"),
            step("Write f(x)", "f(x) = x^3 + x^2 + 1"),
        ],
    )


def _antiderivative_with_condition():
    return problem(
        problem_tex="f'(x) = 2x + 1, \\quad f(1) = 3. \\text{ Find } f(x).",
        answer_tex="f(x) = x^2 + x + 1",
        answer_norm="f(x)=x^2+x+1",
        steps=[
            step("Integrate", "f(x) = \\int (2x+1) \\, dx = x^2 + x + C"),
            step("Apply condition", "f(1) = 1 + 1 + C = 3 \\implies C = 1"),
            step("Result", "f(x) = x^2 + x + 1"),
        ],
    )


def _second_antiderivative():
    return problem(
        problem_tex="f''(x) = 6x, \\quad f'(0) = 2, \\quad f(0) = 1. \\text{ Find } f(x).",
        answer_tex="f(x) = x^3 + 2x + 1",
        answer_norm="f(x)=x^3+2x+1",
        steps=[
            step("Integrate f''", "f'(x) = \\int 6x \\, dx = 3x^2 + C"),
            step("Use f'(0)=2", "f'(0) = C = 2 \\implies C = 2"),
            step("Integrate f'", "f(x) = \\int (3x^2+2) \\, dx = x^3 + 2x + D"),
            step("Use f(0)=1", "f(0) = D = 1 \\implies D = 1"),
            step("Result", "f(x) = x^3 + 2x + 1"),
        ],
    )


def _velocity_from_acceleration():
    return problem(
        problem_tex="a(t) = t^2 - 3t + 2, \\quad v(0) = 1. \\text{ Find } v(t).",
        answer_tex="v(t) = \\dfrac{t^3}{3} - \\dfrac{3t^2}{2} + 2t + 1",
        answer_norm="v(t)=t^3/3-3t^2/2+2t+1",
        steps=[
            step("Integrate acceleration", "v(t) = \\int (t^2-3t+2) \\, dt = \\frac{t^3}{3} - \\frac{3t^2}{2} + 2t + C"),
            step("Use v(0)=1", "C = 1"),
            step("Result", "v(t) = \\frac{t^3}{3} - \\frac{3t^2}{2} + 2t + 1"),
        ],
    )


def _position_from_velocity():
    return problem(
        problem_tex="v(t) = 3t^2 + 1, \\quad s(0) = 2. \\text{ Find } s(t).",
        answer_tex="s(t) = t^3 + t + 2",
        answer_norm="s(t)=t^3+t+2",
        steps=[
            step("Integrate velocity", "s(t) = \\int (3t^2+1) \\, dt = t^3 + t + C"),
            step("Use s(0)=2", "C = 2"),
            step("Result", "s(t) = t^3 + t + 2"),
        ],
    )


def _exponential_growth():
    k = pick([0.1, 0.2, 0.5, -0.3])
    P0 = pick([100, 50, 200])
    return problem(
        problem_tex=f"P'(t) = {k}P, \\quad P(0) = {P0}. \\text{{ Solve for }} P(t).",
        answer_tex=f"P(t) = {P0} e^{{{k}t}}",
        answer_norm=f"P(t)={P0}*e^({k}*t)",
        steps=[
            step("Separate variables", f"\\frac{{dP}}{{P}} = {k} \\, dt"),
            step("Integrate", f"\\ln|P| = {k}t + C"),
            step("Exponentiate", f"P(t) = C' e^{{{k}t}}"),
            step("Use P(0)=P0", f"C' = {P0}"),
            step("Result", f"P(t) = {P0} e^{{{k}t}}"),
        ],
    )


def _newtons_law_cooling():
    T0 = pick([90, 80, 100])
    T_env = pick([20, 22, 25])
    k = pick([0.1, 0.2])
    return problem(
        problem_tex=f"T'(t) = -{k}(T - {T_env}), \\quad T(0) = {T0}. \\text{{ Solve for }} T(t).",
        answer_tex=f"T(t) = {T_env} + ({T0-T_env})e^{{-{k}t}}",
        answer_norm=f"T(t)={T_env}+({T0-T_env})*e^(-{k}*t)",
        steps=[
            step("Rewrite", f"T' = -{k}(T - {T_env})"),
            step("Let u = T - T_env", f"u' = -{k}u"),
            step("Solve", f"u(t) = u_0 e^{{-{k}t}} = ({T0-T_env})e^{{-{k}t}}"),
            step("Back-substitute", f"T(t) = {T_env} + ({T0-T_env})e^{{-{k}t}}"),
        ],
    )


def _build_sine_wave():
    return problem(
        problem_tex="f'(x) = 2\\cos(x) - 1, \\quad f(0) = 3. \\text{ Find } f(x).",
        answer_tex="f(x) = 2\\sin(x) - x + 3",
        answer_norm="f(x)=2*sin(x)-x+3",
        steps=[
            step("Integrate", "f(x) = \\int (2\\cos(x)-1) \\, dx = 2\\sin(x) - x + C"),
            step("Apply f(0)=3", "2\\sin(0) - 0 + C = 3 \\implies C = 3"),
            step("Result", "f(x) = 2\\sin(x) - x + 3"),
        ],
    )


function_construction1 = [_antiderivative_basic, _antiderivative_with_condition]
function_construction2 = [_second_antiderivative]
function_construction3 = [_velocity_from_acceleration, _position_from_velocity]
function_construction4 = [_exponential_growth, _newtons_law_cooling]
function_construction5 = [_build_sine_wave]

POOLS = {1: function_construction1, 2: function_construction2, 3: function_construction3, 4: function_construction4, 5: function_construction5}