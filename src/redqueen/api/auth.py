"""Request authentication for the Mini App API: initData → user, then admin gate."""
from __future__ import annotations

from aiohttp import web

from ..services import roles
from ..services.webapp_auth import InitDataError, WebAppUser, verify_init_data

_USER_KEY = "webapp_user"


def _extract_init_data(request: web.Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("tma "):
        return auth[4:]
    return request.headers.get("X-Init-Data", "")


async def get_user(request: web.Request) -> WebAppUser:
    """Validate initData once per request; cache the user on the request object."""
    cached = request.get(_USER_KEY)
    if cached is not None:
        return cached
    settings = request.app["settings"]
    try:
        user = verify_init_data(_extract_init_data(request), settings.bot_token)
    except InitDataError as exc:
        raise web.HTTPUnauthorized(reason=f"initData: {exc}") from exc
    request[_USER_KEY] = user
    return user


async def require_chat_admin(request: web.Request, chat_id: int) -> WebAppUser:
    """Authenticated caller must be an administrator (or bot owner) of `chat_id`."""
    user = await get_user(request)
    settings = request.app["settings"]
    if user.id in settings.owner_id_set:
        return user
    is_admin = await roles.is_admin(
        request.app["bot"], request.app["redis"], chat_id=chat_id, user_id=user.id
    )
    if not is_admin:
        raise web.HTTPForbidden(reason="not a chat administrator")
    return user
