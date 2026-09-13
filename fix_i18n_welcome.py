import re
with open("webapp/src/i18n/translations.js", "r") as f: text = f.read()

en = """    'sec.welcome': 'Welcome Messages',
    'sec.welcome.desc': 'Greet new members automatically',
    'welcome.text': 'Welcome Message',
    'welcome.text.ph': 'Welcome, {name}! Enjoy the {chat} chat.',
    'welcome.desc': 'Configure a message to greet new members when they join the group. Use {name} and {chat} variables.',"""

ru = """    'sec.welcome': 'Приветствия',
    'sec.welcome.desc': 'Автоматически приветствовать новых участников',
    'welcome.text': 'Текст приветствия',
    'welcome.text.ph': 'Добро пожаловать, {name}! Приятного общения в чате {chat}.',
    'welcome.desc': 'Настройте сообщение, которое бот отправит при входе нового участника. Поддерживаются переменные {name} и {chat}.',"""

uk = """    'sec.welcome': 'Привітання',
    'sec.welcome.desc': 'Автоматично вітати нових учасників',
    'welcome.text': 'Текст привітання',
    'welcome.text.ph': 'Ласкаво просимо, {name}! Приємного спілкування у чаті {chat}.',
    'welcome.desc': 'Налаштуйте повідомлення, яке бот надішле при вході нового учасника. Підтримуються змінні {name} та {chat}.',"""

text = re.sub(r"    'sec.triggers': 'Auto-Replies',", en + "\n    'sec.triggers': 'Auto-Replies',", text)
text = re.sub(r"    'sec.triggers': 'Авто-Ответы',", ru + "\n    'sec.triggers': 'Авто-Ответы',", text)
text = re.sub(r"    'sec.triggers': 'Авто-Відповіді',", uk + "\n    'sec.triggers': 'Авто-Відповіді',", text)

with open("webapp/src/i18n/translations.js", "w") as f: f.write(text)
