from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import Cookie, Depends

from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.utils.exceptions.auth_exceptions import (
    LoginTaken,
    RefreshTokenNotValid,
    InvalidUserUUID,
)
from src.schemas.auth_schemas import AuthUser, UserCreate


async def valid_user_create(user: UserCreate) -> AuthUser:
    if await UserService.get_user_by_login(user.login):
        raise LoginTaken()

    return user


async def valid_user_id(user_id: UUID) -> UUID:
    if not user_id:
        raise InvalidUserUUID()

    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise InvalidUserUUID()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await AuthService.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await UserService.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
