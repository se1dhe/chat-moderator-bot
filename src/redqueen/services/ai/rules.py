"""Rule-based fallback provider. Works with zero external dependencies.

Deterministic and cheap; used when AI is disabled or Ollama is unreachable.
"""
from __future__ import annotations

import re

from .provider import AIProvider, Verdict

_SCAM_PATTERNS = [
    r"\bt\.me/\+?\w+",
    r"\bfree\s+(?:crypto|bitcoin|btc|eth|usdt|giveaway)",
    r"\b(?:pump|airdrop|x100|guaranteed profit)\b",
    r"(?:earn|make)\s+\$?\d{2,}\s*(?:per|/)\s*day",
    r"\bwhatsapp\b.*\+\d{6,}",
]
_TOXIC_WORDS = {
    "idiot", "moron", "scum", "trash", "loser",  # keep mild; extend per-locale later
}
_SPAM_HINTS = [
    r"(.)\1{9,}",              # long char runs (aaaaa...)
]
_URL_RE = re.compile(r"https?://\S+")


class RuleProvider(AIProvider):
    name = "rules"

    async def classify_text(self, text: str, *, context: str | None = None) -> Verdict:
        low = text.lower()
        for pat in _SCAM_PATTERNS:
            if re.search(pat, low):
                return Verdict("scam", 85, f"Matched scam pattern: /{pat}/")
        if len(_URL_RE.findall(low)) >= 3:
            return Verdict("spam", 75, "Excessive links")
        for pat in _SPAM_HINTS:
            if re.search(pat, low):
                return Verdict("spam", 75, "Repeated characters / flooding")
        hits = [w for w in _TOXIC_WORDS if re.search(rf"\b{re.escape(w)}\b", low)]
        if hits:
            return Verdict("toxicity", 65, f"Toxic language: {', '.join(hits)}")
        return Verdict("ok", 95, "No rule matched")
