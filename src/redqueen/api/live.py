import asyncio
import json
from aiohttp import web
from sqlalchemy import text

async def live_feed(request: web.Request) -> web.Response:
    response = web.StreamResponse(headers={
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*',
    })
    await response.prepare(request)
    
    redis = request.app["redis"]
    pubsub = redis.pubsub()
    await pubsub.subscribe("live_events")
    
    try:
        # ping to keep connection alive
        async def ping_loop():
            while True:
                await asyncio.sleep(15)
                await response.write(b": ping\n\n")
        
        ping_task = asyncio.create_task(ping_loop())
        
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                data = msg["data"].decode("utf-8") if isinstance(msg["data"], bytes) else msg["data"]
                await response.write(f"data: {data}\n\n".encode("utf-8"))
    except (asyncio.CancelledError, ConnectionResetError):
        pass
    finally:
        ping_task.cancel()
        await pubsub.unsubscribe("live_events")
        await pubsub.close()
    
    return response

async def global_stats(request: web.Request) -> web.Response:
    async with request.app["sessionmaker"]() as session:
        chats = await session.scalar(text("SELECT COUNT(id) FROM chats"))
        actions = await session.scalar(text("SELECT COUNT(id) FROM mod_actions"))
        # we can also add users or verdicts
        verdicts = await session.scalar(text("SELECT COUNT(id) FROM ai_verdicts"))
        
        return web.json_response({
            "chats": chats or 0,
            "mod_actions": actions or 0,
            "ai_verdicts": verdicts or 0,
        })
