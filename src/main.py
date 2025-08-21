from fastapi import FastAPI

from src.api.main import app_router

app = FastAPI(root_path="/api")
app.include_router(app_router)
