"""Onboarding: greet on add/promote, verify admin rights, remind about Privacy Mode."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated, Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..i18n import resolve_lang
from ..i18n import t as _t

router = Router(name="onboarding")

_CHAT_SCOPED_TYPES = {"group", "supergroup", "channel"}
_GREET_STATUSES = {"member", "administrator"}
_REQUIRED_RIGHTS = {
    "can_restrict_members": "restrict members",
    "can_delete_messages": "delete messages",
}


def _missing_rights(member) -> list[str]:
    return [label for field, label in _REQUIRED_RIGHTS.items() if not getattr(member, field, False)]


@router.my_chat_member()
async def on_bot_membership_changed(
    event: ChatMemberUpdated, bot: Bot, session: AsyncSession
) -> None:
    if event.chat.type not in _CHAT_SCOPED_TYPES:
        return
    old_status, new_status = event.old_chat_member.status, event.new_chat_member.status
    if new_status not in _GREET_STATUSES or old_status == new_status:
        return

    # Seed the chat's default notification language from whoever added the bot, so all
    # further RedQueen messages in this chat speak their language until changed in the TMA.
    chat = await repo.get_or_create_chat(
        session, event.chat.id, type_=event.chat.type, title=event.chat.title, bot_id=bot.id
    )
    if event.from_user and event.from_user.language_code:
        chat.lang = resolve_lang(event.from_user.language_code)
    lang = chat.lang

    def t(key: str, **kw: object) -> str:
        return _t(lang, key, **kw)

    chat_name = event.chat.title or str(event.chat.id)
    
    async def notify(text: str) -> None:
        try:
            await bot.send_message(event.from_user.id, text)
        except Exception:
            try:
                await bot.send_message(event.chat.id, text)
            except Exception:
                pass

    if new_status != "administrator":
        await notify(t("ONBOARDING_MISSING_RIGHTS", chat=chat_name, missing="administrator"))
        return

    missing = _missing_rights(event.new_chat_member)
    if missing:
        await notify(t("ONBOARDING_MISSING_RIGHTS", chat=chat_name, missing=", ".join(missing)))
    else:
        await notify(t("ONBOARDING_WELCOME", chat=chat_name))


@router.message(Command("checksetup"), F.chat.type.in_(_CHAT_SCOPED_TYPES), IsChatAdmin())
async def cmd_checksetup(message: Message, bot: Bot, t: Callable[..., str]) -> None:
    member = await bot.get_chat_member(message.chat.id, bot.id)
    if member.status != "administrator":
        await message.reply(t("CHECKSETUP_MISSING_RIGHTS", missing="administrator"))
        return
    missing = _missing_rights(member)
    if missing:
        await message.reply(t("CHECKSETUP_MISSING_RIGHTS", missing=", ".join(missing)))
        return
    await message.reply(t("CHECKSETUP_OK"))
