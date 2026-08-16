"""RedQueen persona strings (Resident Evil 'Red Queen' voice).

Cold, precise, security-AI tone — but never toxic toward users.
Kept as a flat dict for now; will migrate to per-locale files in M4.
"""
from __future__ import annotations

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
    "/warnlimit N — warnings before auto-action\n\n"
    "Grant me admin rights and disable Privacy Mode so I can see the threat surface."
)

NOT_ADMIN = "⛔ You are not authorized. This protocol requires administrator clearance."
BOT_NOT_ADMIN = (
    "⚠️ I lack administrator rights in this chat. Promote me so I can enforce protocols."
)
REPLY_OR_TARGET_REQUIRED = "Specify a target: reply to a message, or pass a user id / @username."
CANT_ACT_ON_ADMIN = "That member holds administrator clearance. I will not act against them."
PRIVATE_ONLY = "This command runs inside a group or channel, not in a private chat."

BANNED = "\U0001F534 <b>{name}</b> has been terminated (banned)."
KICKED = "\U0001F534 <b>{name}</b> has been removed."
MUTED = "\U0001F507 <b>{name}</b> is silenced{until}."
UNMUTED = "\U0001F509 <b>{name}</b> may speak again."
UNBANNED = "♻️ <b>{name}</b> is unblocked."
WARNED = "⚠️ <b>{name}</b> warned ({count}/{limit}). Reason: {reason}"
WARN_LIMIT_HIT = "\U0001F534 <b>{name}</b> reached the warning limit and has been {action}."
UNWARNED = "<b>{name}</b> — one warning cleared ({count} left)."
NO_WARNS = "<b>{name}</b> has no active warnings."

AI_QUARANTINE_CARD = (
    "\U0001F534 <b>RedQueen flagged a message</b>\n\n"
    "From: <b>{name}</b>\n"
    "Category: <b>{category}</b>  (confidence {score:.0%})\n"
    "Reason: {reason}\n\n"
    "<i>Message held for your decision.</i>"
)
