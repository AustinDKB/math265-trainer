MODULES = {
    # ── Algebra ──
    "factoring":       {"tier": 0, "label": "Factoring",                "group": "algebra"},
    "exponents":       {"tier": 0, "label": "Exponents",                "group": "algebra"},
    "fractions":       {"tier": 0, "label": "Fractions",                "group": "algebra"},

    # ── Algebra Phase 1 (WP5) ──
    "linear_equations":    {"tier": 0, "label": "Linear Equations",          "group": "algebra"},
    "quadratic":           {"tier": 0, "label": "Quadratic Equations",       "group": "algebra"},
    "polynomials":         {"tier": 0, "label": "Polynomials",                "group": "algebra"},
    "rational_expressions": {"tier": 0, "label": "Rational Expressions",       "group": "algebra"},
    "systems":             {"tier": 0, "label": "Systems of Equations",       "group": "algebra"},
    "absolute_value":      {"tier": 0, "label": "Absolute Value",             "group": "algebra"},
    "radicals":            {"tier": 0, "label": "Radicals",                   "group": "algebra"},
    "inequalities":        {"tier": 0, "label": "Inequalities",                "group": "algebra"},
    "sequences":           {"tier": 0, "label": "Sequences & Series",          "group": "algebra"},
    "probability":         {"tier": 0, "label": "Probability",                 "group": "algebra"},

    # ── Precalculus ──
    "trig":            {"tier": 1, "label": "Trig & Unit Circle",       "group": "precalc"},
    "logs":            {"tier": 2, "label": "Logarithms",               "group": "precalc"},
    "composition":     {"tier": 3, "label": "Function Composition",     "group": "precalc"},

    # ── Calculus 1 ──
    "limits":          {"tier": 4, "label": "Limits",                   "group": "calc1"},
    "derivatives":     {"tier": 5, "label": "Derivatives (Calc 1)",     "group": "calc1"},
    "integration":     {"tier": 6, "label": "Integration (Calc 1)",     "group": "calc1"},

    # ── Calculus 2 ──
    "adv_integration": {"tier": 7, "label": "Advanced Integration (Calc 2)", "group": "calc2"},

    # ── Calculus 1 Computational (WP4) ──
    "asymptotes":            {"tier": 4, "label": "Asymptotes",              "group": "calc1"},
    "increasing_decreasing": {"tier": 5, "label": "Inc/Dec & Extrema",       "group": "calc1"},
    "mvt":                   {"tier": 5, "label": "Mean Value Theorem",       "group": "calc1"},
    "numerical_methods":     {"tier": 5, "label": "Numerical Methods",        "group": "calc1"},
    "indeterminate_forms":   {"tier": 5, "label": "L'Hospital's Rule",        "group": "calc1"},
    "epsilon_delta":         {"tier": 5, "label": "Epsilon-Delta",            "group": "calc1"},
    "hyperbolic_apps":       {"tier": 6, "label": "Hyperbolic Functions",     "group": "calc1"},
    "center_of_mass":        {"tier": 6, "label": "Center of Mass",            "group": "calc1"},
    "function_construction": {"tier": 6, "label": "Function Construction",    "group": "calc1"},
    "extrema":               {"tier": 5, "label": "Extrema & Optimization",   "group": "calc1"},
}

UNLOCK_TIERS = [
    ["factoring", "exponents", "fractions", "linear_equations", "quadratic", "polynomials", "rational_expressions", "systems", "absolute_value", "radicals", "inequalities", "sequences", "probability"],
    ["trig"],
    ["logs"],
    ["composition"],
    ["limits", "asymptotes", "epsilon_delta", "indeterminate_forms"],
    ["derivatives", "increasing_decreasing", "mvt", "numerical_methods", "extrema"],
    ["integration", "hyperbolic_apps", "center_of_mass", "function_construction"],
    ["adv_integration"],
]