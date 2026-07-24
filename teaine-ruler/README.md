# Teaine-Ruler

茶因计划·资源管理器后端。

Ruler 是 Project Teaine 的内部控制面服务，提供 HTTP API、内部服务鉴权、Prompt、KMS、Record 和 Tool 等底层能力。

## 技术选择

Ruler 以 Supabase PostgreSQL 作为主数据存储。服务端核心数据访问优先通过 SQLAlchemy async / PostgreSQL connection 完成；Supabase SDK 只作为后续访问 Supabase Auth、Storage、Realtime 等能力的可选基础设施封装。

## API 分层

- `/api/v1/public/**`：公开探活等低风险接口。
- `/api/v1/internal/**`：内部服务接口，默认需要 API key 鉴权。

内部接口需要携带：

```http
X-Teaine-Service: grail
X-Teaine-Api-Key: secret
X-Teaine-Common-Version: 0.1.0
```

## 当前领域

- `system`：服务信息与 common 版本读取。
- `kms`：普通命名空间 KV。
- `prompt`：Prompt 模板创建、删除、更新和渲染。

Common 版本不使用独立 policy；它只是 KMS 中的普通 KV：`system/common_version`。
