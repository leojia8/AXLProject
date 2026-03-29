"""
ai_service.py — LLM Integration Layer (Gemini)

Handles board generation, semantic matching, and optional hints.
This is the ONLY module that talks to the LLM.

Phase 3 will fully implement this. Stubs return None for now.
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Board Generation (Phase 3)
# ---------------------------------------------------------------------------
async def generate_board(category: str = None, topic: str = None) -> Optional[dict]:
    """Generate a Family Feud board using Gemini. Returns None until Phase 3."""
    return None


# ---------------------------------------------------------------------------
# Semantic Guess Matching (Phase 3)
# ---------------------------------------------------------------------------
async def semantic_match(guess: str, answers: list[str]) -> Optional[dict]:
    """Use LLM to check if guess semantically matches any answer. Returns None until Phase 3."""
    return None


# ---------------------------------------------------------------------------
# Hint Generation (Stretch)
# ---------------------------------------------------------------------------
async def generate_hint(prompt: str, revealed: list[str], hidden: list[str]) -> Optional[str]:
    """Generate a hint. Returns None until implemented."""
    return None


# ---------------------------------------------------------------------------
# Commentary Generation (Stretch)
# ---------------------------------------------------------------------------
async def generate_commentary(prompt: str, answers: list[dict], source_type: str) -> Optional[str]:
    """Generate end-of-round commentary. Returns None until implemented."""
    return None
