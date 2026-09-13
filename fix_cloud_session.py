import re

with open('src/redqueen/services/ai/cloud.py', 'r') as f:
    text = f.read()

# Change CloudAIProvider to accept session
old_init = """    def __init__(self, api_key: str, model: str, fallback: AIProvider):
        self.api_key = api_key
        self.model = model
        self.fallback = fallback
        self._session: aiohttp.ClientSession | None = None

    def _client(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None"""

new_init = """    def __init__(self, api_key: str, model: str, fallback: AIProvider, session: aiohttp.ClientSession | None = None):
        self.api_key = api_key
        self.model = model
        self.fallback = fallback
        self._session = session

    def _client(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        # Let the RouterProvider manage the shared session
        pass"""

text = text.replace(old_init, new_init)

with open('src/redqueen/services/ai/cloud.py', 'w') as f:
    f.write(text)

