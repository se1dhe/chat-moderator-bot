"""AI moderation package. Swappable runtime behind a single interface."""
from __future__ import annotations

from ...config import Settings
from .provider import AIProvider, Verdict
from .rules import RuleProvider

__all__ = ["AIProvider", "Verdict", "RuleProvider", "build_provider"]


def build_provider(settings: Settings) -> AIProvider:
    """Return the configured provider. Falls back to rules when AI is disabled."""
    if settings.ai_enabled:
        from .ollama import OllamaProvider

        return OllamaProvider(
            base_url=settings.ollama_url,
            model=settings.ollama_model,
            fallback=RuleProvider(),
        )
    return RuleProvider()
