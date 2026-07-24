from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


def create_postgres_engine(database_url: str) -> AsyncEngine:
    if database_url in {"sqlite+aiosqlite:///:memory:", "sqlite+aiosqlite://"}:
        return create_async_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    return create_async_engine(database_url, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


__all__ = ["create_postgres_engine", "create_session_factory"]
