import re

with open('src/redqueen/services/moderation.py', 'r') as f:
    text = f.read()

text = text.replace(
    'await bot.restrict_chat_member(chat_id, user_id, permissions=_UNMUTED_PERMISSIONS)',
    'await bot.restrict_chat_member(chat_id, user_id, permissions=_UNMUTED_PERMISSIONS, use_independent_chat_permissions=False)'
)

with open('src/redqueen/services/moderation.py', 'w') as f:
    f.write(text)

