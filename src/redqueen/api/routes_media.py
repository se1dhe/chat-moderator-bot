from __future__ import annotations

import asyncio

import aiogram.exceptions
from aiohttp import web
from aiogram.types import BufferedInputFile

from .utils import _chat_id
from .auth import require_chat_admin, request_bot

upload_semaphore = asyncio.Semaphore(3)

async def upload_media(request: web.Request) -> web.Response:
    """Accept multipart upload, send to admin's PM to get a permanent file_id."""
    cid = _chat_id(request)
    user = await require_chat_admin(request, cid)
    uid = user.id

    async with upload_semaphore:
        reader = await request.multipart()
        field = await reader.next()
        if not field:
            raise web.HTTPBadRequest(reason="No file provided")
        
        filename = field.filename or "file"
        
        MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
        chunks = []
        total = 0
        while True:
            chunk = await field.read_chunk(8192)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_UPLOAD_SIZE:
                raise web.HTTPRequestEntityTooLarge(max_size=MAX_UPLOAD_SIZE, actual_size=total)
            chunks.append(chunk)
        content = b''.join(chunks)
    
    bot = request_bot(request)
    
    file = BufferedInputFile(content, filename=filename)
    
    try:
        if filename.lower().endswith((".mp4", ".gif")):
            msg = await bot.send_animation(uid, animation=file)
            file_id = f"animation:{msg.animation.file_id}"
        else:
            msg = await bot.send_photo(uid, photo=file)
            file_id = f"photo:{msg.photo[-1].file_id}"
    except aiogram.exceptions.TelegramAPIError as e:
        raise web.HTTPBadRequest(reason=f"Failed to process media (bot might need PM access): {e}")
        
    return web.json_response({"file_id": file_id})
