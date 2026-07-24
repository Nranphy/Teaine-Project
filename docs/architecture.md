# Project Teaine 架构设计

## 1. 目标

Project Teaine 是一个分布式、以本地优先为核心的虚拟 Agent 系统。项目被拆分为多个服务，使运行时编排、云端协调、平台接入和演出执行可以独立演进。

当前服务集合如下：

- `Ruler`：中心服务与共享控制面。
- `Grail`：本地 Agent 运行时与编排引擎。
- `Caster`：本地演出执行器，负责 Live2D、语音和文本输出。
- `Archer`：平台入口采集器，负责弹幕和外部事件接入。
- `Rider`：本地管理界面。
- `Common`：公共模型、类型、错误和 SDK。

## 2. 服务边界

### 2.1 Ruler

`Ruler` 是共享控制面。它负责内部 HTTP API、内部服务鉴权、共享数据访问、KMS、Prompt、Corpus、Record、Tool 等底层能力。

Ruler 当前以 Supabase PostgreSQL 作为主数据存储。服务端核心数据访问优先通过 SQLAlchemy async / PostgreSQL connection 完成；Supabase SDK 只作为后续访问 Auth、Storage、Realtime 等 Supabase 能力的可选基础设施封装。

内部接口统一放在 `/api/v1/internal/**`，默认要求内部服务 API key。公开接口统一放在 `/api/v1/public/**`，当前只用于探活等低风险能力。

### 2.2 Common

`Common` 存放跨服务稳定共享的定义和 SDK。

适合放在 Common 的内容：

- DTO 和协议模型。
- 枚举和错误类型。
- JSON、ID、时间戳等 typing helper。
- 面向跨模块调用的 SDK，例如 `teaine_common.sdk.ruler`。
- 不依赖具体服务运行时的纯工具函数。

不适合放在 Common 的内容：

- Ruler 内部 ORM 模型。
- 服务专属数据库访问逻辑。
- 隐式依赖运行时环境的单例。
- 业务编排逻辑。

Common 版本由 Ruler KMS 中的普通 KV 记录，默认键为 `system/common_version`。Common SDK 可以在启动时读取该 KV，并与本地包版本做严格一致性检查。

### 2.3 Grail

`Grail` 是本地 Agent 执行引擎，负责上下文构造、推理循环、工具调度和交互流程。

### 2.4 Caster

`Caster` 是本地表现层，将结构化输出意图转换为 Live2D、TTS、文本等演出行为。

### 2.5 Archer

`Archer` 是第三方平台入口适配层，负责连接平台事件源、标准化事件并上传到 Ruler。

### 2.6 Rider

`Rider` 是本地管理界面，用于展示服务状态、管理配置、查看 Session、Run、日志和待播放输出。

## 3. 推荐通信路径

- `Archer -> Ruler`
- `Rider -> Ruler`
- `Grail -> Ruler`
- `Grail -> Caster`
- `Rider -> Grail`
- `Rider -> Caster`

除非有充分理由，应避免：

- `Archer -> Grail` 的直接运行时注入。
- `Archer -> Caster`。
- `Ruler -> Caster` 的直接演出控制。
- `Rider` 与内部业务逻辑的重耦合。

## 4. 运行时主流程

`平台输入 -> Archer -> Ruler -> 触发/同步 -> Grail -> 工具循环 -> OutputIntent -> Caster -> 演出结果 -> 同步/记录`

后续应在 Common 中补齐 `Event`、`Session`、`Run`、`Task`、`OutputIntent` 和 `PerformanceJob` 等跨服务协议对象。
