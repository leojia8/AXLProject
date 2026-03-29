"""
api.py — JSON API Routes

All game logic endpoints. Returns JSON for the frontend JS to consume.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    NewRoundRequest, NewRoundResponse, GuessRequest, GuessResponse,
    RevealRequest, RevealResponse, CategoriesResponse
)
from app.services import board_service, game_service, matching_service

router = APIRouter(prefix="/api", tags=["game"])


# ---------------------------------------------------------------------------
# POST /api/new-round
# ---------------------------------------------------------------------------
@router.post("/new-round", response_model=NewRoundResponse)
async def new_round(req: NewRoundRequest):
    """Start a new game round."""
    board = await board_service.get_board(
        category=req.category,
        prefer_real=req.prefer_real,
    )

    state = game_service.create_round(board)
    client_board = game_service.get_client_board(state)

    return NewRoundResponse(
        round_id=state["round_id"],
        prompt=state["prompt"],
        board_size=len(state["answers"]),
        board=client_board,
        score=state["score"],
        strikes=state["strikes"],
        max_strikes=state["max_strikes"],
        source_type=state["source_type"],
        category=state["category"],
    )


# ---------------------------------------------------------------------------
# POST /api/guess
# ---------------------------------------------------------------------------
@router.post("/guess", response_model=GuessResponse)
async def submit_guess(req: GuessRequest):
    """Submit a guess for the current round."""
    state = game_service.get_round(req.round_id)
    if not state:
        raise HTTPException(status_code=404, detail="Round not found")

    if state["round_over"]:
        raise HTTPException(status_code=400, detail="Round is already over")

    guess = req.guess.strip()
    if not guess:
        raise HTTPException(status_code=400, detail="Guess cannot be empty")

    # Check guess against answers
    match = await matching_service.check_guess(guess, state["answers"])

    if match:
        # Correct guess
        state = game_service.reveal_answer(
            req.round_id, match["matched_index"], guess
        )
        client_board = game_service.get_client_board(state)
        return GuessResponse(
            correct=True,
            matched_index=match["matched_index"],
            matched_answer=match["matched_answer"],
            answer_score=state["answers"][match["matched_index"]]["score"],
            match_type=match["match_type"],
            board=client_board,
            score=state["score"],
            strikes=state["strikes"],
            round_over=state["round_over"],
            guesses=state["guesses"],
        )
    else:
        # Wrong guess — strike
        state = game_service.add_strike(req.round_id, guess)
        client_board = game_service.get_client_board(state)
        return GuessResponse(
            correct=False,
            board=client_board,
            score=state["score"],
            strikes=state["strikes"],
            round_over=state["round_over"],
            guesses=state["guesses"],
        )


# ---------------------------------------------------------------------------
# POST /api/reveal
# ---------------------------------------------------------------------------
@router.post("/reveal", response_model=RevealResponse)
async def reveal(req: RevealRequest):
    """Reveal the full board (end round)."""
    state = game_service.get_round(req.round_id)
    if not state:
        raise HTTPException(status_code=404, detail="Round not found")

    state = game_service.reveal_board(req.round_id)
    client_board = game_service.get_client_board(state)

    return RevealResponse(
        prompt=state["prompt"],
        board=client_board,
        score=state["score"],
        strikes=state["strikes"],
        source_type=state["source_type"],
        category=state["category"],
    )


# ---------------------------------------------------------------------------
# GET /api/categories
# ---------------------------------------------------------------------------
@router.get("/categories", response_model=CategoriesResponse)
async def categories():
    """Return available categories."""
    return CategoriesResponse(
        categories=board_service.get_categories()
    )
