import bcrypt
from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.core.config import settings
from src.utils.exceptions.auth_exceptions import AuthRequired, InvalidToken
from src.schemas.auth_schemas import JWTData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user/tokens", auto_error=False)


def hash_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, password_in_db)


def create_access_token(
    *,
    user: dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=settings.JWT_EXP),
) -> str:
    jwt_data = {
        "sub": str(user["id"]),
        "exp": datetime.utcnow() + expires_delta,
        # "is_admin": user["is_admin"],
    }

    return jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token
