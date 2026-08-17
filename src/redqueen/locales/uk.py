"""RedQueen persona strings — Ukrainian."""
from __future__ import annotations

# --- Загальне / онбординг ---------------------------------------------------
START = (
    "\U0001F534 <b>RedQueen Security на зв'язку.</b>\n\n"
    "Я — система захисту цього вулика. Додайте мене до групи чи каналу, надайте права "
    "адміністратора — і я не впущу чужих.\n\n"
    "Команда /help покаже мої протоколи."
)

HELP = (
    "<b>RedQueen — протоколи модерації</b>\n\n"
    "<b>Дії</b> (відповіддю на повідомлення або @username / id):\n"
    "/ban — видалити та заблокувати учасника\n"
    "/kick — видалити учасника (може повернутись)\n"
    "/mute [час] — обмежити повідомлення (напр. <code>/mute 30m</code>)\n"
    "/unmute — зняти обмеження\n"
    "/warn [причина] — винести попередження\n"
    "/unwarn — зняти останнє попередження\n"
    "/unban — розблокувати учасника\n"
    "/purge — видалити повідомлення від вказаного до поточного\n\n"
    "<b>Налаштування</b>\n"
    "/settings — протоколи цього чату\n"
    "/lang en|ru|uk — мова цього чату\n"
    "/warnlimit N — кількість попереджень до авто-дії\n"
    "/captcha on|off, /captchamode button|math, /captchatimeout N\n"
    "/antiflood on|off N,M — N повідомлень за M секунд вмикає авто-мʼют\n"
    "/bannedwords add|remove|list <слово>\n"
    "/blocklinks, /blockforwards, /blockmentions, /blockmedia — on|off\n"
    "/nightmode, /silentmode, /slowmode — синтаксис у /settings\n"
    "/exempt add|remove|list <користувач>\n"
    "/checksetup — перевірити мої права та Privacy Mode\n\n"
    "Надайте мені права адміністратора та вимкніть Privacy Mode, щоб я бачила всю "
    "поверхню загрози."
)

PRO_INVOICE_TITLE = "RedQueen Pro"
PRO_INVOICE_DESC = "Розблоковує AI авто-бан, raid shield та розширену аналітику для цього чату на {days} днів."
PRO_INVOICE_LABEL = "RedQueen Pro · {days} днів"
PRO_CMD_GROUP_ONLY = "Виконайте /pro у групі або каналі, який хочете покращити."
PRO_ALREADY = "⭐ У цього чату вже є Pro — активний до {until}. Нова оплата продовжить його."
PRO_OFFER = "Покращити цей чат до <b>RedQueen Pro</b> ({stars} ⭐ / {days} днів): AI авто-бан, raid shield, розширена аналітика."
PRO_ACTIVATED = "⭐ <b>Pro активовано</b> для цього чату до {until}. Дякуємо."
SUB_STATUS_PRO = "Тариф: <b>Pro</b> · активний до {until}."
SUB_STATUS_FREE = "Тариф: <b>Free</b>. Команда /pro розблокує AI авто-бан, raid shield та аналітику."
PRO_REQUIRED = "🔒 Це функція Pro. Використайте /pro, щоб покращити цей чат."

PANEL_BUTTON = "🛡 Відкрити панель керування"
PANEL_PROMPT = "Відкрийте консоль RedQueen для керування цим вуликом:"
PANEL_UNCONFIGURED = "URL панелі керування ще не налаштовано. Задайте WEBAPP_URL, щоб увімкнути його."

NOT_ADMIN = "⛔ Доступ заборонено. Цей протокол потребує прав адміністратора."
BOT_NOT_ADMIN = "⚠️ У мене немає прав адміністратора в цьому чаті. Підвищте мене, щоб я могла застосовувати протоколи."
REPLY_OR_TARGET_REQUIRED = "Вкажіть ціль: дайте відповідь на повідомлення або передайте id / @username."
CANT_ACT_ON_ADMIN = "Цей учасник має права адміністратора. Я не діятиму проти нього."
PRIVATE_ONLY = "Ця команда працює в групі чи каналі, не в особистих повідомленнях."

