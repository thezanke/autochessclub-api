from fastapi import APIRouter

from src.api.routes import games

app_router = APIRouter(prefix="/api")
app_router.include_router(games.router)
