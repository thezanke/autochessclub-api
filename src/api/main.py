from fastapi import APIRouter

from src.api.routes import health, game

app_router = APIRouter()

app_router.include_router(health.router)
app_router.include_router(game.router)
