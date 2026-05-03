CHECKER_MAP = {}


def get_checker(module):
    if not CHECKER_MAP:
        from checker import (
            check_factoring_answer, check_exponent_answer, check_fraction_answer,
            check_norm_answer, check_integration_answer, check_exp_factoring_answer,
            check_trig_factoring_answer,
        )
        CHECKER_MAP.update({
            "factoring":       check_factoring_answer,
            "exponents":       check_exponent_answer,
            "fractions":       check_fraction_answer,
            "trig":            check_norm_answer,
            "logs":            check_norm_answer,
            "composition":     check_norm_answer,
            "limits":          check_norm_answer,
            "derivatives":     check_norm_answer,
            "integration":     check_integration_answer,
            "adv_integration": check_integration_answer,
            "asymptotes":            check_norm_answer,
            "increasing_decreasing": check_norm_answer,
            "extrema":               check_norm_answer,
            "mvt":                   check_norm_answer,
            "numerical_methods":     check_norm_answer,
            "indeterminate_forms":    check_norm_answer,
            "epsilon_delta":          check_norm_answer,
            "hyperbolic_apps":        check_norm_answer,
            "center_of_mass":         check_norm_answer,
            "function_construction":  check_norm_answer,
            "linear_equations":       check_norm_answer,
            "quadratic":              check_norm_answer,
            "polynomials":            check_norm_answer,
            "rational_expressions":   check_norm_answer,
            "systems":                check_norm_answer,
            "absolute_value":         check_norm_answer,
            "radicals":               check_norm_answer,
            "inequalities":           check_norm_answer,
            "sequences":              check_norm_answer,
            "probability":            check_norm_answer,
        })
    return CHECKER_MAP.get(module)


def register_checker(module, checker_fn):
    CHECKER_MAP[module] = checker_fn