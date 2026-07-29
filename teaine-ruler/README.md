# Teaine-Ruler

茶因计划·资源管理器后端。

Ruler 是 Project Teaine 的内部控制面服务，提供 HTTP API、内部服务鉴权、Prompt、KMS、Record 和 Tool 等底层能力。

## 技术选择

Ruler 以 Supabase PostgreSQL 作为主数据存储。服务端核心数据访问优先通过 SQLAlchemy async / PostgreSQL connection 完成；Supabase SDK 只作为后续访问 Supabase Auth、Storage、Realtime 等能力的可选基础设施封装。

## 本地配置

仓库只提交 `.env.test.example` 和 `.env.prod.example` 模板文件；真实 `.env.test`、`.env.prod` 存放本地密钥和数据库链接，不提交到 Git。

首次配置时复制模板并填入本地值：

```powershell
Copy-Item .env.test.example .env.test
Copy-Item .env.prod.example .env.prod
```

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

Common 版本由 `teaine-common` 程序包内的 `__version__` 定义。Ruler 的 system 接口会报告服务端当前导入的 common 版本。
Common SDK 会在内部请求头中自动携带本地 common 版本；如果请求未携带 `X-Teaine-Common-Version`，Ruler 会跳过版本检查。
