"""RedQueen Mini App HTTP API (aiohttp). Auth via Telegram initData, admin-gated."""
from .app import create_api_app

__all__ = ["create_api_app"]
