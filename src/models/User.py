import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    LargeBinary,
    String,
    Table,
    func,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID

from src.utils.enums.enums import EnvironmentEnum, DomainEnum
from src.core.database import metadata

auth_user = Table(
    "auth_user",
    metadata,
    Column("id", UUID, default=uuid.uuid4, unique=True, primary_key=True),
    Column("login", String, unique=True, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("project_id", UUID, nullable=False),
    Column("env", Enum(EnvironmentEnum), nullable=False),
    Column("domain", Enum(DomainEnum), nullable=False),
    Column("locktime", DateTime, default=datetime.utcfromtimestamp(0), nullable=True),
)
