from typing import Any

from pydantic import UUID4
from src.repositories.auth_repository import RefreshTokenRepository
from src.utils.exceptions.auth_exceptions import InvalidCredentials
from src.schemas.auth_schemas import AuthUser, UserCreate
from src.core.security import check_password
from src.core.database import execute, fetch_one
from src.utils.generate_random_alphanum import generate_random_alphanum
from src.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    async def create_user(user: UserCreate) -> dict[str, Any] | None:
        insert_query = await UserRepository.create(user)

        return await fetch_one(insert_query)

    @staticmethod
    async def create_refresh_token(*, refresh_token: str | None = None,
                                   user_id: int) -> str:
        if not refresh_token:
            refresh_token = generate_random_alphanum(64)

        insert_query = await RefreshTokenRepository.create(user_id, refresh_token)
        await execute(insert_query)

        return refresh_token

    @staticmethod
    async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
        select_query = await RefreshTokenRepository.get(refresh_token)

        return await fetch_one(select_query)

    @staticmethod
    async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
        update_query = await RefreshTokenRepository.expire(refresh_token_uuid)

        await execute(update_query)

    @staticmethod
    async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
        select_query = await UserRepository.get_by_login(auth_data.login)

        user = await fetch_one(select_query)
        if not user:
            raise InvalidCredentials()

        if not check_password(auth_data.password, user["password"]):
            raise InvalidCredentials()

        return user
