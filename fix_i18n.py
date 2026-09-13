import re

filename = 'webapp/src/i18n/translations.js'
with open(filename, 'r') as f:
    text = f.read()

en_add = """
    'sec.triggers': 'Auto-Replies',
    'sec.triggers.desc': 'Custom command triggers',
"""
ru_add = """
    'sec.triggers': 'Авто-Ответы',
    'sec.triggers.desc': 'Кастомные триггеры и команды',
"""
uk_add = """
    'sec.triggers': 'Авто-Відповіді',
    'sec.triggers.desc': 'Кастомні тригери та команди',
"""

text = text.replace("'sec.modes.desc': 'Night mode, read-only, slow mode',", "'sec.modes.desc': 'Night mode, read-only, slow mode'," + en_add)
text = text.replace("'sec.modes.desc': 'Ночной режим, только чтение, слоумод',", "'sec.modes.desc': 'Ночной режим, только чтение, слоумод'," + ru_add)
text = text.replace("'sec.modes.desc': 'Нічний режим, тільки читання, слоумод',", "'sec.modes.desc': 'Нічний режим, тільки читання, слоумод'," + uk_add)

with open(filename, 'w') as f:
    f.write(text)
