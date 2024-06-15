import os

from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    OWNER_TELEGRAM_ID: int
    ADMIN_TELEGRAM_ID: int
    OUTPUT_CHAT_TELEGRAM_ID: int
    TELEGRAM_BOT_TOKEN: str
    DEBUG_MODE: bool

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
