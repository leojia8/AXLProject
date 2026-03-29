"""
schemas.py — Pydantic Models for Request/Response Validation

Defines typed request/response models for all API endpoints
and internal data models for boards, answers, game state.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ===========================================================================
# Data Models (Internal)
# ===========================================================================

class Answer(BaseModel):
    """A single answer on a Family Feud board."""
    text: str
    score: int
    revealed: bool = False


class Board(BaseModel):
    """A complete Family Feud board (question + ranked answers)."""
    id: str
    prompt: str
    answers: list[Answer]
    source_type: str  # "real" | "ai" | "hybrid"
    category: str
    source_meta: Optional[dict] = None


# ===========================================================================
# API Request Models
# ===========================================================================

class NewRoundRequest(BaseModel):
    """Request body for POST /api/new-round."""
    category: Optional[str] = None
    prefer_real: bool = True


class GuessRequest(BaseModel):
    """Request body for POST /api/guess."""
    round_id: str
    guess: str


class RevealRequest(BaseModel):
    """Request body for POST /api/reveal."""
    round_id: str


# ===========================================================================
# API Response Models
# ===========================================================================

class AnswerSlot(BaseModel):
    """A single slot on the board as shown to the client."""
    rank: int
    text: Optional[str] = None
    score: Optional[int] = None
    revealed: bool = False


class NewRoundResponse(BaseModel):
    """Response for POST /api/new-round."""
    round_id: str
    prompt: str
    board_size: int
    board: list[AnswerSlot]
    score: int = 0
    strikes: int = 0
    max_strikes: int = 3
    source_type: str
    category: str


class GuessResponse(BaseModel):
    """Response for POST /api/guess."""
    correct: bool
    matched_index: Optional[int] = None
    matched_answer: Optional[str] = None
    answer_score: Optional[int] = None
    match_type: Optional[str] = None
    board: list[AnswerSlot]
    score: int
    strikes: int
    round_over: bool
    guesses: list[str]


class RevealResponse(BaseModel):
    """Response for POST /api/reveal."""
    prompt: str
    board: list[AnswerSlot]
    score: int
    strikes: int
    source_type: str
    category: str
    commentary: Optional[str] = None


class CategoriesResponse(BaseModel):
    """Response for GET /api/categories."""
    categories: list[str]
