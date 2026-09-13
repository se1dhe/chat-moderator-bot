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
    # White-label: display brand for this bot instance (used in the registry + persona).
    bot_brand: str = Field(default="RedQueen", alias="BOT_BRAND")
    # Run several brand bots in one process (orchestrator). Comma/newline-separated
    # tokens + parallel brands; empty falls back to the single BOT_TOKEN / BOT_BRAND.
    bot_tokens: str = Field(default="", alias="BOT_TOKENS")
    bot_brands: str = Field(default="", alias="BOT_BRANDS")

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
    ollama_model: str = Field(default="qwen3:4b", alias="OLLAMA_MODEL")
    # Vision model for multimodal anti-scam (e.g. "qwen2.5vl:7b", "llava:7b"). Empty
    # disables image analysis (captions still checked by the text path).
    ollama_vision_model: str = Field(default="", alias="OLLAMA_VISION_MODEL")
    ai_enabled: bool = Field(default=True, alias="AI_ENABLED")
    ai_max_concurrency: int = Field(default=2, alias="AI_MAX_CONCURRENCY")
    # Voice anti-scam via faster-whisper. Empty disables it. Needs the `voice` extra
    # (`uv sync --extra voice`); the model auto-downloads on first use.
    whisper_model: str = Field(default="", alias="WHISPER_MODEL")  # e.g. "small", "base"
    whisper_device: str = Field(default="cpu", alias="WHISPER_DEVICE")
    whisper_compute: str = Field(default="int8", alias="WHISPER_COMPUTE")
    # Pull OLLAMA_MODEL automatically on startup if it isn't present yet (backend
    # self-provisioning). Runs in the background; AI uses the rule fallback until ready.
    ollama_auto_pull: bool = Field(default=True, alias="OLLAMA_AUTO_PULL")

    # Runtime
    run_mode: str = Field(default="polling", alias="RUN_MODE")
    webhook_base_url: str = Field(default="", alias="WEBHOOK_BASE_URL")
    webhook_path: str = Field(default="/webhook", alias="WEBHOOK_PATH")
    webhook_host: str = Field(default="0.0.0.0", alias="WEBHOOK_HOST")
    webhook_port: int = Field(default=8080, alias="WEBHOOK_PORT")
    webhook_secret: str = Field(default="", alias="WEBHOOK_SECRET")

    # Mini App / API server. In polling mode the API listens here; in webhook mode the
    # webhook is mounted onto the same app on webhook_host/webhook_port instead.
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8080, alias="API_PORT")
    webapp_dist: str = Field(default="webapp/dist", alias="WEBAPP_DIST")
    # Public HTTPS URL of the served Mini App (e.g. https://<domain>/app). When set,
    # the bot wires it to the chat menu button and the /panel command.
    webapp_url: str = Field(default="", alias="WEBAPP_URL")

    default_lang: str = Field(default="en", alias="DEFAULT_LANG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    secret_key: str = Field(default="", alias="SECRET_KEY")
    cryptopay_token: str = Field(default="", alias="CRYPTOPAY_TOKEN")

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

    @property
    def token_list(self) -> list[str]:
        """All bot tokens to run (BOT_TOKENS if set, else the single BOT_TOKEN)."""
        raw = self.bot_tokens or self.bot_token
        return [t.strip() for t in raw.replace("\n", ",").split(",") if t.strip()]

    @property
    def brand_list(self) -> list[str]:
        """Brands parallel to token_list; padded with BOT_BRAND when shorter."""
        brands = [b.strip() for b in self.bot_brands.replace("\n", ",").split(",") if b.strip()]
        tokens = self.token_list
        while len(brands) < len(tokens):
            brands.append(self.bot_brand)
        return brands[: len(tokens)]


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    if not settings.secret_key or settings.secret_key == "KKFASYFPZEdaRYZcFdhDHBsMCaJhT-tG6F3axLXZuUY=":
        import logging
        logging.getLogger(__name__).warning(
            "CRITICAL SECURITY WARNING: Using the default SECRET_KEY. "
            "Please set a secure SECRET_KEY in your .env file to protect user API keys."
        )
    return settings
