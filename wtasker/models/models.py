from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from datetime import datetime


metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, nullable=False, default=datetime.utcnow),
)


tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("status", String, nullable=False, default="pending"),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
)
