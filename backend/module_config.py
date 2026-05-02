MODULES = {
    # ── Algebra ──
    "factoring":       {"tier": 0, "label": "Factoring",                "group": "algebra"},
    "exponents":       {"tier": 0, "label": "Exponents",                "group": "algebra"},
    "fractions":       {"tier": 0, "label": "Fractions",                "group": "algebra"},

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
}

UNLOCK_TIERS = [
    ["factoring", "exponents", "fractions"],
    ["trig"],
    ["logs"],
    ["composition"],
    ["limits"],
    ["derivatives"],
    ["integration"],
    ["adv_integration"],
]