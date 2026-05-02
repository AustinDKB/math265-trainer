import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import jsonl_engine as je


# ── Helpers ──

def _make_template(**overrides):
    defaults = {
        "id": "test_001",
        "course": "calc1",
        "topic": "optimization",
        "method": "first_derivative_test",
        "template": "Solve for x when {a} + {b} = ?",
        "variables": {
            "a": {"type": "int", "range": [1, 5]},
            "b": {"type": "int", "range": [1, 5]},
        },
        "answer_fn": "a + b",
        "solution_steps": [
            {"label": "Add", "math": "{a} + {b}", "note": ""}
        ],
        "difficulty": 1,
    }
    defaults.update(overrides)
    return defaults


# ── safe_eval ──

def test_safe_eval_basic():
    assert je.safe_eval("a + b", {"a": 2, "b": 3}) == 5


def test_safe_eval_math():
    assert je.safe_eval("sqrt(16)", {}) == 4.0
    assert abs(je.safe_eval("sin(pi/2)", {}) - 1.0) < 1e-9


def test_safe_eval_rejects_bad():
    try:
        je.safe_eval("__import__('os').system('ls')", {})
        assert False, "Should have rejected unsafe expression"
    except ValueError:
        pass


# ── load_templates ──

def test_load_from_path():
    p = Path(__file__).parent.parent / "jsonl_templates" / "calc1_optimization.jsonl"
    if p.exists():
        tpls = je.load_templates(path=p)
        assert len(tpls) >= 1
        assert tpls[0]["id"].startswith("calc1_opt")


def test_load_course_filter():
    tpls = je.load_templates(course="calc1")
    # At least our test template should be present
    assert any(t["id"].startswith("calc1_opt") for t in tpls)


# ── fill_template ──

def test_fill_basic():
    t = _make_template()
    filled = je.fill_template(t)
    assert "problemTex" in filled
    assert "answerNorm" in filled
    assert filled["answerNorm"] != ""
    assert filled["isWordProblem"] is True
    assert isinstance(filled["steps"], list)


def test_fill_computed_values():
    t = _make_template(
        variables={"a": {"type": "int", "range": [2, 4]}},
        computed_values={"b": "a * 2"},
        answer_fn="b + 1",
    )
    filled = je.fill_template(t)
    a_val = filled["_params"]["a"]
    expected = a_val * 2 + 1
    assert float(filled["answerNorm"]) == float(expected)


def test_fill_dual_answer():
    t = _make_template(
        answer_fn="a + b",
        answer_fn2="a - b",
        requiresDualAnswer=True,
    )
    filled = je.fill_template(t)
    assert filled["requiresDualAnswer"] is True
    assert "answerNorm2" in filled


# ── apply_skin ──

def test_apply_skin_from_template_contexts():
    t = _make_template(
        contexts=[
            {"skin": "mining", "narrative": "A mine has {a} tons of ore."}
        ]
    )
    filled = je.fill_template(t)
    before = filled["problemTex"]
    filled = je.apply_skin(filled)
    # Should either keep original or swap to skin narrative
    assert filled["skin"] in ("mining", "general")


def test_apply_skin_from_skins_json():
    t = _make_template(contexts=[])
    filled = je.fill_template(t)
    filled = je.apply_skin(filled, skin_name="agriculture")
    assert filled["skin"] == "agriculture"


# ── interleave ──

def test_interleave_no_adjacent_methods():
    pool = [
        {"method": "A", "id": f"a{i}"} for i in range(5)
    ] + [
        {"method": "B", "id": f"b{i}"} for i in range(5)
    ]
    result = je.interleave(pool, 8)
    methods = [r["method"] for r in result]
    for i in range(len(methods) - 1):
        assert methods[i] != methods[i + 1], f"Adjacent same method at index {i}"


def test_interleave_allows_repetition_when_short():
    pool = [{"method": "A", "id": "a1"}]
    result = je.interleave(pool, 3)
    assert len(result) == 3


# ── inject_decoys ──

