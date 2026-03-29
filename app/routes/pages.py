"""
pages.py — HTML Page Routes

Responsibilities:
- GET /          → Landing page (index.html)
- GET /play      → Game page (game.html)

These routes return rendered Jinja2 templates.
All game logic is driven by the API routes; these just serve the HTML shells.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

# TODO: Initialize templates = Jinja2Templates(directory="app/templates")

# ---------------------------------------------------------------------------
# GET / — Landing Page
# ---------------------------------------------------------------------------
# TODO: Render index.html
# - Pass app title, description, available categories
# - Template should have "Play Now" CTA button


# ---------------------------------------------------------------------------
# GET /play — Game Page
# ---------------------------------------------------------------------------
# TODO: Render game.html
# - This is the main SPA shell
# - All gameplay is driven by JS fetch() calls to /api/* endpoints
# - Optionally accept ?category= query param to pre-select category
