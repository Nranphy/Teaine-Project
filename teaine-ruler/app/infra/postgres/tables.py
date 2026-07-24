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

__all__ = ["kms_entries", "metadata", "prompt_templates"]
