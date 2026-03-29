"""
config.py — Centralized Configuration

Loads all settings from environment variables / .env file.
Single source of truth for API keys, model names, thresholds, game rules.
"""

from pydantic_settings import BaseSettings
from pathlib import Path


# Resolve project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # --- LLM Configuration ---
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- App Environment ---
    APP_ENV: str = "development"

    # --- Game Rules ---
    MAX_STRIKES: int = 3
    BOARD_MIN_ANSWERS: int = 5
    BOARD_MAX_ANSWERS: int = 8

    # --- Matching Thresholds ---
    FUZZY_MATCH_THRESHOLD: int = 80        # rapidfuzz score 0-100
    SEMANTIC_MATCH_CONFIDENCE: float = 0.75

    # --- Data Paths (relative to project root) ---
    REAL_BOARDS_PATH: str = "data/real_boards.json"
    TRENDING_TOPICS_PATH: str = "data/trending_topics.json"
    CACHE_PATH: str = "data/generated_boards_cache.json"

    model_config = {
        "env_file": str(PROJECT_ROOT / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    def get_real_boards_path(self) -> Path:
        return PROJECT_ROOT / self.REAL_BOARDS_PATH

    def get_trending_topics_path(self) -> Path:
        return PROJECT_ROOT / self.TRENDING_TOPICS_PATH

    def get_cache_path(self) -> Path:
        return PROJECT_ROOT / self.CACHE_PATH


# Singleton settings instance
settings = Settings()
