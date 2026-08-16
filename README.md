# RedQueen Security 🔴

Advanced public Telegram moderation bot — an explainable-AI alternative to @GroupHelpBot.
Built with **aiogram 3.x**, PostgreSQL, and a swappable local **Qwen/Ollama** AI runtime.
Persona: the "Red Queen" defense system from *Resident Evil*.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/ROADMAP.md](docs/ROADMAP.md).

## Status — M1 (foundation)

Working: `/start`, `/help`, admin-gated `ban / kick / mute / unmute / warn / unwarn /
unban / purge`, warn limits with auto-action, per-chat settings, full audit log, and an
AI moderation listener with an explainable **quarantine decision card** (rule fallback
today, Qwen via Ollama when enabled).

## Quick start (local, polling)

1. **Get fresh secrets.** Create a bot with [@BotFather](https://t.me/BotFather) and copy
   its token. In BotFather, run `/setprivacy` → **Disable** so the bot can see messages.
2. Configure env:

   ```sh
   cp .env.example .env
   # edit .env: set BOT_TOKEN and OWNER_IDS (your numeric Telegram id)
   ```

3. Start infra + bot with Docker:

   ```sh
   docker compose up --build postgres redis bot
   ```

   Or run the bot on the host with `uv`:

   ```sh
   uv sync --extra dev
   docker compose up -d postgres redis
   uv run redqueen
   ```

4. Add the bot to a group and **promote it to admin** (Delete messages, Ban users,
   Restrict members). Try `/help` in the group.

## Enabling AI moderation (Qwen)

On Apple Silicon, run Ollama natively for GPU acceleration:

```sh
brew install ollama
ollama serve
ollama pull qwen3.5:4b     # 9b/27b for higher quality if you have the RAM
```

Then in `.env` set `AI_ENABLED=true` and `OLLAMA_MODEL=qwen3.5:4b`, restart the bot,
and per chat run `/aimode quarantine`. On Linux servers use the `ai` compose profile:
`docker compose --profile ai up -d ollama`.

## Webhook / ngrok (optional)

For webhook mode during development, expose the bot with ngrok and point Telegram at it:

```sh
ngrok http 8080          # copy the https domain it prints
```

In `.env`: `RUN_MODE=webhook`, `WEBHOOK_BASE_URL=https://<your-ngrok-domain>`,
`WEBHOOK_SECRET=<random-string>`, then restart. The bot registers the webhook on boot.

## Security

Never commit real tokens. `.env` is git-ignored. If a token was ever pasted somewhere
public, rotate it: bot token via `@BotFather → /revoke`, ngrok token in the ngrok
dashboard. The database schema is created automatically in dev; use Alembic migrations
(`migrations/`) for production.

## Tests

```sh
uv run pytest
```
