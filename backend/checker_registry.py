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
        })
    return CHECKER_MAP.get(module)


def register_checker(module, checker_fn):
    CHECKER_MAP[module] = checker_fn