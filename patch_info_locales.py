with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

en_info = """
    'defcon.info.threshold': 'How many users must join within 1 minute to trigger the shield.',
    'defcon.info.action': 'What to do with new users during an attack:\\n• Read-Only: Cannot send messages.\\n• Strict: Cannot send media/links.\\n• Captcha: Must solve captcha.',
    'ai.info.mode': 'How AI handles violations:\\n• Quarantine: Sends message to moderators for review.\\n• Auto-ban: Instantly bans the user.',
    'ai.info.log': 'ID of a private channel/group where the bot will send Quarantine cards. Moderators can vote inline. If empty, bot PMs moderators.',
"""
text = text.replace("'ai.log_channel.desc': 'Channel/Group ID for Quarantine cards to vote on',", "'ai.log_channel.desc': 'Channel/Group ID for Quarantine cards to vote on'," + en_info)

ru_info = """
    'defcon.info.threshold': 'Сколько новых участников должно зайти за 1 минуту, чтобы активировалась защита.',
    'defcon.info.action': 'Что делать с новичками во время атаки:\\n• Read-Only: Запрет писать.\\n• Strict: Запрет медиа/ссылок.\\n• Капча: Проверка капчей.',
    'ai.info.mode': 'Реакция ИИ на спам:\\n• Карантин: Отправляет сообщение модераторам на проверку.\\n• Авто-бан: Сразу блокирует нарушителя.',
    'ai.info.log': 'ID приватного канала или группы, куда бот будет присылать сообщения из Карантина. Модераторы смогут голосовать прямо там. Если пусто — бот пишет модераторам в личку.',
"""
text = text.replace("'ai.log_channel.desc': 'ID канала/группы для отправки карточек Quarantine на голосование',", "'ai.log_channel.desc': 'ID канала/группы для отправки карточек Quarantine на голосование'," + ru_info)

uk_info = """
    'defcon.info.threshold': 'Скільки нових учасників має зайти за 1 хвилину, щоб активувався захист.',
    'defcon.info.action': 'Що робити з новачками під час атаки:\\n• Read-Only: Заборона писати.\\n• Strict: Заборона медіа/посилань.\\n• Капча: Перевірка капчею.',
    'ai.info.mode': 'Реакція ШІ на спам:\\n• Карантин: Відправляє повідомлення модераторам на перевірку.\\n• Авто-бан: Одразу блокує порушника.',
    'ai.info.log': 'ID приватного каналу або групи, куди бот буде надсилати повідомлення з Карантину. Модератори зможуть голосувати прямо там. Якщо порожньо — бот пише модераторам в особисті.',
"""
text = text.replace("'ai.log_channel.desc': 'ID каналу/групи для відправки карток Quarantine на голосування',", "'ai.log_channel.desc': 'ID каналу/групи для відправки карток Quarantine на голосування'," + uk_info)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

