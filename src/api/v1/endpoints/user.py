from typing import Any
from fastapi import APIRouter, Depends

from src.core.dependencies import valid_user_id
from src.schemas.auth_schemas import (
    UsersListResponse,
    UserLockResponse,
)
from src.services.user_service import UserService


router = APIRouter(
    tags=["User"],
)


@router.get("/users",
            response_model=UsersListResponse,
            summary="Список пользователей")
async def get_list_users() -> list[dict]:
    users = await UserService.get_list_users()

    return {"users": users}


@router.patch("/user/acquire",
              response_model=UserLockResponse,
              summary="Наложение блокировки на пользователя")
async def acquire_lock_user(
        user: dict[str, Any] = Depends(valid_user_id)) -> dict[str, Any]:
    """
    - **user_id**: uuid пользователя
    """

    return await UserService.acquire_lock_user(user)


@router.patch("/user/release",
              response_model=UserLockResponse,
              summary="Снятие блокировки на пользователя")
async def release_lock_user(
        user: dict[str, Any] = Depends(valid_user_id)) -> dict[str, Any]:
    """
    - **user_id**: uuid пользователя
    """

    return await UserService.release_lock_user(user)
