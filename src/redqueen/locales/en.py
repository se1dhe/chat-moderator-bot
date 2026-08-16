"""RedQueen persona strings — English (canonical; other locales fall back here)."""
from __future__ import annotations

# --- Common / onboarding ---------------------------------------------------
START = (
    "\U0001F534 <b>RedQueen Security online.</b>\n\n"
    "I am the defense system for this hive. Add me to a group or channel, grant me "
    "administrator rights, and I will keep intruders out.\n\n"
    "Use /help to see my protocols."
)

HELP = (
    "<b>RedQueen — moderation protocols</b>\n\n"
    "<b>Actions</b> (reply to a user or pass @username / id):\n"
    "/ban — remove and block a member\n"
    "/kick — remove a member (can rejoin)\n"
    "/mute [time] — restrict messages (e.g. <code>/mute 30m</code>)\n"
    "/unmute — lift restrictions\n"
    "/warn [reason] — issue a warning\n"
    "/unwarn — remove the last warning\n"
    "/unban — unblock a member\n"
    "/purge — delete messages from replied one to now\n\n"
    "<b>Config</b>\n"
    "/settings — show this chat's protocols\n"
    "/lang en|ru|uk — set this chat's language\n"
    "/warnlimit N — warnings before auto-action\n"
    "/captcha on|off, /captchamode button|math, /captchatimeout N\n"
    "/antiflood on|off N,M — N messages per M seconds triggers auto-mute\n"
    "/bannedwords add|remove|list <word>\n"
    "/blocklinks, /blockforwards, /blockmentions, /blockmedia — on|off\n"
    "/nightmode, /silentmode, /slowmode — see /settings for syntax\n"
    "/exempt add|remove|list <user>\n"
    "/checksetup — verify my rights and Privacy Mode\n\n"
    "Grant me admin rights and disable Privacy Mode so I can see the threat surface."
)

NOT_ADMIN = "⛔ You are not authorized. This protocol requires administrator clearance."
BOT_NOT_ADMIN = (
    "⚠️ I lack administrator rights in this chat. Promote me so I can enforce protocols."
)
REPLY_OR_TARGET_REQUIRED = "Specify a target: reply to a message, or pass a user id / @username."
CANT_ACT_ON_ADMIN = "That member holds administrator clearance. I will not act against them."
PRIVATE_ONLY = "This command runs inside a group or channel, not in a private chat."

ONBOARDING_WELCOME = (
    "\U0001F534 <b>RedQueen Security online in {chat}.</b>\n"
    "Administrator clearance confirmed. All systems armed.\n\n"
    "One manual step remains: disable <b>Privacy Mode</b> via "
    "@BotFather → /setprivacy → Disable, so I can see the full message stream. "
    "Run /checksetup any time to re-verify."
)
ONBOARDING_MISSING_RIGHTS = (
    "⚠️ <b>Insufficient clearance in {chat}.</b>\n"
    "Grant me these rights to operate: {missing}.\n"
    "Run /checksetup once you have."
)
CHECKSETUP_OK = (
    "✅ Administrator rights: granted.\n"
    "Reminder: Privacy Mode must be disabled manually via "
    "@BotFather → /setprivacy → Disable — I cannot verify that status via the API."
)
CHECKSETUP_MISSING_RIGHTS = "⚠️ Missing rights: {missing}. Grant them, then run /checksetup again."

# --- Moderation --------------------------------------------------------------
BANNED = "\U0001F534 <b>{name}</b> has been terminated (banned)."
KICKED = "\U0001F534 <b>{name}</b> has been removed."
MUTED = "\U0001F507 <b>{name}</b> is silenced{until}."
UNMUTED = "\U0001F509 <b>{name}</b> may speak again."
UNBANNED = "♻️ <b>{name}</b> is unblocked."
WARNED = "⚠️ <b>{name}</b> warned ({count}/{limit}). Reason: {reason}"
WARN_LIMIT_HIT = "\U0001F534 <b>{name}</b> reached the warning limit and has been {action}."
UNWARNED = "<b>{name}</b> — one warning cleared ({count} left)."
NO_WARNS = "<b>{name}</b> has no active warnings."
PURGE_NEED_REPLY = "Reply to the first message you want to purge from."
PURGED = "\U0001F534 Purged {count} messages."
TRUST_SCORE = "<b>{name}</b> trust score: <b>{score}</b>/100"

