import re

with open('src/redqueen/api/routes_billing.py', 'r') as f:
    text = f.read()

# Modify billing_status to return purchased_presets
old_status = """        return web.json_response({
            "pro": await billing.is_pro(session, cid),
            "active_until": sub.active_until.isoformat() if sub and sub.active_until else None,
            "price_stars": billing.PRO_PRICE_STARS,
            "period_days": billing.PRO_PERIOD_DAYS,
            "features": sorted(billing.PRO_FEATURES),
        })"""

new_status = """        
        from ..db.models import ChatSettings
        from sqlalchemy import select
        settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == cid))
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
        })"""
text = text.replace(old_status, new_status)

# Modify billing_invoice to accept preset_id
old_invoice = """    try:
        body = await request.json()
    except ValueError:
        body = {}
    method = body.get("method", "stars")
    
    days = billing.PRO_PERIOD_DAYS
    
    if method == "crypto":"""

new_invoice = """    try:
        body = await request.json()
    except ValueError:
        body = {}
    method = body.get("method", "stars")
    preset_id = body.get("preset_id")
    
    days = billing.PRO_PERIOD_DAYS
    
    if method == "crypto":"""
text = text.replace(old_invoice, new_invoice)

old_crypto = """            invoice = await crypto.create_invoice(
                asset="USDT",
                amount=5.0,
                description=f"RedQueen Pro ({days} days) for chat {cid}",
                payload=f"pro:{cid}:{days}"
            )"""
new_crypto = """            payload_str = f"preset:{cid}:{preset_id}" if preset_id else f"pro:{cid}:{days}"
            desc_str = f"Template: {preset_id}" if preset_id else f"RedQueen Pro ({days} days)"
            amt = 2.0 if preset_id else 5.0  # Presets are cheaper
            invoice = await crypto.create_invoice(
                asset="USDT",
                amount=amt,
                description=desc_str + f" for chat {cid}",
                payload=payload_str
            )"""
text = text.replace(old_crypto, new_crypto)

old_stars = """    url = await request_bot(request).create_invoice_link(
        title="RedQueen Pro",
        description=f"AI auto-ban, raid shield and advanced analytics for {days} days.",
        payload=f"pro:{cid}:{days}",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=f"RedQueen Pro · {days} days", amount=billing.PRO_PRICE_STARS)],
    )"""
new_stars = """    
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
        )"""
text = text.replace(old_stars, new_stars)

# Cryptopay webhook handler update
old_webhook = """    if data.get("update_type") == "invoice_paid":
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
    return web.Response(status=200)"""

new_webhook = """    if data.get("update_type") == "invoice_paid":
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
                    
                    from ..db.models import ChatSettings
                    from sqlalchemy import select
                    from sqlalchemy.orm.attributes import flag_modified
                    
                    settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == int(cid)))
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
    return web.Response(status=200)"""
text = text.replace(old_webhook, new_webhook)

with open('src/redqueen/api/routes_billing.py', 'w') as f:
    f.write(text)
