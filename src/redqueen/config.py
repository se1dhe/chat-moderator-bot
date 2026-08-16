"""Application configuration loaded from environment / .env."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Telegram
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    owner_ids: str = Field(default="", alias="OWNER_IDS")

    # Database
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="redqueen", alias="POSTGRES_DB")
    postgres_user: str = Field(default="redqueen", alias="POSTGRES_USER")
    postgres_password: str = Field(default="change-me", alias="POSTGRES_PASSWORD")
    database_url: str = Field(default="", alias="DATABASE_URL")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # AI
    ollama_url: str = Field(default="http://localhost:11434", alias="OLLAMA_URL")
    ollama_model: str = Field(default="qwen3.5:4b", alias="OLLAMA_MODEL")
    ai_enabled: bool = Field(default=False, alias="AI_ENABLED")

    # Runtime
    run_mode: str = Field(default="polling", alias="RUN_MODE")
    webhook_base_url: str = Field(default="", alias="WEBHOOK_BASE_URL")
    webhook_path: str = Field(default="/webhook", alias="WEBHOOK_PATH")
    webhook_host: str = Field(default="0.0.0.0", alias="WEBHOOK_HOST")
    webhook_port: int = Field(default=8080, alias="WEBHOOK_PORT")
    webhook_secret: str = Field(default="", alias="WEBHOOK_SECRET")

    default_lang: str = Field(default="en", alias="DEFAULT_LANG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_dsn(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def owner_id_set(self) -> set[int]:
        out: set[int] = set()
        for part in self.owner_ids.replace(";", ",").split(","):
            part = part.strip()
            if part.isdigit():
                out.add(int(part))
        return out


@lru_cache
def get_settings() -> Settings:
    return Settings()
