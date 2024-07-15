import uuid
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from src.core.constants import ErrorCode
from src.core.database import fetch_one, fetch_all
from src.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    async def get_list_users() -> list[dict]:
        select_query = await UserRepository.list()

        return await fetch_all(select_query)

    @staticmethod
    async def get_user_by_id(user_id: uuid.UUID) -> dict[str, Any] | None:
        select_query = await UserRepository.get_by_id(user_id)

        return await fetch_one(select_query)

    @staticmethod
    async def acquire_lock_user(user: dict[str, Any]) -> dict[str, Any] | None:
        if user["locktime"].timestamp() > 0:
            raise HTTPException(status_code=403, detail=ErrorCode.USER_ALREADY_BLOCK)

        update_query = await UserRepository.set_lock(user["id"], datetime.utcnow())

        return await fetch_one(update_query)

    @staticmethod
    async def release_lock_user(user: dict[str, Any]) -> dict[str, Any] | None:
        if user["locktime"].timestamp() == 0:
            return user
        update_query = await UserRepository.set_lock(user["id"], datetime.utcfromtimestamp(0))

        return await fetch_one(update_query)

    @staticmethod
    async def get_user_by_login(login: str) -> dict[str, Any] | None:
        select_query = await UserRepository.get_by_login(login)

        return await fetch_one(select_query)
