"""
pages.py -- HTML Page Routes

Serves the landing page and game page via Jinja2 templates.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/")
async def landing_page(request: Request):
    """Serve the landing page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@router.get("/play")
async def game_page(request: Request):
    """Serve the game page shell. All gameplay driven by JS + API."""
    return templates.TemplateResponse("game.html", {
        "request": request,
    })
