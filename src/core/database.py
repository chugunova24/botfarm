from typing import Any, AsyncGenerator

from sqlalchemy import (
    CursorResult,
    Insert,
    MetaData,
    Select,
    Update,
    create_engine,
    Delete,
    TextClause,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.core.config import settings
from src.core.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)
SYNC_DATABASE_URL = str(settings.SYNC_DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=False)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as db:
        yield db


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as db:
        cursor: CursorResult = await db.execute(select_query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as db:
        cursor: CursorResult = await db.execute(select_query)
        return [r._asdict() for r in cursor.all()]


async def execute(query: Insert | Update | Delete | TextClause) -> None:
    async with engine.begin() as db:
        await db.execute(query)
