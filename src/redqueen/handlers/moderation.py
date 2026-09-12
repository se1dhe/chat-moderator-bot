"""Moderation commands. All are admin-gated and run in groups only."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..services import moderation, warns
from ..utils.duration import humanize, parse_duration, until_from_now
from ..utils.targets import resolve_target

router = Router(name="moderation")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

_PROTECTED = {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}


async def _target_is_admin(message: Message, user_id: int) -> bool:
    try:
        member = await message.chat.get_member(user_id)
    except Exception:  # noqa: BLE001
        return False
    return member.status in _PROTECTED


@router.message(Command("ban"), IsChatAdmin())
async def cmd_ban(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    if await _target_is_admin(message, target.user_id):
        await message.reply(t("CANT_ACT_ON_ADMIN"))
        return
    await moderation.ban(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                         actor_id=message.from_user.id, reason=command.args)
    await message.reply(t("BANNED", name=target.name, until=""))


@router.message(Command("kick"), IsChatAdmin())
async def cmd_kick(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    if await _target_is_admin(message, target.user_id):
        await message.reply(t("CANT_ACT_ON_ADMIN"))
        return
    await moderation.kick(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                          actor_id=message.from_user.id, reason=command.args)
    await message.reply(t("KICKED", name=target.name))


@router.message(Command("mute"), IsChatAdmin())
async def cmd_mute(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession,
    t: Callable[..., str], lang: str,
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    if await _target_is_admin(message, target.user_id):
        await message.reply(t("CANT_ACT_ON_ADMIN"))
        return
    # First token after the target may be a duration when using reply form.
    duration_token = command.args if message.reply_to_message else None
    delta = parse_duration(duration_token)
    until = until_from_now(delta)
    await moderation.mute(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                          actor_id=message.from_user.id, until=until)
    await message.reply(t("MUTED", name=target.name, until=humanize(delta, lang)))


@router.message(Command("unmute"), IsChatAdmin())
async def cmd_unmute(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    await moderation.unmute(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                            actor_id=message.from_user.id)
    await message.reply(t("UNMUTED", name=target.name))


@router.message(Command("unban"), IsChatAdmin())
async def cmd_unban(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    await moderation.unban(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                           actor_id=message.from_user.id)
    await message.reply(t("UNBANNED", name=target.name))


@router.message(Command("warn"), IsChatAdmin())
async def cmd_warn(
    message: Message, command: CommandObject, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    if await _target_is_admin(message, target.user_id):
        await message.reply(t("CANT_ACT_ON_ADMIN"))
        return
    reason = command.args if message.reply_to_message else None
    result = await warns.issue_warn(bot, session, chat_id=message.chat.id, user_id=target.user_id,
                                    actor_id=message.from_user.id, reason=reason)
    await message.reply(t("WARNED", name=target.name, count=result.count, limit=result.limit,
                          reason=reason or "—"))
    if result.triggered:
        action_word = {"ban": "banned", "kick": "removed", "mute": "silenced"}.get(
            result.action or "mute", "silenced"
        )
        await message.answer(t("WARN_LIMIT_HIT", name=target.name, action=action_word))


@router.message(Command("unwarn"), IsChatAdmin())
async def cmd_unwarn(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    left = await repo.clear_last_warn(session, message.chat.id, target.user_id)
    await message.reply(t("UNWARNED", name=target.name, count=left))


@router.message(Command("purge"), IsChatAdmin())
async def cmd_purge(message: Message, bot: Bot, t: Callable[..., str]) -> None:
    reply = message.reply_to_message
    if reply is None:
        await message.reply(t("PURGE_NEED_REPLY"))
        return
    start_id = max(reply.message_id, message.message_id - 1000)
    ids = list(range(start_id, message.message_id + 1))
    deleted = 0
    # delete_messages accepts up to 100 ids per call
    for i in range(0, len(ids), 100):
        chunk = ids[i : i + 100]
        try:
            await bot.delete_messages(message.chat.id, chunk)
            deleted += len(chunk)
        except Exception:  # noqa: BLE001
            pass
    await message.answer(t("PURGED", count=deleted))


@router.message(Command("trust"), IsChatAdmin())
async def cmd_trust(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    target = resolve_target(message, command.args)
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return
    user = await repo.upsert_user(session, target.user_id)
    await message.reply(t("TRUST_SCORE", name=target.name, score=user.trust_score))
