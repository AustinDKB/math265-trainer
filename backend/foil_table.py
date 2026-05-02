# ── Justify foil method lookup ──
# Maps a correct method → a plausible but incorrect alternative method.
# Used in justify mode to ask "why this method and not [foil]?"

JUSTIFY_FOILS = {
    # Calc 1
    "first_derivative_test": "related_rates",
    "related_rates": "first_derivative_test",
    "optimization": "related_rates",
    "u_substitution": "integration_by_parts",
    "integration_by_parts": "u_substitution",
    "disk_method": "shell_method",
    "shell_method": "disk_method",
    "washer_method": "shell_method",
    "chain_rule": "product_rule",
    "product_rule": "chain_rule",
    "quotient_rule": "product_rule",
    "implicit_differentiation": "chain_rule",
    "logarithmic_differentiation": "chain_rule",
    "lhopital": "factor_cancel",
    "factor_cancel": "lhopital",
    "direct_substitution": "lhopital",
    "riemann_sum": "ftc",
    "ftc": "riemann_sum",
    "linear_approximation": "taylor_series",
    "taylor_series": "linear_approximation",
    "bisection": "newtons_method",
    "newtons_method": "bisection",
    "epsilon_delta": "sequential_criterion",
    "mean_value_theorem": "rolles_theorem",
    "rolles_theorem": "mean_value_theorem",
    "trig_identity": "trig_substitution",
    "trig_substitution": "trig_identity",
    "partial_fractions": "u_substitution",
    "area_between_curves": "volume_revolution",
    "volume_revolution": "area_between_curves",
    "arc_length": "surface_area",
    "surface_area": "arc_length",
    "work_spring": "work_pump",
    "work_pump": "work_spring",
    # Algebra
    "factoring": "quadratic_formula",
    "quadratic_formula": "factoring",
    "complete_the_square": "quadratic_formula",
    "substitution": "elimination",
    "elimination": "substitution",
    "graphing": "substitution",
}

JUSTIFY_PROMPTS = {
    "contrast": "Solve. Then explain why {method} applies here and not {foil_method}.",
    "condition": "Solve. Then state the condition that makes {method} correct.",
    "pre_solve": "Before solving: identify the method and why. Then solve.",
}
