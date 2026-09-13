"""Abstract AI moderation provider and its result type."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

CATEGORIES = ("ok", "spam", "scam", "toxicity", "nsfw", "flood")


@dataclass
class Verdict:
    category: str          # one of CATEGORIES
    score: int             # confidence 0..100
    explanation: str       # short human-readable reason

    @property
    def is_violation(self) -> bool:
        return self.category != "ok"


class AIProvider(ABC):
    """A provider classifies a piece of text (later: image/audio) for moderation."""

    name: str = "abstract"

    @abstractmethod
    async def classify_text(
        self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        ...

    async def classify_image(
        self, image: bytes, *, caption: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        """Classify an image (scam poster, NSFW, phishing screenshot). Providers without
        vision may fall back to inspecting the caption. Default: analyze the caption only."""
        if caption:
            return await self.classify_text(caption, lang=lang, chat_settings=chat_settings)
        return Verdict("ok", 50, "No vision analysis available")

    async def health(self) -> bool:
        """Whether the provider is reachable/usable right now."""
        return True

    async def generate_text(self, prompt: str, chat_settings=None) -> str:
        return "Summary not supported on this provider."

    async def close(self) -> None:
        return None
