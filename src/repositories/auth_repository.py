import uuid
from datetime import datetime, timedelta

from pydantic import UUID4
from sqlalchemy import (
    Insert,
    Select,
    Update,
)

from src.core.config import settings
from src.models.Tokens import refresh_tokens


class RefreshTokenRepository:

    @staticmethod
    async def create(user_id: int, refresh_token: str | None = None) -> Insert:
        insert_query = refresh_tokens.insert().values(
            uuid=uuid.uuid4(),
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(seconds=settings.REFRESH_TOKEN_EXP),
            user_id=user_id,
        )

        return insert_query

    @staticmethod
    async def get(refresh_token: str) -> Select:
        select_query = refresh_tokens.select().where(
            refresh_tokens.c.refresh_token == refresh_token
        )

        return select_query

    @staticmethod
    async def expire(refresh_token_uuid: UUID4) -> Update:
        update_query = (
            refresh_tokens.update()
            .values(expires_at=datetime.utcnow() - timedelta(days=1))
            .where(refresh_tokens.c.uuid == refresh_token_uuid)
        )

        await update_query
