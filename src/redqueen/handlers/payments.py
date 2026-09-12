"""Telegram Stars monetization: Pro invoices, checkout, and status."""
from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import Settings
from ..db import repo
from ..filters import IsChatAdmin
from ..services import billing

log = logging.getLogger(__name__)

router = Router(name="payments")

_CHAT_TYPES = {"group", "supergroup", "channel"}


def _fmt(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d") if dt else "—"


def build_prices(t: Callable[..., str], days: int) -> list[LabeledPrice]:
    return [LabeledPrice(label=t("PRO_INVOICE_LABEL", days=days), amount=billing.PRO_PRICE_STARS)]


def pro_payload(chat_id: int, days: int) -> str:
    return f"pro:{chat_id}:{days}"


@router.message(Command("pro"), F.chat.type.in_(_CHAT_TYPES), IsChatAdmin())
async def cmd_pro(
    message: Message, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    cid = message.chat.id
    if await billing.is_pro(session, cid):
        sub = await billing.get_subscription(session, cid)
        await message.reply(t("PRO_ALREADY", until=_fmt(sub.active_until if sub else None)))
        return
    days = billing.PRO_PERIOD_DAYS
    await message.answer(t("PRO_OFFER", stars=billing.PRO_PRICE_STARS, days=days))
    await bot.send_invoice(
        chat_id=cid,
        title=t("PRO_INVOICE_TITLE"),
        description=t("PRO_INVOICE_DESC", days=days),
        payload=pro_payload(cid, days),
        provider_token="",          # empty for Telegram Stars
        currency="XTR",             # Telegram Stars
        prices=build_prices(t, days),
    )


@router.message(Command("pro"))
async def cmd_pro_wrong_scope(message: Message, t: Callable[..., str]) -> None:
    await message.reply(t("PRO_CMD_GROUP_ONLY"))


@router.message(Command("subscription"), F.chat.type.in_(_CHAT_TYPES), IsChatAdmin())
async def cmd_subscription(message: Message, session: AsyncSession, t: Callable[..., str]) -> None:
    sub = await billing.get_subscription(session, message.chat.id)
    if await billing.is_pro(session, message.chat.id):
        await message.reply(t("SUB_STATUS_PRO", until=_fmt(sub.active_until if sub else None)))
    else:
        await message.reply(t("SUB_STATUS_FREE"))


@router.message(Command("grantpro"), F.chat.type.in_(_CHAT_TYPES))
async def cmd_grantpro(
    message: Message, command: CommandObject, session: AsyncSession, settings: Settings,
    t: Callable[..., str],
) -> None:
    """Owner-only: comp Pro on this chat without payment (support / testing)."""
    if message.from_user is None or message.from_user.id not in settings.owner_id_set:
        return  # silent for non-owners — this command is not advertised
    days = int(command.args) if (command.args or "").strip().isdigit() else billing.PRO_PERIOD_DAYS
    until = await billing.activate_pro(session, message.chat.id, days=days)
    await repo.log_action(
        session, chat_telegram_id=message.chat.id, user_telegram_id=message.from_user.id,
        actor_id=message.from_user.id, action="pro_grant", reason=f"owner comp {days}d",
    )
    try:
        await message.bot.send_message(message.from_user.id, t("PRO_ACTIVATED", until=_fmt(until)))
    except Exception:
        await message.reply(t("PRO_ACTIVATED", until=_fmt(until)))


@router.pre_checkout_query()
async def on_pre_checkout(query: PreCheckoutQuery) -> None:
    # Nothing to reserve — accept every well-formed Stars checkout.
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: Message, session: AsyncSession, t: Callable[..., str]
) -> None:
    sp = message.successful_payment
    chat_id, days = message.chat.id, billing.PRO_PERIOD_DAYS
    parts = (sp.invoice_payload or "").split(":")
    if len(parts) >= 3 and parts[0] == "pro":
        try:
            chat_id, days = int(parts[1]), int(parts[2])
        except ValueError:
            pass

    until = await billing.record_payment(
        session, chat_id=chat_id, payer_id=message.from_user.id, stars=sp.total_amount,
        charge_id=sp.telegram_payment_charge_id, days=days,
    )
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=message.from_user.id,
        actor_id=message.from_user.id, action="pro_payment", reason=f"{sp.total_amount} XTR",
        meta={"charge_id": sp.telegram_payment_charge_id, "days": days},
    )
    log.info("Pro payment: chat=%s payer=%s stars=%s until=%s",
             chat_id, message.from_user.id, sp.total_amount, until)
    try:
        await message.bot.send_message(message.from_user.id, t("PRO_ACTIVATED", until=_fmt(until)))
    except Exception:
        await message.answer(t("PRO_ACTIVATED", until=_fmt(until)))
