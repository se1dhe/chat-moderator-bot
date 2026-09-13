import re

with open('src/redqueen/handlers/payments.py', 'r') as f:
    text = f.read()

# Add logic to on_successful_payment
old_success = """    if len(parts) >= 3 and parts[0] == "pro":
        try:
            chat_id, days = int(parts[1]), int(parts[2])
        except ValueError:
            pass

    until = await billing.record_payment(
        session, chat_id=chat_id, payer_id=message.from_user.id, stars=sp.total_amount,
        charge_id=sp.telegram_payment_charge_id, days=days,
    )
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=message.from_user.id,
        actor_id=message.from_user.id, action="pro_payment", reason=f"{sp.total_amount} XTR",
        meta={"charge_id": sp.telegram_payment_charge_id, "days": days},
    )
    log.info("Pro payment: chat=%s payer=%s stars=%s until=%s",
             chat_id, message.from_user.id, sp.total_amount, until)
    try:
        await message.bot.send_message(message.from_user.id, t("PRO_ACTIVATED", until=_fmt(until)))
    except Exception:
        await message.answer(t("PRO_ACTIVATED", until=_fmt(until)))"""

new_success = """    if len(parts) >= 3 and parts[0] == "pro":
        try:
            chat_id, days = int(parts[1]), int(parts[2])
        except ValueError:
            pass

        until = await billing.record_payment(
            session, chat_id=chat_id, payer_id=message.from_user.id, stars=sp.total_amount,
            charge_id=sp.telegram_payment_charge_id, days=days,
        )
        await repo.log_action(
            session, chat_telegram_id=chat_id, user_telegram_id=message.from_user.id,
            actor_id=message.from_user.id, action="pro_payment", reason=f"{sp.total_amount} XTR",
            meta={"charge_id": sp.telegram_payment_charge_id, "days": days},
        )
        log.info("Pro payment: chat=%s payer=%s stars=%s until=%s",
                 chat_id, message.from_user.id, sp.total_amount, until)
        try:
            await message.bot.send_message(message.from_user.id, t("PRO_ACTIVATED", until=_fmt(until)))
        except Exception:
            await message.answer(t("PRO_ACTIVATED", until=_fmt(until)))
            
    elif len(parts) >= 3 and parts[0] == "preset":
        # Handle preset purchase
        try:
            chat_id = int(parts[1])
            preset_id = parts[2]
            
            # Fetch settings and update
            from ..db.models import ChatSettings
            from sqlalchemy import select
            
            settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == chat_id))
            if settings_obj:
                data = settings_obj.data or {}
                purchased = data.get("purchased_presets", [])
                if preset_id not in purchased:
                    purchased.append(preset_id)
                    data["purchased_presets"] = purchased
                    settings_obj.data = data
                    # force update
                    from sqlalchemy.orm.attributes import flag_modified
                    flag_modified(settings_obj, "data")
                    await session.commit()
            
            await repo.log_action(
                session, chat_telegram_id=chat_id, user_telegram_id=message.from_user.id,
                actor_id=message.from_user.id, action="preset_payment", reason=f"preset: {preset_id} ({sp.total_amount} XTR)",
                meta={"charge_id": sp.telegram_payment_charge_id, "preset": preset_id},
            )
            log.info("Preset payment: chat=%s preset=%s stars=%s", chat_id, preset_id, sp.total_amount)
            # We don't send a confirmation message for presets yet, it just unlocks in UI
        except ValueError:
            pass"""
            
text = text.replace(old_success, new_success)

with open('src/redqueen/handlers/payments.py', 'w') as f:
    f.write(text)
