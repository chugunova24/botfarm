from typing import Any

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import Environment


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SITE_DOMAIN: str

    ENVIRONMENT: Environment = Environment.LOCAL

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    API_V1_STR: str

    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 10000  # minutes

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def SYNC_DATABASE_URL(self) -> PostgresDsn:
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding='utf-8',
                                      extra='allow')


settings = Config()

print(settings.DATABASE_URL)

app_configs: dict[str, Any] = {"title": "Botfarm API"}
