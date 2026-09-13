from __future__ import annotations

from aiohttp import web
from sqlalchemy import select, func

from .utils import _chat_id, _session
from .auth import require_chat_admin
from ..db.models import ChatTrigger

async def get_triggers(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        triggers = await session.scalars(
            select(ChatTrigger).where(ChatTrigger.chat_telegram_id == cid).order_by(ChatTrigger.created_at.desc())
        )
        return web.json_response([
            {
                "id": t.id,
                "trigger_word": t.trigger_word,
                "reply_text": t.reply_text,
                "is_regex": t.is_regex,
                "created_at": t.created_at.isoformat()
            } for t in triggers
        ])

async def create_trigger(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    try:
        body = await request.json()
    except ValueError as exc:
        raise web.HTTPBadRequest(reason="invalid JSON body") from exc
        
    word = body.get("trigger_word", "").strip()
    reply = body.get("reply_text", "").strip()
    is_regex = bool(body.get("is_regex", False))
    
    if not word or not reply:
        raise web.HTTPBadRequest(reason="trigger_word and reply_text are required")
        
    async with _session(request) as session:
        count = await session.scalar(
            select(func.count(ChatTrigger.id)).where(ChatTrigger.chat_telegram_id == cid)
        )
        if count >= 100:
            raise web.HTTPBadRequest(reason="Maximum 100 triggers per chat")
        
        trigger = ChatTrigger(
            chat_telegram_id=cid,
            trigger_word=word[:255],
            reply_text=reply[:4000],
            is_regex=is_regex
        )
        session.add(trigger)
        await session.commit()
        return web.json_response({"id": trigger.id, "status": "created"})

async def delete_trigger(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    try:
        tid = int(request.match_info["tid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad trigger id") from exc
        
    async with _session(request) as session:
        trigger = await session.get(ChatTrigger, tid)
        if not trigger or trigger.chat_telegram_id != cid:
            raise web.HTTPNotFound(reason="trigger not found")
        await session.delete(trigger)
        await session.commit()
        return web.json_response({"status": "deleted"})
