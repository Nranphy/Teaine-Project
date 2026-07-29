"""
Ruler 当前使用的数据库表定义。

kms_entries：
    存储版本化 KMS 键值。namespace、key、version 组成复合主键，
    value 为加密后的密文文本。

prompt_templates：
    存储 Prompt 模板。name 为主键，description 是说明文本，
    content 是模板内容，params 是半角逗号分隔的必需参数名。
"""

from sqlalchemy import Column, Integer, MetaData, String, Table


metadata = MetaData()

kms_entries = Table(
    "kms_entries",
    metadata,
    Column("namespace", String, primary_key=True),
    Column("key", String, primary_key=True),
    Column("version", Integer, primary_key=True),
    Column("value", String, nullable=False),
)

prompt_templates = Table(
    "prompt_templates",
    metadata,
    Column("name", String, primary_key=True),
    Column("description", String, nullable=False),
    Column("content", String, nullable=False),
    Column("params", String, nullable=False),
)

__all__ = [
    "metadata",
    "kms_entries",
    "prompt_templates",
]
