from fastapi import APIRouter, FastAPI

from src.routes import health, game

app = FastAPI(root_path="/api")

router = APIRouter()
router.include_router(health.router)
router.include_router(game.router)

app.include_router(router)
