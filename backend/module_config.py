MODULES = {
    # ── Tier 0: Foundational ──
    "polynomials":         {"tier": 0, "label": "Polynomials",                "group": "algebra"},
    "linear_equations":    {"tier": 0, "label": "Linear Equations",          "group": "algebra"},
    "sequences":           {"tier": 0, "label": "Sequences & Series",        "group": "algebra"},

    # ── Tier 1: Requires Polynomials ──
    "factoring":           {"tier": 1, "label": "Factoring",                 "group": "algebra"},
    "quadratic":           {"tier": 1, "label": "Quadratic Equations",       "group": "algebra"},

    # ── Tier 2: Requires basic algebra ──
    "exponents":           {"tier": 2, "label": "Exponents",                 "group": "algebra"},
    "radicals":            {"tier": 2, "label": "Radicals",                  "group": "algebra"},
    "fractions":           {"tier": 2, "label": "Fractions",                 "group": "algebra"},

    # ── Tier 3: Requires Factoring, Fractions, Exponents ──
    "rational_expressions": {"tier": 3, "label": "Rational Expressions",     "group": "algebra"},
    "inequalities":        {"tier": 3, "label": "Inequalities",              "group": "algebra"},
    "absolute_value":      {"tier": 3, "label": "Absolute Value",            "group": "algebra"},

    # ── Tier 4: Requires Linear Eq, Quadratic, Fractions ──
    "systems":             {"tier": 4, "label": "Systems of Equations",      "group": "algebra"},
    "probability":         {"tier": 4, "label": "Probability",               "group": "algebra"},

    # ── Tier 5: Precalculus ──
    "trig":                {"tier": 5, "label": "Trig & Unit Circle",        "group": "precalc"},

    # ── Tier 6: Requires Exponents ──
    "logs":                {"tier": 6, "label": "Logarithms",                "group": "precalc"},

    # ── Tier 7: Requires Trig, Logs ──
    "composition":         {"tier": 7, "label": "Function Composition",      "group": "precalc"},

    # ── Tier 8: Requires Composition ──
    "limits":              {"tier": 8, "label": "Limits",                    "group": "calc1"},

    # ── Tier 9: Requires Limits, Polynomials, Rational Expressions ──
    "asymptotes":          {"tier": 9, "label": "Asymptotes",                "group": "calc1"},
    "epsilon_delta":       {"tier": 9, "label": "Epsilon-Delta",             "group": "calc1"},

    # ── Tier 10: Requires Limits ──
    "derivatives":         {"tier": 10, "label": "Derivatives",              "group": "calc1"},

    # ── Tier 11: Requires Derivatives, Inequalities ──
    "increasing_decreasing": {"tier": 11, "label": "Increasing/Decreasing",  "group": "calc1"},
    "extrema":             {"tier": 11, "label": "Extrema & Optimization",   "group": "calc1"},

    # ── Tier 12: Requires Derivatives ──
    "integration":         {"tier": 12, "label": "Integration",              "group": "calc1"},

    # ── Tier 13: Requires Derivatives, Limits ──
    "mvt":                 {"tier": 13, "label": "Mean Value Theorem",        "group": "calc1"},
    "numerical_methods":   {"tier": 13, "label": "Numerical Methods",         "group": "calc1"},

    # ── Tier 14: Requires Limits, Derivatives, Trig, Logs ──
    "indeterminate_forms": {"tier": 14, "label": "L'Hospital's Rule",         "group": "calc1"},

    # ── Tier 15: Requires Derivatives, Exponents, Trig ──
    "hyperbolic_apps":     {"tier": 15, "label": "Hyperbolic Functions",      "group": "calc1"},

    # ── Tier 16: Requires Integration, Derivatives ──
    "function_construction": {"tier": 16, "label": "Function Construction",   "group": "calc1"},
    "center_of_mass":      {"tier": 16, "label": "Center of Mass",            "group": "calc1"},

    # ── Tier 17: Requires Integration ──
    "adv_integration":     {"tier": 17, "label": "Advanced Integration",      "group": "calc2"},
}

UNLOCK_TIERS = [
    ["polynomials", "linear_equations", "sequences"],
    ["factoring", "quadratic"],
    ["exponents", "radicals", "fractions"],
    ["rational_expressions", "inequalities", "absolute_value"],
    ["systems", "probability"],
    ["trig"],
    ["logs"],
    ["composition"],
    ["limits"],
    ["asymptotes", "epsilon_delta"],
    ["derivatives"],
    ["increasing_decreasing", "extrema"],
    ["integration"],
    ["mvt", "numerical_methods"],
    ["indeterminate_forms"],
    ["hyperbolic_apps"],
    ["function_construction", "center_of_mass"],
    ["adv_integration"],
]
