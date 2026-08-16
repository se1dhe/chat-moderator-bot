// Flat i18n dicts for the Mini App. EN is canonical; RU/UK mirror it.
export const EN = {
  'app.title': 'RedQueen Security',
  'app.subtitle': 'Defense console',
  'common.on': 'On',
  'common.off': 'Off',
  'common.save': 'Save',
  'common.saved': 'Saved',
  'common.saving': 'Saving…',
  'common.cancel': 'Cancel',
  'common.add': 'Add',
  'common.remove': 'Remove',
  'common.loading': 'Loading…',
  'common.error': 'Something went wrong',
  'common.retry': 'Retry',
  'common.seconds': 'sec',
  'common.minutes': 'min',
  'common.none': 'None',
  'common.back': 'Back',

  'chats.title': 'Your chats',
  'chats.subtitle': 'Chats where you are an administrator',
  'chats.empty': 'No chats yet. Add RedQueen to a group and grant admin rights.',
  'chats.group': 'Group',
  'chats.channel': 'Channel',
  'chats.supergroup': 'Group',

  'nav.dashboard': 'Overview',
  'nav.quarantine': 'Quarantine',
  'nav.audit': 'Audit',
  'nav.stats': 'Stats',

  'dash.protection': 'Protection',
  'dash.content': 'Content & flood',
  'dash.intelligence': 'Intelligence',
  'dash.enabled': 'Active',
  'dash.disabled': 'Off',

  'sec.captcha': 'Captcha',
  'sec.captcha.desc': 'Verify newcomers before they can speak',
  'sec.antiflood': 'Antiflood',
  'sec.antiflood.desc': 'Throttle message bursts',
  'sec.filters': 'Content filters',
  'sec.filters.desc': 'Banned words, links, media',
  'sec.modes': 'Modes',
  'sec.modes.desc': 'Night, silent and slow mode',
  'sec.ai': 'AI moderation',
  'sec.ai.desc': 'Explainable quarantine & auto-actions',
  'sec.raid': 'Raid shield',
  'sec.raid.desc': 'Auto-lock on coordinated join surges',
  'sec.warns': 'Warnings',
  'sec.warns.desc': 'Limit and auto-action',
  'sec.exempt': 'Exemptions',
  'sec.exempt.desc': 'Members bypassing automation',

  'captcha.enabled': 'Require captcha on join',
  'captcha.mode': 'Challenge type',
  'captcha.mode.button': 'Button',
  'captcha.mode.math': 'Math',
  'captcha.timeout': 'Timeout',

  'antiflood.enabled': 'Enable antiflood',
  'antiflood.limit': 'Messages',
  'antiflood.window': 'Per window',
  'antiflood.action': 'Action',
  'antiflood.muteSeconds': 'Mute duration',

  'filters.words': 'Banned words',
  'filters.wordsPlaceholder': 'Add a word or phrase',
  'filters.links': 'Block links',
  'filters.forwards': 'Block forwards',
  'filters.mentions': 'Block @mentions',
  'filters.media': 'Blocked media',
  'media.sticker': 'Stickers',
  'media.animation': 'GIFs',
  'media.voice': 'Voice',
  'media.video_note': 'Video notes',

  'modes.night': 'Night mode',
  'modes.nightRange': 'Active hours (UTC)',
  'modes.silent': 'Silent mode',
  'modes.silentDesc': 'Delete every non-admin message',
  'modes.slow': 'Slow mode',
  'modes.slowDesc': 'Min seconds between messages per member',

  'ai.mode': 'Mode',
  'ai.mode.off': 'Off',
  'ai.mode.quarantine': 'Quarantine',
  'ai.mode.autoban': 'Auto-ban',
  'ai.threshold': 'Default confidence',
  'ai.perCategory': 'Per-category thresholds',
  'ai.maxPerMinute': 'Max AI checks / min',
  'cat.spam': 'Spam',
  'cat.scam': 'Scam',
  'cat.toxicity': 'Toxicity',
  'cat.nsfw': 'NSFW',
  'cat.flood': 'Flood',

  'raid.enabled': 'Enable raid shield',
  'raid.threshold': 'Join threshold',
  'raid.window': 'Window',
  'raid.lock': 'Lock duration',
  'raid.locked': 'Chat is locked now',
  'raid.unlock': 'Unlock now',

  'warns.limit': 'Warnings before action',
  'warns.action': 'Action at limit',
  'action.mute': 'Mute',
  'action.kick': 'Kick',
  'action.ban': 'Ban',

  'exempt.empty': 'No exemptions',
  'exempt.add': 'Add user ID',

  'quar.title': 'Quarantine queue',
  'quar.empty': 'Queue is clear. Nothing awaiting review.',
  'quar.from': 'User',
  'quar.confidence': 'confidence',
  'quar.approve': 'Approve',
  'quar.ban': 'Ban',
  'quar.rule': 'Rule',

  'audit.title': 'Audit log',
  'audit.empty': 'No actions logged yet.',

  'stats.title': 'Statistics',
  'stats.actions': 'Actions',
  'stats.pending': 'Pending quarantine',
  'stats.total': 'Total actions',
  'stats.empty': 'No data yet.',

  'pro.badge': 'PRO',
  'pro.active': 'Pro active',
  'pro.until': 'until {date}',
  'pro.free': 'Free plan',
  'pro.upgrade': 'Upgrade to Pro',
  'pro.pitch': 'AI auto-ban · Raid shield · Advanced analytics',
  'pro.price': '{stars} ⭐ / {days} days',
  'pro.opening': 'Opening payment…',
  'pro.thanks': 'Pro activated. Thank you!',
  'pro.locked': 'Pro feature',
}

