with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

# English
en_keys = """
    'dashboard.ai_summary': 'AI Digest',
    'dashboard.ai_summary.desc': 'Generate a short summary from the last 300 messages.',
    'dashboard.ai_summary.btn': 'Generate Digest',
    'dashboard.ai_summary.loading': 'Analyzing chat history...',
    'sec.overview': 'Overview',
    
    'sec.defcon': 'Auto-DEFCON',
    'defcon.enabled': 'Enable Shield',
    'defcon.enabled_desc': 'Activates during a spam attack',
    'defcon.threshold': 'Activation threshold',
    'defcon.lockSeconds': 'Alert duration',
    'defcon.action': 'Action on alert',
    'action.read_only': 'Read-Only (new)',
    'action.strict': 'Strict (block media)',
    'action.captcha': 'Captcha',
    
    'ai.log_channel': 'AI Tribunal (Log Channel)',
    'ai.log_channel.desc': 'Channel/Group ID for Quarantine cards to vote on',
"""

text = text.replace("'sec.warns': 'Warns',", en_keys + "\n    'sec.warns': 'Warns',")

# Russian
ru_keys = """
    'dashboard.ai_summary': 'Умный Дайджест',
    'dashboard.ai_summary.desc': 'Сгенерировать краткую выжимку из последних 300 сообщений.',
    'dashboard.ai_summary.btn': 'Создать Дайджест',
    'dashboard.ai_summary.loading': 'Анализирую историю чата...',
    'sec.overview': 'Обзор',
    
    'sec.defcon': 'Auto-DEFCON',
    'defcon.enabled': 'Включить защиту',
    'defcon.enabled_desc': 'Активируется при атаке спамеров',
    'defcon.threshold': 'Порог активации',
    'defcon.lockSeconds': 'Длительность тревоги',
    'defcon.action': 'Действие при тревоге',
    'action.read_only': 'Read-Only (новым)',
    'action.strict': 'Strict (удалять медиа)',
    'action.captcha': 'Капча',
    
    'ai.log_channel': 'AI Tribunal (Лог-канал)',
    'ai.log_channel.desc': 'ID канала/группы для отправки карточек Quarantine на голосование',
"""

text = text.replace("'sec.warns': 'Варны',", ru_keys + "\n    'sec.warns': 'Варны',")

# Ukrainian
uk_keys = """
    'dashboard.ai_summary': 'Розумний Дайджест',
    'dashboard.ai_summary.desc': 'Згенерувати коротку витримку з останніх 300 повідомлень.',
    'dashboard.ai_summary.btn': 'Створити Дайджест',
    'dashboard.ai_summary.loading': 'Аналізую історію чату...',
    'sec.overview': 'Огляд',
    
    'sec.defcon': 'Auto-DEFCON',
    'defcon.enabled': 'Увімкнути захист',
    'defcon.enabled_desc': 'Активується при спам-атаці',
    'defcon.threshold': 'Поріг активації',
    'defcon.lockSeconds': 'Тривалість тривоги',
    'defcon.action': 'Дія під час тривоги',
    'action.read_only': 'Read-Only (новим)',
    'action.strict': 'Strict (видаляти медіа)',
    'action.captcha': 'Капча',
    
    'ai.log_channel': 'AI Tribunal (Лог-канал)',
    'ai.log_channel.desc': 'ID каналу/групи для відправки карток Quarantine на голосування',
"""

text = text.replace("'sec.warns': 'Варни',", uk_keys + "\n    'sec.warns': 'Варни',")

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)
