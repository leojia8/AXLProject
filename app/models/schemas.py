"""
schemas.py — Pydantic Models for Request/Response Validation

Responsibilities:
- Define typed request/response models for all API endpoints
- Define internal data models for boards, answers, game state
- Ensure all API contracts are explicit and validated

All API routes use these models for request parsing and response serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ===========================================================================
# Data Models (Internal)
# ===========================================================================

class Answer(BaseModel):
    """A single answer on a Family Feud board."""
    # TODO: text: str           — the answer text
    # TODO: score: int          — point value (all answers sum to ~100)
    # TODO: revealed: bool = False  — whether this answer has been uncovered
    pass


class Board(BaseModel):
    """A complete Family Feud board (question + ranked answers)."""
    # TODO: id: str                  — unique board identifier
    # TODO: prompt: str              — survey question ("Name something...")
    # TODO: answers: list[Answer]    — ranked answers (highest score first)
    # TODO: source_type: str         — "real" | "ai" | "hybrid"
    # TODO: category: str            — e.g. "student_life", "technology"
    # TODO: source_meta: Optional[dict] = None  — origin info for real boards
    pass


# ===========================================================================
# API Request Models
# ===========================================================================

class NewRoundRequest(BaseModel):
    """Request body for POST /api/new-round."""
    # TODO: category: Optional[str] = None     — optional category filter
    # TODO: prefer_real: bool = True            — prefer real boards over AI
    pass


class GuessRequest(BaseModel):
    """Request body for POST /api/guess."""
    # TODO: round_id: str      — which round this guess is for
    # TODO: guess: str          — the player's free-text guess
    pass


class RevealRequest(BaseModel):
    """Request body for POST /api/reveal."""
    # TODO: round_id: str      — which round to reveal
    pass


# ===========================================================================
# API Response Models
# ===========================================================================

class AnswerSlot(BaseModel):
    """A single slot on the board as shown to the client."""
    # TODO: rank: int                        — position (1-indexed)
    # TODO: text: Optional[str] = None       — answer text (None if hidden)
    # TODO: score: Optional[int] = None      — points (None if hidden)
    # TODO: revealed: bool = False           — whether slot is uncovered
    pass


class NewRoundResponse(BaseModel):
    """Response for POST /api/new-round."""
    # TODO: round_id: str
    # TODO: prompt: str
    # TODO: board_size: int                  — number of answer slots
    # TODO: board: list[AnswerSlot]          — initial board (all hidden)
    # TODO: score: int = 0
    # TODO: strikes: int = 0
    # TODO: max_strikes: int = 3
    # TODO: source_type: str
    # TODO: category: str
    pass


class GuessResponse(BaseModel):
    """Response for POST /api/guess."""
    # TODO: correct: bool
    # TODO: matched_index: Optional[int] = None    — which slot was matched
    # TODO: matched_answer: Optional[str] = None   — revealed answer text
    # TODO: answer_score: Optional[int] = None     — points earned
    # TODO: match_type: Optional[str] = None       — "exact" | "fuzzy" | "semantic"
    # TODO: board: list[AnswerSlot]                — updated board state
    # TODO: score: int                              — total score
    # TODO: strikes: int
    # TODO: round_over: bool
    # TODO: guesses: list[str]                     — all guesses so far
    pass


class RevealResponse(BaseModel):
    """Response for POST /api/reveal."""
    # TODO: prompt: str
    # TODO: board: list[AnswerSlot]          — all answers revealed
    # TODO: score: int
    # TODO: strikes: int
    # TODO: source_type: str
    # TODO: category: str
    # TODO: commentary: Optional[str] = None  — AI-generated end commentary
    pass


class CategoriesResponse(BaseModel):
    """Response for GET /api/categories."""
    # TODO: categories: list[str]
    pass
