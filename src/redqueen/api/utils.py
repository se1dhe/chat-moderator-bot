from __future__ import annotations

from aiohttp import web
from contextlib import asynccontextmanager

def _chat_id(request: web.Request) -> int:
    try:
        return int(request.match_info["cid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad chat id") from exc

@asynccontextmanager
async def _session(request: web.Request):
    async with request.app["sessionmaker"]() as session:
        session.info["redis"] = request.app["redis"]
        yield session
