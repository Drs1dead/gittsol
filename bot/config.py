from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str
    super_admin_ids: str = ""

    db_driver: str = "sqlite"
    db_path: str = "data/bot.db"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "botuser"
    db_password: str = "secret"
    db_name: str = "broadcast_bot"

    default_interval: int = 10
    chat_monitor_interval: int = 600

    chats_per_page: int = 8
    posts_per_page: int = 5
    logs_per_page: int = 10
    admins_per_page: int = 8

    @property
    def super_admins(self) -> set[int]:
        if not self.super_admin_ids.strip():
            return set()
        return {int(x.strip()) for x in self.super_admin_ids.split(",") if x.strip()}

    @property
    def database_url(self) -> str:
        if self.db_driver == "sqlite":
            path = Path(self.db_path).resolve()
            return f"sqlite+aiosqlite:///{path.as_posix()}"
        if self.db_driver == "mysql":
            return (
                f"mysql+aiomysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
