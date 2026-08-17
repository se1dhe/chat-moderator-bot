"""Mini App REST endpoints. Thin: authenticate → call services/repo → JSON."""
from __future__ import annotations

from aiogram.types import LabeledPrice
from aiohttp import web

from ..db import repo
from ..i18n import SUPPORTED_LANGS
from ..services import billing, quarantine, roles
from ..services.config import apply_patch, full_view
from .auth import get_user, require_chat_admin


def _chat_id(request: web.Request) -> int:
    try:
        return int(request.match_info["cid"])
    except (KeyError, ValueError) as exc:
        raise web.HTTPBadRequest(reason="bad chat id") from exc


def _session(request: web.Request):
    return request.app["sessionmaker"]()


async def health(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


async def me(request: web.Request) -> web.Response:
    user = await get_user(request)
    bot, redis = request.app["bot"], request.app["redis"]
    owner = user.id in request.app["settings"].owner_id_set
    chats = []
    async with _session(request) as session:
        for chat in await repo.list_active_chats(session):
            if owner or await roles.is_admin(bot, redis, chat_id=chat.telegram_id, user_id=user.id):
                chats.append({"id": chat.telegram_id, "title": chat.title, "type": chat.type,
                              "lang": chat.lang})
    return web.json_response({
        "user": {"id": user.id, "username": user.username, "name": user.full_name},
        "chats": chats,
    })


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
            request.app["bot"], session, verdict, actor_id=user.id, action=action
        )
        await session.commit()
        return web.json_response({"status": verdict.status, "action": result})


async def stats(request: web.Request) -> web.Response:
    cid = _chat_id(request)
    await require_chat_admin(request, cid)
    async with _session(request) as session:
        counts = await repo.action_counts(session, cid)
        pending = len(await repo.pending_ai_verdicts(session, cid, limit=1000))
        return web.json_response({"actions": counts, "pending_quarantine": pending})


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
    days = billing.PRO_PERIOD_DAYS
    url = await request.app["bot"].create_invoice_link(
        title="RedQueen Pro",
        description=f"AI auto-ban, raid shield and advanced analytics for {days} days.",
        payload=f"pro:{cid}:{days}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"RedQueen Pro · {days} days", amount=billing.PRO_PRICE_STARS)],
    )
    return web.json_response({"url": url})


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/api/health", health)
    app.router.add_get("/api/me", me)
    app.router.add_get("/api/chats/{cid}/settings", get_settings)
    app.router.add_put("/api/chats/{cid}/settings", put_settings)
    app.router.add_get("/api/chats/{cid}/audit", audit)
    app.router.add_get("/api/chats/{cid}/quarantine", quarantine_list)
    app.router.add_post("/api/chats/{cid}/quarantine/{vid}", quarantine_decide)
    app.router.add_get("/api/chats/{cid}/stats", stats)
    app.router.add_get("/api/chats/{cid}/billing", billing_status)
    app.router.add_post("/api/chats/{cid}/billing/invoice", billing_invoice)
