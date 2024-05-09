from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from src.core.dependencies import valid_user_create, valid_refresh_token, valid_refresh_token_user
from src.core.security import parse_jwt_user_data, create_access_token
from src.schemas.auth_schemas import (
    UserCreate,
    UserResponse,
    JWTData,
    AccessTokenResponse,
    AuthUser,
    UserPropertiesResponse,
)
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.utils.auth_utils import get_refresh_token_settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/user", status_code=status.HTTP_201_CREATED,
             response_model=UserPropertiesResponse,
             summary="Регистрация пользователя")
async def register_user(
        auth_data: UserCreate = Depends(valid_user_create),
) -> dict[str, str]:
    """
    - **login**: логин пользователя
    - **password**: пароль пользователя
    - **project_id**: проект, к которому принадлежит пользователь
    - **env**: название окружения, к которому принадлежит пользователь
    - **domain**: тип пользователя
    """
    user = await AuthService.create_user(auth_data)
    return {
        "id": user["id"],
        "login": user["login"],
        "project_id": user["project_id"],
        "env": user["env"],
        "domain": user["domain"]
    }


@router.get("/user/me", response_model=UserResponse,
            summary="Получить информацию о текущем пользователе",
            response_description="Возращает id и логин пользователя")
async def get_my_account(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user = await UserService.get_user_by_id(jwt_data.user_id)

    return {
        "id": user["id"],
        "login": user["login"]
    }


@router.post("/user/tokens", response_model=AccessTokenResponse,
             summary="Аутентификация пользователя",
             response_description="Возращает 2 токена: access и refresh")
async def auth_user(auth_data: AuthUser, response: Response) -> AccessTokenResponse:
    """
    - **login**: логин пользователя
    - **password**: пароль пользователя
    """
    user = await AuthService.authenticate_user(auth_data)
    refresh_token_value = await AuthService.create_refresh_token(user_id=user["id"])

    response.set_cookie(**get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/user/tokens", response_model=AccessTokenResponse,
            summary="Обновление токенов")
async def refresh_tokens(
        worker: BackgroundTasks,
        response: Response,
        refresh_token: dict[str, Any] = Depends(valid_refresh_token),
        user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await AuthService.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**get_refresh_token_settings(refresh_token_value))

    worker.add_task(AuthService.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/user/tokens", summary="Выход из учетной записи")
async def logout_user(
        response: Response,
        refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await AuthService.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
