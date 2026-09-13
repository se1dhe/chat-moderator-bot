"""Routes for managing RBAC (Role-Based Access Control) for chat moderators."""
from aiohttp import web

from ..db import repo
from .auth import require_chat_admin

routes = web.RouteTableDef()

@routes.get("/api/chats/{cid:\\-?\\d+}/moderators")
async def get_moderators(request: web.Request) -> web.Response:
    cid = int(request.match_info["cid"])
    await require_chat_admin(request, cid)
    
    session_maker = request.app["db_session_maker"]
    async with session_maker() as session:
        mods_data = await repo.get_chat_moderators(session, cid)
        
        result = []
        for mod, member in mods_data:
            result.append({
                "user_id": mod.user_telegram_id,
                "username": member.username,
                "full_name": member.full_name,
                "promoted_by": mod.promoted_by,
                "created_at": mod.created_at.isoformat() if mod.created_at else None
            })
            
    return web.json_response(result)

@routes.post("/api/chats/{cid:\\-?\\d+}/moderators")
async def add_moderator(request: web.Request) -> web.Response:
    cid = int(request.match_info["cid"])
    user = await require_chat_admin(request, cid)
    
    data = await request.json()
    
    session_maker = request.app["db_session_maker"]
    async with session_maker() as session:
        user_id = data.get("user_id")
        
        if not user_id:
            username = data.get("username")
            if not username:
                raise web.HTTPBadRequest(reason="user_id or username required")
            
            username = username.lstrip('@')
            
            from sqlalchemy import select
            from ..db.models import ChatMember
            member = await session.execute(
                select(ChatMember)
                .where(ChatMember.chat_telegram_id == cid)
                .where(ChatMember.username.ilike(username))
            )
            member = member.scalar_one_or_none()
            if not member:
                raise web.HTTPNotFound(reason="User not found in chat members")
            user_id = member.user_telegram_id
            
        await repo.add_chat_moderator(session, cid, user_id, user.id)
        await session.commit()
        
    return web.json_response({"status": "ok", "user_id": user_id})

@routes.delete("/api/chats/{cid:\\-?\\d+}/moderators/{uid:\\d+}")
async def remove_moderator(request: web.Request) -> web.Response:
    cid = int(request.match_info["cid"])
    uid = int(request.match_info["uid"])
    await require_chat_admin(request, cid)
    
    session_maker = request.app["db_session_maker"]
    async with session_maker() as session:
        await repo.remove_chat_moderator(session, cid, uid)
        await session.commit()
        
    return web.json_response({"status": "ok"})
