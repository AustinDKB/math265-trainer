import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jsonl_engine as je

SAMPLE_FILLED = {
    "problemTex": r"Find \(\frac{d}{dx}[x^3 + 2x]\)",
    "answerTex": r"\(3x^2 + 2\)",
    "answerNorm": "3*x^2+2",
    "steps": [
        {"label": "Step 1", "math": r"f(x) = x^3 + 2x", "note": "Original"},
        {"label": "Step 2", "math": r"f'(x) = 3x^2 + 2", "note": "Power rule"},
    ],
    "skin": "justify",
    "modeData": {
        "foil_table_version": "calc1_v1",
        "derivation_hint": "power rule",
    },
}


class TestWrapJustify:
    def test_wrap_justify_adds_prompt(self):
        result = je.wrap_justify(SAMPLE_FILLED)
        assert "problemTex" in result
        assert "justify" in result.get("problemTex", "").lower() or "Explain" in result.get("problemTex", "")

    def test_wrap_justify_preserves_answer(self):
        result = je.wrap_justify(SAMPLE_FILLED)
        assert result.get("answerTex") == SAMPLE_FILLED["answerTex"]

    def test_wrap_justify_preserves_steps(self):
        result = je.wrap_justify(SAMPLE_FILLED)
        assert "steps" in result

    def test_wrap_justify_handles_missing_skin(self):
        filled = {k: v for k, v in SAMPLE_FILLED.items() if k != "skin"}
        result = je.wrap_justify(filled)
        assert "problemTex" in result

    def test_wrap_justify_handles_empty_skin(self):
        filled = dict(SAMPLE_FILLED, skin="")
        result = je.wrap_justify(filled)
        assert "problemTex" in result


class TestWrapBackwards:
    def test_wrap_backwards_adds_prompt(self):
        result = je.wrap_backwards(SAMPLE_FILLED)
        assert "problemTex" in result
        assert "backwards" in result.get("problemTex", "").lower() or "reconstruct" in result.get("problemTex", "").lower()

    def test_wrap_backwards_preserves_answerTex(self):
        result = je.wrap_backwards(SAMPLE_FILLED)
        assert result.get("answerTex") == SAMPLE_FILLED["answerTex"]

    def test_wrap_backwards_preserves_steps(self):
        result = je.wrap_backwards(SAMPLE_FILLED)
        assert "steps" in result


class TestWrapBreak:
    def test_wrap_break_adds_break_prefix(self):
        filled = dict(SAMPLE_FILLED, modeData={
            "error": {
                "type": "power_rule",
                "description": "Applied power rule incorrectly",
            }
        })
        result = je.wrap_break(filled)
        assert "problemTex" in result
        assert "Break" in result.get("problemTex", "") or "break" in result.get("problemTex", "").lower()

    def test_wrap_break_stores_error_in_modeData(self):
        filled = dict(SAMPLE_FILLED, modeData={
            "error": {"type": "power_rule"}
        })
        result = je.wrap_break(filled)
        assert result.get("modeData", {}).get("type") == "break"

    def test_wrap_break_preserves_original_steps(self):
        filled = dict(SAMPLE_FILLED, modeData={"error": {"type": "chain_rule"}})
        result = je.wrap_break(filled)
        assert "steps" in result

    def test_wrap_break_handles_no_modeData(self):
        filled = {k: v for k, v in SAMPLE_FILLED.items() if k != "modeData"}
        result = je.wrap_break(filled)
        assert "problemTex" in result

    def test_wrap_break_handles_empty_modeData(self):
        filled = dict(SAMPLE_FILLED, modeData={})
        result = je.wrap_break(filled)
        assert "problemTex" in result

    def test_wrap_break_preserves_answerTex(self):
        filled = dict(SAMPLE_FILLED, modeData={"error": {"type": "power_rule"}})
        result = je.wrap_break(filled)
        assert result.get("answerTex") == SAMPLE_FILLED["answerTex"]


class TestWrapDerive:
    def test_wrap_derive_adds_prompt(self):
        result = je.wrap_derive(SAMPLE_FILLED)
        assert "problemTex" in result

    def test_wrap_derive_preserves_answerTex(self):
        result = je.wrap_derive(SAMPLE_FILLED)
        assert result.get("answerTex") == SAMPLE_FILLED["answerTex"]

    def test_wrap_derive_preserves_steps(self):
        result = je.wrap_derive(SAMPLE_FILLED)
        assert "steps" in result

    def test_wrap_derive_handles_no_derive_library(self):
        result = je.wrap_derive(SAMPLE_FILLED, derive_library=None)
        assert "problemTex" in result

    def test_wrap_derive_handles_empty_derive_library(self):
        result = je.wrap_derive(SAMPLE_FILLED, derive_library={})
        assert "problemTex" in result
