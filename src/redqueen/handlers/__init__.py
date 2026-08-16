"""Router registration."""
from __future__ import annotations

from aiogram import Dispatcher

from . import ai_review, common, moderation, settings


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(common.router)
    dp.include_router(moderation.router)
    dp.include_router(settings.router)
    dp.include_router(ai_review.router)  # message listener last
