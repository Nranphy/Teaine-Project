from fastapi import FastAPI

from app.api import router as api_router
from app.config import settings
from app.middleware import (
    common_version_middleware,
    internal_api_key_middleware,
    service_identity_middleware,
)


def create_app() -> FastAPI:
    app = FastAPI(title="Teaine Ruler", version="0.1.0")
    app.state.settings = settings
    app.middleware("http")(common_version_middleware)
    app.middleware("http")(internal_api_key_middleware)
    app.middleware("http")(service_identity_middleware)
    app.include_router(api_router)
    return app


app = create_app()
__all__ = ["app", "create_app"]