# --- AI review -----------------------------------------------------------
AI_QUARANTINE_CARD = (
    "\U0001F534 <b>RedQueen flagged a message</b>\n\n"
    "From: <b>{name}</b>\n"
    "Category: <b>{category}</b>  (confidence {score:.0%})\n"
    "Reason: {reason}\n\n"
    "<i>Message held for your decision.</i>"
)
AI_CONFIRMED_BAN = "\U0001F534 Confirmed. Member banned."
AI_APPROVED = "✅ Approved. No action taken."
AI_RULE_BUTTON = "\U0001F4CF Rule"
AI_RULE_CREATED = "\U0001F4CF Rule created — future matches will be caught automatically."
AI_VERDICT_NOT_FOUND = "Verdict not found."
AI_ADMIN_REQUIRED = "Administrator clearance required."

# --- Settings --------------------------------------------------------------
SETTINGS_CARD = (
    "<b>RedQueen protocols for this chat</b>\n"
    "• Language: <b>{lang}</b>\n"
    "• Warn limit: <b>{warn_limit}</b> → <b>{warn_action}</b>\n"
    "• AI mode: <b>{ai_mode}</b> (threshold {ai_threshold}%)\n"
    "• Captcha: <b>{captcha}</b>\n"
    "• Antiflood: <b>{antiflood}</b>\n"
    "• Raid shield: <b>{raid_shield}</b>\n"
    "• Banned words: <b>{banned_words_count}</b>\n"
    "• Block links/forwards/mentions: <b>{block_links}/{block_forwards}/{block_mentions}</b>\n"
    "• Night / silent / slow mode: <b>{night_mode}/{silent_mode}/{slow_mode}</b>\n\n"
    "Full command list: /help"
)
WARNLIMIT_USAGE = "Usage: /warnlimit N (e.g. /warnlimit 3)"
WARNLIMIT_SET = "Warn limit set to <b>{limit}</b>."
WARNACTION_USAGE = "Usage: /warnaction mute|kick|ban"
WARNACTION_SET = "Warn action set to <b>{action}</b>."
AIMODE_USAGE = "Usage: /aimode off|quarantine|autoban"
AIMODE_SET = "AI moderation mode set to <b>{mode}</b>."
LANG_USAGE = "Usage: /lang en|ru|uk"
LANG_SET = "Language set to <b>{lang}</b>."

# --- Captcha -----------------------------------------------------------------
CAPTCHA_USAGE = "Usage: /captcha on|off"
CAPTCHA_ENABLED = "Captcha screening <b>enabled</b>."
CAPTCHA_DISABLED = "Captcha screening <b>disabled</b>."
CAPTCHA_MODE_USAGE = "Usage: /captchamode button|math"
CAPTCHA_MODE_SET = "Captcha mode set to <b>{mode}</b>."
CAPTCHA_TIMEOUT_USAGE = "Usage: /captchatimeout SECONDS (60-1800)"
CAPTCHA_TIMEOUT_SET = "Captcha timeout set to <b>{seconds}s</b>."
CAPTCHA_BUTTON_LABEL = "\U0001F513 I am not a machine"
CAPTCHA_BUTTON_PROMPT = (
    "\U0001F534 <b>{name}</b>, verification required.\n"
    "Confirm you are not a machine within <b>{minutes} min</b> or you will be removed."
)
CAPTCHA_MATH_PROMPT = (
    "\U0001F534 <b>{name}</b>, verification required.\n"
    "Solve to proceed: <b>{a} + {b} = ?</b>\n"
    "Tap the correct answer within <b>{minutes} min</b> or you will be removed."
)
CAPTCHA_PASSED = "✅ <b>{name}</b> verified. Welcome to the hive."
CAPTCHA_FAILED_KICK = "\U0001F534 <b>{name}</b> failed verification and has been removed."
CAPTCHA_NOT_YOURS = "This challenge is not yours."
CAPTCHA_WRONG_ANSWER = "Incorrect. Try again."
CAPTCHA_JOINREQUEST_DM = (
    "\U0001F534 <b>RedQueen Security</b> — verification required to join <b>{chat}</b>.\n\n"
    "{challenge}"
)
CAPTCHA_JOINREQUEST_APPROVED = "✅ Verified. Your request to join <b>{chat}</b> has been approved."
CAPTCHA_JOINREQUEST_DECLINED = "\U0001F534 Verification failed or expired. Your request to join <b>{chat}</b> was declined."