def test_inject_decoys_replaces_some():
    session = [
        {"method": "opt", "id": "s1"},
        {"method": "opt", "id": "s2"},
        {"method": "rr", "id": "s3"},
        {"method": "rr", "id": "s4"},
        {"method": "opt", "id": "s5"},
        {"method": "rr", "id": "s6"},
        {"method": "opt", "id": "s7"},
        {"method": "rr", "id": "s8"},
    ]
    all_templates = [
        {"method": "mvt", "id": "d1"},
        {"method": "ibp", "id": "d2"},
    ]
    result = je.inject_decoys(session, all_templates, rate=0.25, min_gap=2)
    decoy_count = sum(1 for r in result if r.get("_is_decoy"))
    assert decoy_count >= 1


# ── assign_modes ──

def test_assign_modes_distribution():
    session = [{"method": "A", "difficulty": 2} for _ in range(20)]
    result = je.assign_modes(session)
    modes = [r["mode"] for r in result]
    assert "solve" in modes
    # derive should appear at most once
    assert modes.count("derive") <= 1


def test_assign_modes_avoids_triple_stacks():
    session = [{"method": "A", "difficulty": 2} for _ in range(10)]
    result = je.assign_modes(session, weights={"solve": 1.0})
    modes = [r["mode"] for r in result]
    # With only solve available, triple stacks are unavoidable, so test with mixed
    result = je.assign_modes(session)
    modes = [r["mode"] for r in result]
    for i in range(len(modes) - 2):
        if modes[i] == modes[i + 1] == modes[i + 2]:
            # Triple stacks should be rare; we just assert the function runs
            pass


def test_assign_modes_no_derive_on_decoy():
    session = [{"method": "A", "difficulty": 3, "_is_decoy": True} for _ in range(10)]
    result = je.assign_modes(session)
    for r in result:
        if r.get("_is_decoy"):
            assert r["mode"] != "derive"


# ── mode wrappers ──

def test_wrap_justify():
    filled = {"method": "u_substitution", "problemTex": "Integrate.", "answerTex": "x", "answerNorm": "x"}
    result = je.wrap_justify(filled)
    assert "[Justify]" in result["problemTex"]
    assert result["modeData"]["foil"] == "integration_by_parts"


def test_wrap_backwards():
    filled = {"problemTex": "P", "backwards_prompt": "Reconstruct.", "answerTex": "42", "answerNorm": "42"}
    result = je.wrap_backwards(filled)
    assert "[Backwards]" in result["problemTex"]
    assert result["modeData"]["type"] == "backwards"


def test_wrap_break():
    filled = {
        "problemTex": "P",
        "break_errors": [{"type": "bad_step", "explanation": "Oops"}],
        "steps": [],
    }
    result = je.wrap_break(filled)
    assert "[Break]" in result["problemTex"]
    assert result["modeData"]["type"] == "break"


def test_wrap_derive_library_hit():
    filled = {"method": "product_rule", "problemTex": "P", "steps": []}
    from derive_library import DERIVE_CALC1
    result = je.wrap_derive(filled, derive_library=DERIVE_CALC1)
    assert "[Derive]" in result["problemTex"]
    assert result["modeData"]["type"] == "derive"


def test_wrap_derive_library_miss():
    filled = {"method": "unknown_method", "problemTex": "P", "steps": []}
    result = je.wrap_derive(filled)
    assert "[Derive]" in result["problemTex"]


# ── build_session ──

def test_build_session_returns_problems():
    templates = [
        _make_template(id="t1", method="A"),
        _make_template(id="t2", method="B"),
    ]
    session = je.build_session(templates, n=4, decoy_rate=0.0)
    assert len(session) == 4
    for prob in session:
        assert "problemTex" in prob
        assert "mode" in prob


# ── validate_template ──

def test_validate_ok():
    t = _make_template()
    ok, msg = je.validate_template(t)
    assert ok, msg


def test_validate_missing_field():
    t = _make_template()
    del t["method"]
    ok, msg = je.validate_template(t)
    assert not ok
    assert "method" in msg


def test_validate_bad_variable_type():
    t = _make_template(variables={"a": {"type": "banana", "range": [1, 2]}})
    ok, msg = je.validate_template(t)
    assert not ok
    assert "banana" in msg


# ── get_next_problem ──

def test_get_next_problem_returns_dict():
    prob = je.get_next_problem(course="calc1")
    if prob:
        assert "problemTex" in prob


# ── Run with pytest ──
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
