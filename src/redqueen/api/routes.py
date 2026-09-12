"""Mini App REST endpoints. Thin: authenticate → call services/repo → JSON."""
from __future__ import annotations

from datetime import timedelta

import aiogram.exceptions
from aiogram.types import LabeledPrice
from aiohttp import web

from ..db import repo
from ..i18n import SUPPORTED_LANGS
from ..i18n import t as _t
from ..services import billing, moderation, quarantine, roles, warns
from ..services.config import apply_patch, full_view
from ..utils.duration import humanize, until_from_now
from .auth import get_user, request_bot, require_chat_admin


def _chat_id(request: web.Request) -> int:
    try:
        return int(request.match_info["cid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad chat id") from exc


from contextlib import asynccontextmanager

@asynccontextmanager
async def _session(request: web.Request):
    async with request.app["sessionmaker"]() as session:
        session.info["redis"] = request.app["redis"]
        yield session


async def health(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


async def me(request: web.Request) -> web.Response:
    user = await get_user(request)
    bot, redis = request_bot(request), request.app["redis"]
    owner = user.id in request.app["settings"].owner_id_set
    chats = []
    
    async with _session(request) as session:
        # Auto-create user if they opened TMA without ever sending /start
        db_user = await repo.get_user(session, user.id)
        if db_user is None:
            db_user = await repo.upsert_user(
                session,
                telegram_id=user.id,
                username=user.username,
                full_name=user.full_name,
                lang=user.language_code or "en",
            )
            await session.commit()
        db_user_lang = db_user.lang or "en"
            
        for chat in await repo.list_active_chats(session, bot_id=bot.id):
            if owner or await roles.is_admin(bot, redis, chat_id=chat.telegram_id, user_id=user.id):
                chats.append({"id": chat.telegram_id, "title": chat.title, "type": chat.type,
                              "lang": chat.lang})
    bot_me = await bot.get_me()
    return web.json_response({
        "user": {"id": user.id, "username": user.username, "name": user.full_name, "lang": db_user_lang},
        "bot": {"username": bot_me.username},
        "chats": chats,
    })


async def put_me(request: web.Request) -> web.Response:
    user = await get_user(request)
    try:
        body = await request.json()
    except Exception as exc:
        raise web.HTTPBadRequest(reason="invalid JSON body") from exc
        
    lang = body.get("lang")
    if lang and isinstance(lang, str):
        async with _session(request) as session:
            await repo.upsert_user(
                session, 
                telegram_id=user.id,
                username=user.username,
                full_name=user.full_name,
                lang=lang[:8]
            )
            await session.commit()
    
    return web.json_response({"ok": True})


async def get_settings(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        chat = await repo.get_or_create_chat(session, cid)
        settings = await repo.get_settings(session, cid)
        await session.commit()  # get_settings may create the chat row
        view = full_view(settings)
        view["lang"] = chat.lang
        return web.json_response(view)


async def put_settings(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    try:
        patch = await request.json()
    except Exception as exc:
        raise web.HTTPBadRequest(reason="invalid JSON body") from exc
    if not isinstance(patch, dict):
        raise web.HTTPBadRequest(reason="body must be an object")
    async with _session(request) as session:
        chat = await repo.get_or_create_chat(session, cid)
        settings = await repo.get_settings(session, cid)
        if patch.get("lang") in SUPPORTED_LANGS:
            chat.lang = patch["lang"]

        if "core" in patch and "ai_api_key" in patch["core"]:
            api_key = patch["core"]["ai_api_key"]
            if api_key:
                from cryptography.fernet import Fernet
                try:
                    f = Fernet(request.app["settings"].secret_key)
                    settings.ai_api_key_encrypted = f.encrypt(api_key.encode()).decode()
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f"Failed to encrypt API key: {e}")
                    raise web.HTTPBadRequest(reason="Invalid SERVER_KEY configuration, cannot save API key")
            else:
                settings.ai_api_key_encrypted = None

        view = apply_patch(settings, patch)
        view["lang"] = chat.lang
        await session.commit()
        return web.json_response(view)


async def audit(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    limit = min(int(request.query.get("limit", 50)), 200)
    async with _session(request) as session:
        rows = await repo.recent_mod_actions(session, cid, limit=limit)
        return web.json_response([{
            "id": r.id, "action": r.action, "user_id": r.user_telegram_id,
            "actor_id": r.actor_id, "reason": r.reason, "meta": r.meta,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        } for r in rows])


async def quarantine_list(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        rows = await repo.pending_ai_verdicts(session, cid)
        return web.json_response([{
            "id": r.id, "user_id": r.user_telegram_id, "category": r.category,
            "score": r.score, "explanation": r.explanation, "text": r.text,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        } for r in rows])


async def quarantine_decide(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    user = await require_chat_admin(request, cid)
    try:
        body = await request.json()
    except Exception as exc:
        raise web.HTTPBadRequest(reason="invalid JSON body") from exc
    action = (body or {}).get("action")
    if action not in quarantine.VALID_ACTIONS:
        raise web.HTTPBadRequest(reason="action must be approve|ban|rule")
    try:
        vid = int(request.match_info["vid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad verdict id") from exc

    async with _session(request) as session:
        verdict = await repo.get_ai_verdict(session, vid)
        if verdict is None or verdict.chat_telegram_id != cid:
            raise web.HTTPNotFound(reason="verdict not found")
        result = await quarantine.decide(
            request_bot(request), session, verdict, actor_id=user.id, action=action
        )
        await session.commit()
        return web.json_response({"status": verdict.status, "action": result})


async def stats(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        counts = await repo.action_counts(session, cid)
        pending = len(await repo.pending_ai_verdicts(session, cid, limit=1000))
        timeline = await repo.actions_timeline(session, cid, days=14)
        categories = await repo.verdict_category_counts(session, cid)
        members = await repo.count_members(session, cid)
        return web.json_response({
            "actions": counts,
            "pending_quarantine": pending,
            "timeline": timeline,
            "categories": categories,
            "members": members,
        })


async def billing_status(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        sub = await billing.get_subscription(session, cid)
        return web.json_response({
            "pro": await billing.is_pro(session, cid),
            "active_until": sub.active_until.isoformat() if sub and sub.active_until else None,
            "price_stars": billing.PRO_PRICE_STARS,
            "period_days": billing.PRO_PERIOD_DAYS,
            "features": sorted(billing.PRO_FEATURES),
        })


async def billing_invoice(request: web.Request) -> web.Response:
    """Create a Telegram Stars invoice link the Mini App opens via openInvoice()."""
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    
    try:
        body = await request.json()
    except Exception:
        body = {}
    method = body.get("method", "stars")
    
    days = billing.PRO_PERIOD_DAYS
    
    if method == "crypto":
        cryptopay_token = request.app["settings"].cryptopay_token
        if not cryptopay_token:
            raise web.HTTPBadRequest(reason="CryptoPay is not configured")
        
        from aiocryptopay import AioCryptoPay, Networks
        crypto = AioCryptoPay(token=cryptopay_token, network=Networks.MAIN_NET)
        try:
            # We use USDT 5.0 as an equivalent to 500 Stars? Let's say 5 USDT for Pro
            invoice = await crypto.create_invoice(
                asset="USDT",
                amount=5.0,
                description=f"RedQueen Pro ({days} days) for chat {cid}",
                payload=f"pro:{cid}:{days}"
            )
            return web.json_response({"url": invoice.bot_invoice_url, "method": "crypto"})
        finally:
            await crypto.close()
    
    # Default: Telegram Stars
    url = await request_bot(request).create_invoice_link(
        title="RedQueen Pro",
        description=f"AI auto-ban, raid shield and advanced analytics for {days} days.",
        payload=f"pro:{cid}:{days}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"RedQueen Pro · {days} days", amount=billing.PRO_PRICE_STARS)],
    )
    return web.json_response({"url": url, "method": "stars"})


async def cryptopay_webhook(request: web.Request) -> web.Response:
    cryptopay_token = request.app["settings"].cryptopay_token
    if not cryptopay_token:
        return web.Response(status=400)
    
    body = await request.text()
    signature = request.headers.get("crypto-pay-api-signature", "")
    
    import hmac
    import hashlib
    secret = hashlib.sha256(cryptopay_token.encode()).digest()
    expected_sig = hmac.new(secret, body.encode(), hashlib.sha256).hexdigest()
    
    if signature != expected_sig:
        return web.Response(status=401)
        
    data = await request.json()
    if data.get("update_type") == "invoice_paid":
        payload = data.get("payload", {}).get("payload", "")
        if payload.startswith("pro:"):
            parts = payload.split(":")
            if len(parts) == 3:
                _, cid, days = parts
                async with request.app["sessionmaker"]() as session:
                    await billing.activate_pro(session, int(cid), days=int(days))
                    await repo.log_action(
                        session, chat_telegram_id=int(cid), user_telegram_id=0,
                        actor_id=None, action="pro_grant", reason=f"cryptopay {days}d"
                    )
    return web.Response(status=200)


async def members_search(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    q = request.query.get("q", "")
    async with _session(request) as session:
        rows = await repo.search_members(session, cid, query=q)
        return web.json_response([{
            "user_id": r.user_telegram_id, "username": r.username, "full_name": r.full_name,
            "message_count": r.message_count,
            "state": r.state,
            "muted_until": r.muted_until.isoformat() if r.muted_until else None,
            "last_seen": r.last_seen.isoformat() if r.last_seen else None,
        } for r in rows])


_MEMBER_ACTIONS = {"ban", "kick", "mute", "unmute", "unban", "warn"}


async def member_action(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    actor = await require_chat_admin(request, cid)
    try:
        uid = int(request.match_info["uid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad user id") from exc
    try:
        body = await request.json()
    except Exception as exc:
        raise web.HTTPBadRequest(reason="invalid JSON body") from exc
    action = (body or {}).get("action")
    if action not in _MEMBER_ACTIONS:
        raise web.HTTPBadRequest(reason=f"action must be one of {sorted(_MEMBER_ACTIONS)}")

    bot = request_bot(request)
    minutes = body.get("minutes")
    reason = (body.get("reason") or "").strip()[:200] or None
    _ACTION_WORDS = {"ban": "banned", "kick": "removed", "mute": "silenced"}

    async with _session(request) as session:
        chat = await repo.get_or_create_chat(session, cid)
        lang = chat.lang
        member = await repo.get_member(session, cid, uid)
        name = (member.full_name if member and member.full_name
                else f"@{member.username}" if member and member.username else str(uid))

        notice = None
        try:
            if action == "ban":
                ban_delta = timedelta(minutes=int(minutes)) if minutes else None
                await moderation.ban(bot, session, chat_id=cid, user_id=uid, actor_id=actor.id,
                                     until=until_from_now(ban_delta), reason=reason)
                notice = _t(lang, "BANNED", name=name, until=humanize(ban_delta, lang))
            elif action == "kick":
                await moderation.kick(bot, session, chat_id=cid, user_id=uid, actor_id=actor.id, reason=reason)
                notice = _t(lang, "KICKED", name=name)
            elif action == "unban":
                await moderation.unban(bot, session, chat_id=cid, user_id=uid, actor_id=actor.id)
                notice = _t(lang, "UNBANNED", name=name)
            elif action == "unmute":
                await moderation.unmute(bot, session, chat_id=cid, user_id=uid, actor_id=actor.id)
                notice = _t(lang, "UNMUTED", name=name)
            elif action == "mute":
                delta = timedelta(minutes=int(minutes)) if minutes else None
                await moderation.mute(bot, session, chat_id=cid, user_id=uid, actor_id=actor.id,
                                      until=until_from_now(delta), reason=reason)
                notice = _t(lang, "MUTED", name=name, until=humanize(delta, lang))
            elif action == "warn":
                result = await warns.issue_warn(bot, session, chat_id=cid, user_id=uid,
                                                actor_id=actor.id, reason=reason)
                notice = _t(lang, "WARNED", name=name, count=result.count, limit=result.limit,
                            reason=reason or "—")
                if result.triggered:
                    word = _ACTION_WORDS.get(result.action or "mute", "silenced")
                    notice += "\n" + _t(lang, "WARN_LIMIT_HIT", name=name, action=word)
        except aiogram.exceptions.TelegramAPIError as exc:
            # Telegram refuses to act on admins/owners or when lacking rights.
            raise web.HTTPBadRequest(reason=f"action failed: {exc}") from exc

        # Announce in the chat (in the chat's language, with the reason) — parity with
        # the slash-command flow, so members and other admins see what happened and why.
        if notice and action != "warn" and reason:
            notice += _t(lang, "ACTION_REASON", reason=reason)
        if notice:
            try:
                await bot.send_message(cid, notice)
            except Exception:  # noqa: BLE001
                pass

        await session.commit()
        return web.json_response({"ok": True, "action": action})


@web.middleware
async def rate_limit_middleware(request: web.Request, handler):
    if request.path.startswith("/api/"):
        redis = request.app["redis"]
        # Basic rate limiting by IP (or user ID if authed, but let's use IP/User ID).
        # We can extract user ID from initData if possible, but for simplicity, we'll use a token bucket or simple counter per IP/Auth.
        # Actually, get_user might throw if not authed, so let's limit by auth header if present, or IP.
        key = request.headers.get("Authorization", request.remote)
        rl_key = f"rl:{key}"
        try:
            async with redis.pipeline() as pipe:
                pipe.incr(rl_key)
                pipe.expire(rl_key, 1, nx=True)
                results = await pipe.execute()
                
            count = results[0]
            if count > 30: # 30 requests per second
                raise web.HTTPTooManyRequests()
        except Exception as e:
            if isinstance(e, web.HTTPException): raise
            # Ignore redis errors for rate limiting
            pass
    return await handler(request)

@web.middleware
async def error_handling_middleware(request: web.Request, handler):
    try:
        return await handler(request)
    except web.HTTPException:
        raise
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Unhandled API Error")
        raise web.HTTPInternalServerError(reason="Internal Server Error")

async def upload_media(request: web.Request) -> web.Response:
    """Accept multipart upload, send to admin's PM to get a permanent file_id."""
    init = _init_data(request)
    uid = init.user.id
    cid = _chat_id(request)
    await require_chat_admin(request, cid)

    reader = await request.multipart()
    field = await reader.next()
    if not field:
        raise web.HTTPBadRequest(reason="No file provided")
    
    filename = field.filename or "file"
    content = await field.read()
    
    bot = request_bot(request)
    
    from aiogram.types import BufferedInputFile
    file = BufferedInputFile(content, filename=filename)
    
    try:
        if filename.lower().endswith((".mp4", ".gif")):
            msg = await bot.send_animation(uid, animation=file)
            file_id = f"animation:{msg.animation.file_id}"
        else:
            msg = await bot.send_photo(uid, photo=file)
            file_id = f"photo:{msg.photo[-1].file_id}"
    except Exception as e:
        raise web.HTTPBadRequest(reason=f"Failed to process media (bot might need PM access): {e}")
        
    return web.json_response({"file_id": file_id})

def setup_routes(app: web.Application) -> None:
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(rate_limit_middleware)
    app.router.add_get("/api/health", health)
    app.router.add_get("/api/me", me)
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
    app.router.add_get("/api/chats/{cid}/billing", billing_status)
    app.router.add_post("/api/chats/{cid}/billing/invoice", billing_invoice)
    app.router.add_get("/api/chats/{cid}/members", members_search)
    app.router.add_post("/api/chats/{cid}/members/{uid}/action", member_action)
    app.router.add_post("/api/chats/{cid}/upload", upload_media)
    app.router.add_post("/webhook/cryptopay", cryptopay_webhook)


