from __future__ import annotations

import hmac
import hashlib

from aiohttp import web
from aiogram.types import LabeledPrice

from .utils import _chat_id, _session
from .auth import require_chat_admin, request_bot
from ..services import billing
from ..db import repo

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
    except ValueError:
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
    
    secret = hashlib.sha256(cryptopay_token.encode()).digest()
    expected_sig = hmac.new(secret, body.encode(), hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(signature, expected_sig):
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
