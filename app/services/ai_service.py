"""
ai_service.py — LLM Integration Layer

Responsibilities:
- Initialize and manage the Gemini API client
- Generate Family Feud boards via structured LLM prompts
- Perform semantic guess matching via LLM adjudication
- Generate optional hints and commentary (stretch)

This is the ONLY module that talks to the LLM. All other services call this.

Design notes:
- All LLM calls return parsed Python dicts/objects, never raw strings
- All prompts request strict JSON output
- Errors are caught and returned as None so callers can fall back gracefully
"""

# from google import genai
# from app.config import settings

# ---------------------------------------------------------------------------
# Client Initialization
# ---------------------------------------------------------------------------
# TODO: Initialize Gemini client with API key from settings
# TODO: Set default model from settings.GEMINI_MODEL


# ---------------------------------------------------------------------------
# Board Generation
# ---------------------------------------------------------------------------
async def generate_board(category: str = None, topic: str = None) -> dict | None:
    """
    Generate a Family Feud-style board using the LLM.

    Args:
        category: Optional category like "student_life", "technology"
        topic: Optional trending topic to seed the board generation

    Returns:
        Dict with keys: prompt, answers (list of {text, score}), category, source_type
        Returns None if LLM call fails (callers should fall back to real boards)

    Prompt strategy:
        - System: "You generate Family Feud style survey boards..."
        - User: Category/topic + format requirements
        - Require 5-8 ranked answers summing to ~100
        - Return strict JSON
    """
    # TODO: Build system prompt for board generation
    # TODO: Build user prompt with category/topic context
    # TODO: Call Gemini API with JSON response format
    # TODO: Parse and validate response against BoardSchema
    # TODO: Return parsed dict or None on failure
    pass


# ---------------------------------------------------------------------------
# Semantic Guess Matching
# ---------------------------------------------------------------------------
async def semantic_match(guess: str, answers: list[str]) -> dict | None:
    """
    Use LLM to determine if a guess semantically matches any board answer.

    Args:
        guess: The player's free-text guess
        answers: List of unrevealed answer strings on the board

    Returns:
        Dict with keys: is_match (bool), matched_answer (str), confidence (float)
        Returns None if LLM call fails (callers should treat as no match)

    This is only called AFTER exact and fuzzy matching fail.
    It's the key differentiator of the app.

    Prompt strategy:
        - System: "You judge whether a guess matches a Family Feud answer..."
        - User: List answers + guess
        - Allow synonyms, shorthand, common paraphrases
        - Reject overly broad/unrelated guesses
        - Return strict JSON
    """
    # TODO: Build semantic match prompt
    # TODO: Call Gemini API
    # TODO: Parse response
    # TODO: Check confidence against threshold
    # TODO: Return result or None
    pass


# ---------------------------------------------------------------------------
# Optional: Hint Generation (Stretch)
# ---------------------------------------------------------------------------
async def generate_hint(prompt: str, revealed: list[str], hidden: list[str]) -> str | None:
    """
    Generate a short hint for remaining hidden answers without revealing them.

    Args:
        prompt: The survey question
        revealed: Already revealed answer texts
        hidden: Still hidden answer texts

    Returns:
        Short hint string, or None on failure
    """
    # TODO: Implement if time remains
    pass


# ---------------------------------------------------------------------------
# Optional: Commentary Generation (Stretch)
# ---------------------------------------------------------------------------
async def generate_commentary(prompt: str, answers: list[dict], source_type: str) -> str | None:
    """
    Generate a short end-of-round commentary about the board.

    Returns:
        One or two sentence commentary, or None on failure
    """
    # TODO: Implement if time remains
    pass
