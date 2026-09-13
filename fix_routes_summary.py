import re

with open('src/redqueen/api/routes.py', 'r') as f:
    text = f.read()

# Add get_summary function
new_func = """
async def get_summary(request: web.Request) -> web.Response:
    chat_id = int(request.match_info["cid"])
    await require_chat_admin(request, chat_id)
    redis = request.app["redis"]
    key = f"rq:history:{chat_id}"
    raw_msgs = await redis.lrange(key, 0, -1)
    if not raw_msgs:
        return web.json_response({"summary": "Недостаточно истории сообщений для дайджеста."})
    
    import json
    lines = []
    for raw in reversed(raw_msgs):
        try:
            d = json.loads(raw)
            lines.append(f"{d['author']}: {d['text']}")
        except Exception:
            pass
            
    if len(lines) < 5:
        return web.json_response({"summary": "Недостаточно истории сообщений для дайджеста."})
        
    text_to_summarize = "\\n".join(lines)
    prompt = "Составь краткую выжимку (дайджест) следующих сообщений из чата в 3-5 буллитах. Выдели главные темы и решения. Пиши коротко и по делу.\\n\\n" + text_to_summarize
    
    provider = request.app["bot"].dispatcher.get("ai_provider")
    if not provider or not hasattr(provider, "generate_text"):
        return web.json_response({"summary": "AI Summarizer is not available on this provider."})
        
    session_maker = request.app["db_session_maker"]
    from ..db import repo
    async with session_maker() as session:
        chat_settings = await repo.get_settings(session, chat_id)
        
    try:
        summary = await provider.generate_text(prompt, chat_settings=chat_settings)
        return web.json_response({"summary": summary})
    except Exception as exc:
        return web.json_response({"summary": f"Ошибка генерации: {exc}"})
"""

text = text.replace("async def get_settings(", new_func + "\nasync def get_settings(")

# Add route
route = """    app.router.add_get("/api/chats/{cid}/settings", get_settings)
    app.router.add_get("/api/chats/{cid}/summary", get_summary)"""
text = text.replace('    app.router.add_get("/api/chats/{cid}/settings", get_settings)', route)

with open('src/redqueen/api/routes.py', 'w') as f:
    f.write(text)

