"""Resolve a moderation target (user id + display name) from a message."""
from __future__ import annotations

from dataclasses import dataclass

from aiogram.types import Message


@dataclass
class Target:
    user_id: int
    name: str
    username: str | None = None


def target_from_reply(message: Message) -> Target | None:
    reply = message.reply_to_message
    if reply is None or reply.from_user is None:
        return None
    u = reply.from_user
    return Target(user_id=u.id, name=u.full_name, username=u.username)


def target_from_arg(arg: str | None) -> Target | None:
    """Resolve a numeric id argument. @username resolution needs an API call and is
    handled by the caller when possible; here we only parse a raw id."""
    if not arg:
        return None
    arg = arg.strip().lstrip("@")
    if arg.isdigit():
        return Target(user_id=int(arg), name=arg)
    return None


def resolve_target(message: Message, arg: str | None) -> Target | None:
    return target_from_reply(message) or target_from_arg(arg)
