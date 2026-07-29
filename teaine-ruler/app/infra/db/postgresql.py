"""
PostgreSQL engine 工厂。
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_postgresql_engine(database_url: str) -> AsyncEngine:
    """
    创建 PostgreSQL 异步 engine。

    :param database_url: SQLAlchemy PostgreSQL 异步数据库连接 URL。
    :return: SQLAlchemy 异步 engine。
    """

    return create_async_engine(database_url, pool_pre_ping=True)


__all__ = ["create_postgresql_engine"]
