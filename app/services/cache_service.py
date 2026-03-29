"""
cache_service.py — Generated Board Caching

Caches AI-generated boards to avoid re-hitting the LLM.
Simple JSON file persistence.
"""

import json
import uuid
from pathlib import Path
from typing import Optional
import random

from app.config import settings


# ---------------------------------------------------------------------------
# In-Memory Cache
# ---------------------------------------------------------------------------
_cache: list[dict] = []


# ---------------------------------------------------------------------------
# Load Cache from Disk
# ---------------------------------------------------------------------------
def load_cache() -> None:
    """Load generated_boards_cache.json into memory at startup."""
    global _cache
    path = settings.get_cache_path()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                _cache = json.load(f)
            print(f"[cache_service] Loaded {len(_cache)} cached boards")
        except (json.JSONDecodeError, IOError):
            _cache = []
            print("[cache_service] Cache file corrupt, starting fresh")
    else:
        _cache = []
        print("[cache_service] No cache file found, starting fresh")


# ---------------------------------------------------------------------------
# Save Cache to Disk
# ---------------------------------------------------------------------------
def save_cache() -> None:
    """Persist in-memory cache to disk."""
    path = settings.get_cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_cache, f, indent=2)
        print(f"[cache_service] Saved {len(_cache)} boards to cache")
    except IOError as e:
        print(f"[cache_service] Failed to save cache: {e}")


# ---------------------------------------------------------------------------
# Cache a New Board
# ---------------------------------------------------------------------------
def cache_board(board: dict) -> None:
    """Add a newly generated board to the cache."""
    if "id" not in board:
        board["id"] = f"ai_{uuid.uuid4().hex[:8]}"
    _cache.append(board)
    # Cap cache at 100 boards
    if len(_cache) > 100:
        _cache.pop(0)


# ---------------------------------------------------------------------------
# Retrieve Cached Board
# ---------------------------------------------------------------------------
def get_cached_board(category: str = None) -> Optional[dict]:
    """Find a cached board, optionally filtered by category."""
    candidates = _cache
    if category:
        candidates = [b for b in candidates if b.get("category") == category]
    if not candidates:
        return None
    return random.choice(candidates)
