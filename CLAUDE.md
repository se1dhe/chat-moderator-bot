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
  bot.py               Bot + Dispatcher factory (middlewares, AI provider+semaphore, redis, routers)
  __main__.py          entry point: always runs the aiohttp API; polling or webhook; menu button; captcha sweeper
  i18n.py              t(lang, key, **kw) locale lookup, resolve_lang(), SUPPORTED_LANGS
  locales/             en.py (canonical) · ru.py · uk.py — persona strings per language
  db/                  base (async engine/session), models, repo helpers
  middlewares/         DbSessionMiddleware · LangMiddleware (Chat.lang / language_code)
  filters/             IsChatAdmin (ACL)
  handlers/            common(+/panel) · onboarding · moderation · settings · captcha · raid ·
                       antiflood · content_filters · modes · ai_review (+ future: payments)
                       Join-watch (chat_member) and message-scan pipelines use SkipHandler so
                       independent routers each observe the same event: captcha → raid (joins);
                       antiflood → content_filters → modes → ai_review (messages, ai_review last).
                       content_filters + ai_review also register on edited_message (re-scan edits).
  api/                 Mini App backend (aiohttp): app factory (CORS, serves webapp/dist at /app),
                       auth (initData → user → chat-admin gate), routes (me, settings, audit,
                       quarantine, stats)
  services/            moderation, warns, trust (score + effective_threshold), quarantine
                       (shared approve/ban/rule), config (ChatSettings.data JSONB view + full_view/
                       apply_patch — the Mini App contract), roles (exemptions/admin cache),
                       antiflood, ai_budget (per-chat AI rate limit), ai_cache (Redis verdict cache),
                       filters, captcha, webapp_auth (initData HMAC), ai/ (ollama + rules)
  utils/               duration parsing, target resolution
webapp/                Mini App frontend — React 19 + Vite (design adapted from CP-helper), built
                       to webapp/dist and served by aiohttp at /app. Auth = Telegram initData.
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

AI: on Apple Silicon run Ollama natively (`ollama serve`, `ollama pull qwen3:4b`),
set `AI_ENABLED=true`, then per chat `/aimode quarantine`.

Mini App (dev): `cd webapp && npm install && npm run build` (aiohttp then serves it at
`/app`), or `npm run dev` for hot-reload (proxies `/api` to the running bot). Expose the
bot's port 8080 over HTTPS (ngrok) and set `WEBAPP_URL=https://<host>/app` so the menu
button + `/panel` open it. In BotFather, set the bot's Menu Button / Main Mini App URL
to the same URL. **The Mini App is the primary management surface; slash commands are a
fallback.** The TMA auths every request with Telegram `initData` (validated server-side)
and is admin-gated per chat.

## Current status & next step

**M1–M4 done — TMA-first pivot delivered (see the `redqueen-tma-pivot` memory).**
The Mini App is now the primary console: an always-on aiohttp API (`src/redqueen/api/`,
runs in both polling and webhook modes) validated by Telegram `initData`, and a premium
React/Vite frontend (`webapp/`, dark-red design adapted from CP-helper) covering every
setting (captcha, antiflood, filters, modes, AI incl. per-category thresholds, raid,
warns, exemptions) plus quarantine review, audit, and stats — all editable live.
AI effectiveness was overhauled: reply-to context + language-aware few-shot prompt,
Redis verdict cache (`ai_cache`), per-category thresholds tuned by the author's
trust score (`trust.effective_threshold`), and edited-message re-scan.
Monetization is in: **Telegram Stars** — `services/billing.py` (is_pro / activate /
record_payment), `handlers/payments.py` (/pro, /subscription, invoice, pre_checkout,
successful_payment), `Payment` ledger, and Pro gating (`billing.PRO_FEATURES` =
ai_autoban · raid_shield · analytics — enforced at runtime; core moderation stays free).
The TMA shows a Pro banner + Stars upgrade via `openInvoice` (`/api/chats/{id}/billing`
[+ `/invoice`]). Alembic revisions: initial, `CaptchaSession`, `RaidEvent`,
`ai_verdicts.text`, `payments`, `chat_members`.
**M5 in progress.** Delivered: **multimodal anti-scam (Pro)** — `classify_image` (Ollama
vision via `OLLAMA_VISION_MODEL`, e.g. `qwen2.5vl:7b`; empty → caption fallback);
`ai_review.scan_visual` runs photos/stickers/GIFs through the same quarantine flow;
`ensure_model` auto-pulls the vision model. **Cross-chat reputation** — trusted members
(`trust.should_bypass_captcha`) skip the join gate. **Member roster + TMA moderation** —
`handlers/members.py` records seen members (`ChatMember`, upsert per message, defers via
SkipHandler); `/api/chats/{id}/members` search + `/members/{uid}/action`
(ban/kick/mute/unmute/unban/warn); TMA **Members** screen with search and action buttons.
Chat notification language is set from the adder on join and editable in the TMA.
**Voice anti-scam** — `services/asr.py` (lazy faster-whisper via `WHISPER_MODEL`, optional
`voice` extra); `ai_review.scan_voice` transcribes voice/video-notes and runs them
through the text pipeline (Pro-gated). **Analytics** — stats API returns a 14-day
timeline + AI-category breakdown + member count; the TMA Stats screen charts them and
the Dashboard shows contextual **tips**. All four modalities (text/vision/voice) are
wired through the one explainable-quarantine flow.
**Remaining M5:** document/URL extractor analysis, clone-bots / white-label (multi-bot
over the shared DB). See PROJECT_PLAN §12.

Note: `DbSessionMiddleware` commits (not rolls back) on `SkipHandler` — handlers that
write then defer (captcha→raid, members→scanners) rely on this; keep it.

## Notes

- The user pasted a live bot token and ngrok token in chat once; both must be rotated.
  Never store or reuse those values.
- Bot commands and persona should be authored in the RedQueen voice (see `locales/en.py`,
  the canonical source; keep `ru.py`/`uk.py` in sync when adding new strings).
