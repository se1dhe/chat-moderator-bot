"""services/webapp_auth: Telegram initData signature + freshness validation."""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pytest

from redqueen.services.webapp_auth import InitDataError, verify_init_data

BOT_TOKEN = "123456:TEST-TOKEN"


def _sign(fields: dict, token: str = BOT_TOKEN) -> str:
    """Build a valid initData query string for the given fields (mirrors Telegram)."""
    data_check_string = "\n".join(f"{k}={fields[k]}" for k in sorted(fields))
    secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    h = hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode({**fields, "hash": h})


def _fields(**over) -> dict:
    base = {
        "auth_date": str(int(time.time())),
        "query_id": "AAterm",
        "user": json.dumps({"id": 42, "username": "neo", "first_name": "Thomas"}),
    }
    base.update(over)
    return base


def test_valid_init_data_returns_user():
    user = verify_init_data(_sign(_fields()), BOT_TOKEN)
    assert user.id == 42
    assert user.username == "neo"
    assert user.full_name == "Thomas"


def test_empty_rejected():
    with pytest.raises(InitDataError):
        verify_init_data("", BOT_TOKEN)


def test_tampered_field_rejected():
    signed = _sign(_fields())
    tampered = signed.replace("id%3A+42", "id%3A+999")  # flip user id after signing
    if tampered == signed:  # urlencode spacing differs; force a change another way
        tampered = signed + "&extra=1"
    with pytest.raises(InitDataError):
        verify_init_data(tampered, BOT_TOKEN)


def test_wrong_token_rejected():
    with pytest.raises(InitDataError):
        verify_init_data(_sign(_fields()), "999999:OTHER-TOKEN")


def test_stale_init_data_rejected():
    old = _fields(auth_date=str(int(time.time()) - 10_000))
    with pytest.raises(InitDataError):
        verify_init_data(_sign(old), BOT_TOKEN, max_age_seconds=3600)


def test_missing_hash_rejected():
    fields = _fields()
    with pytest.raises(InitDataError):
        verify_init_data(urlencode(fields), BOT_TOKEN)  # no hash appended