const RU = {
  'app.subtitle': 'Консоль защиты',
  'common.on': 'Вкл', 'common.off': 'Выкл', 'common.save': 'Сохранить', 'common.saved': 'Сохранено',
  'common.saving': 'Сохранение…', 'common.cancel': 'Отмена', 'common.add': 'Добавить',
  'common.remove': 'Удалить', 'common.loading': 'Загрузка…', 'common.error': 'Что-то пошло не так',
  'common.retry': 'Повторить', 'common.seconds': 'сек', 'common.minutes': 'мин',
  'common.none': 'Нет', 'common.back': 'Назад',

  'chats.title': 'Ваши чаты', 'chats.subtitle': 'Чаты, где вы администратор',
  'chats.empty': 'Пока нет чатов. Добавьте RedQueen в группу и выдайте права админа.',
  'chats.group': 'Группа', 'chats.channel': 'Канал', 'chats.supergroup': 'Группа',

  'nav.dashboard': 'Обзор', 'nav.quarantine': 'Карантин', 'nav.audit': 'Аудит', 'nav.stats': 'Статистика',

  'dash.protection': 'Защита', 'dash.content': 'Контент и флуд', 'dash.intelligence': 'Интеллект',
  'dash.enabled': 'Активно', 'dash.disabled': 'Выкл',

  'sec.captcha': 'Капча', 'sec.captcha.desc': 'Проверка новичков до первого сообщения',
  'sec.antiflood': 'Антифлуд', 'sec.antiflood.desc': 'Сдерживание всплесков сообщений',
  'sec.filters': 'Фильтры контента', 'sec.filters.desc': 'Слова, ссылки, медиа',
  'sec.modes': 'Режимы', 'sec.modes.desc': 'Ночной, тихий и медленный режим',
  'sec.ai': 'AI-модерация', 'sec.ai.desc': 'Объяснимый карантин и авто-действия',
  'sec.raid': 'Raid shield', 'sec.raid.desc': 'Авто-лок при наплыве',
  'sec.warns': 'Предупреждения', 'sec.warns.desc': 'Лимит и авто-действие',
  'sec.exempt': 'Исключения', 'sec.exempt.desc': 'Кто обходит автоматику',

  'captcha.enabled': 'Требовать капчу при входе', 'captcha.mode': 'Тип проверки',
  'captcha.mode.button': 'Кнопка', 'captcha.mode.math': 'Пример', 'captcha.timeout': 'Таймаут',

  'antiflood.enabled': 'Включить антифлуд', 'antiflood.limit': 'Сообщений',
  'antiflood.window': 'За период', 'antiflood.action': 'Действие', 'antiflood.muteSeconds': 'Длительность мьюта',

  'filters.words': 'Запрещённые слова', 'filters.wordsPlaceholder': 'Добавить слово или фразу',
  'filters.links': 'Блокировать ссылки', 'filters.forwards': 'Блокировать пересылки',
  'filters.mentions': 'Блокировать @упоминания', 'filters.media': 'Заблокированные медиа',
  'media.sticker': 'Стикеры', 'media.animation': 'GIF', 'media.voice': 'Голосовые', 'media.video_note': 'Кружочки',

  'modes.night': 'Ночной режим', 'modes.nightRange': 'Часы работы (UTC)',
  'modes.silent': 'Тихий режим', 'modes.silentDesc': 'Удалять все сообщения не-админов',
  'modes.slow': 'Медленный режим', 'modes.slowDesc': 'Мин. секунд между сообщениями участника',

  'ai.mode': 'Режим', 'ai.mode.off': 'Выкл', 'ai.mode.quarantine': 'Карантин', 'ai.mode.autoban': 'Авто-бан',
  'ai.threshold': 'Порог по умолчанию', 'ai.perCategory': 'Пороги по категориям',
  'ai.maxPerMinute': 'Макс. AI-проверок / мин',
  'cat.spam': 'Спам', 'cat.scam': 'Скам', 'cat.toxicity': 'Токсичность', 'cat.nsfw': 'NSFW', 'cat.flood': 'Флуд',

  'raid.enabled': 'Включить raid shield', 'raid.threshold': 'Порог входов', 'raid.window': 'Окно',
  'raid.lock': 'Длительность лока', 'raid.locked': 'Чат сейчас заблокирован', 'raid.unlock': 'Разблокировать',

  'warns.limit': 'Предупреждений до действия', 'warns.action': 'Действие при лимите',
  'action.mute': 'Мьют', 'action.kick': 'Кик', 'action.ban': 'Бан',

  'exempt.empty': 'Исключений нет', 'exempt.add': 'Добавить ID пользователя',

  'quar.title': 'Очередь карантина', 'quar.empty': 'Очередь пуста. Ничего на проверку.',
  'quar.from': 'Пользователь', 'quar.confidence': 'уверенность',
  'quar.approve': 'Одобрить', 'quar.ban': 'Бан', 'quar.rule': 'Правило',

  'audit.title': 'Журнал аудита', 'audit.empty': 'Пока нет действий.',

  'stats.title': 'Статистика', 'stats.actions': 'Действия', 'stats.pending': 'В карантине',
  'stats.total': 'Всего действий', 'stats.empty': 'Данных пока нет.',

  'pro.badge': 'PRO', 'pro.active': 'Pro активен', 'pro.until': 'до {date}',
  'pro.free': 'Тариф Free', 'pro.upgrade': 'Улучшить до Pro',
  'pro.pitch': 'AI авто-бан · Raid shield · Расширенная аналитика',
  'pro.price': '{stars} ⭐ / {days} дней', 'pro.opening': 'Открываю оплату…',
  'pro.thanks': 'Pro активирован. Спасибо!', 'pro.locked': 'Функция Pro',
}

