"""
matching_service.py — Guess Matching Pipeline

Responsibilities:
- Normalize user guesses (lowercase, strip punctuation, trim)
- Run layered matching: exact → containment → fuzzy → LLM semantic
- Return match result with the specific matched answer and confidence

Matching pipeline (in order):
1. Normalize guess text
2. Exact match against answer texts
3. Containment check (guess in answer OR answer in guess)
4. Fuzzy string similarity via rapidfuzz (threshold from config)
5. LLM semantic adjudication via ai_service (only if above steps fail)

This layered approach is intentional:
- Fast deterministic checks handle 80%+ of cases
- LLM is only called for genuinely ambiguous guesses
- Reduces latency, cost, and makes the system more resilient
"""

import re
import string
from typing import Optional

# from rapidfuzz import fuzz
# from app.services.ai_service import semantic_match
# from app.config import settings


# ---------------------------------------------------------------------------
# Text Normalization
# ---------------------------------------------------------------------------
def normalize(text: str) -> str:
    """
    Normalize text for comparison.

    Steps:
        - lowercase
        - strip leading/trailing whitespace
        - remove punctuation
        - collapse multiple spaces
        - optional: singularize simple plurals (e.g. "phones" → "phone")
    """
    # TODO: Implement normalization pipeline
    pass


# ---------------------------------------------------------------------------
# Main Match Entry Point
# ---------------------------------------------------------------------------
async def check_guess(guess: str, answers: list[dict]) -> Optional[dict]:
    """
    Check a guess against all unrevealed answers using the layered pipeline.

    Args:
        guess: Raw user guess string
        answers: List of answer dicts (each has "text", "score", "revealed")

    Returns:
        Dict with: matched_index (int), matched_answer (str), match_type (str)
        Returns None if no match found at any layer

    Only checks against unrevealed answers.
    """
    # TODO: Normalize guess
    # TODO: Get list of unrevealed answers
    # TODO: Try exact match
    # TODO: Try containment match
    # TODO: Try fuzzy match
    # TODO: Try semantic LLM match (async)
    # TODO: Return best match or None
    pass


# ---------------------------------------------------------------------------
# Layer 1: Exact Match
# ---------------------------------------------------------------------------
def _exact_match(normalized_guess: str, answers: list[tuple[int, str]]) -> Optional[tuple[int, str]]:
    """
    Check if normalized guess exactly matches any normalized answer.

    Args:
        normalized_guess: Already normalized guess
        answers: List of (original_index, normalized_answer_text) tuples

    Returns:
        (index, original_text) if match found, else None
    """
    # TODO: Compare normalized strings
    pass


# ---------------------------------------------------------------------------
# Layer 2: Containment Match
# ---------------------------------------------------------------------------
def _containment_match(normalized_guess: str, answers: list[tuple[int, str]]) -> Optional[tuple[int, str]]:
    """
    Check if guess is contained in any answer, or answer is contained in guess.
    Useful for: guess "phone" matching answer "check their phone"

    Only match if the contained string is a significant portion (not single char).
    """
    # TODO: Check both directions of containment
    # TODO: Require minimum length (e.g., 3+ chars) to avoid false positives
    pass


# ---------------------------------------------------------------------------
# Layer 3: Fuzzy Match
# ---------------------------------------------------------------------------
def _fuzzy_match(normalized_guess: str, answers: list[tuple[int, str]]) -> Optional[tuple[int, str]]:
    """
    Use rapidfuzz to find best fuzzy match above threshold.

    Uses token_sort_ratio for word-order-independent matching.
    Threshold from config (default: 80).
    """
    # TODO: Compute fuzz scores for each answer
    # TODO: Find best match above threshold
    # TODO: Return match or None
    pass


# ---------------------------------------------------------------------------
# Layer 4: Semantic LLM Match
# ---------------------------------------------------------------------------
async def _semantic_match(guess: str, answers: list[tuple[int, str]]) -> Optional[tuple[int, str]]:
    """
    Call ai_service.semantic_match() as final fallback.

    Only called when deterministic methods fail.
    Returns None if LLM call fails (graceful degradation).
    """
    # TODO: Call ai_service.semantic_match()
    # TODO: If is_match and confidence >= threshold, return match
    # TODO: If LLM fails, return None (don't crash the game)
    pass
