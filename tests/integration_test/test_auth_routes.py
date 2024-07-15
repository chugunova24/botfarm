import asyncio
from uuid import UUID
from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from pydantic import ValidationError
from contextlib import nullcontext as does_not_raise

from src.core.config import settings
from src.core.constants import ErrorCode
from src.schemas.auth_schemas import UserCreate
from src.services.auth_service import AuthService
from src.services.user_service import UserService

prefix_url = settings.API_V1_STR

user_ok = {"login": "superuser1000",
           "password": "iFetup66!",
           "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
           "env": "stage",
           "domain": "canary"}

resp_ok = {"login": "superuser1000",
           "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
           "env": "stage",
           "domain": "canary"}


# @pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expectation",
    [
        (user_ok, does_not_raise()),
        # (user_ok["login"], pytest.raises(ValidationError)),
        # (user_ok["password"], pytest.raises(ValidationError)),
        # (user_ok["project_id"], pytest.raises(ValidationError)),
        # (user_ok["env"], pytest.raises(ValidationError)),
        # (user_ok["domain"], pytest.raises(ValidationError)),
    ]
)
def test_register(client: TestClient,
                  payload: dict[str, str],
                  expectation) -> None:
    """Тестирование регистрации пользователя"""

    resp = asyncio.run(client.post(prefix_url + "/auth/user",
                                      json=payload))

    print(f"RESP: {resp.json()}")

    if isinstance(expectation, does_not_raise):
        with expectation:
            assert resp.status_code == status.HTTP_201_CREATED
            resp = resp.json()
            assert len(resp.pop("id")) == 36
            assert resp == resp_ok
    elif isinstance(expectation.expected_exception, ValidationError):
        with expectation:
            assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# @pytest.mark.asyncio
# async def test_register_login_taken(client: TestClient,
#                                     user_payload: dict[str, str]) -> None:
#     """Попытка добавить двух пользователей с одинаковым логином"""
#     for _ in range(2):
#         resp = await client.post(prefix_url + "/auth/user",
#                                  json=user_payload)
#
#     assert resp.status_code == status.HTTP_400_BAD_REQUEST
#     assert resp.json() == {"detail": ErrorCode.LOGIN_TAKEN}
#
#
# @pytest.mark.asyncio
# async def test_users_list(client: TestClient,
#                           user_payload: dict[str, str]) -> None:
#     """Тестирование эндпоинта для вывода списка существующих пользователей"""
#
#     # добавление пользователей
#     for i in range(3):
#         user_payload["login"] = "superuser100" + str(i)
#         await client.post(prefix_url + "/auth/user",
#                           json=user_payload)
#
#     resp = await client.get(prefix_url + "/users")
#
#     assert resp.status_code == status.HTTP_200_OK
#     assert len(resp.json()["users"]) == 3
#
#
# # @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_user_acquire(client: TestClient,
#                             user_payload: dict[str, str]) -> None:
#     """Тестирование блокировки пользователя"""
#
#     # добавление пользователя
#     new_user = await AuthService.create_user(UserCreate(**user_payload))
#
#     resp = await client.patch(prefix_url + "/user/acquire",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_200_OK
#
#     resp = resp.json()
#     assert UUID(resp["id"]) == new_user["id"]
#     assert resp["locktime"] != datetime.utcfromtimestamp(0)
#
#     # Попытка заблокировать уже заблокированного пользователя
#     resp = await client.patch(prefix_url + "/user/acquire",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_403_FORBIDDEN
#
#     resp = resp.json()
#     assert resp["detail"] == ErrorCode.USER_ALREADY_BLOCK
#
#
# @pytest.mark.skip
# @pytest.mark.asyncio
# async def test_user_release(client: TestClient,
#                             user_payload: dict[str, str]) -> None:
#     """Тестирование снятие блокировки с пользователя"""
#
#     # Добавление пользователя
#     new_user = await AuthService.create_user(UserCreate(**user_payload))
#
#     # Разблокировка неблокированного пользователя
#     resp = await client.patch(prefix_url + "/user/release",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_200_OK
#
#     # Блокирование пользователя
#     resp = await client.patch(prefix_url + "/user/acquire",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_200_OK
#     resp = resp.json()
#     format_dt = "%Y-%m-%dT%H:%M:%S+%f"
#     assert UUID(resp["id"]) == new_user["id"]
#     assert datetime.strptime(resp["locktime"], format_dt).date() == datetime.utcnow().date()
#
#     # Повторное блокирование заблокированного пользователя
#     resp = await client.patch(prefix_url + "/user/acquire",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_403_FORBIDDEN
#     resp = resp.json()
#     assert resp["detail"] == ErrorCode.USER_ALREADY_BLOCK
#
#     # Разблокировка пользователя
#     resp = await client.patch(prefix_url + "/user/release",
#                               query_string={"user_id": new_user["id"]})
#     assert resp.status_code == status.HTTP_200_OK
#     resp = resp.json()
#     assert UUID(resp["id"]) == new_user["id"]
#     assert datetime.strptime(resp["locktime"], format_dt) == datetime.utcfromtimestamp(0)
