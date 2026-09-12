from __future__ import annotations

import logging
from cryptography.fernet import Fernet
from .provider import AIProvider, Verdict
from .cloud import OpenAIProvider, GeminiProvider, ClaudeProvider

log = logging.getLogger(__name__)

class RouterProvider(AIProvider):
    name = "router"

    def __init__(self, ollama_provider: AIProvider, fallback: AIProvider, secret_key: str):
        self.ollama = ollama_provider
        self.fallback = fallback
        # Fail fast if SECRET_KEY is invalid (BUG-3)
        self.fernet = Fernet(secret_key) if secret_key else None
        self._cache: dict[tuple, AIProvider] = {}

    def _decrypt_key(self, encrypted: str | None) -> str | None:
        if not encrypted or not self.fernet:
            return None
        try:
            return self.fernet.decrypt(encrypted.encode()).decode()
        except Exception:
            return None

    def _get_provider(self, chat_settings) -> AIProvider:
        if not chat_settings:
            return self.ollama

        provider_name = getattr(chat_settings, "ai_provider", "ollama")
        if provider_name == "ollama":
            return self.ollama

        encrypted_key = getattr(chat_settings, "ai_api_key_encrypted", None)
        api_key = self._decrypt_key(encrypted_key)
        if not api_key:
            return self.ollama  # fallback if no key provided

        model_name = getattr(chat_settings, "ai_model", None)
        import hashlib
        key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
        cache_key = (provider_name, key_hash, model_name)
        
        if cache_key in self._cache:
            # Move to end to simulate LRU
            provider = self._cache.pop(cache_key)
            self._cache[cache_key] = provider
            return provider
        
        provider = self.ollama
        if provider_name == "openai":
            provider = OpenAIProvider(api_key, model_name, self.fallback)
        elif provider_name == "gemini":
            provider = GeminiProvider(api_key, model_name, self.fallback)
        elif provider_name == "claude":
            provider = ClaudeProvider(api_key, model_name, self.fallback)
            
        if len(self._cache) > 500:
            # Pop the oldest item (first item in dict)
            old_key = next(iter(self._cache))
            old_provider = self._cache.pop(old_key)
            import asyncio
            asyncio.create_task(old_provider.close())
            
        self._cache[cache_key] = provider
        return provider

    async def classify_text(
        self, text: str, *, context: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        provider = self._get_provider(chat_settings)
        return await provider.classify_text(text, context=context, lang=lang, chat_settings=chat_settings)

    async def classify_image(
        self, image: bytes, *, caption: str | None = None, lang: str | None = None, chat_settings = None
    ) -> Verdict:
        provider = self._get_provider(chat_settings)
        return await provider.classify_image(image, caption=caption, lang=lang, chat_settings=chat_settings)

    async def ensure_model(self) -> bool:
        if hasattr(self.ollama, "ensure_model"):
            return await self.ollama.ensure_model()
        return True

    async def close(self) -> None:
        await self.ollama.close()
        for provider in self._cache.values():
            if hasattr(provider, "close"):
                await provider.close()
        self._cache.clear()
