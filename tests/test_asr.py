"""services/asr.Transcriber: graceful disable when no model / library."""
from __future__ import annotations

import pytest

from redqueen.services.asr import Transcriber


def test_disabled_without_model():
    assert Transcriber("").enabled is False


@pytest.mark.asyncio
async def test_transcribe_returns_none_when_disabled():
    assert await Transcriber("").transcribe(b"audio") is None


def test_enabled_with_model_name():
    # enabled reflects config even before the (lazy) model actually loads.
    assert Transcriber("small").enabled is True
