"""
PostgreSQL/测试数据库 engine 工厂。

生产环境使用配置中的 PostgreSQL async URL；测试环境可以使用
sqlite+aiosqlite 的内存数据库，并通过 StaticPool 复用同一连接。
"""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool


def create_postgres_engine(database_url: str) -> AsyncEngine:
    """
    根据数据库 URL 创建 SQLAlchemy 异步 engine。

    sqlite+aiosqlite 的内存库会使用 StaticPool，保证建表和查询复用
    同一个内存数据库连接。其他 URL 默认按 PostgreSQL 场景开启
    pool_pre_ping。

    :param database_url: SQLAlchemy 异步数据库连接 URL。
    :return: SQLAlchemy 异步 engine。
    """

    if database_url in {"sqlite+aiosqlite:///:memory:", "sqlite+aiosqlite://"}:
        return create_async_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    return create_async_engine(database_url, pool_pre_ping=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    """
    为指定 engine 创建异步 session factory。

    :param engine: SQLAlchemy 异步 engine。
    :return: 绑定该 engine 的异步 session factory。
    """

    return async_sessionmaker(engine, expire_on_commit=False)


__all__ = ["create_postgres_engine", "create_session_factory"]
