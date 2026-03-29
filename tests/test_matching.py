"""
Tests for matching_service.py — the core differentiator of the app.
Tests all 4 matching layers: exact, containment, fuzzy, (semantic stub).
"""

import pytest
from app.services.matching_service import normalize, check_guess, _exact_match, _containment_match, _fuzzy_match


# ---------------------------------------------------------------------------
# Normalize Tests
# ---------------------------------------------------------------------------

class TestNormalize:
    def test_basic(self):
        assert normalize("Hello World") == "hello world"

    def test_punctuation(self):
        assert normalize("don't stop!") == "dont stop"

    def test_whitespace(self):
        assert normalize("  extra   spaces  ") == "extra space"

    def test_plural_strip(self):
        assert normalize("phones") == "phone"
        assert normalize("studies") == "studies"  # "ies" not stripped

    def test_empty(self):
        assert normalize("") == ""


# ---------------------------------------------------------------------------
# Exact Match Tests
# ---------------------------------------------------------------------------

class TestExactMatch:
    def test_exact(self):
        answers = [(0, "study", "study"), (1, "check note", "check notes")]
        result = _exact_match("study", answers)
        assert result == (0, "study")

    def test_no_match(self):
        answers = [(0, "study", "study")]
        result = _exact_match("phone", answers)
        assert result is None


# ---------------------------------------------------------------------------
# Containment Match Tests
# ---------------------------------------------------------------------------

class TestContainmentMatch:
    def test_guess_in_answer(self):
        answers = [(0, "check their phone", "check their phone")]
        result = _containment_match("phone", answers)
        assert result is not None
        assert result[0] == 0

    def test_gadgets_word_match(self):
        """'gadget' should match 'gadgets they don't need' via word-level matching."""
        answers = [(0, "gadget they dont need", "gadgets they don't need")]
        result = _containment_match("gadget", answers)
        assert result is not None
        assert result[0] == 0

    def test_answer_in_guess(self):
        answers = [(0, "study", "study")]
        result = _containment_match("study hard", answers)
        assert result is not None
        assert result[0] == 0

    def test_too_short(self):
        result = _containment_match("hi", [(0, "check hi there", "check hi there")])
        assert result is None

    def test_no_match(self):
        answers = [(0, "study", "study")]
        result = _containment_match("phone", answers)
        assert result is None


# ---------------------------------------------------------------------------
# Fuzzy Match Tests
# ---------------------------------------------------------------------------

class TestFuzzyMatch:
    def test_typo(self):
        answers = [(0, "study", "study")]
        result = _fuzzy_match("studt", answers)
        assert result is not None
        assert result[0] == 0

    def test_reorder(self):
        answers = [(0, "drink coffee", "drink coffee")]
        result = _fuzzy_match("coffee drink", answers)
        assert result is not None

    def test_no_match(self):
        answers = [(0, "study", "study")]
        result = _fuzzy_match("phone", answers)
        assert result is None


# ---------------------------------------------------------------------------
# Full Pipeline Tests
# ---------------------------------------------------------------------------

class TestCheckGuess:
    @pytest.mark.asyncio
    async def test_exact_match(self):
        answers = [
            {"text": "study", "score": 42, "revealed": False},
            {"text": "check notes", "score": 24, "revealed": False},
        ]
        result = await check_guess("study", answers)
        assert result is not None
        assert result["match_type"] == "exact"
        assert result["matched_answer"] == "study"

    @pytest.mark.asyncio
    async def test_containment_match(self):
        answers = [
            {"text": "check their phone", "score": 7, "revealed": False},
        ]
        result = await check_guess("phone", answers)
        assert result is not None
        assert result["match_type"] == "containment"

    @pytest.mark.asyncio
    async def test_skip_revealed(self):
        answers = [
            {"text": "study", "score": 42, "revealed": True},
        ]
        result = await check_guess("study", answers)
        assert result is None

    @pytest.mark.asyncio
    async def test_no_match(self):
        answers = [
            {"text": "study", "score": 42, "revealed": False},
        ]
        result = await check_guess("airplane", answers)
        assert result is None

    @pytest.mark.asyncio
    async def test_empty_guess(self):
        answers = [{"text": "study", "score": 42, "revealed": False}]
        result = await check_guess("", answers)
        assert result is None

    @pytest.mark.asyncio
    async def test_fuzzy_match(self):
        answers = [
            {"text": "drink coffee", "score": 9, "revealed": False},
        ]
        result = await check_guess("coffee drinking", answers)
        assert result is not None