const UK = {
  'app.subtitle': 'Консоль захисту',
  'common.on': 'Увімк', 'common.off': 'Вимк', 'common.save': 'Зберегти', 'common.saved': 'Збережено',
  'common.saving': 'Збереження…', 'common.cancel': 'Скасувати', 'common.add': 'Додати',
  'common.remove': 'Видалити', 'common.loading': 'Завантаження…', 'common.error': 'Щось пішло не так',
  'common.retry': 'Повторити', 'common.seconds': 'сек', 'common.minutes': 'хв',
  'common.none': 'Немає', 'common.back': 'Назад',

  'chats.title': 'Ваші чати', 'chats.subtitle': 'Чати, де ви адміністратор',
  'chats.empty': 'Поки немає чатів. Додайте RedQueen у групу та надайте права адміна.',
  'chats.group': 'Група', 'chats.channel': 'Канал', 'chats.supergroup': 'Група',

  'nav.dashboard': 'Огляд', 'nav.quarantine': 'Карантин', 'nav.audit': 'Аудит', 'nav.stats': 'Статистика',

  'dash.protection': 'Захист', 'dash.content': 'Контент і флуд', 'dash.intelligence': 'Інтелект',
  'dash.enabled': 'Активно', 'dash.disabled': 'Вимк',

  'sec.captcha': 'Капча', 'sec.captcha.desc': 'Перевірка новачків до першого повідомлення',
  'sec.antiflood': 'Антифлуд', 'sec.antiflood.desc': 'Стримування сплесків повідомлень',
  'sec.filters': 'Фільтри контенту', 'sec.filters.desc': 'Слова, посилання, медіа',
  'sec.modes': 'Режими', 'sec.modes.desc': 'Нічний, тихий і повільний режим',
  'sec.ai': 'AI-модерація', 'sec.ai.desc': 'Пояснюваний карантин і авто-дії',
  'sec.raid': 'Raid shield', 'sec.raid.desc': 'Авто-лок під час напливу',
  'sec.warns': 'Попередження', 'sec.warns.desc': 'Ліміт і авто-дія',
  'sec.exempt': 'Винятки', 'sec.exempt.desc': 'Хто обходить автоматику',

  'captcha.enabled': 'Вимагати капчу при вході', 'captcha.mode': 'Тип перевірки',
  'captcha.mode.button': 'Кнопка', 'captcha.mode.math': 'Приклад', 'captcha.timeout': 'Таймаут',

  'antiflood.enabled': 'Увімкнути антифлуд', 'antiflood.limit': 'Повідомлень',
  'antiflood.window': 'За період', 'antiflood.action': 'Дія', 'antiflood.muteSeconds': 'Тривалість мʼюту',

  'filters.words': 'Заборонені слова', 'filters.wordsPlaceholder': 'Додати слово або фразу',
  'filters.links': 'Блокувати посилання', 'filters.forwards': 'Блокувати пересилання',
  'filters.mentions': 'Блокувати @згадки', 'filters.media': 'Заблоковані медіа',
  'media.sticker': 'Стікери', 'media.animation': 'GIF', 'media.voice': 'Голосові', 'media.video_note': 'Кружечки',

  'modes.night': 'Нічний режим', 'modes.nightRange': 'Години роботи (UTC)',
  'modes.silent': 'Тихий режим', 'modes.silentDesc': 'Видаляти всі повідомлення не-адмінів',
  'modes.slow': 'Повільний режим', 'modes.slowDesc': 'Мін. секунд між повідомленнями учасника',

  'ai.mode': 'Режим', 'ai.mode.off': 'Вимк', 'ai.mode.quarantine': 'Карантин', 'ai.mode.autoban': 'Авто-бан',
  'ai.threshold': 'Поріг за замовчуванням', 'ai.perCategory': 'Пороги за категоріями',
  'ai.maxPerMinute': 'Макс. AI-перевірок / хв',
  'cat.spam': 'Спам', 'cat.scam': 'Скам', 'cat.toxicity': 'Токсичність', 'cat.nsfw': 'NSFW', 'cat.flood': 'Флуд',

  'raid.enabled': 'Увімкнути raid shield', 'raid.threshold': 'Поріг входів', 'raid.window': 'Вікно',
  'raid.lock': 'Тривалість локу', 'raid.locked': 'Чат зараз заблоковано', 'raid.unlock': 'Розблокувати',

  'warns.limit': 'Попереджень до дії', 'warns.action': 'Дія при ліміті',
  'action.mute': 'Мʼют', 'action.kick': 'Кік', 'action.ban': 'Бан',

  'exempt.empty': 'Винятків немає', 'exempt.add': 'Додати ID користувача',

  'quar.title': 'Черга карантину', 'quar.empty': 'Черга порожня. Нічого на перевірку.',
  'quar.from': 'Користувач', 'quar.confidence': 'впевненість',
  'quar.approve': 'Схвалити', 'quar.ban': 'Бан', 'quar.rule': 'Правило',

  'audit.title': 'Журнал аудиту', 'audit.empty': 'Поки немає дій.',

  'stats.title': 'Статистика', 'stats.actions': 'Дії', 'stats.pending': 'У карантині',
  'stats.total': 'Всього дій', 'stats.empty': 'Даних поки немає.',

  'pro.badge': 'PRO', 'pro.active': 'Pro активний', 'pro.until': 'до {date}',
  'pro.free': 'Тариф Free', 'pro.upgrade': 'Покращити до Pro',
  'pro.pitch': 'AI авто-бан · Raid shield · Розширена аналітика',
  'pro.price': '{stars} ⭐ / {days} днів', 'pro.opening': 'Відкриваю оплату…',
  'pro.thanks': 'Pro активовано. Дякуємо!', 'pro.locked': 'Функція Pro',
}

export const LOCALES = { en: EN, ru: { ...EN, ...RU }, uk: { ...EN, ...UK } }

export function resolveLang(code) {
  const c = (code || 'en').slice(0, 2).toLowerCase()
  return c in LOCALES ? c : 'en'
}
