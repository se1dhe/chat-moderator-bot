"""RedQueen persona strings — Russian."""
from __future__ import annotations

# --- Общее / онбординг ---------------------------------------------------
START = (
    "\U0001F534 <b>RedQueen Security на связи.</b>\n\n"
    "Я — система защиты этого улья. Добавьте меня в группу или канал, выдайте права "
    "администратора — и я не пущу внутрь чужих.\n\n"
    "Команда /help покажет мои протоколы."
)

HELP = (
    "<b>RedQueen — протоколы модерации</b>\n\n"
    "<b>Действия</b> (ответом на сообщение или @username / id):\n"
    "/ban — удалить и заблокировать участника\n"
    "/kick — удалить участника (может вернуться)\n"
    "/mute [время] — ограничить сообщения (напр. <code>/mute 30m</code>)\n"
    "/unmute — снять ограничения\n"
    "/warn [причина] — вынести предупреждение\n"
    "/unwarn — снять последнее предупреждение\n"
    "/unban — разблокировать участника\n"
    "/purge — удалить сообщения от указанного до текущего\n\n"
    "<b>Настройки</b>\n"
    "/settings — протоколы этого чата\n"
    "/lang en|ru|uk — язык этого чата\n"
    "/warnlimit N — число предупреждений до авто-действия\n"
    "/captcha on|off, /captchamode button|math, /captchatimeout N\n"
    "/antiflood on|off N,M — N сообщений за M секунд включает авто-мьют\n"
    "/bannedwords add|remove|list <слово>\n"
    "/blocklinks, /blockforwards, /blockmentions, /blockmedia — on|off\n"
    "/nightmode, /silentmode, /slowmode — синтаксис см. в /settings\n"
    "/exempt add|remove|list <пользователь>\n"
    "/checksetup — проверить мои права и Privacy Mode\n\n"
    "Выдайте мне права администратора и отключите Privacy Mode, чтобы я видела всю "
    "поверхность угрозы."
)

PRO_INVOICE_TITLE = "RedQueen Pro"
PRO_INVOICE_DESC = "Разблокирует AI авто-бан, raid shield и расширенную аналитику для этого чата на {days} дней."
PRO_INVOICE_LABEL = "RedQueen Pro · {days} дней"
PRO_CMD_GROUP_ONLY = "Выполните /pro в группе или канале, который хотите улучшить."
PRO_ALREADY = "⭐ У этого чата уже есть Pro — активен до {until}. Новая оплата продлит его."
PRO_OFFER = "Улучшить этот чат до <b>RedQueen Pro</b> ({stars} ⭐ / {days} дней): AI авто-бан, raid shield, расширенная аналитика."
PRO_ACTIVATED = "⭐ <b>Pro активирован</b> для этого чата до {until}. Спасибо."
SUB_STATUS_PRO = "Тариф: <b>Pro</b> · активен до {until}."
SUB_STATUS_FREE = "Тариф: <b>Free</b>. Команда /pro разблокирует AI авто-бан, raid shield и аналитику."
PRO_REQUIRED = "🔒 Это функция Pro. Используйте /pro, чтобы улучшить этот чат."

PANEL_BUTTON = "🛡 Открыть панель управления"
PANEL_PROMPT = "Откройте консоль RedQueen для управления этим ульем:"
PANEL_UNCONFIGURED = "URL панели управления ещё не настроен. Задайте WEBAPP_URL, чтобы включить его."

NOT_ADMIN = "⛔ Доступ запрещён. Этот протокол требует прав администратора."
BOT_NOT_ADMIN = "⚠️ У меня нет прав администратора в этом чате. Повысьте меня, чтобы я могла применять протоколы."
REPLY_OR_TARGET_REQUIRED = "Укажите цель: ответьте на сообщение или передайте id / @username."
CANT_ACT_ON_ADMIN = "У этого участника права администратора. Я не буду действовать против него."
PRIVATE_ONLY = "Эта команда работает в группе или канале, не в личных сообщениях."

ONBOARDING_WELCOME = (
    "\U0001F534 <b>RedQueen Security активна в {chat}.</b>\n"
    "Права администратора подтверждены. Все системы вооружены.\n\n"
    "Остался один ручной шаг: отключите <b>Privacy Mode</b> через "
    "@BotFather → /setprivacy → Disable, чтобы я видела полный поток сообщений. "
    "В любой момент можно проверить статус командой /checksetup."
)
ONBOARDING_MISSING_RIGHTS = (
    "⚠️ <b>Недостаточно прав в {chat}.</b>\n"
    "Выдайте мне следующие права: {missing}.\n"
    "После этого выполните /checksetup."
)
CHECKSETUP_OK = (
    "✅ Права администратора: подтверждены.\n"
    "Напоминание: Privacy Mode нужно отключить вручную через "
    "@BotFather → /setprivacy → Disable — API не позволяет проверить этот статус автоматически."
)
CHECKSETUP_MISSING_RIGHTS = "⚠️ Не хватает прав: {missing}. Выдайте их и выполните /checksetup ещё раз."

