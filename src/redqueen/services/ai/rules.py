"""Rule-based fallback provider. Works with zero external dependencies.

Deterministic and cheap; used when AI is disabled or Ollama is unreachable. Patterns
cover EN/RU/UK since RedQueen ships trilingual from day one.
"""
from __future__ import annotations

import re

from .provider import AIProvider, Verdict

_SCAM_PATTERNS = [
    r"\bt\.me/\+?\w+",
    r"\b(?:free|бесплатн\w*|безкоштовн\w*)\s+(?:crypto|bitcoin|btc|eth|usdt|crypto|крипт\w*|биткоин\w*)",
    r"\b(?:pump|airdrop|x\d{2,}|guaranteed profit|аирдроп|памп|гарантированн\w* (?:доход|прибыл\w*))\b",
    r"(?:earn|make|заработа\w*|зароби\w*)\s+\$?\d{2,}\s*(?:per|/|в|на)\s*(?:day|week|день|неделю|тиждень)",
    r"\b(?:whatsapp|вотсап|телеграм менеджер)\b.*[\+]?\d{6,}",
    r"\b(?:investment|инвест\w*|інвест\w*)\b.*\b(?:profit|доход|прибут\w*|%)\b",
    r"(?:нужны люди|ищу людей|требуются|набор в команду).*(?:доход|заработ\w*|\$)",
]
_SPAM_HINTS = [
    r"(.)\1{9,}",                    # long char runs (aaaaa...)
    r"(?:https?://\S+\s*){3,}",      # several links crammed together
    # URL shorteners — classic scam-link obfuscation.
    r"\b(?:bit\.ly|tinyurl\.com|cutt\.ly|is\.gd|t\.co|goo\.gl|rb\.gy|shorturl\.at)/\w+",
]
_TOXIC_WORDS = {
    # kept mild; extend per-locale over time
    "idiot", "moron", "scum", "trash", "loser", "retard",
    "идиот", "придурок", "мраз", "быдло", "дебил", "уёбок", "мудак",
    "ідіот", "виродок", "довбень",
}
_URL_RE = re.compile(r"https?://\S+")


class RuleProvider(AIProvider):
    name = "rules"

    async def classify_text(
        self, text: str, *, context: str | None = None, lang: str | None = None
    ) -> Verdict:
        low = text.lower()
        for pat in _SCAM_PATTERNS:
            if re.search(pat, low):
                return Verdict("scam", 85, f"Matched scam pattern: /{pat}/")
        if len(_URL_RE.findall(low)) >= 3:
            return Verdict("spam", 75, "Excessive links")
        for pat in _SPAM_HINTS:
            if re.search(pat, low):
                return Verdict("spam", 75, "Repeated characters / flooding")
        hits = [w for w in _TOXIC_WORDS if re.search(rf"\b{re.escape(w)}", low)]
        if hits:
            return Verdict("toxicity", 65, f"Toxic language: {', '.join(sorted(hits))}")
        return Verdict("ok", 95, "No rule matched")
