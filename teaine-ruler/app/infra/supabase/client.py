class SupabaseClientNotConfigured(RuntimeError):
    """
    Supabase 客户端尚未配置时抛出的异常。

    当前 Ruler 的核心数据访问已经走 SQLAlchemy/PostgreSQL。
    该异常用于保留后续接入 Supabase Auth、Storage 或 Realtime 时的
    明确失败语义。
    """

    pass


__all__ = ["SupabaseClientNotConfigured"]
