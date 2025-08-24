from fastapi import APIRouter

from src.api.routes import games, positions

app_router = APIRouter(prefix="/api")
app_router.include_router(games.router)
app_router.include_router(positions.router)
