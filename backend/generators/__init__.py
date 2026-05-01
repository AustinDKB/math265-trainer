from . import factoring, exponents, fractions, trig_circle, logs, composition
from . import limits, derivatives, integration_basic, integration_advanced
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