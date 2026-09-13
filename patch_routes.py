import re

with open('src/redqueen/api/routes.py', 'r') as f:
    content = f.read()

setup_routes_content = """def setup_routes(app: web.Application) -> None:
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(rate_limit_middleware)
    app.router.add_get("/api/health", health)
    app.router.add_get("/metrics", metrics)
    app.router.add_get("/api/me", me)
    from .avatar import get_avatar
    app.router.add_get("/api/chats/{cid}/avatar", get_avatar)
    app.router.add_put("/api/me", put_me)
    app.router.add_get("/api/chats/{cid}/settings", get_settings)
    app.router.add_put("/api/chats/{cid}/settings", put_settings)
    app.router.add_get("/api/chats/{cid}/audit", audit)
    app.router.add_get("/api/chats/{cid}/quarantine", quarantine_list)
    
    from .live import live_feed, global_stats
    app.router.add_get("/api/live/feed", live_feed)
    app.router.add_get("/api/stats/global", global_stats)
    app.router.add_post("/api/chats/{cid}/quarantine/{vid}", quarantine_decide)
    app.router.add_get("/api/chats/{cid}/stats", stats)
    app.router.add_get("/api/chats/{cid}/members", members_search)
    app.router.add_post("/api/chats/{cid}/members/{uid}/action", member_action)
    
    from .routes_billing import billing_status, billing_invoice, cryptopay_webhook
    app.router.add_get("/api/chats/{cid}/billing", billing_status)
    app.router.add_post("/api/chats/{cid}/billing/invoice", billing_invoice)
    app.router.add_post("/webhook/cryptopay", cryptopay_webhook)
    
    from .routes_media import upload_media
    app.router.add_post("/api/chats/{cid}/upload", upload_media)
    
    from .routes_triggers import get_triggers, create_trigger, delete_trigger
    app.router.add_get("/api/chats/{cid}/triggers", get_triggers)
    app.router.add_post("/api/chats/{cid}/triggers", create_trigger)
    app.router.add_delete("/api/chats/{cid}/triggers/{tid}", delete_trigger)
"""

content = re.sub(r'def setup_routes\(app: web\.Application\) -> None:.*', setup_routes_content, content, flags=re.DOTALL)

with open('src/redqueen/api/routes.py', 'w') as f:
    f.write(content)
