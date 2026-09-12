"""AI moderation package. Swappable runtime behind a single interface."""
from __future__ import annotations

from ...config import Settings
from .provider import AIProvider, Verdict
from .rules import RuleProvider

__all__ = ["AIProvider", "RuleProvider", "Verdict", "build_provider"]


def build_provider(settings: Settings) -> AIProvider:
    """Return the configured provider. Supports per-chat routing even if global Ollama is disabled."""
    from .rules import RuleProvider
    from .router import RouterProvider

    fallback = RuleProvider()
    
    if settings.ai_enabled:
        from .ollama import OllamaProvider
        ollama = OllamaProvider(
            base_url=settings.ollama_url,
            model=settings.ollama_model,
            fallback=fallback,
            vision_model=settings.ollama_vision_model,
        )
    else:
        ollama = fallback

    return RouterProvider(ollama, fallback, settings.secret_key)
