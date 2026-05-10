# Tables SQL

本目录存放数据库表结构 DDL，每个表一个 `.sql` 文件，文件名与表名保持一致。

## 文件规范

- 使用 PostgreSQL 语法。
- 每个文件只定义一张表。
- 表 SQL 保持干净，不写行内注释；字段语义以 `teaine_common.models.entity` 中的实体模型为准。
- 本目录只允许定义字段、主键和唯一约束；不允许定义索引、外键、触发器、函数、视图或查询 SQL。

## 字段规范

- 主键统一使用 `id SERIAL NOT NULL`，并在表尾声明 `PRIMARY KEY (id)`。
- 时间戳字段使用 `BIGINT`，单位统一为毫秒。
- JSON 字段使用 `JSON`，需要空对象默认值时写 `DEFAULT '{}'::json`。
- 可为空字段显式说明业务含义。

## 默认值规范

- 必填业务标识字段不设置空字符串默认值，例如 `platform`、`platform_user_id`。
- 可缺省文本字段可使用 `DEFAULT ''`。
- JSON 扩展字段可使用 `DEFAULT '{}'::json`。
- 毫秒时间戳默认值可使用 `DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT`

## 命名规范

- 表名使用小写蛇形命名，例如 `user_info`。
- 字段名使用小写蛇形命名，例如 `platform_user_id`。
- 唯一约束命名为 `uq_<table>_<columns>`，例如 `uq_user_info_platform_user_id`。
- 普通索引命名为 `idx_<table>_<columns>`。
- 唯一索引命名为 `uidx_<table>_<columns>`。
- 检查约束命名为 `ck_<table>_<rule>`。
- 所有非主键约束和索引都必须显式命名，避免依赖数据库自动命名。
