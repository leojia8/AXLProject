"""
config.py — Centralized Configuration

Responsibilities:
- Load environment variables from .env file
- Expose typed settings for the entire app
- Single source of truth for API keys, model names, thresholds, game rules
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # --- LLM Configuration ---
    # TODO: GEMINI_API_KEY: str
    # TODO: GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- App Environment ---
    # TODO: APP_ENV: str = "development"

    # --- Game Rules ---
    # TODO: MAX_STRIKES: int = 3
    # TODO: BOARD_MIN_ANSWERS: int = 5
    # TODO: BOARD_MAX_ANSWERS: int = 8

    # --- Matching Thresholds ---
    # TODO: FUZZY_MATCH_THRESHOLD: int = 80  (rapidfuzz score 0-100)
    # TODO: SEMANTIC_MATCH_CONFIDENCE: float = 0.75

    # --- Data Paths ---
    # TODO: REAL_BOARDS_PATH: str = "data/real_boards.json"
    # TODO: TRENDING_TOPICS_PATH: str = "data/trending_topics.json"
    # TODO: CACHE_PATH: str = "data/generated_boards_cache.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance
# TODO: settings = Settings()
settings = None  # Placeholder until Settings fields are defined
