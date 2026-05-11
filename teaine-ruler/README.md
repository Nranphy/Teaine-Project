# Teaine-Ruler

茶因计划·资源管理器后端

本文档描述 Teaine Ruler 的目标架构和开发规则。它基于当前最新设计，而不是旧版实现。

## 角色定位

Ruler 是 Project Teaine 的共享后端控制服务。

Ruler 是唯一直接接入 Supabase、LanceDB 等底层存储与检索基础设施的服务。其他服务应通过 Ruler API，或通过 `teaine-common` 中提供的 SDK 和数据模型访问这些能力。

Ruler 负责共享数据访问、持久化协调、检索支持、工具执行和密钥存储。Ruler 不应演变成 Agent 运行时、角色运行时、平台适配器或表现层。

Ruler 主要面向内部服务使用。服务间访问通过 API key 中间件进行鉴权和审计。每个内部服务应拥有独立 API key。

## 依赖边界

Ruler 可以依赖：

- `teaine-common`：提供共享数据模型、SDK 类型、请求/响应 schema 和面向客户端的契约。
- Supabase：提供结构化持久化能力。
- LanceDB：提供向量存储与检索能力。
- 工具能力所需的外部 API。

其他 Teaine 服务不应直接连接 Supabase、LanceDB 或类似共享基础设施。它们应通过 Ruler，或通过 `teaine-common` 中的 SDK 接口访问这些能力。

## API 领域

Ruler API 按领域组织。每个领域都应在 `api/` 下拥有自己的 router。

API 应预留版本层，例如 `api/v1/`。当前即使没有外部服务依赖，也应把新接口放在版本目录下，避免未来服务间契约发生破坏性变更时难以迁移。

### prompt

`prompt` 领域管理存储在 Supabase 表中的提示词模板。

预期能力：

- 创建 prompt 记录。
- 读取 prompt 记录。
- 更新 prompt 记录。
- 删除 prompt 记录。
- 使用传入参数渲染 prompt。
- 在共享模型需要时支持 prompt 版本和元数据。

Prompt 渲染应作为共享 core 能力实现，不应在路由函数中临时拼接或做零散字符串处理。

### knowledge

`knowledge` 领域管理知识文本。知识文本维护在 Supabase 表中，对应向量维护在 LanceDB 中。

预期能力：

- 创建 knowledge 记录。
- 读取 knowledge 记录。
- 更新 knowledge 记录。
- 删除 knowledge 记录。
- 基于语义相似度和结构化过滤条件搜索知识。
- 刷新 embedding 和向量索引。
- 保持 Supabase 记录和 LanceDB 向量条目同步。

Supabase 行记录是知识结构化元数据的事实来源。LanceDB 是检索索引。

`knowledge` 与 `memory` 在底层能力上高度相似，可以共享同一套 core 管理逻辑，例如文本存储、embedding、向量同步和搜索流程。但二者在 API 层必须保持领域区分，因为知识和记忆不是同一种业务对象。

### memory

`memory` 领域管理长记忆和短记忆。

记忆数据维护在 Supabase 中；当需要检索能力时，对应内容也会索引到 LanceDB。

预期能力：

- 添加记忆。
- 搜索记忆。
- 区分长记忆和短记忆。
- 在 common 模型提供支持时，维护 owner、scope、source、timestamp、过期策略等结构化元数据。
- 刷新记忆 embedding 和索引。

长记忆应视为持久共享状态。短记忆可以具有生命周期或过期行为，但相关策略必须在模型和 core 逻辑中明确表达。

### record

`record` 领域是最简单的结构化记录模块，也是其他服务向 Ruler 上报结构化数据的 HTTP 暴露层。

它会细分为多个模型，例如 interaction 等。每个模型使用 `teaine-common` 提供的共享语义模型作为 API 契约，由 Ruler 接收后写入数据库。虽然这些模型通常会对应数据库表，但 API 不应直接暴露裸 SQL 字段，而应以 common 模型表达业务语义。

每个 record 模型都应提供基础 CRUD 能力。

预期能力：

- 创建记录。
- 按 id 或查询过滤条件读取记录。
- 更新记录。
- 删除记录。
- 在不同 record 模型之间保持一致的路由行为。

Record 路由应保持轻量。共享 CRUD 行为应放在 `core/` 或可复用 helper 中。

### tool

`tool` 领域向其他服务暴露通用工具能力。

示例能力：

- 查询日期和时间。
- 网页搜索。
- 图像识别。
- 其他需要集中管控的共享工具。

当工具 API 会被多个服务消费时，应在 `teaine-common` 中定义清晰的输入/输出模型。`teaine-common` 更新后，Ruler 可以随之重新部署，因此工具契约可以跟随 common 演进。

### kms

`kms` 领域管理加密的键值数据。

