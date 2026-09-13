filename = "webapp/src/i18n/translations.js"
with open(filename, "r") as f:
    text = f.read()

en_add = """
    'sec.triggers': 'Auto-Replies',
    'sec.triggers.desc': 'Custom command triggers',
    'triggers.desc': 'Configure the bot to reply automatically to specific phrases or commands.',
    'triggers.add': 'Add New Trigger',
    'triggers.phrase': 'Phrase or Command',
    'triggers.phrase.ph': 'e.g. /rules or price',
    'triggers.reply': 'Reply Text',
    'triggers.reply.ph': 'The bot will send this...',
    'triggers.regex': 'Use Regex',
    'triggers.btn.add': 'Add Trigger',
    'triggers.active': 'Active Triggers',
    'triggers.empty': 'No triggers found.',
    'triggers.btn.delete': 'Delete',
"""

ru_add = """
    'sec.triggers': 'Авто-Ответы',
    'sec.triggers.desc': 'Кастомные триггеры и команды',
    'triggers.desc': 'Настройте автоматические ответы бота на определенные фразы или команды.',
    'triggers.add': 'Добавить новый триггер',
    'triggers.phrase': 'Фраза или команда',
    'triggers.phrase.ph': 'напр. /rules или цена',
    'triggers.reply': 'Текст ответа',
    'triggers.reply.ph': 'Бот отправит этот текст...',
    'triggers.regex': 'Использовать Regex',
    'triggers.btn.add': 'Добавить триггер',
    'triggers.active': 'Активные триггеры',
    'triggers.empty': 'Триггеры не найдены.',
    'triggers.btn.delete': 'Удалить',
"""

uk_add = """
    'sec.triggers': 'Авто-Відповіді',
    'sec.triggers.desc': 'Кастомні тригери та команди',
    'triggers.desc': 'Налаштуйте автоматичні відповіді бота на певні фрази або команди.',
    'triggers.add': 'Додати новий тригер',
    'triggers.phrase': 'Фраза або команда',
    'triggers.phrase.ph': 'напр. /rules або ціна',
    'triggers.reply': 'Текст відповіді',
    'triggers.reply.ph': 'Бот надішле цей текст...',
    'triggers.regex': 'Використовувати Regex',
    'triggers.btn.add': 'Додати тригер',
    'triggers.active': 'Активні тригери',
    'triggers.empty': 'Тригери не знайдені.',
    'triggers.btn.delete': 'Видалити',
"""

text = text.replace("'sec.triggers': 'Auto-Replies',\\n    'sec.triggers.desc': 'Custom command triggers',", en_add)
text = text.replace("'sec.triggers': 'Авто-Ответы',\\n    'sec.triggers.desc': 'Кастомные триггеры и команды',", ru_add)
text = text.replace("'sec.triggers': 'Авто-Відповіді',\\n    'sec.triggers.desc': 'Кастомні тригери та команди',", uk_add)

with open(filename, "w") as f:
    f.write(text)
