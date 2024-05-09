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

    POSTGRES_TEST_DB: str

    SITE_DOMAIN: str

    ENVIRONMENT: Environment = Environment.PRODUCTION
    # ENVIRONMENT: Environment = Environment.LOCAL

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    API_V1_STR: str = "/api/v1"

    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 10000  # minutes

    REFRESH_TOKEN_KEY: str = "5fd418df0f7aa74383a791ebfdbe115d078b36f71ca32b1875859847fa002209"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True

    # PATH_FILE_ENV: str = ".env_dev" if ENVIRONMENT == "LOCAL" else ".env"

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        if self.ENVIRONMENT == "LOCAL":
            self.POSTGRES_HOST = "127.0.0.1"
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def TEST_DATABASE_URL(self) -> PostgresDsn:
        if self.ENVIRONMENT == "LOCAL":
            self.POSTGRES_HOST = "127.0.0.1"
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}")

    @property
    def SYNC_DATABASE_URL(self) -> PostgresDsn:
        if self.ENVIRONMENT == "LOCAL":
            self.POSTGRES_HOST = "127.0.0.1"
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding='utf-8',
                                      extra='allow')


settings = Config()

print(settings.DATABASE_URL)

app_configs: dict[str, Any] = {"title": "Botfarm API"}