ONBOARDING_WELCOME = (
    "\U0001F534 <b>RedQueen Security активна в {chat}.</b>\n"
    "Права адміністратора підтверджено. Усі системи озброєні.\n\n"
    "Залишився один ручний крок: вимкніть <b>Privacy Mode</b> через "
    "@BotFather → /setprivacy → Disable, щоб я бачила повний потік повідомлень. "
    "Статус можна перевірити командою /checksetup."
)
ONBOARDING_MISSING_RIGHTS = (
    "⚠️ <b>Недостатньо прав у {chat}.</b>\n"
    "Надайте мені такі права: {missing}.\n"
    "Після цього виконайте /checksetup."
)
CHECKSETUP_OK = (
    "✅ Права адміністратора: підтверджено.\n"
    "Нагадування: Privacy Mode потрібно вимкнути вручну через "
    "@BotFather → /setprivacy → Disable — API не дозволяє перевірити цей статус автоматично."
)
CHECKSETUP_MISSING_RIGHTS = "⚠️ Бракує прав: {missing}. Надайте їх і виконайте /checksetup ще раз."

# --- Модерація --------------------------------------------------------------
BANNED = "\U0001F534 <b>{name}</b> ліквідовано (бан)."
KICKED = "\U0001F534 <b>{name}</b> видалено з чату."
MUTED = "\U0001F507 <b>{name}</b> заглушено{until}."
UNMUTED = "\U0001F509 <b>{name}</b> знову може говорити."
UNBANNED = "♻️ <b>{name}</b> розблоковано."
WARNED = "⚠️ <b>{name}</b> отримав(ла) попередження ({count}/{limit}). Причина: {reason}"
WARN_LIMIT_HIT = "\U0001F534 <b>{name}</b> досяг(ла) ліміту попереджень і був(ла) {action}."
UNWARNED = "<b>{name}</b> — одне попередження знято (залишилось {count})."
NO_WARNS = "У <b>{name}</b> немає активних попереджень."
ACTION_REASON = " · Причина: {reason}"
ADMIN_ACTION_BY = " · ініціатор: {actor}"
PURGE_NEED_REPLY = "Дайте відповідь на перше повідомлення, з якого почати очищення."
PURGED = "\U0001F534 Видалено повідомлень: {count}."
TRUST_SCORE = "Рівень довіри <b>{name}</b>: <b>{score}</b>/100"

# --- AI-перевірка -----------------------------------------------------------
AI_QUARANTINE_CARD = (
    "\U0001F534 <b>RedQueen позначила повідомлення</b>\n\n"
    "Від: <b>{name}</b>\n"
    "Категорія: <b>{category}</b>  (впевненість {score:.0%})\n"
    "Причина: {reason}\n\n"
    "<i>Повідомлення утримано до вашого рішення.</i>"
)
AI_CONFIRMED_BAN = "\U0001F534 Підтверджено. Учасника забанено."
AI_APPROVED = "✅ Схвалено. Дій не потрібно."
AI_RULE_BUTTON = "\U0001F4CF Правило"
AI_RULE_CREATED = "\U0001F4CF Правило створено — надалі такі повідомлення ловитимуться автоматично."
AI_VERDICT_NOT_FOUND = "Вердикт не знайдено."
AI_ADMIN_REQUIRED = "Потрібні права адміністратора."

