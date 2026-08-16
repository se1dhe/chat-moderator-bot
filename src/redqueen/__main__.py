"""Entry point: `python -m redqueen` or `redqueen` console script.

Always runs the Mini App API (aiohttp). In polling mode the API listens on its own
host/port; in webhook mode the Telegram webhook is mounted onto that same app.
"""
from __future__ import annotations

import asyncio
import logging

from aiohttp import web

from .api import create_api_app
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

    api_app = create_api_app(
        bot=bot, settings=settings, sessionmaker=get_sessionmaker(), redis=redis
    )

    me = await bot.get_me()
    dp["bot_username"] = me.username
    log.info("Authorized as @%s", me.username)
    await _setup_menu_button(bot, settings)

    background = [asyncio.create_task(_captcha_sweeper(bot))]

    # Self-provision the AI model on the backend: pull it in the background if missing,
    # so a fresh deploy needs no manual `ollama pull`. AI uses rules until it's ready.
    provider = dp.get("ai_provider")
    if settings.ai_enabled and settings.ollama_auto_pull and hasattr(provider, "ensure_model"):
        log.info("AI enabled (model=%s) — ensuring model on %s", settings.ollama_model, settings.ollama_url)
        background.append(asyncio.create_task(provider.ensure_model()))
    elif not settings.ai_enabled:
        log.info("AI disabled — using rule-based moderation")

    runner: web.AppRunner | None = None
    try:
        if settings.run_mode == "webhook":
            runner = await _serve_webhook(bot, dp, api_app, settings)
            await asyncio.Event().wait()  # webhook is push-driven; just stay alive
        else:
            runner = await _serve_api(api_app, settings)
            log.info("Starting polling as RedQueen…")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
    finally:
        for task in background:
            task.cancel()
        if runner is not None:
            await runner.cleanup()
        if provider is not None:
            await provider.close()
        await redis.aclose()
        await bot.session.close()
        await dispose_engine()


async def _setup_menu_button(bot, settings) -> None:
    """Point the private-chat menu button at the Mini App when a public URL is set."""
    if not settings.webapp_url.startswith("https://"):
        return
    from aiogram.types import MenuButtonWebApp, WebAppInfo
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(text="RedQueen", web_app=WebAppInfo(url=settings.webapp_url))
        )
        log.info("Menu button wired to Mini App at %s", settings.webapp_url)
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not set menu button: %s", exc)


async def _serve_api(app: web.Application, settings) -> web.AppRunner:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.api_host, port=settings.api_port)
    await site.start()
    log.info("Mini App API listening on %s:%s", settings.api_host, settings.api_port)
    return runner


async def _serve_webhook(bot, dp, app: web.Application, settings) -> web.AppRunner:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

    url = f"{settings.webhook_base_url}{settings.webhook_path}"
    await bot.set_webhook(
        url, secret_token=settings.webhook_secret or None, drop_pending_updates=True
    )
    log.info("Webhook set to %s", url)

    SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.webhook_secret or None
    ).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=settings.webhook_host, port=settings.webhook_port)
    await site.start()
    log.info("Webhook + Mini App API listening on %s:%s", settings.webhook_host, settings.webhook_port)
    return runner


def main() -> None:
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit) as exc:
        if isinstance(exc, SystemExit) and exc.code:
            raise
        log.info("RedQueen shutting down.")


if __name__ == "__main__":
    main()
