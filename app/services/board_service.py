"""
board_service.py — Board Selection & Management

Responsibilities:
- Load real boards from data/real_boards.json at startup
- Select a board for a new round (real → hybrid → AI fallback)
- Generate hybrid boards by combining trending topics + AI
- Track which boards have been served to avoid immediate repeats

Board selection priority:
1. If category specified and real boards available → choose real board
2. If trending topic available for category → generate hybrid board via AI
3. Else → generate pure AI board
4. Cache any AI-generated board for reuse

This is the central data orchestrator for the game.
"""

import json
import random
from pathlib import Path
from typing import Optional

# from app.services.ai_service import generate_board
# from app.services.cache_service import get_cached_board, cache_board
# from app.config import settings

# ---------------------------------------------------------------------------
# In-Memory Board Storage
# ---------------------------------------------------------------------------
# TODO: _real_boards: list[dict] = []         — loaded from JSON at startup
# TODO: _trending_topics: list[dict] = []     — loaded from JSON at startup
# TODO: _served_board_ids: set = set()         — track recently served boards


# ---------------------------------------------------------------------------
# Startup Loading
# ---------------------------------------------------------------------------
def load_real_boards() -> None:
    """
    Load real_boards.json into memory.
    Called once at app startup.

    Expected JSON structure: list of board dicts, each with:
        id, prompt, answers, source_type, source_meta, category
    """
    # TODO: Read data/real_boards.json
    # TODO: Validate structure
    # TODO: Store in _real_boards
    pass


def load_trending_topics() -> None:
    """
    Load trending_topics.json into memory.
    Called once at app startup.

    Expected JSON structure: list of dicts, each with:
        topic, category, freshness_date (optional)
    """
    # TODO: Read data/trending_topics.json
    # TODO: Store in _trending_topics
    pass


# ---------------------------------------------------------------------------
# Board Selection (Main Entry Point)
# ---------------------------------------------------------------------------
async def get_board(category: str = None, prefer_real: bool = True) -> dict:
    """
    Select or generate a board for a new round.

    Args:
        category: Optional category filter
        prefer_real: If True, try real boards first before AI fallback

    Returns:
        A complete board dict ready for game_service to create a round

    Selection logic:
        1. Try real board matching category (if prefer_real)
        2. Try cached AI board matching category
        3. Try generating hybrid board from trending topic
        4. Fall back to pure AI generation
        5. Last resort: random real board regardless of category
    """
    # TODO: Implement selection cascade
    pass


# ---------------------------------------------------------------------------
# Real Board Selection
# ---------------------------------------------------------------------------
def _find_real_board(category: str = None) -> Optional[dict]:
    """
    Find a real board, optionally filtered by category.
    Avoid returning recently served boards.
    """
    # TODO: Filter _real_boards by category
    # TODO: Exclude recently served IDs
    # TODO: Random selection from remaining
    # TODO: Return board or None
    pass


# ---------------------------------------------------------------------------
# Trending Topic Selection
# ---------------------------------------------------------------------------
def _get_trending_topic(category: str = None) -> Optional[str]:
    """
    Pick a trending topic for AI board generation.
    Optionally filter by category.
    """
    # TODO: Filter topics by category if specified
    # TODO: Random selection
    # TODO: Return topic string or None
    pass


# ---------------------------------------------------------------------------
# Category Listing
# ---------------------------------------------------------------------------
def get_categories() -> list[str]:
    """
    Return list of unique categories across real boards and trending topics.
    Used by the /api/categories endpoint.
    """
    # TODO: Collect unique categories from _real_boards + _trending_topics
    pass
