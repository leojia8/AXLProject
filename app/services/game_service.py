"""
game_service.py — Game Round Lifecycle Management

Creates rounds, processes guesses, manages strikes/score/reveal.
Game state is stored IN-MEMORY in a dict keyed by round_id.
"""

import uuid
from typing import Optional

from app.config import settings
from app.models.schemas import AnswerSlot


# ---------------------------------------------------------------------------
# In-Memory State
# ---------------------------------------------------------------------------
_active_rounds: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Create Round
# ---------------------------------------------------------------------------
def create_round(board: dict) -> dict:
    """
    Initialize a new game round from a board dict.
    Returns the full round state including round_id.
    """
    round_id = str(uuid.uuid4())

    # Build answer list with revealed=False
    answers = []
    for ans in board["answers"]:
        answers.append({
            "text": ans["text"] if isinstance(ans, dict) else ans.text,
            "score": ans["score"] if isinstance(ans, dict) else ans.score,
            "revealed": False,
        })

    round_state = {
        "round_id": round_id,
        "prompt": board["prompt"] if isinstance(board, dict) else board.prompt,
        "answers": answers,
        "source_type": board.get("source_type", "real") if isinstance(board, dict) else board.source_type,
        "category": board.get("category", "general") if isinstance(board, dict) else board.category,
        "score": 0,
        "strikes": 0,
        "max_strikes": settings.MAX_STRIKES,
        "guesses": [],
        "round_over": False,
    }

    _active_rounds[round_id] = round_state
    return round_state


# ---------------------------------------------------------------------------
# Get Round
# ---------------------------------------------------------------------------
def get_round(round_id: str) -> Optional[dict]:
    """Retrieve active round state by ID."""
    return _active_rounds.get(round_id)


# ---------------------------------------------------------------------------
# Process Correct Guess
# ---------------------------------------------------------------------------
def reveal_answer(round_id: str, answer_index: int, guess: str) -> dict:
    """Mark an answer as revealed and update score."""
    state = _active_rounds[round_id]

    state["answers"][answer_index]["revealed"] = True
    state["score"] += state["answers"][answer_index]["score"]
    state["guesses"].append(guess)

    # Check if all answers revealed
    if all(a["revealed"] for a in state["answers"]):
        state["round_over"] = True

    return state


# ---------------------------------------------------------------------------
# Process Incorrect Guess (Strike)
# ---------------------------------------------------------------------------
def add_strike(round_id: str, guess: str) -> dict:
    """Add a strike for an incorrect guess."""
    state = _active_rounds[round_id]

    state["strikes"] += 1
    state["guesses"].append(guess)

    if state["strikes"] >= state["max_strikes"]:
        state["round_over"] = True

    return state


# ---------------------------------------------------------------------------
# Reveal Full Board
# ---------------------------------------------------------------------------
def reveal_board(round_id: str) -> dict:
    """Reveal all answers and end the round."""
    state = _active_rounds[round_id]

    for answer in state["answers"]:
        answer["revealed"] = True
    state["round_over"] = True

    return state


# ---------------------------------------------------------------------------
# Build Client-Safe State
# ---------------------------------------------------------------------------
def get_client_board(state: dict) -> list[AnswerSlot]:
    """Build board representation safe to send to client (hides unrevealed answers)."""
    slots = []
    for i, answer in enumerate(state["answers"]):
        if answer["revealed"]:
            slots.append(AnswerSlot(
                rank=i + 1,
                text=answer["text"],
                score=answer["score"],
                revealed=True,
            ))
        else:
            slots.append(AnswerSlot(
                rank=i + 1,
                text=None,
                score=None,
                revealed=False,
            ))
    return slots
