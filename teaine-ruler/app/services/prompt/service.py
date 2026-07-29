import re

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.infra.db.tables import metadata, prompt_templates
from teaine_common.models.prompt import (
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateRead,
    PromptTemplateUpdate,
)


class PromptService:
    """
    基于关系型数据库的 Prompt 模板服务。

    模板按 name 存储，并使用 {{{param}}} 占位符进行渲染。
    params 字段使用半角逗号分隔，用于声明渲染时必须提供的参数。
    """

    def __init__(self, engine: AsyncEngine, session_factory: async_sessionmaker):
        """
        初始化 Prompt 服务。

        :param engine: SQLAlchemy 异步数据库 engine。
        :param session_factory: SQLAlchemy 异步 session factory。
        :return: None。
        """

        self.engine = engine
        self.session_factory = session_factory

    async def _ensure_initialized(self) -> None:
        """
        在 Prompt 所需数据表不存在时创建它们。

        :return: None。
        """

        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    @staticmethod
    def _split_params(params: str) -> list[str]:
        """
        解析数据库中以半角逗号分隔的必需参数列表。

        :param params: 半角逗号分隔的参数名字符串。
        :return: 去除空白和空项后的参数名列表。
        """

        return [param.strip() for param in params.split(",") if param.strip()]

    @staticmethod
    def _render(content: str, params: dict[str, str]) -> str:
        """
        用传入参数替换内容中的 {{{param}}} 占位符。

        :param content: Prompt 模板内容。
        :param params: 渲染时提供的参数字典。
        :return: 完成参数替换后的文本。
        """

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
        """
        把 SQLAlchemy 行映射转换为对外 Prompt DTO。

        :param row: SQLAlchemy 查询得到的行映射。
        :return: 对外返回的 Prompt 模板 DTO。
        """

        return PromptTemplateRead(
            name=row["name"],
            description=row["description"],
            content=row["content"],
            params=row["params"],
        )

    async def create(self, payload: PromptTemplateCreate) -> PromptTemplateRead:
        """
        创建新的 Prompt 模板。

        :param payload: Prompt 创建请求。
        :return: 创建后的 Prompt 模板。
        :raises FileExistsError: 当同名 Prompt 已存在时抛出。
        """

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
        """
        删除已有 Prompt 模板。

        :param name: 要删除的 Prompt 名称。
        :return: None。
        :raises FileNotFoundError: 当 Prompt 不存在时抛出。
        """

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
        """
        替换已有 Prompt 模板的可编辑字段。

        :param name: 要更新的 Prompt 名称。
        :param payload: Prompt 更新请求。
        :return: 更新后的 Prompt 模板。
        :raises FileNotFoundError: 当 Prompt 不存在时抛出。
        """

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
        """
        按名称读取 Prompt 模板。

        :param name: 要读取的 Prompt 名称。
        :return: 读取到的 Prompt 模板。
        :raises FileNotFoundError: 当 Prompt 不存在时抛出。
        """

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
        """
        校验必需参数后渲染 Prompt 模板。

        :param name: 要渲染的 Prompt 名称。
        :param params: 渲染时提供的参数字典。
        :return: 渲染结果。
        :raises FileNotFoundError: 当 Prompt 不存在时抛出。
        :raises ValueError: 当模板声明的必需参数缺失时抛出。
        """

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
