"""
sqlite engine 工厂。
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import StaticPool

from app.infra.db.utils import is_sqlite_memory_url


def create_sqlite_engine(database_url: str) -> AsyncEngine:
    """
    创建 sqlite 异步 engine。

    内存数据库会使用 StaticPool，保证建表和查询复用同一个连接。

    :param database_url: SQLAlchemy sqlite 异步数据库连接 URL。
    :return: SQLAlchemy 异步 engine。
    """

    if is_sqlite_memory_url(database_url):
        return create_async_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    return create_async_engine(database_url)


__all__ = ["create_sqlite_engine"]
