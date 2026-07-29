"""
数据库 URL 工具。
"""


def is_sqlite_url(database_url: str) -> bool:
    """
    判断数据库 URL 是否为 sqlite URL。

    :param database_url: SQLAlchemy 异步数据库连接 URL。
    :return: sqlite URL 返回 True，否则返回 False。
    """

    return database_url.startswith("sqlite+aiosqlite://")


def is_sqlite_memory_url(database_url: str) -> bool:
    """
    判断数据库 URL 是否为 sqlite 内存数据库 URL。

    :param database_url: SQLAlchemy 异步数据库连接 URL。
    :return: sqlite 内存数据库 URL 返回 True，否则返回 False。
    """

    return database_url in {
        'sqlite+aiosqlite:///:memory:',
        'sqlite+aiosqlite://',
    }


def is_postgresql_url(database_url: str) -> bool:
    """
    判断数据库 URL 是否为 PostgreSQL URL。

    :param database_url: SQLAlchemy 异步数据库连接 URL。
    :return: PostgreSQL URL 返回 True，否则返回 False。
    """

    return database_url.startswith(
        (
            'postgresql+asyncpg://',
            'postgresql://',
            'postgres://',
        )
    )


__all__ = [
    'is_postgresql_url',
    'is_sqlite_memory_url',
    'is_sqlite_url',
]
