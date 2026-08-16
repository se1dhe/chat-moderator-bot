"""Entry point: `python -m redqueen` or `redqueen` console script."""
from __future__ import annotations

import asyncio
import logging

from .bot import create_bot, create_dispatcher, create_redis
from .config import get_settings
from .db.base import dispose_engine, get_sessionmaker, init_engine
from .services.captcha import sweep_expired

log = logging.getLogger("redqueen")

_CAPTCHA_SWEEP_INTERVAL = 15  # seconds


async def _captcha_sweeper(bot) -> None:
    sessionmaker = get_sessionmaker()
    while True:
        await asyncio.sleep(_CAPTCHA_SWEEP_INTERVAL)
        try:
            await sweep_expired(bot, sessionmaker)
        except Exception:
            log.exception("captcha sweep failed")


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    if not settings.bot_token:
        raise SystemExit("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    init_engine(settings.sqlalchemy_dsn)

    bot = create_bot(settings)
    redis = create_redis(settings)
    dp = create_dispatcher(settings, redis)

    sweeper = asyncio.create_task(_captcha_sweeper(bot))
    try:
        if settings.run_mode == "webhook":
            await _run_webhook(bot, dp, settings)
        else:
            log.info("Starting polling as RedQueen…")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
    finally:
        sweeper.cancel()
        provider = dp.get("ai_provider")
        if provider is not None:
            await provider.close()
        await redis.aclose()
        await bot.session.close()
        await dispose_engine()


async def _run_webhook(bot, dp, settings) -> None:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp import web

    url = f"{settings.webhook_base_url}{settings.webhook_path}"
    await bot.set_webhook(
        url, secret_token=settings.webhook_secret or None, drop_pending_updates=True
    )
    log.info("Webhook set to %s", url)

    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.webhook_secret or None
    ).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.webhook_host, port=settings.webhook_port)
    await site.start()
    log.info("Listening on %s:%s", settings.webhook_host, settings.webhook_port)
    await asyncio.Event().wait()  # run forever


def main() -> None:
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit) as exc:
        if isinstance(exc, SystemExit) and exc.code:
            raise
        log.info("RedQueen shutting down.")


if __name__ == "__main__":
    main()
