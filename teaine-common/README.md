# Teaine-Common

Project Teaine 的公共模型、类型定义、错误类型和跨服务 SDK 包。

## 职责

- 提供跨模块传输使用的 Pydantic DTO。
- 提供平台、交互、活动、服务等公共枚举。
- 提供 JSON、ID、时间戳等 typing helper。
- 提供面向其他服务的 SDK，目前包含 `teaine_common.sdk.ruler`。

## 非职责

- 不保存服务内部运行时状态。
- 不直接连接数据库、Supabase 或向量存储。
- 不定义 Ruler 内部 ORM 模型。

## Ruler SDK 示例

```python
from teaine_common.sdk.ruler import RulerClient

async with RulerClient(
    base_url="http://localhost:8000",
    service_name="grail",
    api_key="secret",
) as client:
    prompt = await client.prompt.render("default", {"name": "茶因"})
```

Ruler SDK 当前覆盖 `system`、`kms` 和 `prompt`。SDK 会自动在内部请求头中携带本地 common 版本，Ruler 在请求带有版本头时会与服务端 common 版本做一致性检查。
