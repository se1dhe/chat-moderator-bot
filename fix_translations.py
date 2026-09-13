with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

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

text = text.replace("'tips.quarantine': 'У вас есть новые сообщения в Карантине.',", "'tips.quarantine': 'У вас есть новые сообщения в Карантине.'," + ru_keys)
text = text.replace("'tips.quarantine': 'У вас є нові повідомлення в Карантині.',", "'tips.quarantine': 'У вас є нові повідомлення в Карантині.'," + uk_keys)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)
