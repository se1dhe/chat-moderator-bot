with open('src/redqueen/services/moderation.py', 'r') as f:
    text = f.read()

old_send = """async def _send_webhook(url: str, payload: dict) -> None:
    try:
        async with aiohttp.ClientSession() as http_session:
            await http_session.post(url, json=payload, timeout=5)
    except Exception:
        pass"""

new_send = """async def _send_webhook(url: str, payload: dict) -> None:
    import asyncio
    await asyncio.sleep(2.0)  # Wait for DB transaction to commit to prevent race conditions
    try:
        async with aiohttp.ClientSession() as http_session:
            await http_session.post(url, json=payload, timeout=5)
    except Exception:
        pass"""

text = text.replace(old_send, new_send)

with open('src/redqueen/services/moderation.py', 'w') as f:
    f.write(text)

