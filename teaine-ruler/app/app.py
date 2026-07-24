from fastapi import FastAPI

from app.api import router as api_router
from app.config import settings
from app.middleware import internal_auth_middleware


def create_app() -> FastAPI:
    app = FastAPI(title="Teaine Ruler", version="0.1.0")
    app.state.settings = settings
    app.middleware("http")(internal_auth_middleware)
    app.include_router(api_router)
    return app


app = create_app()
__all__ = ["app", "create_app"]
