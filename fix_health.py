import re

with open('src/redqueen/api/routes.py', 'r') as f:
    text = f.read()

old_health = """async def health(request: web.Request) -> web.Response:
    checks = {"status": "ok"}
    try:
        pool = request.app.get("db_pool") or request.app.get("engine")
        if pool:
            # проверка БД
            checks["db"] = "ok"
    except SQLAlchemyError:
        checks["db"] = "error"
        checks["status"] = "degraded\""""

new_health = """async def health(request: web.Request) -> web.Response:
    checks = {"status": "ok"}
    try:
        pool = request.app.get("db_pool") or request.app.get("engine")
        if pool:
            import sqlalchemy as sa
            async with pool.connect() as conn:
                await conn.execute(sa.text("SELECT 1"))
            checks["db"] = "ok"
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("DB Healthcheck failed: %s", e)
        checks["db"] = "error"
        checks["status"] = "degraded\""""

text = text.replace(old_health, new_health)

with open('src/redqueen/api/routes.py', 'w') as f:
    f.write(text)

