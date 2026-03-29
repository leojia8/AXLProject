"""
main.py — FastAPI Application Entry Point

Initializes the app, mounts static files, includes routes,
and runs startup/shutdown lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.services import board_service, cache_service
from app.routes import pages, api


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    # Startup
    board_service.load_real_boards()
    board_service.load_trending_topics()
    cache_service.load_cache()
    print("[main] App started successfully")
    yield
    # Shutdown
    cache_service.save_cache()
    print("[main] App shut down, cache saved")


# Create FastAPI app
app = FastAPI(
    title="Family Feud AI",
    description="AI-powered Family Feud with real crowd data and smart semantic matching",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routes
app.include_router(pages.router)
app.include_router(api.router)
