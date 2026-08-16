"""Content filters: banned words, links, forwards, mentions, blocked media types."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..services import roles
from ..services.config import get_config, save_section
from ..services.filters import evaluate

router = Router(name="content_filters")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

_BLOCKABLE_MEDIA = {"sticker", "animation", "voice", "video_note"}


@router.message()
async def check_content(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    if message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    settings = await repo.get_settings(session, message.chat.id)
    cfg = get_config(settings)["filters"]

    hit = evaluate(message, cfg)
    if hit is None:
        raise SkipHandler

    if await roles.is_exempt(
        bot, redis, chat_id=message.chat.id, user_id=message.from_user.id, settings=settings
    ):
        raise SkipHandler

    try:
        await message.delete()
    except Exception:  # noqa: BLE001
        pass

    await repo.log_action(
        session, chat_telegram_id=message.chat.id, user_telegram_id=message.from_user.id,
        actor_id=None, action="filter_delete", reason=hit.reason, meta={"kind": hit.kind},
    )


# Re-check edits too: a member may post clean text then edit in a banned word/link.
router.edited_message.register(check_content, F.chat.type.in_({"group", "supergroup"}))


@router.message(Command("bannedwords"), IsChatAdmin())
async def cmd_bannedwords(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split(maxsplit=1)
    settings = await repo.get_settings(session, message.chat.id)
    words = get_config(settings)["filters"]["banned_words"]

    if not parts or parts[0] not in {"add", "remove", "list"}:
        await message.reply(t("BANNEDWORDS_USAGE"))
        return

    if parts[0] == "list":
        if not words:
            await message.reply(t("BANNEDWORDS_EMPTY"))
            return
        await message.reply(t("BANNEDWORDS_LIST", count=len(words), words="\n".join(f"• {w}" for w in words)))
        return

    if len(parts) < 2 or not parts[1].strip():
        await message.reply(t("BANNEDWORDS_USAGE"))
        return
    word = parts[1].strip().lower()

    if parts[0] == "add":
        if word not in words:
            words.append(word)
        save_section(settings, "filters", {"banned_words": words})
        await message.reply(t("BANNEDWORDS_ADDED", word=word))
    else:
        if word in words:
            words.remove(word)
        save_section(settings, "filters", {"banned_words": words})
        await message.reply(t("BANNEDWORDS_REMOVED", word=word))


async def _toggle(session: AsyncSession, chat_id: int, key: str, arg: str | None) -> bool | None:
    choice = (arg or "").strip().lower()
    if choice not in {"on", "off"}:
        return None
    settings = await repo.get_settings(session, chat_id)
    enabled = choice == "on"
    save_section(settings, "filters", {key: enabled})
    return enabled


@router.message(Command("blocklinks"), IsChatAdmin())
async def cmd_blocklinks(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    enabled = await _toggle(session, message.chat.id, "block_links", command.args)
    if enabled is None:
        await message.reply(t("BLOCKLINKS_USAGE"))
        return
    await message.reply(t("BLOCKLINKS_SET", state="on" if enabled else "off"))


@router.message(Command("blockforwards"), IsChatAdmin())
async def cmd_blockforwards(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    enabled = await _toggle(session, message.chat.id, "block_forwards", command.args)
    if enabled is None:
        await message.reply(t("BLOCKFORWARDS_USAGE"))
        return
    await message.reply(t("BLOCKFORWARDS_SET", state="on" if enabled else "off"))


@router.message(Command("blockmentions"), IsChatAdmin())
async def cmd_blockmentions(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    enabled = await _toggle(session, message.chat.id, "block_mentions", command.args)
    if enabled is None:
        await message.reply(t("BLOCKMENTIONS_USAGE"))
        return
    await message.reply(t("BLOCKMENTIONS_SET", state="on" if enabled else "off"))


@router.message(Command("blockmedia"), IsChatAdmin())
async def cmd_blockmedia(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split()
    if len(parts) != 2 or parts[0] not in _BLOCKABLE_MEDIA or parts[1] not in {"on", "off"}:
        await message.reply(t("BLOCKMEDIA_USAGE"))
        return
    media, choice = parts[0], parts[1]
    settings = await repo.get_settings(session, message.chat.id)
    blocked = set(get_config(settings)["filters"]["blocked_media"])
    if choice == "on":
        blocked.add(media)
    else:
        blocked.discard(media)
    save_section(settings, "filters", {"blocked_media": sorted(blocked)})
    await message.reply(t("BLOCKMEDIA_SET", media=media, state=choice))
