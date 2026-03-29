"""
board_service.py — Board Selection & Management

Loads real boards from JSON, selects boards by category, avoids repeats.
AI fallback and trending topic hybrid generation added in Phase 3.
"""

import json
import random
from pathlib import Path
from typing import Optional

from app.config import settings


# ---------------------------------------------------------------------------
# In-Memory Board Storage
# ---------------------------------------------------------------------------
_real_boards: list[dict] = []
_trending_topics: list[dict] = []
_served_board_ids: set = set()


# ---------------------------------------------------------------------------
# Startup Loading
# ---------------------------------------------------------------------------
def load_real_boards() -> None:
    """Load real_boards.json into memory at startup."""
    global _real_boards
    path = settings.get_real_boards_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            _real_boards = json.load(f)
        print(f"[board_service] Loaded {len(_real_boards)} real boards")
    else:
        print(f"[board_service] WARNING: {path} not found, no real boards loaded")


def load_trending_topics() -> None:
    """Load trending_topics.json into memory at startup."""
    global _trending_topics
    path = settings.get_trending_topics_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            _trending_topics = json.load(f)
        print(f"[board_service] Loaded {len(_trending_topics)} trending topics")
    else:
        print(f"[board_service] WARNING: {path} not found, no trending topics loaded")


# ---------------------------------------------------------------------------
# Board Selection (Main Entry Point)
# ---------------------------------------------------------------------------
async def get_board(category: str = None, prefer_real: bool = True) -> dict:
    """
    Select or generate a board for a new round.

    Selection cascade:
    1. Try real board matching category (if prefer_real)
    2. Try any real board (if category match fails)
    3. (Phase 3) Try cached AI board
    4. (Phase 3) Generate hybrid board from trending topic
    5. (Phase 3) Generate pure AI board
    6. Last resort: random real board
    """
    if prefer_real:
        board = _find_real_board(category)
        if board:
            return board

    # Try without category filter
    board = _find_real_board(None)
    if board:
        return board

    # Phase 3: AI fallback will go here

    # Last resort: reset served IDs and try again
    _served_board_ids.clear()
    board = _find_real_board(category)
    if board:
        return board

    # Absolute fallback: first real board
    if _real_boards:
        return _real_boards[0]

    # No boards at all — return a hardcoded emergency board
    return {
        "id": "emergency_01",
        "prompt": "Name something people do every morning",
        "answers": [
            {"text": "brush teeth", "score": 30},
            {"text": "eat breakfast", "score": 25},
            {"text": "check phone", "score": 20},
            {"text": "shower", "score": 15},
            {"text": "make coffee", "score": 10},
        ],
        "source_type": "real",
        "category": "daily_life",
    }


# ---------------------------------------------------------------------------
# Real Board Selection
# ---------------------------------------------------------------------------
def _find_real_board(category: str = None) -> Optional[dict]:
    """Find a real board, optionally filtered by category. Avoids recently served."""
    candidates = _real_boards

    if category:
        candidates = [b for b in candidates if b.get("category") == category]

    # Exclude recently served
    candidates = [b for b in candidates if b.get("id") not in _served_board_ids]

    if not candidates:
        return None

    board = random.choice(candidates)
    _served_board_ids.add(board.get("id"))
    return board


# ---------------------------------------------------------------------------
# Trending Topic Selection
# ---------------------------------------------------------------------------
def _get_trending_topic(category: str = None) -> Optional[str]:
    """Pick a trending topic for AI board generation."""
    candidates = _trending_topics
    if category:
        candidates = [t for t in candidates if t.get("category") == category]
    if not candidates:
        candidates = _trending_topics
    if not candidates:
        return None
    return random.choice(candidates).get("topic")


# ---------------------------------------------------------------------------
# Category Listing
# ---------------------------------------------------------------------------
def get_categories() -> list[str]:
    """Return list of unique categories across real boards and trending topics."""
    cats = set()
    for board in _real_boards:
        if board.get("category"):
            cats.add(board["category"])
    for topic in _trending_topics:
        if topic.get("category"):
            cats.add(topic["category"])
    return sorted(cats)