# --- Налаштування --------------------------------------------------------------
SETTINGS_CARD = (
    "<b>Протоколи RedQueen для цього чату</b>\n"
    "• Мова: <b>{lang}</b>\n"
    "• Ліміт попереджень: <b>{warn_limit}</b> → <b>{warn_action}</b>\n"
    "• Режим AI: <b>{ai_mode}</b> (поріг {ai_threshold}%)\n"
    "• Капча: <b>{captcha}</b>\n"
    "• Антифлуд: <b>{antiflood}</b>\n"
    "• Raid shield: <b>{raid_shield}</b>\n"
    "• Заборонені слова: <b>{banned_words_count}</b>\n"
    "• Блок посилань/пересилань/згадок: <b>{block_links}/{block_forwards}/{block_mentions}</b>\n"
    "• Нічний / тихий / повільний режим: <b>{night_mode}/{silent_mode}/{slow_mode}</b>\n\n"
    "Повний список команд: /help"
)
WARNLIMIT_USAGE = "Використання: /warnlimit N (напр. /warnlimit 3)"
WARNLIMIT_SET = "Ліміт попереджень встановлено: <b>{limit}</b>."
WARNACTION_USAGE = "Використання: /warnaction mute|kick|ban"
WARNACTION_SET = "Дію при ліміті встановлено: <b>{action}</b>."
AIMODE_USAGE = "Використання: /aimode off|quarantine|autoban"
AIMODE_SET = "Режим AI-модерації встановлено: <b>{mode}</b>."
LANG_USAGE = "Використання: /lang en|ru|uk"
LANG_SET = "Мову встановлено: <b>{lang}</b>."

# --- Капча -----------------------------------------------------------------
CAPTCHA_USAGE = "Використання: /captcha on|off"
CAPTCHA_ENABLED = "Перевірку капчею <b>увімкнено</b>."
CAPTCHA_DISABLED = "Перевірку капчею <b>вимкнено</b>."
CAPTCHA_MODE_USAGE = "Використання: /captchamode button|math"
CAPTCHA_MODE_SET = "Режим капчі встановлено: <b>{mode}</b>."
CAPTCHA_TIMEOUT_USAGE = "Використання: /captchatimeout СЕКУНДИ (60-1800)"
CAPTCHA_TIMEOUT_SET = "Таймаут капчі встановлено: <b>{seconds}с</b>."
CAPTCHA_BUTTON_LABEL = "\U0001F513 Я не машина"
CAPTCHA_BUTTON_PROMPT = (
    "\U0001F534 <b>{name}</b>, потрібна перевірка.\n"
    "Підтвердіть, що ви не машина, протягом <b>{minutes} хв</b>, інакше вас буде видалено."
)
CAPTCHA_MATH_PROMPT = (
    "\U0001F534 <b>{name}</b>, потрібна перевірка.\n"
    "Розв'яжіть, щоб пройти: <b>{a} + {b} = ?</b>\n"
    "Натисніть правильну відповідь протягом <b>{minutes} хв</b>, інакше вас буде видалено."
)
CAPTCHA_PASSED = "✅ <b>{name}</b> пройшов(ла) перевірку. Ласкаво просимо до вулика."
CAPTCHA_FAILED_KICK = "\U0001F534 <b>{name}</b> не пройшов(ла) перевірку і був(ла) видалений(а)."
CAPTCHA_NOT_YOURS = "Це випробування не для вас."
CAPTCHA_WRONG_ANSWER = "Невірно. Спробуйте ще раз."
CAPTCHA_JOINREQUEST_DM = (
    "\U0001F534 <b>RedQueen Security</b> — для вступу до <b>{chat}</b> потрібна перевірка.\n\n"
    "{challenge}"
)
CAPTCHA_JOINREQUEST_APPROVED = "✅ Перевірку пройдено. Заявку на вступ до <b>{chat}</b> схвалено."
CAPTCHA_JOINREQUEST_DECLINED = "\U0001F534 Перевірка провалена або минув час. Заявку на вступ до <b>{chat}</b> відхилено."

