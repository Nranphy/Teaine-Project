import re

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.infra.postgres.tables import metadata, prompt_templates
from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateRead,
    PromptTemplateUpdate,
)


class PromptService:
    def __init__(self, engine: AsyncEngine, session_factory: async_sessionmaker):
        self.engine = engine
        self.session_factory = session_factory

    async def _ensure_initialized(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    @staticmethod
    def _split_params(params: str) -> list[str]:
        return [param.strip() for param in params.split(",") if param.strip()]

    @staticmethod
    def _render(content: str, params: dict[str, str]) -> str:
        if not params:
            return content
        pattern = re.compile(
            r"\{\{\{("
            + "|".join(map(re.escape, sorted(params, key=len, reverse=True)))
            + r")\}\}\}"
        )
        return pattern.sub(lambda match: str(params[match.group(1)]), content)

    @staticmethod
    def _read(row) -> PromptTemplateRead:
        return PromptTemplateRead(
            name=row["name"],
            description=row["description"],
            content=row["content"],
            params=row["params"],
        )

    async def create(self, payload: PromptTemplateCreate) -> PromptTemplateRead:
        await self._ensure_initialized()
        try:
            async with self.session_factory.begin() as session:
                await session.execute(
                    insert(prompt_templates).values(
                        name=payload.name,
                        description=payload.description,
                        content=payload.content,
                        params=payload.params,
                    )
                )
        except IntegrityError as exc:
            raise FileExistsError(payload.name) from exc
        return PromptTemplateRead(**payload.model_dump())

    async def delete(self, name: str) -> None:
        await self._ensure_initialized()
        async with self.session_factory.begin() as session:
            result = await session.execute(
                delete(prompt_templates).where(prompt_templates.c.name == name)
            )
            if result.rowcount == 0:
                raise FileNotFoundError(name)

    async def update(
        self, name: str, payload: PromptTemplateUpdate
    ) -> PromptTemplateRead:
        await self._ensure_initialized()
        async with self.session_factory.begin() as session:
            result = await session.execute(
                update(prompt_templates)
                .where(prompt_templates.c.name == name)
                .values(
                    description=payload.description,
                    content=payload.content,
                    params=payload.params,
                )
            )
            if result.rowcount == 0:
                raise FileNotFoundError(name)
        return await self.get(name)

    async def get(self, name: str) -> PromptTemplateRead:
        await self._ensure_initialized()
        async with self.session_factory() as session:
            row = (
                await session.execute(
                    select(prompt_templates).where(prompt_templates.c.name == name)
                )
            ).mappings().first()
            if row is None:
                raise FileNotFoundError(name)
            return self._read(row)

    async def render(
        self, name: str, params: dict[str, str]
    ) -> PromptRenderResponse:
        prompt = await self.get(name)
        required_params = set(self._split_params(prompt.params))
        missing_params = sorted(required_params - set(params))
        if missing_params:
            raise ValueError(f"missing prompt params: {', '.join(missing_params)}")

        return PromptRenderResponse(
            name=name,
            text=self._render(prompt.content, params),
        )


__all__ = ["PromptService"]
