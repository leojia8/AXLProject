"""
matching_service.py — Guess Matching Pipeline

Layered matching: exact → containment → fuzzy → (LLM semantic in Phase 3)
This layered approach handles 80%+ of cases without hitting the LLM.
"""

import re
import string
from typing import Optional

from rapidfuzz import fuzz
from app.config import settings


# ---------------------------------------------------------------------------
# Text Normalization
# ---------------------------------------------------------------------------
def normalize(text: str) -> str:
    """
    Normalize text for comparison:
    lowercase, strip whitespace, remove punctuation, collapse spaces.
    """
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    # Simple plural handling
    if text.endswith("ies"):
        pass  # Don't mess with "ies" words
    elif text.endswith("s") and not text.endswith("ss"):
        text = text[:-1]
    return text


# ---------------------------------------------------------------------------
# Main Match Entry Point
# ---------------------------------------------------------------------------
async def check_guess(guess: str, answers: list[dict]) -> Optional[dict]:
    """
    Check a guess against all unrevealed answers using the layered pipeline.

    Returns dict with: matched_index, matched_answer, match_type
    Returns None if no match found.
    """
    normalized_guess = normalize(guess)

    if not normalized_guess:
        return None

    # Build list of (original_index, normalized_text, original_text) for unrevealed only
    unrevealed = []
    for i, ans in enumerate(answers):
        if not ans["revealed"]:
            unrevealed.append((i, normalize(ans["text"]), ans["text"]))

    if not unrevealed:
        return None

    # Layer 1: Exact match
    result = _exact_match(normalized_guess, unrevealed)
    if result:
        return {"matched_index": result[0], "matched_answer": result[1], "match_type": "exact"}

    # Layer 2: Containment
    result = _containment_match(normalized_guess, unrevealed)
    if result:
        return {"matched_index": result[0], "matched_answer": result[1], "match_type": "containment"}

    # Layer 3: Fuzzy
    result = _fuzzy_match(normalized_guess, unrevealed)
    if result:
        return {"matched_index": result[0], "matched_answer": result[1], "match_type": "fuzzy"}

    # Layer 4: Semantic LLM (added in Phase 3)
    result = await _semantic_match(normalized_guess, unrevealed)
    if result:
        return {"matched_index": result[0], "matched_answer": result[1], "match_type": "semantic"}

    return None


# ---------------------------------------------------------------------------
# Layer 1: Exact Match
# ---------------------------------------------------------------------------
def _exact_match(normalized_guess: str, answers: list[tuple[int, str, str]]) -> Optional[tuple[int, str]]:
    """Check if normalized guess exactly matches any normalized answer."""
    for orig_idx, norm_text, orig_text in answers:
        if normalized_guess == norm_text:
            return (orig_idx, orig_text)
    return None


# ---------------------------------------------------------------------------
# Layer 2: Containment Match
# ---------------------------------------------------------------------------
def _containment_match(normalized_guess: str, answers: list[tuple[int, str, str]]) -> Optional[tuple[int, str]]:
    """
    Check if guess is contained in any answer, or answer is contained in guess.
    Requires minimum 3 char match to avoid false positives.
    """
    if len(normalized_guess) < 3:
        return None

    best_match = None
    best_score = 0

    for orig_idx, norm_text, orig_text in answers:
        # Check if guess appears as a word boundary in the answer
        words_in_answer = norm_text.split()
        guess_words = normalized_guess.split()

        # Word-level match: any word in guess matches a word in answer
        word_match = any(gw in words_in_answer for gw in guess_words if len(gw) >= 3)
        if word_match:
            coverage = len(normalized_guess) / len(norm_text)
            adj_score = coverage + 0.3  # Bonus for word-level match
            if adj_score > best_score:
                best_match = (orig_idx, orig_text)
                best_score = adj_score
                continue

        # Guess contained in answer (e.g., "phone" in "check their phone")
        if normalized_guess in norm_text:
            coverage = len(normalized_guess) / len(norm_text)
            if coverage > best_score and coverage >= 0.2:  # At least 20% coverage
                best_match = (orig_idx, orig_text)
                best_score = coverage

        # Answer contained in guess (e.g., "study hard" contains answer "study")
        elif norm_text in normalized_guess:
            coverage = len(norm_text) / len(normalized_guess)
            if coverage > best_score and coverage >= 0.5:
                best_match = (orig_idx, orig_text)
                best_score = coverage

    return best_match


# ---------------------------------------------------------------------------
# Layer 3: Fuzzy Match
# ---------------------------------------------------------------------------
def _fuzzy_match(normalized_guess: str, answers: list[tuple[int, str, str]]) -> Optional[tuple[int, str]]:
    """Use rapidfuzz token_sort_ratio to find best fuzzy match above threshold."""
    best_match = None
    best_score = 0

    for orig_idx, norm_text, orig_text in answers:
        score = fuzz.token_sort_ratio(normalized_guess, norm_text)
        if score > best_score and score >= settings.FUZZY_MATCH_THRESHOLD:
            best_match = (orig_idx, orig_text)
            best_score = score

    return best_match


# ---------------------------------------------------------------------------
# Layer 4: Semantic LLM Match
# ---------------------------------------------------------------------------
async def _semantic_match(guess: str, answers: list[tuple[int, str, str]]) -> Optional[tuple[int, str]]:
    """
    Call ai_service.semantic_match() as final fallback.
    Only called when deterministic methods fail.
    Returns None if LLM call fails (graceful degradation).
    """
    from app.services.ai_service import semantic_match

    answer_texts = [orig_text for _, _, orig_text in answers]

    try:
        result = await semantic_match(guess, answer_texts)
        if result and result.get("is_match") and result.get("confidence", 0) >= settings.SEMANTIC_MATCH_CONFIDENCE:
            matched_text = result.get("matched_answer")
            # Find the index of the matched answer
            for orig_idx, _, orig_text in answers:
                if orig_text.lower() == matched_text.lower():
                    return (orig_idx, orig_text)
            # If exact text match fails, try containment
            for orig_idx, _, orig_text in answers:
                if matched_text.lower() in orig_text.lower() or orig_text.lower() in matched_text.lower():
                    return (orig_idx, orig_text)
    except Exception as e:
        print(f"[matching_service] Semantic match error: {e}")

    return None

