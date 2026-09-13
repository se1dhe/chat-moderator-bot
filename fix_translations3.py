with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

text = text.replace("'sec.overview': 'Обзор',", "'dashboard.ai_summary': 'Умный Дайджест',\n      'dashboard.ai_summary.desc': 'Сгенерировать краткую выжимку из последних 300 сообщений.',\n      'dashboard.ai_summary.btn': 'Создать Дайджест',\n      'dashboard.ai_summary.loading': 'Анализирую историю чата...',\n      'sec.overview': 'Обзор',")
text = text.replace("'sec.overview': 'Overview',", "'dashboard.ai_summary': 'AI Digest',\n      'dashboard.ai_summary.desc': 'Generate a short summary from the last 300 messages.',\n      'dashboard.ai_summary.btn': 'Generate Digest',\n      'dashboard.ai_summary.loading': 'Analyzing chat history...',\n      'sec.overview': 'Overview',")
text = text.replace("'sec.overview': 'Огляд',", "'dashboard.ai_summary': 'Розумний Дайджест',\n      'dashboard.ai_summary.desc': 'Згенерувати коротку витримку з останніх 300 повідомлень.',\n      'dashboard.ai_summary.btn': 'Створити Дайджест',\n      'dashboard.ai_summary.loading': 'Аналізую історію чату...',\n      'sec.overview': 'Огляд',")

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)
