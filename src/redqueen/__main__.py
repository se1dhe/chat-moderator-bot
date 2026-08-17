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
from .services.ai import build_provider
from .services.asr import Transcriber
from .services.captcha import sweep_expired

log = logging.getLogger("redqueen")

_CAPTCHA_SWEEP_INTERVAL = 15  # seconds


async def _captcha_sweeper(bots) -> None:
    sessionmaker = get_sessionmaker()
    while True:
        await asyncio.sleep(_CAPTCHA_SWEEP_INTERVAL)
        try:
            await sweep_expired(bots, sessionmaker)
        except Exception:
            log.exception("captcha sweep failed")


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )
    tokens = settings.token_list
    if not tokens:
        raise SystemExit("BOT_TOKEN is not set. Copy .env.example to .env and fill it in.")

    init_engine(settings.sqlalchemy_dsn)
    redis = create_redis(settings)

    # AI deps are shared across every brand bot in this process.
    provider = build_provider(settings)
    semaphore = asyncio.Semaphore(settings.ai_max_concurrency)
    transcriber = Transcriber(
        settings.whisper_model, device=settings.whisper_device, compute_type=settings.whisper_compute
    )

    bots: dict[int, object] = {}
    dps: list = []
    for token, brand in zip(tokens, settings.brand_list, strict=False):
        bot = create_bot(settings, token)
        dp = create_dispatcher(settings, redis, provider=provider, semaphore=semaphore,
                               transcriber=transcriber)
        me = await bot.get_me()
        dp["bot_username"] = me.username
        log.info("Authorized as @%s (brand: %s)", me.username, brand)
        await _register_bot(me, brand)
        await _setup_menu_button(bot, settings)
        await _setup_commands(bot)
        bots[me.id] = bot
        dps.append((bot, dp))

    api_app = create_api_app(
        bots=bots, settings=settings, sessionmaker=get_sessionmaker(), redis=redis
    )

    background = [asyncio.create_task(_captcha_sweeper(bots))]
    # Self-provision the AI model on the backend once (shared provider), so a fresh
    # deploy needs no manual `ollama pull`. AI uses rules until it's ready.
    if settings.ai_enabled and settings.ollama_auto_pull and hasattr(provider, "ensure_model"):
        log.info("AI enabled (model=%s) — ensuring model on %s", settings.ollama_model, settings.ollama_url)
        background.append(asyncio.create_task(provider.ensure_model()))
    elif not settings.ai_enabled:
        log.info("AI disabled — using rule-based moderation")

    runner: web.AppRunner | None = None
    try:
        if settings.run_mode == "webhook" and len(dps) == 1:
            bot, dp = dps[0]
            runner = await _serve_webhook(bot, dp, api_app, settings)
            await asyncio.Event().wait()  # webhook is push-driven; just stay alive
        else:
            if settings.run_mode == "webhook":
                log.warning("webhook mode supports one bot; running %d bots via polling", len(dps))
            runner = await _serve_api(api_app, settings)
            log.info("Starting polling (%d bot%s)…", len(dps), "s" if len(dps) != 1 else "")
            polls = []
            for bot, dp in dps:
                await bot.delete_webhook(drop_pending_updates=True)
                polls.append(asyncio.create_task(dp.start_polling(bot)))
            await asyncio.gather(*polls)
    finally:
        for task in background:
            task.cancel()
        if runner is not None:
            await runner.cleanup()
        await provider.close()
        await redis.aclose()
        for bot, _dp in dps:
            await bot.session.close()
        await dispose_engine()


async def _register_bot(me, brand: str) -> None:
    """Record this bot in the fleet registry (white-label / clones)."""
    from .db import repo
    try:
        async with get_sessionmaker()() as session:
            await repo.upsert_bot_instance(
                session, bot_telegram_id=me.id, username=me.username, brand=brand
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not register bot instance: %s", exc)


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


# The "/" command menu, in the RedQueen voice — registered for every UI language so no
# manual BotFather /setcommands is needed.
_COMMANDS = {
    "en": [
        ("panel", "Open the control console"),
        ("settings", "This chat's defense protocols"),
        ("help", "List all protocols"),
        ("ban", "Terminate a member"),
        ("kick", "Remove a member"),
        ("mute", "Silence a member"),
        ("warn", "Issue a warning"),
        ("purge", "Purge messages"),
        ("trust", "Inspect a member's trust score"),
        ("pro", "Unlock RedQueen Pro"),
        ("subscription", "Subscription status"),
        ("checksetup", "Verify my clearance"),
    ],
    "ru": [
        ("panel", "Открыть консоль управления"),
        ("settings", "Протоколы защиты чата"),
        ("help", "Все протоколы"),
        ("ban", "Ликвидировать участника"),
        ("kick", "Удалить участника"),
        ("mute", "Заглушить участника"),
        ("warn", "Вынести предупреждение"),
        ("purge", "Очистить сообщения"),
        ("trust", "Уровень доверия участника"),
        ("pro", "Подключить RedQueen Pro"),
        ("subscription", "Статус подписки"),
        ("checksetup", "Проверить мои права"),
    ],
    "uk": [
        ("panel", "Відкрити консоль керування"),
        ("settings", "Протоколи захисту чату"),
        ("help", "Усі протоколи"),
        ("ban", "Ліквідувати учасника"),
        ("kick", "Видалити учасника"),
        ("mute", "Заглушити учасника"),
        ("warn", "Винести попередження"),
        ("purge", "Очистити повідомлення"),
        ("trust", "Рівень довіри учасника"),
        ("pro", "Підключити RedQueen Pro"),
        ("subscription", "Статус підписки"),
        ("checksetup", "Перевірити мої права"),
    ],
}


async def _setup_commands(bot) -> None:
    from aiogram.types import BotCommand
    try:
        # English is the default (no language_code); RU/UK are localized overlays.
        for lang, items in _COMMANDS.items():
            cmds = [BotCommand(command=c, description=d) for c, d in items]
            if lang == "en":
                await bot.set_my_commands(cmds)
            else:
                await bot.set_my_commands(cmds, language_code=lang)
        log.info("Bot command menu registered (en/ru/uk)")
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not set commands: %s", exc)


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
