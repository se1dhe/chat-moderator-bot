import re

def fix_routes_billing():
    with open('src/redqueen/api/routes_billing.py', 'r') as f:
        text = f.read()

    # Fix in billing_status
    old_status = """        from ..db.models import ChatSettings
        from sqlalchemy import select
        settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == cid))"""
    new_status = """        from ..db.models import ChatSettings, Chat
        from sqlalchemy import select
        settings_obj = await session.scalar(
            select(ChatSettings)
            .join(Chat, Chat.id == ChatSettings.chat_id)
            .where(Chat.telegram_id == cid)
        )"""
    text = text.replace(old_status, new_status)
    
    # Fix in cryptopay_webhook
    old_webhook = """                    from ..db.models import ChatSettings
                    from sqlalchemy import select
                    from sqlalchemy.orm.attributes import flag_modified
                    
                    settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == int(cid)))"""
    new_webhook = """                    from ..db.models import ChatSettings, Chat
                    from sqlalchemy import select
                    from sqlalchemy.orm.attributes import flag_modified
                    
                    settings_obj = await session.scalar(
                        select(ChatSettings)
                        .join(Chat, Chat.id == ChatSettings.chat_id)
                        .where(Chat.telegram_id == int(cid))
                    )"""
    text = text.replace(old_webhook, new_webhook)

    with open('src/redqueen/api/routes_billing.py', 'w') as f:
        f.write(text)

def fix_payments():
    with open('src/redqueen/handlers/payments.py', 'r') as f:
        text = f.read()

    old = """            from ..db.models import ChatSettings
            from sqlalchemy import select
            
            settings_obj = await session.scalar(select(ChatSettings).where(ChatSettings.chat_id == chat_id))"""
    new = """            from ..db.models import ChatSettings, Chat
            from sqlalchemy import select
            
            settings_obj = await session.scalar(
                select(ChatSettings)
                .join(Chat, Chat.id == ChatSettings.chat_id)
                .where(Chat.telegram_id == chat_id)
            )"""
    text = text.replace(old, new)
    with open('src/redqueen/handlers/payments.py', 'w') as f:
        f.write(text)

fix_routes_billing()
fix_payments()
