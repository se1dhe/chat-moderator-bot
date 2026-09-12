"""AI moderation package. Swappable runtime behind a single interface."""
from __future__ import annotations

from ...config import Settings
from .provider import AIProvider, Verdict
from .rules import RuleProvider

__all__ = ["AIProvider", "RuleProvider", "Verdict", "build_provider"]


def build_provider(settings: Settings) -> AIProvider:
    """Return the configured provider. Falls back to rules when AI is disabled."""
    from .rules import RuleProvider
    fallback = RuleProvider()
    
    if settings.gemini_api_key:
        from .gemini import GeminiProvider
        from .router import RouterProvider
        gemini = GeminiProvider(api_key=settings.gemini_api_key)
        return RouterProvider(gemini, fallback)
        
    if settings.ai_enabled:
        from .ollama import OllamaProvider
        from .router import RouterProvider

        ollama = OllamaProvider(
            base_url=settings.ollama_url,
            model=settings.ollama_model,
            fallback=fallback,
            vision_model=settings.ollama_vision_model,
        )
        return RouterProvider(ollama, fallback)

    return fallback
