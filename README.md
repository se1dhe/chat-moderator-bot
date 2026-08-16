# RedQueen Security 🔴

Advanced public Telegram moderation bot — an explainable-AI alternative to @GroupHelpBot.
Built with **aiogram 3.x**, PostgreSQL, and a swappable local **Qwen/Ollama** AI runtime.
Persona: the "Red Queen" defense system from *Resident Evil*.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/ROADMAP.md](docs/ROADMAP.md).

## Status — M4 in progress · TMA-first management console

The **Telegram Mini App is now the primary way to manage RedQueen** — a premium
dark-red console (React + Vite, served by the bot) where admins configure every feature,
review the AI quarantine queue, and read the audit log and stats. Slash commands remain
as a fallback. See [Mini App](#mini-app-management-console) below.

Working: everything from M1+M2+M3 (moderation commands, warn limits, per-chat settings,
full audit log, i18n, captcha, antiflood, content filters, modes, onboarding, AI
moderation queue with explainable quarantine, raid shield, trust score) plus:

- **Mini App** — authenticated by Telegram `initData`, admin-gated per chat; edits all
  settings live and reviews quarantine/audit/stats.
- **Sharper AI** — reply-to context + language-aware few-shot prompt, a Redis verdict
  cache (identical raid spam is classified once per window), per-category confidence
  thresholds nudged by the author's trust score, and edited-message re-scan.

Earlier milestone highlights:

- **AI moderation queue** — classification calls are bounded by a global
  `asyncio.Semaphore` (`AI_MAX_CONCURRENCY`) and a per-chat Redis rate limit, so AI is
  a bounded fallback for whatever the fast rule-filters didn't already catch.
- **Explainable quarantine card** — three actions: Ban, Approve, and **Rule** (promotes
  the flagged text straight into `/bannedwords` so the same pattern is caught instantly
  next time, no AI call needed).
- **Raid shield** — detects a coordinated join surge (Redis window) and auto-locks the
  chat (blocks non-admin messages) for a cooldown, with an audit row per incident
  (`/raidshield`, `/raidconfig`, `/unlock`).
- **Adaptive trust score (scaffold)** — `User.trust_score` moves with moderation
  outcomes (bans/kicks/mutes/warns penalize, passing captcha or an admin overriding a
  false-positive AI verdict rewards). View with `/trust`; using the score to change
  moderation strictness is a later milestone.

Schema is managed by **Alembic** in every environment (`create_all` dev bootstrap was
removed in M2) — see Quick start below.

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
   uv run alembic upgrade head
   uv run redqueen
   ```

4. Add the bot to a group and **promote it to admin** (Delete messages, Ban users,
   Restrict members). Try `/help` in the group.

## Enabling AI moderation (Qwen)

On Apple Silicon, run Ollama natively for GPU acceleration:

```sh
brew install ollama
ollama serve
ollama pull qwen3:4b       # or qwen3:8b/14b for higher quality (more RAM)
```

Then in `.env` set `AI_ENABLED=true` and `OLLAMA_MODEL=qwen3:4b`, restart the bot,
and per chat run `/aimode quarantine`. On Linux servers use the `ai` compose profile:
`docker compose --profile ai up -d ollama`.

`AI_MAX_CONCURRENCY` (default 2) caps concurrent Ollama calls across all chats; each
chat additionally gets its own Redis-backed budget (`config.ai.max_per_minute`,
default 20/min) so one busy chat can't starve the rest.

## Mini App (management console)

The bot always runs an HTTP API (aiohttp) and serves the built Mini App at `/app`.

Build and serve from the bot:

```sh
cd webapp && npm install && npm run build
```

Then start the bot (`uv run redqueen`) and the console is at `http://localhost:8080/app`
(API under `/api`). For hot-reload development, run the frontend separately — it proxies
`/api` to the running bot:

```sh
cd webapp && npm run dev
```

To use it inside Telegram it must be reachable over **HTTPS**. In dev, tunnel port 8080
with ngrok and point the bot and BotFather at it:

```sh
ngrok http 8080
```

- Set `WEBAPP_URL=https://<your-ngrok-domain>/app` in `.env` and restart — the bot wires
  it to the private-chat **menu button** and the `/panel` command.
- In [@BotFather](https://t.me/BotFather): set the bot's **Menu Button** (or **Main Mini
  App**) URL to the same `https://<domain>/app`.
- Open the bot in Telegram → menu button, or send `/panel` in a managed group.

Auth is entirely via Telegram `initData` (HMAC-validated server-side); each request is
gated to administrators of the target chat. No separate login.

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
dashboard. Schema changes go through Alembic (`migrations/`) in every environment —
run `uv run alembic upgrade head` (or let the Docker image's entrypoint do it) before
starting the bot.

## Tests

```sh
uv run pytest
```
