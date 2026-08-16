"""Router registration."""
from __future__ import annotations

from aiogram import Dispatcher

from . import (
    ai_review,
    antiflood,
    captcha,
    common,
    content_filters,
    moderation,
    modes,
    onboarding,
    settings,
)


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(common.router)
    dp.include_router(onboarding.router)
    dp.include_router(moderation.router)
    dp.include_router(settings.router)
    dp.include_router(captcha.router)
    # Message-scanning pipeline: each stage raises SkipHandler to fall through to the
    # next one when it doesn't apply. AI review is the final, catch-all stage.
    dp.include_router(antiflood.router)
    dp.include_router(content_filters.router)
    dp.include_router(modes.router)
    dp.include_router(ai_review.router)
