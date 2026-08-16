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
        self, text: str, *, context: str | None = None, lang: str | None = None
    ) -> Verdict:
        ...

    async def health(self) -> bool:
        """Whether the provider is reachable/usable right now."""
        return True

    async def close(self) -> None:
        return None
