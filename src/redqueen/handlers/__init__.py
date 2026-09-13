"""Router registration."""
from __future__ import annotations

from aiogram import Dispatcher

from . import (
    ai_review,
    antiflood,
    captcha,
    common,
    content_filters,
    members,
    moderation,
    modes,
    onboarding,
    payments,
    defcon,
    summary,
    welcome,
    triggers,
    settings,
    auto_comment,
)


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(common.router)
    dp.include_router(onboarding.router)
    dp.include_router(payments.router)
    dp.include_router(moderation.router)
    dp.include_router(settings.router)
    # Join-watching (chat_member) and message-scanning pipelines: each stage raises
    # SkipHandler to fall through to the next one when it doesn't apply — this lets
    # captcha and raid both observe the same join event, and antiflood/content_filters/
    # modes/ai_review all observe the same message in turn (ai_review is the last,
    # catch-all stage).
    dp.include_router(captcha.router)
    dp.include_router(defcon.router)
    dp.include_router(summary.router)
    dp.include_router(welcome.router)
    dp.include_router(triggers.router)
    dp.include_router(members.router)  # records the sender, then defers to the scanners
    dp.include_router(auto_comment.router)
    dp.include_router(antiflood.router)
    dp.include_router(content_filters.router)
    dp.include_router(modes.router)
    dp.include_router(ai_review.router)
