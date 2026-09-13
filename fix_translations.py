with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

# Add defcon translations
ru = """      'sec.defcon': 'Auto-DEFCON',
      'defcon.enabled': 'Включить защиту',
      'defcon.enabled_desc': 'Активируется при атаке спамеров',
      'defcon.threshold': 'Порог активации',
      'defcon.lockSeconds': 'Длительность тревоги',
      'defcon.action': 'Действие при тревоге',
      'action.read_only': 'Read-Only (новым)',
      'action.strict': 'Strict (удалять медиа)',
      'action.captcha': 'Капча',"""

en = """      'sec.defcon': 'Auto-DEFCON',
      'defcon.enabled': 'Enable Shield',
      'defcon.enabled_desc': 'Activates during a spam attack',
      'defcon.threshold': 'Activation threshold',
      'defcon.lockSeconds': 'Alert duration',
      'defcon.action': 'Action on alert',
      'action.read_only': 'Read-Only (new)',
      'action.strict': 'Strict (block media)',
      'action.captcha': 'Captcha',"""

uk = """      'sec.defcon': 'Auto-DEFCON',
      'defcon.enabled': 'Увімкнути захист',
      'defcon.enabled_desc': 'Активується при спам-атаці',
      'defcon.threshold': 'Поріг активації',
      'defcon.lockSeconds': 'Тривалість тривоги',
      'defcon.action': 'Дія під час тривоги',
      'action.read_only': 'Read-Only (новим)',
      'action.strict': 'Strict (видаляти медіа)',
      'action.captcha': 'Капча',"""

text = text.replace("'sec.raid': 'Рейд-защита',", ru)
text = text.replace("'sec.raid': 'Raid Shield',", en)
text = text.replace("'sec.raid': 'Рейд-захист',", uk)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)
