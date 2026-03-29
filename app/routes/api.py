"""
api.py — JSON API Routes

Responsibilities:
- POST /api/new-round   → Start a new game round, return board metadata
- POST /api/guess        → Submit a guess, return match result + updated state
- POST /api/reveal       → Reveal full board (end round early or after completion)
- GET  /api/categories   → Return available categories for UI dropdown

All responses are JSON. Game state is managed server-side in memory via game_service.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import NewRoundRequest, NewRoundResponse, GuessRequest, GuessResponse, RevealResponse

router = APIRouter(prefix="/api", tags=["game"])

# ---------------------------------------------------------------------------
# POST /api/new-round
# ---------------------------------------------------------------------------
# TODO: Accept NewRoundRequest (category, difficulty, prefer_real)
# TODO: Call board_service.get_board() to select/generate a board
# TODO: Call game_service.create_round() to initialize round state
# TODO: Return NewRoundResponse (round_id, prompt, board_size, source_type, etc.)
# TODO: Do NOT return actual answers — only metadata


# ---------------------------------------------------------------------------
# POST /api/guess
# ---------------------------------------------------------------------------
# TODO: Accept GuessRequest (round_id, guess)
# TODO: Retrieve round state from game_service
# TODO: Call matching_service.check_guess() against unrevealed answers
# TODO: If match found:
#   - Reveal the answer, update score, return match info
# TODO: If no match:
#   - Increment strikes, check if round is over
# TODO: Return GuessResponse with updated board state


# ---------------------------------------------------------------------------
# POST /api/reveal
# ---------------------------------------------------------------------------
# TODO: Accept round_id
# TODO: Mark round as complete
# TODO: Return full board with all answers, scores, and source info
# TODO: Optionally include AI commentary (stretch feature)


# ---------------------------------------------------------------------------
# GET /api/categories
# ---------------------------------------------------------------------------
# TODO: Return list of available categories from board_service
# TODO: Include count of real vs AI boards per category if available
