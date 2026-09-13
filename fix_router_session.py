import re

with open('src/redqueen/services/ai/router.py', 'r') as f:
    text = f.read()

# Add a shared session to RouterProvider
old_init = """    def __init__(self, ollama_provider: AIProvider, fallback: AIProvider, secret_key: str):
        self.ollama = ollama_provider
        self.fallback = fallback
        # Fail fast if SECRET_KEY is invalid (BUG-3)
        self.fernet = Fernet(secret_key) if secret_key else None
        self._cache: dict[tuple, AIProvider] = {}"""

new_init = """    def __init__(self, ollama_provider: AIProvider, fallback: AIProvider, secret_key: str):
        self.ollama = ollama_provider
        self.fallback = fallback
        # Fail fast if SECRET_KEY is invalid (BUG-3)
        self.fernet = Fernet(secret_key) if secret_key else None
        self._cache: dict[tuple, AIProvider] = {}
        import aiohttp
        self._shared_session: aiohttp.ClientSession | None = None"""

text = text.replace(old_init, new_init)

# Use the shared session when instantiating providers
old_inst = """        provider = self.ollama
        if provider_name == "openai":
            provider = OpenAIProvider(api_key, model_name, self.fallback)
        elif provider_name == "gemini":
            provider = GeminiProvider(api_key, model_name, self.fallback)
        elif provider_name == "claude":
            provider = ClaudeProvider(api_key, model_name, self.fallback)"""

new_inst = """        provider = self.ollama
        import aiohttp
        if self._shared_session is None or self._shared_session.closed:
            self._shared_session = aiohttp.ClientSession()
            
        if provider_name == "openai":
            provider = OpenAIProvider(api_key, model_name, self.fallback, self._shared_session)
        elif provider_name == "gemini":
            provider = GeminiProvider(api_key, model_name, self.fallback, self._shared_session)
        elif provider_name == "claude":
            provider = ClaudeProvider(api_key, model_name, self.fallback, self._shared_session)"""

text = text.replace(old_inst, new_inst)

# Close the shared session on close()
old_close = """    async def close(self) -> None:
        await self.ollama.close()
        for provider in self._cache.values():
            if hasattr(provider, "close"):
                await provider.close()
        self._cache.clear()"""

new_close = """    async def close(self) -> None:
        await self.ollama.close()
        self._cache.clear()
        if self._shared_session and not self._shared_session.closed:
            await self._shared_session.close()"""

text = text.replace(old_close, new_close)

with open('src/redqueen/services/ai/router.py', 'w') as f:
    f.write(text)

