from fastapi import APIRouter, FastAPI

from src.routes import health

app = FastAPI(root_path="/api")

router = APIRouter()
router.include_router(health.router)

app.include_router(router)
