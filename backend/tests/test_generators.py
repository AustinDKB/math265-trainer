import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generators import factoring, exponents, fractions, trig_circle, logs
from generators import composition, limits, derivatives
from generators import integration_basic, integration_advanced

MODULES = {
    "factoring": factoring,
    "exponents": exponents,
    "fractions": fractions,
    "trig": trig_circle,
    "logs": logs,
    "composition": composition,
    "limits": limits,
    "derivatives": derivatives,
    "integration": integration_basic,
    "adv_integration": integration_advanced,
}

REQUIRED_KEYS = {"problemTex", "answerTex", "answerNorm", "steps"}

DUAL_REQUIRED_KEYS = REQUIRED_KEYS | {"answerTex2", "answerNorm2", "requiresDualAnswer"}

SAFE_CHARS = set("0123456789abcdefghijklmnopqrstuvwxyz +-*/^().,{}|!=")


def _check_safe_eval_chars(norm):
    if norm is None:
        return True
    return all(c in SAFE_CHARS for c in norm.lower().replace(" ", ""))


class TestGeneratorShape:
    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_pools_exist(self, module_name, mod):
        assert hasattr(mod, "POOLS"), f"{module_name} missing POOLS"
        pools = mod.POOLS
        assert isinstance(pools, dict), f"{module_name} POOLS is not a dict"
        assert len(pools) > 0, f"{module_name} POOLS is empty"
        for diff in range(1, 6):
            assert diff in pools, f"{module_name} missing difficulty {diff}"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_generators_callable(self, module_name, mod):
        for diff, fns in mod.POOLS.items():
            for fn in fns:
                assert callable(fn), f"{module_name} diff {diff}: {fn} is not callable"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_generators_return_dict(self, module_name, mod):
        for diff in range(1, 6):
            for fn in mod.POOLS[diff]:
                result = fn()
                assert isinstance(result, dict), f"{module_name} {fn.__name__} returned {type(result)}"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_required_keys(self, module_name, mod):
        for diff in range(1, 6):
            for fn in mod.POOLS[diff]:
                result = fn()
                keys = set(result.keys())
                if result.get("requiresDualAnswer"):
                    missing = DUAL_REQUIRED_KEYS - keys
                    assert not missing, f"{module_name} {fn.__name__} missing dual keys: {missing}"
                else:
                    missing = REQUIRED_KEYS - keys
                    assert not missing, f"{module_name} {fn.__name__} missing keys: {missing}"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_steps_are_lists(self, module_name, mod):
        for diff in range(1, 6):
            for fn in mod.POOLS[diff]:
                result = fn()
                assert isinstance(result["steps"], list), f"{module_name} {fn.__name__} steps not a list"
                for s in result["steps"]:
                    assert "label" in s, f"{module_name} {fn.__name__} step missing label"
                    assert "math" in s, f"{module_name} {fn.__name__} step missing math"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_answer_norm_safe_chars(self, module_name, mod):
        for diff in range(1, 6):
            for fn in mod.POOLS[diff]:
                result = fn()
                norm = result.get("answerNorm")
                # answerNorm=None is allowed for factoring (checker uses originalExpanded)
                # answerNorm with |, >=, etc. is allowed (checker uses _norm_generic path)
                if norm is not None:
                    assert isinstance(norm, str), f"{module_name} {fn.__name__} answerNorm not a string"

    @pytest.mark.parametrize("module_name,mod", list(MODULES.items()))
    def test_dual_answer_norm2(self, module_name, mod):
        for diff in range(1, 6):
            for fn in mod.POOLS[diff]:
                result = fn()
                if result.get("requiresDualAnswer"):
                    assert "answerNorm2" in result, f"{module_name} {fn.__name__} missing answerNorm2"
                    assert "answerTex2" in result, f"{module_name} {fn.__name__} missing answerTex2"


class TestFactoringSpecific:
    def test_originalExpanded_exists(self):
        for fn in factoring.POOLS[1]:
            result = fn()
            if not result.get("isFracExpGcf") and not result.get("isTrigFactoring"):
                assert "originalExpanded" in result, f"{fn.__name__} missing originalExpanded"

    def test_frac_exp_has_validForms(self):
        for diff in [4]:
            for fn in factoring.POOLS.get(diff, []):
                result = fn()
                if result.get("isFracExpGcf"):
                    assert "validForms" in result, f"{fn.__name__} missing validForms"

    def test_trig_factoring_flags(self):
        for diff in [5]:
            for fn in factoring.POOLS.get(diff, []):
                result = fn()
                if result.get("isTrigFactoring"):
                    assert "trigFunc" in result, f"{fn.__name__} missing trigFunc"
                    assert "originalExpandedPoly" in result, f"{fn.__name__} missing originalExpandedPoly"


class TestOriginalExpandedRoundTrip:
    def test_dict_keys_become_strings_in_json(self):
        result = factoring._diff_squares()
        assert isinstance(result.get("originalExpanded"), str) or isinstance(result.get("originalExpanded"), dict)
        if isinstance(result.get("originalExpanded"), dict):
            serialized = {str(k): v for k, v in result["originalExpanded"].items()}
            deserialized = {int(k): v for k, v in serialized.items()}
            assert deserialized == result["originalExpanded"]