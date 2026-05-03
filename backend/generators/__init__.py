from . import factoring, exponents, fractions, trig_circle, logs, composition
from . import limits, derivatives, integration_basic, integration_advanced
from . import asymptotes, increasing_decreasing, extrema, mvt, numerical_methods
from . import indeterminate_forms, epsilon_delta, hyperbolic_apps, center_of_mass
from . import function_construction
from . import linear_equations, quadratic, polynomials, rational_expressions
from . import systems, absolute_value, radicals, inequalities, sequences, probability
import module_config

GENERATORS = {
    "factoring": factoring.POOLS,
    "exponents": exponents.POOLS,
    "fractions": fractions.POOLS,
    "trig": trig_circle.POOLS,
    "logs": logs.POOLS,
    "composition": composition.POOLS,
    "limits": limits.POOLS,
    "derivatives": derivatives.POOLS,
    "integration": integration_basic.POOLS,
    "adv_integration": integration_advanced.POOLS,
    "asymptotes": asymptotes.POOLS,
    "increasing_decreasing": increasing_decreasing.POOLS,
    "extrema": extrema.POOLS,
    "mvt": mvt.POOLS,
    "numerical_methods": numerical_methods.POOLS,
    "indeterminate_forms": indeterminate_forms.POOLS,
    "epsilon_delta": epsilon_delta.POOLS,
    "hyperbolic_apps": hyperbolic_apps.POOLS,
    "center_of_mass": center_of_mass.POOLS,
    "function_construction": function_construction.POOLS,
    "linear_equations": linear_equations.POOLS,
    "quadratic": quadratic.POOLS,
    "polynomials": polynomials.POOLS,
    "rational_expressions": rational_expressions.POOLS,
    "systems": systems.POOLS,
    "absolute_value": absolute_value.POOLS,
    "radicals": radicals.POOLS,
    "inequalities": inequalities.POOLS,
    "sequences": sequences.POOLS,
    "probability": probability.POOLS,
}

REGISTRY = {}
for module, pools in GENERATORS.items():
    meta = module_config.MODULES.get(module, {})
    REGISTRY[module] = {
        "pools": pools,
        "tier": meta.get("tier", 0),
        "label": meta.get("label", module),
    }

ALL_MODULES = list(REGISTRY.keys())