from asyncio import Lock

from sqlalchemy import desc, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.infra.postgres.tables import kms_entries, metadata
from app.utils.codec import decode_text, encode_text
from teaine_common.models.kms import KmsEntry, KmsEntryUpdate
from teaine_common.version import __version__


class KmsService:
    def __init__(self, engine: AsyncEngine, session_factory: async_sessionmaker):
        self.engine = engine
        self.session_factory = session_factory
        self._init_lock = Lock()
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        if self._initialized:
            return

        async with self._init_lock:
            if self._initialized:
                return

            async with self.engine.begin() as connection:
                await connection.run_sync(metadata.create_all)

            await self._seed_common_version()
            self._initialized = True

    async def _seed_common_version(self) -> None:
        async with self.session_factory() as session:
            existing_version = await session.scalar(
                select(func.max(kms_entries.c.version)).where(
                    kms_entries.c.namespace == "system",
                    kms_entries.c.key == "common_version",
                )
            )

        if existing_version is None:
            await self.set(
                "system",
                "common_version",
                KmsEntryUpdate(value=__version__),
                ensure_initialized=False,
            )

    async def get(self, namespace: str, key: str) -> KmsEntry:
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
