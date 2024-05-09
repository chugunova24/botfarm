import uuid
from datetime import datetime

from sqlalchemy import insert, select
from sqlalchemy import (
    Insert,
    Select,
    Update,
)


from src.schemas.auth_schemas import UserCreate
from src.core.security import hash_password
from src.models.User import auth_user


class UserRepository:

    @staticmethod
    async def create(user: UserCreate) -> Insert:
        print(user)
        insert_query = (
            insert(auth_user)
            .values(
                {
                    "login": user.login,
                    "password": hash_password(user.password),
                    "created_at": datetime.utcnow(),
                    "project_id": user.project_id,
                    "env": user.env,
                    "domain": user.domain
                }
            )
            .returning(auth_user)
        )

        return insert_query

    @staticmethod
    async def list() -> Select:
        select_query = select(auth_user)

        return select_query

    @staticmethod
    async def get_by_id(user_id: int) -> Select:
        select_query = select(auth_user).where(auth_user.c.id == user_id)

        return select_query

    @staticmethod
    async def set_lock(user_id: uuid.UUID, locktime: datetime) -> Update:
        update_query = (
            auth_user.update()
            .values(locktime=locktime)
            .where(auth_user.c.id == user_id)
            .returning(auth_user.c.id,
                       auth_user.c.login,
                       auth_user.c.locktime)
        )

        return update_query

    @staticmethod
    async def get_by_login(login: str) -> Select:
        select_query = select(auth_user).where(auth_user.c.login == login)

        return select_query
