import re

with open("src/pages/Members.jsx", "r") as f:
    content = f.read()
content = content.replace("{t('members.messages', { n: m.message_count })}", "{t('members.messages', { count: m.message_count })}")
with open("src/pages/Members.jsx", "w") as f:
    f.write(content)

with open("src/i18n/translations.js", "r") as f:
    t_content = f.read()

t_content = t_content.replace("'act.ban': 'Ban',", "'act.warn': 'Warn',\n    'act.ban': 'Ban',")
t_content = t_content.replace("'act.ban': 'Забанить',", "'act.warn': 'Варн',\n    'act.ban': 'Забанить',")
t_content = t_content.replace("'act.ban': 'Забанити',", "'act.warn': 'Варн',\n    'act.ban': 'Забанити',")

with open("src/i18n/translations.js", "w") as f:
    f.write(t_content)
