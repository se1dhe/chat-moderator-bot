"""Join captcha: quarantine new members, vet join requests, verify answers."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Bot, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.chat_member_updated import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import CallbackQuery, ChatJoinRequest, ChatMemberUpdated, Message
from aiogram.exceptions import TelegramAPIError

from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..db.models import CaptchaSession
from ..filters import IsChatAdmin
from ..services import captcha, moderation, roles, trust
from ..services.config import get_config, save_section

router = Router(name="captcha")


class CaptchaCB(CallbackData, prefix="cap"):
    session_id: int
    value: int


def _keyboard(row_id: int, challenge: captcha.Challenge, t: Callable[..., str]) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    if challenge.kind == "button":
        kb.button(
            text=t("CAPTCHA_BUTTON_LABEL"),
            callback_data=CaptchaCB(session_id=row_id, value=1).pack(),
        )
    else:
        for option in challenge.options:
            kb.button(text=str(option), callback_data=CaptchaCB(session_id=row_id, value=option).pack())
        kb.adjust(4)
    return kb


def _prompt_text(challenge: captcha.Challenge, *, name: str, minutes: int, t: Callable[..., str]) -> str:
    key = "CAPTCHA_MATH_PROMPT" if challenge.kind == "math" else "CAPTCHA_BUTTON_PROMPT"
    return t(key, name=name, minutes=minutes, **challenge.prompt_kwargs)


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_member_join(
    event: ChatMemberUpdated, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    # Raises SkipHandler (instead of returning) even when captcha isn't applicable so
    # the raid-shield router — registered after this one — still sees every join.
    user = event.new_chat_member.user
    if user.is_bot:
        raise SkipHandler
    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    if not cfg["enabled"]:
        raise SkipHandler

    # Never gate admins or explicitly exempt members.
    if await roles.is_exempt(bot, redis, chat_id=event.chat.id, user_id=user.id, settings=settings):
        raise SkipHandler

    # Cross-chat reputation: a member the Hive already trusts skips the gate.
    if trust.should_bypass_captcha(await trust.get_score(session, user.id)):
        raise SkipHandler

    await moderation.mute(bot, session, chat_id=event.chat.id, user_id=user.id, actor_id=None,
                          until=None, reason="captcha_pending")

    challenge = captcha.build_challenge(cfg["mode"])
    row = await captcha.create_session(
        session, chat_id=event.chat.id, user_id=user.id, challenge=challenge,
        is_join_request=False, timeout_seconds=cfg["timeout_seconds"],
    )
    minutes = max(1, cfg["timeout_seconds"] // 60)
    text = _prompt_text(challenge, name=user.full_name, minutes=minutes, t=t)
    sent = await bot.send_message(
        event.chat.id, text, reply_markup=_keyboard(row.id, challenge, t).as_markup()
    )
    row.prompt_message_id = sent.message_id
    raise SkipHandler


@router.chat_join_request()
async def on_join_request(
    event: ChatJoinRequest, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    if event.from_user.is_bot:
        return
    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    from redqueen.handlers.defcon import is_active
    full_cfg = get_config(settings)
    is_defcon_captcha = is_active(full_cfg) and full_cfg["defcon"]["action"] == "captcha"
    if not cfg["enabled"] and not is_defcon_captcha:
        await bot.approve_chat_join_request(event.chat.id, event.from_user.id)
        return

    challenge = captcha.build_challenge(cfg["mode"])
    row = await captcha.create_session(
        session, chat_id=event.chat.id, user_id=event.from_user.id, challenge=challenge,
        is_join_request=True, timeout_seconds=cfg["timeout_seconds"],
    )
    minutes = max(1, cfg["timeout_seconds"] // 60)
    inner = _prompt_text(challenge, name=event.from_user.full_name, minutes=minutes, t=t)
    dm_text = t("CAPTCHA_JOINREQUEST_DM", chat=event.chat.title or str(event.chat.id), challenge=inner)
    try:
        sent = await bot.send_message(
            event.from_user.id, dm_text, reply_markup=_keyboard(row.id, challenge, t).as_markup()
        )
        row.prompt_message_id = sent.message_id
    except TelegramAPIError:
        # Can't reach the user by DM — decline rather than leave the request stuck.
        await bot.decline_chat_join_request(event.chat.id, event.from_user.id)
        row.status = "failed"


@router.callback_query(CaptchaCB.filter())
async def on_answer(
    query: CallbackQuery, callback_data: CaptchaCB, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    row = await session.scalar(
        select(CaptchaSession).where(CaptchaSession.id == callback_data.session_id)
    )
    if row is None or row.status != "pending":
        await query.answer()
        return
    if query.from_user.id != row.user_telegram_id:
        await query.answer(t("CAPTCHA_NOT_YOURS"), show_alert=True)
        return
    if callback_data.value != row.answer:
        await query.answer(t("CAPTCHA_WRONG_ANSWER"), show_alert=True)
        return

    row.status = "passed"
    name = query.from_user.full_name
    await trust.adjust(session, row.user_telegram_id, trust.CAPTCHA_PASS, redis)

    if row.is_join_request:
        await bot.approve_chat_join_request(row.chat_telegram_id, row.user_telegram_id)
        if query.message:
            await query.message.edit_text(
                t("CAPTCHA_JOINREQUEST_APPROVED", chat=str(row.chat_telegram_id))
            )
    else:
        await moderation.unmute(bot, session, chat_id=row.chat_telegram_id,
                                user_id=row.user_telegram_id, actor_id=None)
        if query.message:
            await query.message.edit_text(t("CAPTCHA_PASSED", name=name))

    await query.answer()


@router.message(Command("captcha"), IsChatAdmin())
async def cmd_captcha(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    choice = (command.args or "").strip().lower()
    if choice not in {"on", "off"}:
        await message.reply(t("CAPTCHA_USAGE"))
        return
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "captcha", {"enabled": choice == "on"})
    await message.reply(t("CAPTCHA_ENABLED" if choice == "on" else "CAPTCHA_DISABLED"))


@router.message(Command("captchamode"), IsChatAdmin())
async def cmd_captchamode(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    mode = (command.args or "").strip().lower()
    if mode not in {"button", "math"}:
        await message.reply(t("CAPTCHA_MODE_USAGE"))
        return
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "captcha", {"mode": mode})
    await message.reply(t("CAPTCHA_MODE_SET", mode=mode))


@router.message(Command("captchatimeout"), IsChatAdmin())
async def cmd_captchatimeout(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    arg = (command.args or "").strip()
    if not arg.isdigit() or not (60 <= int(arg) <= 1800):
        await message.reply(t("CAPTCHA_TIMEOUT_USAGE"))
        return
    seconds = int(arg)
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "captcha", {"timeout_seconds": seconds})
    await message.reply(t("CAPTCHA_TIMEOUT_SET", seconds=seconds))
