"""Common commands: /start, /help."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from .. import texts

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(texts.START)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(texts.HELP)
