import re

with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

# Add DEFCON and AI Summary to RU
ru_add = """      'dashboard.ai_summary': 'Умный Дайджест',
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
      'action.captcha': 'Капча',"""

text = text.replace("'sec.overview': 'Обзор',", ru_add)
text = text.replace("'sec.raid': 'Рейд-защита',", "")
text = text.replace("'ai.mode': 'Режим работы AI',", "'ai.log_channel': 'AI Tribunal (Лог-канал)',\n      'ai.log_channel.desc': 'ID канала/группы для отправки карточек Quarantine на голосование',\n      'ai.mode': 'Режим работы AI',")

# Add DEFCON and AI Summary to EN
en_add = """      'dashboard.ai_summary': 'AI Digest',
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
      'action.captcha': 'Captcha',"""

text = text.replace("'sec.overview': 'Overview',", en_add)
text = text.replace("'sec.raid': 'Raid Shield',", "")
text = text.replace("'ai.mode': 'AI Mode',", "'ai.log_channel': 'AI Tribunal (Log Channel)',\n      'ai.log_channel.desc': 'Channel/Group ID for Quarantine cards to vote on',\n      'ai.mode': 'AI Mode',")

# Add DEFCON and AI Summary to UK
uk_add = """      'dashboard.ai_summary': 'Розумний Дайджест',
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
      'action.captcha': 'Капча',"""

text = text.replace("'sec.overview': 'Огляд',", uk_add)
text = text.replace("'sec.raid': 'Рейд-захист',", "")
text = text.replace("'ai.mode': 'Режим роботи AI',", "'ai.log_channel': 'AI Tribunal (Лог-канал)',\n      'ai.log_channel.desc': 'ID каналу/групи для відправки карток Quarantine на голосування',\n      'ai.mode': 'Режим роботи AI',")


# Fix duplicates specifically by regex
import re

def dedupe_block(block):
    lines = block.split('\n')
    seen = set()
    out = []
    for line in lines:
        m = re.search(r"^\s*'([^']+)':", line)
        if m:
            k = m.group(1)
            if k in seen:
                continue
            seen.add(k)
        out.append(line)
    return '\n'.join(out)

# We need to dedupe per dictionary (en, ru, uk)
# Let's split by "export const" and dedupe each part
parts = text.split('export const')
new_parts = [parts[0]]
for part in parts[1:]:
    new_parts.append(dedupe_block(part))
text = 'export const'.join(new_parts)


with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

