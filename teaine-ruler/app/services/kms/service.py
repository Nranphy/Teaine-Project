from asyncio import Lock

from sqlalchemy import desc, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.infra.postgres.tables import kms_entries, metadata
from app.utils.codec import decode_text, encode_text
from teaine_common.models.kms import KmsEntry, KmsEntryUpdate


class KmsService:
    """
    基于关系型数据库的版本化键值服务。

    每次写入都会为 namespace/key 追加一个新版本，不覆盖旧记录。
    value 入库前会编码，读取时再解码。
    """

    def __init__(self, engine: AsyncEngine, session_factory: async_sessionmaker):
        """
        初始化 KMS 服务。

        :param engine: SQLAlchemy 异步数据库 engine。
        :param session_factory: SQLAlchemy 异步 session factory。
        :return: None。
        """

        self.engine = engine
        self.session_factory = session_factory
        self._init_lock = Lock()
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """
        创建 KMS 所需数据表，并在每个进程内只初始化一次。

        :return: None。
        """

        if self._initialized:
            return

        async with self._init_lock:
            if self._initialized:
                return

            async with self.engine.begin() as connection:
                await connection.run_sync(metadata.create_all)

            self._initialized = True

    async def get(self, namespace: str, key: str) -> KmsEntry:
        """
        读取指定 namespace/key 的最新版本。

        :param namespace: KMS 命名空间。
        :param key: 命名空间下的键名。
        :return: 最新版本的键值记录。
        :raises KeyError: 当该 namespace/key 没有任何已存版本时抛出。
        """

        await self._ensure_initialized()

        async with self.session_factory() as session:
            statement = (
                select(kms_entries)
                .where(
                    kms_entries.c.namespace == namespace,
                    kms_entries.c.key == key,
                )
                .order_by(desc(kms_entries.c.version))
                .limit(1)
            )
            row = (await session.execute(statement)).mappings().first()
            if row is None:
                raise KeyError(f"KMS entry not found: {namespace}/{key}")

            return KmsEntry(
                namespace=row["namespace"],
                key=row["key"],
                value=decode_text(row["value"]),
                version=row["version"],
            )

    async def set(
        self,
        namespace: str,
        key: str,
        payload: KmsEntryUpdate,
        *,
        ensure_initialized: bool = True,
    ) -> KmsEntry:
        """
        为指定 namespace/key 追加一个新版本。

        写入操作不会删除或更新旧版本。如果两个写入者竞争同一个
        下一版本号，会在唯一约束冲突后重试一次。

        :param namespace: KMS 命名空间。
        :param key: 命名空间下的键名。
        :param payload: 写入请求，包含明文 value。
        :param ensure_initialized: 是否在写入前确保表结构已初始化。
        :return: 本次新写入的版本记录。
        :raises RuntimeError: 当版本写入在重试后仍失败时抛出。
        """

        if ensure_initialized:
            await self._ensure_initialized()

        for _ in range(2):
            try:
                async with self.session_factory.begin() as session:
                    latest_version = await session.scalar(
                        select(func.max(kms_entries.c.version)).where(
                            kms_entries.c.namespace == namespace,
                            kms_entries.c.key == key,
                        )
                    )
                    version = (latest_version or 0) + 1
                    await session.execute(
                        insert(kms_entries).values(
                            namespace=namespace,
                            key=key,
                            version=version,
                            value=encode_text(payload.value),
                        )
                    )
                return KmsEntry(
                    namespace=namespace,
                    key=key,
                    value=payload.value,
                    version=version,
                )
            except IntegrityError:
                continue

        raise RuntimeError(f"failed to write KMS entry version: {namespace}/{key}")


__all__ = ["KmsService"]
