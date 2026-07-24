from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_postgres_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url, pool_pre_ping=True)


__all__ = ["create_postgres_engine"]