# --- Антифлуд -----------------------------------------------------------------
ANTIFLOOD_USAGE = "Використання: /antiflood on|off N M (N повідомлень за M секунд, напр. /antiflood on 5 10)"
ANTIFLOOD_SET = "Антифлуд: <b>{limit} повід. / {window}с</b>, дія <b>{action}</b>."
ANTIFLOOD_ENABLED = "Антифлуд <b>увімкнено</b>."
ANTIFLOOD_DISABLED = "Антифлуд <b>вимкнено</b>."
ANTIFLOOD_TRIGGERED = "\U0001F534 <b>{name}</b> перевищив(ла) поріг флуду і був(ла) {action}."

# --- Raid shield -----------------------------------------------------------------
RAIDSHIELD_USAGE = "Використання: /raidshield on|off"
RAIDSHIELD_ENABLED = "Raid shield <b>увімкнено</b>."
RAIDSHIELD_DISABLED = "Raid shield <b>вимкнено</b>."
RAIDCONFIG_USAGE = "Використання: /raidconfig ПОРІГ ВІКНО_СЕК (напр. /raidconfig 5 30)"
RAIDCONFIG_SET = "Raid shield: <b>{threshold} входів / {window}с</b> запускають блокування."
RAID_LOCKED = (
    "\U0001F6A8 <b>Виявлено наплив.</b> {count} входів за коротке вікно — чат "
    "заблоковано на <b>{minutes} хв</b>. Повідомлення не-адмінів видалятимуться. "
    "/unlock — зняти раніше."
)
RAID_UNLOCKED = "\U0001F513 Чат розблоковано."

# --- Фільтри контенту -----------------------------------------------------------
BANNEDWORDS_USAGE = "Використання: /bannedwords add|remove|list <слово>"
BANNEDWORDS_ADDED = "Додано до заборонених слів: <b>{word}</b>."
BANNEDWORDS_REMOVED = "Видалено із заборонених слів: <b>{word}</b>."
BANNEDWORDS_LIST = "<b>Заборонені слова</b> ({count}):\n{words}"
BANNEDWORDS_EMPTY = "Заборонені слова не налаштовані."
BLOCKLINKS_USAGE = "Використання: /blocklinks on|off"
BLOCKLINKS_SET = "Блокування посилань <b>{state}</b>."
BLOCKFORWARDS_USAGE = "Використання: /blockforwards on|off"
BLOCKFORWARDS_SET = "Блокування пересилань <b>{state}</b>."
BLOCKMENTIONS_USAGE = "Використання: /blockmentions on|off"
BLOCKMENTIONS_SET = "Блокування згадок <b>{state}</b>."
BLOCKMEDIA_USAGE = "Використання: /blockmedia sticker|animation|voice|video_note on|off"
BLOCKMEDIA_SET = "Блокування типу медіа <b>{media}</b>: <b>{state}</b>."

# --- Режими -----------------------------------------------------------------
NIGHTMODE_USAGE = "Використання: /nightmode on|off ПОЧАТОК КІНЕЦЬ (години 0-23 UTC, напр. /nightmode on 23 7)"
NIGHTMODE_SET = "Нічний режим <b>{state}</b> ({start}:00–{end}:00 UTC)."
SILENTMODE_USAGE = "Використання: /silentmode on|off"
SILENTMODE_SET = "Тихий режим <b>{state}</b>."
SLOWMODE_USAGE = "Використання: /slowmode СЕКУНДИ (0 — вимкнути)"
SLOWMODE_SET = "Повільний режим: <b>{seconds}с</b> між повідомленнями одного учасника."
EXEMPT_USAGE = "Використання: /exempt add|remove|list <id / @username>"
EXEMPT_ADDED = "<b>{name}</b> тепер звільнений(а) від автоматичних протоколів."
EXEMPT_REMOVED = "<b>{name}</b> більше не звільнений(а)."
EXEMPT_LIST = "<b>Звільнені учасники</b> ({count}):\n{names}"
EXEMPT_EMPTY = "Винятки не налаштовані."
