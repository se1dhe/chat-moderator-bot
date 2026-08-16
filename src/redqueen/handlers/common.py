"""Common commands: /start, /help."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message, t: Callable[..., str]) -> None:
    await message.answer(t("START"))


@router.message(Command("help"))
async def cmd_help(message: Message, t: Callable[..., str]) -> None:
    await message.answer(t("HELP"))
