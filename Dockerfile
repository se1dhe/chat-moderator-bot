# --- Stage 1: build the Mini App bundle ---
FROM node:22-slim AS webapp
WORKDIR /webapp
COPY webapp/package.json webapp/package-lock.json ./
RUN npm ci
COPY webapp/ ./
RUN npm run build

# --- Stage 2: the bot + API ---
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md alembic.ini ./
COPY src ./src
COPY migrations ./migrations

RUN pip install --upgrade pip && pip install .

# Built Mini App, served by aiohttp at /app (WEBAPP_DIST=webapp/dist).
COPY --from=webapp /webapp/dist ./webapp/dist

RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["sh", "-c", "alembic upgrade head && redqueen"]