# --- Модерация --------------------------------------------------------------
BANNED = "\U0001F534 <b>{name}</b> ликвидирован(а) (бан){until}."
KICKED = "\U0001F534 <b>{name}</b> удалён(а) из чата."
MUTED = "\U0001F507 <b>{name}</b> заглушён(а){until}."
UNMUTED = "\U0001F509 <b>{name}</b> снова может говорить."
UNBANNED = "♻️ <b>{name}</b> разблокирован(а)."
WARNED = "⚠️ <b>{name}</b> получил(а) предупреждение ({count}/{limit}). Причина: {reason}"
WARN_LIMIT_HIT = "\U0001F534 <b>{name}</b> достиг(ла) лимита предупреждений и был(а) {action}."
UNWARNED = "<b>{name}</b> — одно предупреждение снято (осталось {count})."
NO_WARNS = "У <b>{name}</b> нет активных предупреждений."
ACTION_REASON = " · Причина: {reason}"
ADMIN_ACTION_BY = " · инициатор: {actor}"
PURGE_NEED_REPLY = "Ответьте на первое сообщение, с которого нужно начать очистку."
PURGED = "\U0001F534 Удалено сообщений: {count}."
TRUST_SCORE = "Уровень доверия <b>{name}</b>: <b>{score}</b>/100"

# --- AI-проверка -----------------------------------------------------------
AI_QUARANTINE_CARD = (
    "\U0001F534 <b>RedQueen пометила сообщение</b>\n\n"
    "От: <b>{name}</b>\n"
    "Категория: <b>{category}</b>  (уверенность {score:.0%})\n"
    "Причина: {reason}\n\n"
    "<i>Сообщение удержано до вашего решения.</i>"
)
AI_CONFIRMED_BAN = "\U0001F534 Подтверждено. Участник забанен."
AI_APPROVED = "✅ Одобрено. Действий не требуется."
AI_RULE_BUTTON = "\U0001F4CF Правило"
AI_RULE_CREATED = "\U0001F4CF Правило создано — впредь такие сообщения будут отловлены автоматически."
AI_VERDICT_NOT_FOUND = "Вердикт не найден."
AI_ADMIN_REQUIRED = "Требуются права администратора."

# --- Настройки --------------------------------------------------------------
SETTINGS_CARD = (
    "<b>Протоколы RedQueen для этого чата</b>\n"
    "• Язык: <b>{lang}</b>\n"
    "• Лимит предупреждений: <b>{warn_limit}</b> → <b>{warn_action}</b>\n"
    "• Режим AI: <b>{ai_mode}</b> (порог {ai_threshold}%)\n"
    "• Капча: <b>{captcha}</b>\n"
    "• Антифлуд: <b>{antiflood}</b>\n"
    "• Raid shield: <b>{raid_shield}</b>\n"
    "• Запрещённые слова: <b>{banned_words_count}</b>\n"
    "• Блок ссылок/пересылок/упоминаний: <b>{block_links}/{block_forwards}/{block_mentions}</b>\n"
    "• Ночной / тихий / медленный режим: <b>{night_mode}/{silent_mode}/{slow_mode}</b>\n\n"
    "Полный список команд: /help"
)
WARNLIMIT_USAGE = "Использование: /warnlimit N (напр. /warnlimit 3)"
WARNLIMIT_SET = "Лимит предупреждений установлен: <b>{limit}</b>."
WARNACTION_USAGE = "Использование: /warnaction mute|kick|ban"
WARNACTION_SET = "Действие при лимите установлено: <b>{action}</b>."
AIMODE_USAGE = "Использование: /aimode off|quarantine|autoban"
AIMODE_SET = "Режим AI-модерации установлен: <b>{mode}</b>."
LANG_USAGE = "Использование: /lang en|ru|uk"
LANG_SET = "Язык установлен: <b>{lang}</b>."

# --- Капча -----------------------------------------------------------------
CAPTCHA_USAGE = "Использование: /captcha on|off"
CAPTCHA_ENABLED = "Проверка капчей <b>включена</b>."
CAPTCHA_DISABLED = "Проверка капчей <b>отключена</b>."
CAPTCHA_MODE_USAGE = "Использование: /captchamode button|math"
CAPTCHA_MODE_SET = "Режим капчи установлен: <b>{mode}</b>."
CAPTCHA_TIMEOUT_USAGE = "Использование: /captchatimeout СЕКУНДЫ (60-1800)"
CAPTCHA_TIMEOUT_SET = "Таймаут капчи установлен: <b>{seconds}с</b>."
CAPTCHA_BUTTON_LABEL = "\U0001F513 Я не машина"
CAPTCHA_BUTTON_PROMPT = (
    "\U0001F534 <b>{name}</b>, требуется проверка.\n"
    "Подтвердите, что вы не машина, в течение <b>{minutes} мин</b>, иначе будете удалены."
)
CAPTCHA_MATH_PROMPT = (
    "\U0001F534 <b>{name}</b>, требуется проверка.\n"
    "Решите, чтобы пройти: <b>{a} + {b} = ?</b>\n"
    "Нажмите верный ответ в течение <b>{minutes} мин</b>, иначе будете удалены."
)
CAPTCHA_PASSED = "✅ <b>{name}</b> прошёл(ла) проверку. Добро пожаловать в улей."
CAPTCHA_FAILED_KICK = "\U0001F534 <b>{name}</b> не прошёл(ла) проверку и был(а) удалён(а)."
CAPTCHA_NOT_YOURS = "Это испытание не для вас."
CAPTCHA_WRONG_ANSWER = "Неверно. Попробуйте ещё раз."
CAPTCHA_JOINREQUEST_DM = (
    "\U0001F534 <b>RedQueen Security</b> — для вступления в <b>{chat}</b> требуется проверка.\n\n"
    "{challenge}"
)
CAPTCHA_JOINREQUEST_APPROVED = "✅ Проверка пройдена. Заявка на вступление в <b>{chat}</b> одобрена."
CAPTCHA_JOINREQUEST_DECLINED = "\U0001F534 Проверка провалена или истекла. Заявка на вступление в <b>{chat}</b> отклонена."

