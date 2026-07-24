from fastapi import FastAPI

from app.api import router as api_router
from config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Teaine Ruler", version="0.1.0")
    app.state.settings = settings
    app.include_router(api_router)
    return app


app = create_app()
__all__ = ["app", "create_app"]
