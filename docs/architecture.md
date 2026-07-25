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

`Ruler` 是共享控制面。它负责内部 HTTP API、内部服务鉴权、共享数据访问、KMS、Prompt、Record、Tool 等底层能力。当前阶段暂不提供 Corpus 能力。

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

Common 版本由 `teaine-common` 程序包内的 `__version__` 定义。Common SDK 会在内部请求头中自动携带调用端 common 版本；Ruler 收到该请求头时会与服务端当前导入的 common 版本做一致性检查。未携带该请求头的内部请求会跳过 common 版本检查。

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

## 5. 开发规范

### 5.1 目录与边界

- 新模块应先明确服务边界和目录职责，再补充实现代码。
- `Common` 只放跨服务稳定共享的 DTO、枚举、错误、类型别名和 SDK；公共兼容路径需要保留或制定迁移计划后再删除。
- 服务内部目录应只保留当前实现需要的代码。废弃兼容层、空包、未接入的占位目录和重复定义应及时删除。
- 当新的设计与既有文档冲突时，以当前确认后的设计为准，并同步修改文档。

### 5.2 Python 代码风格

- Python 代码应尽可能完善类型注解，公共函数、类和数据模型的输入输出类型必须明确。
- 优先使用仓库已有工具进行格式化、静态检查和测试。
- 涉及依赖新增、删除或版本调整时，必须使用对应模块的 `uv add`、`uv remove`、`uv lock` 等命令完成，不直接手写 `pyproject.toml` 或 `uv.lock` 的依赖变更。
- 不在 import 外层添加 try/except。
- 注释和 docstring 使用中文。
- 方法 docstring 使用 Sphinx 风格标签，例如 `:param xxx:`、`:return:`、`:raises Xxx:`。
- 只保留必要注释和 docstring，内容聚焦模块、类、函数、参数、返回值、异常和关键约束。
- 不编写“针对某个需求”“开发方法”“为达成某个目的”等无法帮助理解代码本身的解释性注释。

### 5.3 Ruler 当前实现约定

- Ruler 目录使用 `app/services` 作为业务服务层，不再使用旧名 `core`。
- Ruler 目录使用 `app/infra` 作为基础设施适配层，不再使用旧名 `infrastructure`。
- Ruler 内部请求校验应作为 `app/middleware` 下的 HTTP middleware 提供；服务身份、API key、Common 版本检查分别由独立 middleware 承担，不恢复单独的 `security` 目录。
- 日志入口放在 `app/utils/log.py`，不恢复单独的 `logging` 目录。
- Ruler 配置入口放在 `app/config.py`，不放在 Ruler 根目录。
- Ruler 当前能力保留 `system`、`kms`、`prompt`；Corpus 当前已从 Ruler 和 Common 中移除。
- KMS 使用数据库存储，写入追加新版本，读取返回最新版本，value 入库前需要编码。
- Prompt 使用数据库存储，字段为 `name`、`description`、`content`、`params`；渲染时必须校验 `params` 声明的必需参数。
- Ruler 不再使用本地 `app/data` 存储 KMS、Prompt 或 Corpus 数据。
- Ruler 启动参数为 `python -m app --env test|prod`，默认 `test`；环境变量清单文件使用 `.env.test` 和 `.env.prod`，当前只写变量键名。

### 5.4 测试与提交

- 每个可运行模块都应具备对应单元测试。
- 修改或新增模块时，应同步补齐受影响行为的测试。
- 提交 PR 前必须运行相关测试；如果测试受本地环境限制无法完整执行，需要在 PR 说明中写明限制和已完成的替代检查。
