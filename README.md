# 茶因计划 Teaine-Project

Project Teaine 是一个本地优先的分布式虚拟 Agent 系统。当前仓库按服务拆分为：

- `teaine-common`：跨服务 DTO、typing、错误类型和 SDK。
- `teaine-ruler`：共享控制面后端，提供内部 HTTP API、鉴权、KMS、Prompt 等能力。
- `teaine-grail`：本地 Agent 运行时与编排引擎。
- `teaine-caster`：本地演出执行器。
- `teaine-archer`：第三方平台事件采集器。
- `teaine-rider`：本地管理界面。

当前重构优先级集中在 `common` 和 `ruler`。Ruler 的内部 API 统一放在 `/api/v1/internal/**`，公开探活接口放在 `/api/v1/public/**`。
