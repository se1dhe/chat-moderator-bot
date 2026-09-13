import re

with open('src/redqueen/handlers/captcha.py', 'r') as f:
    text = f.read()

# Add defcon check to on_member_join
old_join = """    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    if not cfg["enabled"]:
        return"""

new_join = """    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    from redqueen.handlers.defcon import is_active
    full_cfg = get_config(settings)
    is_defcon_captcha = is_active(full_cfg) and full_cfg["defcon"]["action"] == "captcha"
    if not cfg["enabled"] and not is_defcon_captcha:
        return"""
text = text.replace(old_join, new_join)

# Add defcon check to on_join_request
old_req = """    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    if not cfg["enabled"]:
        await bot.approve_chat_join_request(event.chat.id, event.from_user.id)
        return"""

new_req = """    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)["captcha"]
    from redqueen.handlers.defcon import is_active
    full_cfg = get_config(settings)
    is_defcon_captcha = is_active(full_cfg) and full_cfg["defcon"]["action"] == "captcha"
    if not cfg["enabled"] and not is_defcon_captcha:
        await bot.approve_chat_join_request(event.chat.id, event.from_user.id)
        return"""
text = text.replace(old_req, new_req)

with open('src/redqueen/handlers/captcha.py', 'w') as f:
    f.write(text)
