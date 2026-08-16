"""Telegram Mini App `initData` validation (pure, no aiohttp/Telegram I/O).

Implements the signature check from
https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app :

    secret_key      = HMAC_SHA256(key="WebAppData", msg=bot_token)
    data_check_str  = "\\n".join(f"{k}={v}" for k, v in sorted(fields without `hash`))
    expected_hash   = hex( HMAC_SHA256(key=secret_key, msg=data_check_str) )

The caller passes the raw `initData` query string exactly as the WebApp SDK produced it.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from urllib.parse import parse_qsl


@dataclass
class WebAppUser:
    id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str | None

    @property
    def full_name(self) -> str:
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts) or (self.username or str(self.id))


class InitDataError(Exception):
    """Raised when initData is missing, malformed, forged, or stale."""


def _secret_key(bot_token: str) -> bytes:
    return hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()


def verify_init_data(init_data: str, bot_token: str, *, max_age_seconds: int = 86400) -> WebAppUser:
    """Validate the signature and freshness of `init_data`; return the authenticated user.

    Raises `InitDataError` on any problem — callers translate that to HTTP 401.
    """
    if not init_data:
        raise InitDataError("empty initData")

    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise InitDataError("missing hash")

    data_check_string = "\n".join(f"{k}={pairs[k]}" for k in sorted(pairs))
    expected = hmac.new(_secret_key(bot_token), data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received_hash):
        raise InitDataError("bad signature")

    auth_date = pairs.get("auth_date")
    if not auth_date or not auth_date.isdigit():
        raise InitDataError("missing auth_date")
    if max_age_seconds and (time.time() - int(auth_date)) > max_age_seconds:
        raise InitDataError("stale initData")

    user_raw = pairs.get("user")
    if not user_raw:
        raise InitDataError("missing user")
    try:
        u = json.loads(user_raw)
    except json.JSONDecodeError as exc:
        raise InitDataError("bad user json") from exc

    if "id" not in u:
        raise InitDataError("user without id")
    return WebAppUser(
        id=int(u["id"]),
        username=u.get("username"),
        first_name=u.get("first_name"),
        last_name=u.get("last_name"),
        language_code=u.get("language_code"),
    )
