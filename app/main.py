"""
main.py — FastAPI Application Entry Point

Responsibilities:
- Initialize the FastAPI application instance
- Mount static file serving (CSS, JS, images)
- Include route modules (pages + API)
- Set up Jinja2 template engine
- Run startup/shutdown lifecycle events (e.g., load real boards into memory)
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.config import settings

# ---------------------------------------------------------------------------
# App Initialization
# ---------------------------------------------------------------------------
# TODO: Create FastAPI instance with title, description, version
# TODO: Mount /static directory for CSS/JS assets
# TODO: Initialize Jinja2Templates pointing to app/templates/

# ---------------------------------------------------------------------------
# Startup Event
# ---------------------------------------------------------------------------
# TODO: On startup, call board_service.load_real_boards() to preload JSON data
# TODO: On startup, call cache_service.load_cache() to restore any cached AI boards

# ---------------------------------------------------------------------------
# Route Inclusion
# ---------------------------------------------------------------------------
# TODO: Include routes.pages router (serves HTML pages)
# TODO: Include routes.api router (serves JSON API endpoints under /api)

# ---------------------------------------------------------------------------
# Shutdown Event
# ---------------------------------------------------------------------------
# TODO: On shutdown, call cache_service.save_cache() to persist generated boards
