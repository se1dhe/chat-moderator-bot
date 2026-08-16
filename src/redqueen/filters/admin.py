"""Filter: the message author is an administrator (or bot owner) in the chat."""
from __future__ import annotations

from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message

from ..config import get_settings

_ADMIN_STATUSES = {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}


class IsChatAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type not in {ChatType.GROUP, ChatType.SUPERGROUP}:
            return False
        user = message.from_user
        if user is None:
            return False
        if user.id in get_settings().owner_id_set:
            return True
        member = await message.chat.get_member(user.id)
        return member.status in _ADMIN_STATUSES
