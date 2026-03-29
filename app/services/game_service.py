"""
game_service.py — Game Round Lifecycle Management

Responsibilities:
- Create new game rounds (initialize state from a board)
- Retrieve round state by round_id
- Process guess results (reveal answer, add score, add strike)
- Check round completion conditions
- End/reveal rounds
- Track score across multiple rounds in a session (optional)

Game state is stored IN-MEMORY in a dict keyed by round_id.
This is fine for a take-home — no database needed.
"""

import uuid
from typing import Optional

# from app.config import settings

# ---------------------------------------------------------------------------
# In-Memory State
# ---------------------------------------------------------------------------
# TODO: _active_rounds: dict[str, dict] = {}
# Keyed by round_id → full round state dict


# ---------------------------------------------------------------------------
# Create Round
# ---------------------------------------------------------------------------
def create_round(board: dict) -> dict:
    """
    Initialize a new game round from a board.

    Args:
        board: Board dict from board_service (prompt, answers, source_type, category)

    Returns:
        Round state dict including round_id

    Round state structure:
    {
        "round_id": "uuid...",
        "prompt": "Name something students do...",
        "answers": [
            {"text": "study", "score": 42, "revealed": False},
            {"text": "check notes", "score": 24, "revealed": False},
            ...
        ],
        "source_type": "real" | "ai" | "hybrid",
        "category": "student_life",
        "score": 0,
        "strikes": 0,
        "max_strikes": 3,  (from settings)
        "guesses": [],
        "round_over": False
    }
    """
    # TODO: Generate UUID for round_id
    # TODO: Build state dict
    # TODO: Store in _active_rounds
    # TODO: Return state
    pass


# ---------------------------------------------------------------------------
# Get Round
# ---------------------------------------------------------------------------
def get_round(round_id: str) -> Optional[dict]:
    """
    Retrieve active round state by ID.
    Returns None if round not found (caller should return 404).
    """
    # TODO: Lookup in _active_rounds
    pass


# ---------------------------------------------------------------------------
# Process Correct Guess
# ---------------------------------------------------------------------------
def reveal_answer(round_id: str, answer_index: int, guess: str) -> dict:
    """
    Mark an answer as revealed and update score.

    Args:
        round_id: Active round ID
        answer_index: Index of the matched answer in the board
        guess: The original guess text (for history)

    Returns:
        Updated round state

    Side effects:
        - Sets answers[answer_index]["revealed"] = True
        - Adds answer score to total score
        - Appends guess to guesses list
        - Checks if all answers revealed → round_over = True
    """
    # TODO: Update answer revealed status
    # TODO: Add score
    # TODO: Record guess
    # TODO: Check completion
    pass


# ---------------------------------------------------------------------------
# Process Incorrect Guess (Strike)
# ---------------------------------------------------------------------------
def add_strike(round_id: str, guess: str) -> dict:
    """
    Add a strike for an incorrect guess.

    Returns:
        Updated round state

    Side effects:
        - Increments strikes
        - Appends guess to guesses list
        - If strikes >= max_strikes → round_over = True
    """
    # TODO: Increment strikes
    # TODO: Record guess
    # TODO: Check if round is over
    pass


# ---------------------------------------------------------------------------
# Reveal Full Board
# ---------------------------------------------------------------------------
def reveal_board(round_id: str) -> dict:
    """
    Reveal all answers and end the round.
    Called when round ends or player requests reveal.

    Returns:
        Full round state with all answers revealed
    """
    # TODO: Set all answers to revealed
    # TODO: Set round_over = True
    # TODO: Return full state
    pass


# ---------------------------------------------------------------------------
# Build Client-Safe State
# ---------------------------------------------------------------------------
def get_client_state(round_id: str) -> dict:
    """
    Build a sanitized version of round state safe to send to the client.
    Hides unrevealed answer texts — only shows slot existence.

    Returns:
        Dict with prompt, board (revealed answers shown, hidden ones masked),
        score, strikes, round_over, source_type, guesses
    """
    # TODO: Build safe state (don't leak answers!)
    pass
