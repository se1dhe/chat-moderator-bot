import re

with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

text = text.replace("'ai.mode': 'Режим работы AI',", "'ai.log_channel': 'AI Tribunal (Лог-канал)',\n      'ai.log_channel.desc': 'ID канала/группы для отправки карточек Quarantine на голосование',\n      'ai.mode': 'Режим работы AI',")
text = text.replace("'ai.mode': 'AI Mode',", "'ai.log_channel': 'AI Tribunal (Log Channel)',\n      'ai.log_channel.desc': 'Channel/Group ID for Quarantine cards to vote on',\n      'ai.mode': 'AI Mode',")
text = text.replace("'ai.mode': 'Режим роботи AI',", "'ai.log_channel': 'AI Tribunal (Лог-канал)',\n      'ai.log_channel.desc': 'ID каналу/групи для відправки карток Quarantine на голосування',\n      'ai.mode': 'Режим роботи AI',")

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

