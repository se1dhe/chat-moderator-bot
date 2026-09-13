"""Request authentication for the Mini App API: initData → user, then admin gate.

Multi-bot aware: the shared API serves every brand bot, so a request's initData is
validated against each registered bot's token; the one that validates binds the request
to that bot (used for admin checks, chat scoping and actions)."""
from __future__ import annotations

from aiogram import Bot
from aiohttp import web

from ..services import roles
from ..services.webapp_auth import InitDataError, WebAppUser, verify_init_data

_USER_KEY = "webapp_user"
_BOT_KEY = "webapp_bot"


def _extract_init_data(request: web.Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("tma "):
        return auth[4:]
    res = request.headers.get("X-Init-Data", "")
    if not res:
        res = request.query.get("initData", "")
    return res


async def get_user(request: web.Request) -> WebAppUser:
    """Validate initData against any registered bot; cache the user + bot on the request."""
    cached = request.get(_USER_KEY)
    if cached is not None:
        return cached
    init_data = _extract_init_data(request)
    bots: dict[int, Bot] = request.app["bots"]
    last_error: InitDataError | None = None
    for bot in bots.values():
        try:
            user = verify_init_data(init_data, bot.token)
        except InitDataError as exc:
            last_error = exc
            continue
        request[_USER_KEY] = user
        request[_BOT_KEY] = bot
        return user
    raise web.HTTPUnauthorized(reason=f"initData: {last_error or 'no registered bot'}")


def request_bot(request: web.Request) -> Bot:
    """The bot bound to this request (whose token validated the initData)."""
    return request.get(_BOT_KEY) or request.app["bot"]


async def require_chat_admin(request: web.Request, chat_id: int) -> WebAppUser:
    """Authenticated caller must be an administrator (or bot owner) of `chat_id` or an explicitly granted ChatModerator."""
    user = await get_user(request)
    settings = request.app["settings"]
    if user.id in settings.owner_id_set:
        return user
    
    is_admin = await roles.is_admin(
        request_bot(request), request.app["redis"], chat_id=chat_id, user_id=user.id
    )
    if is_admin:
        return user
        
    from sqlalchemy.ext.asyncio import AsyncSession
    from ..db import repo
    session_maker = request.app["db_session_maker"]
    async with session_maker() as session:
        is_mod = await repo.is_chat_moderator(session, chat_id, user.id)
    if is_mod:
        return user

    raise web.HTTPForbidden(reason="not a chat administrator or moderator")