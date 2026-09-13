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
        
        from ..db.models import ChatSettings, Chat
        from sqlalchemy import select
        settings_obj = await session.scalar(
            select(ChatSettings)
            .join(Chat, Chat.id == ChatSettings.chat_id)
            .where(Chat.telegram_id == cid)
        )
        purchased_presets = []
        if settings_obj and settings_obj.data:
            purchased_presets = settings_obj.data.get("purchased_presets", [])
            
        return web.json_response({
            "pro": await billing.is_pro(session, cid),
            "active_until": sub.active_until.isoformat() if sub and sub.active_until else None,
            "price_stars": billing.PRO_PRICE_STARS,
            "period_days": billing.PRO_PERIOD_DAYS,
            "features": sorted(billing.PRO_FEATURES),
            "purchased_presets": purchased_presets,
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
    preset_id = body.get("preset_id")
    
    days = billing.PRO_PERIOD_DAYS
    
    if method == "crypto":
        cryptopay_token = request.app["settings"].cryptopay_token
        if not cryptopay_token:
            raise web.HTTPBadRequest(reason="CryptoPay is not configured")
        
        from aiocryptopay import AioCryptoPay, Networks
        crypto = AioCryptoPay(token=cryptopay_token, network=Networks.MAIN_NET)
        try:
            # We use USDT 5.0 as an equivalent to 500 Stars? Let's say 5 USDT for Pro
            payload_str = f"preset:{cid}:{preset_id}" if preset_id else f"pro:{cid}:{days}"
            desc_str = f"Template: {preset_id}" if preset_id else f"RedQueen Pro ({days} days)"
            amt = 2.0 if preset_id else 5.0  # Presets are cheaper
            invoice = await crypto.create_invoice(
                asset="USDT",
                amount=amt,
                description=desc_str + f" for chat {cid}",
                payload=payload_str
            )
            return web.json_response({"url": invoice.bot_invoice_url, "method": "crypto"})
        finally:
            await crypto.close()
    
    # Default: Telegram Stars
    
    if preset_id:
        url = await request_bot(request).create_invoice_link(
            title=f"Smart Preset: {preset_id.title()}",
            description=f"Unlock the {preset_id} moderation template for this chat forever.",
            payload=f"preset:{cid}:{preset_id}",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label=f"Preset · {preset_id.title()}", amount=150)], # 150 stars for a preset
        )
    else:
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
        
        async with request.app["sessionmaker"]() as session:
            if payload.startswith("pro:"):
                parts = payload.split(":")
                if len(parts) == 3:
                    _, cid, days = parts
                    await billing.activate_pro(session, int(cid), days=int(days))
                    await repo.log_action(
                        session, chat_telegram_id=int(cid), user_telegram_id=0,
                        actor_id=None, action="pro_grant", reason=f"cryptopay {days}d"
                    )
            elif payload.startswith("preset:"):
                parts = payload.split(":")
                if len(parts) == 3:
                    _, cid, preset_id = parts
                    
                    from ..db.models import ChatSettings, Chat
                    from sqlalchemy import select
                    from sqlalchemy.orm.attributes import flag_modified
                    
                    settings_obj = await session.scalar(
                        select(ChatSettings)
                        .join(Chat, Chat.id == ChatSettings.chat_id)
                        .where(Chat.telegram_id == int(cid))
                    )
                    if settings_obj:
                        data_json = settings_obj.data or {}
                        purchased = data_json.get("purchased_presets", [])
                        if preset_id not in purchased:
                            purchased.append(preset_id)
                            data_json["purchased_presets"] = purchased
                            settings_obj.data = data_json
                            flag_modified(settings_obj, "data")
                            await session.commit()
                            
                    await repo.log_action(
                        session, chat_telegram_id=int(cid), user_telegram_id=0,
                        actor_id=None, action="preset_payment", reason=f"cryptopay preset {preset_id}"
                    )
    return web.Response(status=200)
