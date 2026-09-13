with open('src/redqueen/services/ai/ollama.py', 'r') as f:
    text = f.read()

new_gen = """
    async def generate_text(self, prompt: str, chat_settings=None) -> str:
        payload = {
            "model": self.model or "llama3",
            "prompt": prompt,
            "stream": False,
        }
        try:
            async with self._client().post(f"{self.base_url}/api/generate", json=payload, timeout=60) as resp:
                data = await resp.json()
                return data.get("response", "")
        except Exception as exc:
            return f"Ollama Error: {exc}"

    async def classify_text("""

text = text.replace('    async def classify_text(', new_gen)

with open('src/redqueen/services/ai/ollama.py', 'w') as f:
    f.write(text)

