import re
from uuid import UUID
from datetime import datetime

from pydantic import Field, field_validator

from src.schemas.CustomModel import CustomModel
from src.utils.enums.enums import EnvironmentEnum, DomainEnum

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")


class UserSchema(CustomModel):
    login: str = Field(min_length=6, max_length=64)


class AuthUser(UserSchema):
    password: str = Field(min_length=6, max_length=128)

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class UserProperties(CustomModel):
    project_id: UUID
    env: EnvironmentEnum
    domain: DomainEnum


class UserCreate(AuthUser, UserProperties):
    ...


class JWTData(CustomModel):
    user_id: UUID = Field(alias="sub")


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserResponse(UserSchema):
    id: UUID


class UserPropertiesResponse(UserResponse, UserProperties):
    ...


class UsersListResponse(CustomModel):
    users: list["UserResponse"]


class UserLockResponse(UserResponse):
    locktime: datetime