# --- Антифлуд -----------------------------------------------------------------
ANTIFLOOD_USAGE = "Использование: /antiflood on|off N M (N сообщений за M секунд, напр. /antiflood on 5 10)"
ANTIFLOOD_SET = "Антифлуд: <b>{limit} сообщ. / {window}с</b>, действие <b>{action}</b>."
ANTIFLOOD_ENABLED = "Антифлуд <b>включён</b>."
ANTIFLOOD_DISABLED = "Антифлуд <b>отключён</b>."
ANTIFLOOD_TRIGGERED = "\U0001F534 <b>{name}</b> превысил(а) порог флуда и был(а) {action}."

# --- Raid shield -----------------------------------------------------------------
RAIDSHIELD_USAGE = "Использование: /raidshield on|off"
RAIDSHIELD_ENABLED = "Raid shield <b>включён</b>."
RAIDSHIELD_DISABLED = "Raid shield <b>отключён</b>."
RAIDCONFIG_USAGE = "Использование: /raidconfig ПОРОГ ОКНО_СЕК (напр. /raidconfig 5 30)"
RAIDCONFIG_SET = "Raid shield: <b>{threshold} входов / {window}с</b> запускают блокировку."
RAID_LOCKED = (
    "\U0001F6A8 <b>Обнаружен наплыв.</b> {count} входов за короткое окно — чат "
    "заблокирован на <b>{minutes} мин</b>. Сообщения не-админов будут удаляться. "
    "/unlock — снять раньше."
)
RAID_UNLOCKED = "\U0001F513 Чат разблокирован."

# --- Фильтры контента -----------------------------------------------------------
BANNEDWORDS_USAGE = "Использование: /bannedwords add|remove|list <слово>"
BANNEDWORDS_ADDED = "Добавлено в запрещённые слова: <b>{word}</b>."
BANNEDWORDS_REMOVED = "Удалено из запрещённых слов: <b>{word}</b>."
BANNEDWORDS_LIST = "<b>Запрещённые слова</b> ({count}):\n{words}"
BANNEDWORDS_EMPTY = "Запрещённые слова не настроены."
BLOCKLINKS_USAGE = "Использование: /blocklinks on|off"
BLOCKLINKS_SET = "Блокировка ссылок <b>{state}</b>."
BLOCKFORWARDS_USAGE = "Использование: /blockforwards on|off"
BLOCKFORWARDS_SET = "Блокировка пересылок <b>{state}</b>."
BLOCKMENTIONS_USAGE = "Использование: /blockmentions on|off"
BLOCKMENTIONS_SET = "Блокировка упоминаний <b>{state}</b>."
BLOCKMEDIA_USAGE = "Использование: /blockmedia sticker|animation|voice|video_note on|off"
BLOCKMEDIA_SET = "Блокировка медиа-типа <b>{media}</b>: <b>{state}</b>."

# --- Режимы -----------------------------------------------------------------
NIGHTMODE_USAGE = "Использование: /nightmode on|off НАЧАЛО КОНЕЦ (часы 0-23 UTC, напр. /nightmode on 23 7)"
NIGHTMODE_SET = "Ночной режим <b>{state}</b> ({start}:00–{end}:00 UTC)."
SILENTMODE_USAGE = "Использование: /silentmode on|off"
SILENTMODE_SET = "Тихий режим <b>{state}</b>."
SLOWMODE_USAGE = "Использование: /slowmode СЕКУНДЫ (0 — отключить)"
SLOWMODE_SET = "Медленный режим: <b>{seconds}с</b> между сообщениями одного участника."
EXEMPT_USAGE = "Использование: /exempt add|remove|list <id / @username>"
EXEMPT_ADDED = "<b>{name}</b> теперь освобождён(а) от автоматических протоколов."
EXEMPT_REMOVED = "<b>{name}</b> больше не освобождён(а)."
EXEMPT_LIST = "<b>Освобождённые участники</b> ({count}):\n{names}"
EXEMPT_EMPTY = "Исключения не настроены."