# --- Antiflood -----------------------------------------------------------------
ANTIFLOOD_USAGE = "Usage: /antiflood on|off N M (N messages per M seconds, e.g. /antiflood on 5 10)"
ANTIFLOOD_SET = "Antiflood set to <b>{limit} msgs / {window}s</b>, action <b>{action}</b>."
ANTIFLOOD_ENABLED = "Antiflood <b>enabled</b>."
ANTIFLOOD_DISABLED = "Antiflood <b>disabled</b>."
ANTIFLOOD_TRIGGERED = "\U0001F534 <b>{name}</b> exceeded the flood threshold and has been {action}."

# --- Raid shield -----------------------------------------------------------------
RAIDSHIELD_USAGE = "Usage: /raidshield on|off"
RAIDSHIELD_ENABLED = "Raid shield <b>enabled</b>."
RAIDSHIELD_DISABLED = "Raid shield <b>disabled</b>."
RAIDCONFIG_USAGE = "Usage: /raidconfig THRESHOLD WINDOW_SECONDS (e.g. /raidconfig 5 30)"
RAIDCONFIG_SET = "Raid shield: <b>{threshold} joins / {window}s</b> triggers a lock."
RAID_LOCKED = (
    "\U0001F6A8 <b>Raid detected.</b> {count} joins in a short window — chat locked "
    "for <b>{minutes} min</b>. Non-admin messages will be removed. /unlock to lift early."
)
RAID_UNLOCKED = "\U0001F513 Chat unlocked."

# --- Content filters -----------------------------------------------------------
BANNEDWORDS_USAGE = "Usage: /bannedwords add|remove|list <word>"
BANNEDWORDS_ADDED = "Added to banned words: <b>{word}</b>."
BANNEDWORDS_REMOVED = "Removed from banned words: <b>{word}</b>."
BANNEDWORDS_LIST = "<b>Banned words</b> ({count}):\n{words}"
BANNEDWORDS_EMPTY = "No banned words configured."
BLOCKLINKS_USAGE = "Usage: /blocklinks on|off"
BLOCKLINKS_SET = "Link blocking <b>{state}</b>."
BLOCKFORWARDS_USAGE = "Usage: /blockforwards on|off"
BLOCKFORWARDS_SET = "Forward blocking <b>{state}</b>."
BLOCKMENTIONS_USAGE = "Usage: /blockmentions on|off"
BLOCKMENTIONS_SET = "Mention blocking <b>{state}</b>."
BLOCKMEDIA_USAGE = "Usage: /blockmedia sticker|animation|voice|video_note on|off"
BLOCKMEDIA_SET = "Media type <b>{media}</b> blocking <b>{state}</b>."

# --- Modes -----------------------------------------------------------------
NIGHTMODE_USAGE = "Usage: /nightmode on|off START END (hours 0-23 UTC, e.g. /nightmode on 23 7)"
NIGHTMODE_SET = "Night mode <b>{state}</b> ({start}:00–{end}:00 UTC)."
SILENTMODE_USAGE = "Usage: /silentmode on|off"
SILENTMODE_SET = "Silent mode <b>{state}</b>."
SLOWMODE_USAGE = "Usage: /slowmode SECONDS (0 to disable)"
SLOWMODE_SET = "Slow mode set to <b>{seconds}s</b> between messages per member."
EXEMPT_USAGE = "Usage: /exempt add|remove|list <user id / @username>"
EXEMPT_ADDED = "<b>{name}</b> is now exempt from automated protocols."
EXEMPT_REMOVED = "<b>{name}</b> is no longer exempt."
EXEMPT_LIST = "<b>Exempt members</b> ({count}):\n{names}"
EXEMPT_EMPTY = "No exemptions configured."
