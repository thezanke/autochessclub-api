from fastapi import APIRouter

from src.api.routes import game

app_router = APIRouter(prefix="/api")
app_router.include_router(game.router)
