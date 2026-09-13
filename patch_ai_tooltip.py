with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

text = text.replace(
    'Реакция ИИ на спам:\\n• Карантин: Отправляет сообщение модераторам на проверку.\\n• Авто-бан: Сразу блокирует нарушителя.',
    'Реакция ИИ на спам:\\n• Карантин: Сохраняет в Карантин (внутри TMA) на проверку.\\n• Авто-бан: Сразу блокирует нарушителя.'
)
text = text.replace(
    'How AI handles violations:\\n• Quarantine: Sends message to moderators for review.\\n• Auto-ban: Instantly bans the user.',
    'How AI handles violations:\\n• Quarantine: Saves to TMA Quarantine tab for review.\\n• Auto-ban: Instantly bans the user.'
)
text = text.replace(
    'Реакція ШІ на спам:\\n• Карантин: Відправляє повідомлення модераторам на перевірку.\\n• Авто-бан: Одразу блокує порушника.',
    'Реакція ШІ на спам:\\n• Карантин: Зберігає в Карантин (всередині TMA) на перевірку.\\n• Авто-бан: Одразу блокує порушника.'
)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)
