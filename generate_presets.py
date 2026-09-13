import re

with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

en_keys = """
    'presets.title': 'Smart Presets',
    'presets.apply': 'Apply',
    'presets.basic': 'Safe & Simple',
    'presets.basic.desc': 'Standard protection. Basic filters, anti-flood.',
    'presets.crypto': 'Crypto & Web3',
    'presets.crypto.desc': 'Max security. Auto-ban bots, Strict DEFCON, Captcha.',
    'presets.corp': 'Corporate',
    'presets.corp.desc': 'Zero tolerance for toxicity. Quarantine mode.',
    'presets.chill': 'Chill Chat',
    'presets.chill.desc': 'Relaxed rules. Minimal interruptions.',
"""

ru_keys = """
    'presets.title': 'Умные Пресеты',
    'presets.apply': 'Применить',
    'presets.basic': 'Базовый',
    'presets.basic.desc': 'Стандартная защита от спама и флуда.',
    'presets.crypto': 'Крипто и Web3',
    'presets.crypto.desc': 'Максимальная защита. Автобан, Captcha, DEFCON.',
    'presets.corp': 'Строгий (Корпорат)',
    'presets.corp.desc': 'Никакой токсичности и мата. Карантин включен.',
    'presets.chill': 'Свободное Общение',
    'presets.chill.desc': 'Расслабленные правила. Минимум вмешательств.',
"""

uk_keys = """
    'presets.title': 'Розумні Пресети',
    'presets.apply': 'Застосувати',
    'presets.basic': 'Базовий',
    'presets.basic.desc': 'Стандартний захист від спаму та флуду.',
    'presets.crypto': 'Крипто та Web3',
    'presets.crypto.desc': 'Максимальний захист. Автобан, Captcha, DEFCON.',
    'presets.corp': 'Суворий (Корпорат)',
    'presets.corp.desc': 'Жодної токсичності та лайки. Карантин увімкнено.',
    'presets.chill': 'Вільне Спілкування',
    'presets.chill.desc': 'Розслаблені правила. Мінімум втручань.',
"""

text = text.replace("'tips.quarantine': 'You have pending messages in Quarantine.',", "'tips.quarantine': 'You have pending messages in Quarantine.'," + en_keys)
text = text.replace("'tips.quarantine': 'В Карантине есть сообщения на проверку.',", "'tips.quarantine': 'В Карантине есть сообщения на проверку.'," + ru_keys)
text = text.replace("'tips.quarantine': 'У Карантині є повідомлення на перевірку.',", "'tips.quarantine': 'У Карантині є повідомлення на перевірку.'," + uk_keys)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

