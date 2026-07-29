"""
数据库 engine 和 session factory 入口。
"""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.infra.db.postgresql import create_postgresql_engine
from app.infra.db.sqlite import create_sqlite_engine
from app.infra.db.utils import is_postgresql_url, is_sqlite_url


def create_database_engine(database_url: str) -> AsyncEngine:
    """
    根据数据库 URL 创建对应的 SQLAlchemy 异步 engine。

    :param database_url: SQLAlchemy 异步数据库连接 URL。
    :return: SQLAlchemy 异步 engine。
    :raises ValueError: 当数据库 URL 类型不支持时抛出。
    """

    if is_sqlite_url(database_url):
        return create_sqlite_engine(database_url)
    if is_postgresql_url(database_url):
        return create_postgresql_engine(database_url)

    raise ValueError(f"unsupported database url: {database_url}")


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    """
    为指定 engine 创建异步 session factory。

    :param engine: SQLAlchemy 异步 engine。
    :return: 绑定该 engine 的异步 session factory。
    """

    return async_sessionmaker(engine, expire_on_commit=False)


__all__ = ["create_database_engine", "create_session_factory"]
