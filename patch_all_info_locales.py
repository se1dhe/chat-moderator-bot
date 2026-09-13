with open('webapp/src/i18n/translations.ts', 'r') as f:
    text = f.read()

en_info = """
    'captcha.info.timeout': 'How much time (in seconds) the user has to pass the verification. If they fail, they will be kicked.',
    'antiflood.info.messages': 'How many consecutive messages a user can send within the time window.',
    'antiflood.info.window': 'The time window (in seconds) for the message limit.',
    'filters.info.links': 'Automatically delete any links sent by regular users.',
    'filters.info.forwards': 'Prevent users from forwarding messages from other chats/channels.',
    'filters.info.badwords': 'Delete messages containing profanity or insults.',
    'modes.info.readonly': 'Nobody except admins will be able to write in the chat.',
    'modes.info.slowmode': 'Restricts how often a single user can send messages.',
"""

ru_info = """
    'captcha.info.timeout': 'Сколько времени (в секундах) есть у пользователя, чтобы пройти проверку. Если не успеет — будет исключен.',
    'antiflood.info.messages': 'Сколько сообщений подряд можно написать за отведенное время.',
    'antiflood.info.window': 'Окно времени (в секундах), за которое считается лимит сообщений.',
    'filters.info.links': 'Автоматически удалять любые ссылки, кроме тех, что скинули администраторы.',
    'filters.info.forwards': 'Запретить пересылку сообщений из других каналов и чатов.',
    'filters.info.badwords': 'Удалять сообщения, содержащие нецензурную лексику или оскорбления.',
    'modes.info.readonly': 'Никто кроме админов не сможет писать в чат. Режим "Только чтение".',
    'modes.info.slowmode': 'Задержка между отправкой сообщений (ограничивает флуд).',
"""

uk_info = """
    'captcha.info.timeout': 'Скільки часу (у секундах) є у користувача, щоб пройти перевірку. Якщо не встигне — буде виключений.',
    'antiflood.info.messages': 'Скільки повідомлень поспіль можна написати за відведений час.',
    'antiflood.info.window': 'Вікно часу (в секундах), за яке рахується ліміт повідомлень.',
    'filters.info.links': 'Автоматично видаляти будь-які посилання, крім тих, що надіслали адміністратори.',
    'filters.info.forwards': 'Заборонити пересилання повідомлень з інших каналів і чатів.',
    'filters.info.badwords': 'Видаляти повідомлення, що містять нецензурну лексику або образи.',
    'modes.info.readonly': 'Ніхто крім адмінів не зможе писати в чат. Режим "Тільки читання".',
    'modes.info.slowmode': 'Затримка між відправкою повідомлень (обмежує флуд).',
"""

text = text.replace("'ai.info.log': 'ID of a private channel/group where the bot will send Quarantine cards. Moderators can vote inline. If empty, bot PMs moderators.',", "'ai.info.log': 'ID of a private channel/group where the bot will send Quarantine cards. Moderators can vote inline. If empty, bot PMs moderators.'," + en_info)

text = text.replace("'ai.info.log': 'ID приватного канала или группы, куда бот будет присылать сообщения из Карантина. Модераторы смогут голосовать прямо там. Если пусто — бот пишет модераторам в личку.',", "'ai.info.log': 'ID приватного канала или группы, куда бот будет присылать сообщения из Карантина. Модераторы смогут голосовать прямо там. Если пусто — бот пишет модераторам в личку.'," + ru_info)

text = text.replace("'ai.info.log': 'ID приватного каналу або групи, куди бот буде надсилати повідомлення з Карантину. Модератори зможуть голосувати прямо там. Якщо порожньо — бот пише модераторам в особисті.',", "'ai.info.log': 'ID приватного каналу або групи, куди бот буде надсилати повідомлення з Карантину. Модератори зможуть голосувати прямо там. Якщо порожньо — бот пише модераторам в особисті.'," + uk_info)

with open('webapp/src/i18n/translations.ts', 'w') as f:
    f.write(text)

