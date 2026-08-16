# CLAUDE.md — RedQueen Security

Guidance for Claude Code working in this repository.

## What this is

**RedQueen Security** (@RedQueenSecurity_Bot) — a public Telegram moderation SaaS bot,
an explainable-AI alternative to @GroupHelpBot. Persona: the "Red Queen" AI from
*Resident Evil* (cold, precise; lore references are **strong** but text stays clear and
never toxic to users). Global SaaS, freemium **per chat**.

**Read [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) first — it is the master plan.**
Technical detail in `docs/ARCHITECTURE.md`; release breakdown in `docs/ROADMAP.md`.

## Key decisions (do not re-litigate without the user)

- Chats: **groups + channels**. Monetization: **Free core + Pro via Telegram Stars**.
- UI languages: **EN + RU + UK** from the start (i18n from M2).
- AI: **Qwen via Ollama**, model **swappable via env** (dev 4B, prod 9B+), with a
  rule-based fallback. Prod AI hosting TBD.
- Data: **full audit** + delete/export on request. Deploy: **VPS + Docker Compose**.
- Mini App: **M4 (later)**. Persona: **strong lore**. Pace: **quality over speed**.
- Clone-bots / white-label: **M5**; keep data keyed by `chat_telegram_id` for multi-bot.
- Priority killer features: Explainable AI quarantine, Raid shield, Adaptive trust
  score, multimodal anti-scam.

## Tech stack

aiogram 3.30 · Python 3.11–3.13 · SQLAlchemy 2 async + asyncpg (PostgreSQL) · Alembic ·
Redis · pydantic-settings · aiohttp · Ollama/Qwen · Docker Compose · ngrok (dev webhook).

## Layout

```
src/redqueen/
  config.py            pydantic-settings (.env)
  bot.py               Bot + Dispatcher factory (wires middlewares, AI provider, redis, routers)
  __main__.py          entry point (polling / webhook) + captcha timeout sweeper task
  i18n.py              t(lang, key, **kw) locale lookup, resolve_lang(), SUPPORTED_LANGS
  locales/             en.py (canonical) · ru.py · uk.py — persona strings per language
  db/                  base (async engine/session), models, repo helpers
  middlewares/         DbSessionMiddleware · LangMiddleware (resolves Chat.lang / language_code)
  filters/             IsChatAdmin (ACL)
  handlers/            common · onboarding · moderation · settings · captcha ·
                       antiflood · content_filters · modes · ai_review (+ future: payments)
                       Message-scan pipeline order: antiflood → content_filters → modes →
                       ai_review, each raising SkipHandler to fall through when it doesn't apply.
  services/            moderation, warns, config (ChatSettings.data JSONB view), roles
                       (exemptions/admin cache), antiflood, filters, captcha,
                       ai/ (provider abstraction: ollama + rules)
  utils/               duration parsing, target resolution
docs/                  PROJECT_PLAN.md (master), ARCHITECTURE.md, ROADMAP.md
migrations/            Alembic (env.py wired to app settings/metadata) — authoritative from M2
tests/                 pytest (framework-agnostic logic; fake_redis fixture in conftest.py)
```

## Conventions

- **aiogram 3.x only.** No 2.x APIs (`dp.message_handler`, `state.set()`, `aiogram.contrib`).
  Use `Router`, `@router.message(Command(...))`, `F` magic filters, `FSMContext`,
  `CallbackData`, keyboard builders. Async + type hints everywhere.
- Handlers stay thin: parse update → call a `services/` function → reply. Business logic
  lives in `services/` (no aiogram imports there) so it stays testable and Mini-App-reusable.
- All persistent data keyed by `chat_telegram_id`. New tables get an index on it.
- Every moderation action writes a `ModAction` audit row via `repo.log_action`.
- Secrets only via `.env` (git-ignored). Never hardcode or log tokens.
- Use Alembic migrations from M2 onward (not `create_all`, which is dev bootstrap only).

## Commands

```sh
uv sync --extra dev                     # install deps (regenerates uv.lock)
docker compose up -d postgres redis     # infra
cp .env.example .env                     # then set BOT_TOKEN + OWNER_IDS
uv run redqueen                          # run the bot (polling by default)
uv run pytest                            # tests
uv run ruff check src                    # lint
uv run alembic revision --autogenerate -m "msg"   # new migration
uv run alembic upgrade head              # apply migrations
```

AI: on Apple Silicon run Ollama natively (`ollama serve`, `ollama pull qwen3.5:4b`),
set `AI_ENABLED=true`, then per chat `/aimode quarantine`.

## Current status & next step

**M1 and M2 are done.** M2 added: i18n scaffold (`locales/` + `t(lang, key, **kw)` +
`LangMiddleware`, `/lang`), join captcha (button/math, DB-driven timeout sweeper, join
requests via DM), Redis antiflood, content filters (banned words / links / forwards /
mentions / media), night/silent/slow mode + role exemptions, and onboarding
(admin-rights check, `/checksetup`). Alembic is now authoritative (`create_all` removed
from `__main__.py`); two revisions exist (initial schema, `CaptchaSession`).
**Next: M3** — AI-moderation to prod quality (Ollama+Qwen queue, off/quarantine/autoban
modes), Raid shield, Adaptive trust score scaffold. See PROJECT_PLAN §12.

## Notes

- The user pasted a live bot token and ngrok token in chat once; both must be rotated.
  Never store or reuse those values.
- Bot commands and persona should be authored in the RedQueen voice (see `locales/en.py`,
  the canonical source; keep `ru.py`/`uk.py` in sync when adding new strings).
