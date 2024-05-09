from sqlalchemy import (
    Column,
    DateTime,
    String,
    Table,
    func,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import metadata

refresh_tokens = Table(
    "auth_refresh_token",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
