import aiohttp
from aiohttp import web
from aiogram import Bot
from .auth import request_bot

def _chat_id(request: web.Request) -> int:
    try:
        return int(request.match_info["cid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad chat id") from exc

async def get_avatar(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    bot = request_bot(request)
    redis = request.app["redis"]
    
    import base64
    cache_key = f"avatar:{cid}"
    cached = await redis.get(cache_key)
    if cached is not None:
        if cached == "":
            raise web.HTTPNotFound(reason="No avatar (cached failure)")
        return web.Response(body=base64.b64decode(cached), content_type="image/jpeg")
        
    try:
        chat = await bot.get_chat(cid)
        if not chat.photo:
            raise web.HTTPNotFound(reason="No avatar")
            
        file = await bot.get_file(chat.photo.small_file_id)
        url = bot.session.api.file_url(bot.token, file.file_path)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise web.HTTPNotFound()
                data = await resp.read()
                
        b64_data = base64.b64encode(data).decode('utf-8')
        await redis.setex(cache_key, 3600, b64_data)
        return web.Response(body=data, content_type="image/jpeg")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to fetch avatar for {cid}: {e}")
        # Cache the failure for 10 minutes to prevent rate-limit loops
        await redis.setex(cache_key, 600, "")
        raise web.HTTPNotFound(reason="Failed to fetch avatar")