密钥和服务配置值会由 SDK 加密后发送给 Ruler，并存储到 Supabase 中。Ruler 负责保存加密后的 KV 数据，不负责明文加密逻辑。

KMS 当前不提供细粒度权限模型。内部服务在通过 API key 鉴权后，可以通过 Ruler API 存取 KV 数据。

预期能力：

- 存储加密 KV 数据。
- 读取加密后的 value。
- 更新 value。
- 删除 value。
- 在共享模型支持时，提供 namespace、owner 或 scope。

不得记录明文密钥、凭据或敏感 KMS value。正常情况下，Ruler 不应接触明文 secret。

## 程序结构

Ruler 的目标目录结构为：

```text
teaine-ruler/
  app/
    api/
      __init__.py
      v1/
        __init__.py
        prompt/
        knowledge/
        memory/
        record/
        tool/
        kms/
    core/
      prompt/
      knowledge/
      memory/
      record/
      tool/
      kms/
    utils/
    config.py
    app.py
    __main__.py
```

### api/

`api/` 存放按 API 领域和版本分组的 HTTP router。

每个领域可以定义一个或多个 router。路由函数应保持轻量：负责校验请求模型、调用 core 服务、把已知领域错误映射为 HTTP 响应，并返回响应模型。

### api/__init__.py

`api/__init__.py` 暴露 `routers` 列表，供 `app.py` 集中注册。

新增 API 领域时，应把 router 加入该列表，而不是直接在 `app.py` 中手动注册。

Router 注册项应包含必要的注册元数据，例如 router、prefix、tags 和版本信息。可以使用简单的数据结构表达，不需要引入复杂框架。

### core/

`core/` 存放领域服务逻辑。

Core 模块可以共享以下能力：

- CRUD 编排。
- Prompt 渲染。
- Embedding 生成。
- 向量索引刷新。
- Supabase SDK 访问与领域编排。
- LanceDB 同步。
- 加密和解密流程。

路由处理函数不应承载这些行为。

当多个 API 领域拥有相同底层流程时，应优先在 core 中抽出共享管理逻辑。例如 `knowledge` 和 `memory` 可以共用一套依赖 Supabase 与 LanceDB 的文本检索管理能力，再由各自 API 层提供不同领域入口。

### utils/

`utils/` 存放底层包装和基础设施 helper。

示例：

- Supabase client 创建。
- LanceDB client 类或函数封装。
- Embedding provider 包装。
- 加密 helper。
- 日志 helper。
- 通用错误类型。

Utils 应保持基础设施导向，不应编码领域业务规则。Utils 中的能力应尽量保持无状态；如果需要状态，例如 LanceDB client，也应通过实例化后交由 core 使用。

### config.py

`config.py` 负责运行时配置。

配置应包括连接设置、凭据、功能开关和服务级默认值。配置需要类型化并经过校验。

密钥应安全加载，且不得打印到日志中。

### app.py

`app.py` 创建 FastAPI 应用，并从 `api.routers` 注册所有 router。

应用级 middleware、异常处理器、生命周期钩子和 API 元数据应放在这里。

API key 鉴权和审计中间件也应在这里注册，或由这里引用统一的 middleware 实现。

### __main__.py

`__main__.py` 是可执行入口。

它应使用配置好的 ASGI server 启动应用，不应包含领域逻辑或路由注册逻辑。

## 设计规则

- 保持 Ruler 作为共享基础设施访问边界。
- 将共享契约放在 `teaine-common` 中。
- 保持 HTTP route handler 轻量。
- 将可复用领域行为放在 `core/` 中。
- 将基础设施包装放在 `utils/` 中。
- 将 Supabase 视为结构化数据的事实来源。
- 将 LanceDB 视为向量检索和索引层。
- 显式处理 Supabase 与 LanceDB 的同步。
- 使用 API key 中间件完成内部服务鉴权和审计。
- 避免让 Ruler 耦合到特定平台适配器或 Agent 运行时。
- 避免重复定义应归属于 `teaine-common` 的数据模型。
- 不得记录明文密钥、凭据或敏感 KMS value。

## 迁移说明

更新旧版 Ruler 代码时，应优先向本文档定义的目标架构迁移，而不是保留旧的本地文件型 manager 或 common 重构前的导入方式。

当现有行为与本文档定义的架构冲突时，可以替换现有行为。

## 旧版 TODO

### db 模型相关

- [ ] 用户表模型中的私参部分目前只支持了 Bilibili，其他平台需要在调研后再设计私参模型。

- [ ] 场景实例模型中的私参部分未进行标准化定义。

- [ ] 交互模型当前仅提供了直播场景枚举。

- [ ] 交互模型未考虑直播弹幕相互回复的场景。

- [ ] 交互模型中的私参部分未进行标准化定义。

### corpus 相关

- [ ] 语料数据集信息需要加上已有语料数量
