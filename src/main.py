from fastapi import FastAPI

from src.api.main import app_router
from src.api.routes import health

app = FastAPI()

app.include_router(app_router)
app.include_router(health.router)
