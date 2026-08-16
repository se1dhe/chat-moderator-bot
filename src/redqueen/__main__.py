"""Entry point: `python -m redqueen` or `redqueen` console script."""
from __future__ import annotations

import asyncio
import logging

from .bot import create_bot, create_dispatcher
from .config import get_settings
from .db.base import create_all, dispose_engine, init_engine

log = logging.getLogger("redqueen")


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    if not settings.bot_token:
        raise SystemExit("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    init_engine(settings.sqlalchemy_dsn)
    await create_all()  # dev bootstrap; use Alembic migrations in production

    bot = create_bot(settings)
    dp = create_dispatcher(settings)

    try:
        if settings.run_mode == "webhook":
            await _run_webhook(bot, dp, settings)
        else:
            log.info("Starting polling as RedQueen…")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
    finally:
        provider = dp.get("ai_provider")
        if provider is not None:
            await provider.close()
        await bot.session.close()
        await dispose_engine()


async def _run_webhook(bot, dp, settings) -> None:
    from aiohttp import web
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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
