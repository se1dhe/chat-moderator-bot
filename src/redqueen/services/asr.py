"""Voice/video-note transcription via faster-whisper (lazy, optional, graceful).

`faster-whisper` is an optional dependency; if it (or a configured model) is missing,
the transcriber simply reports itself disabled and voice scanning is skipped. The model
is loaded once on first use and runs in a worker thread so it never blocks the loop.
"""
from __future__ import annotations

import asyncio
import logging
from io import BytesIO

log = logging.getLogger(__name__)


class Transcriber:
    def __init__(self, model_name: str, *, device: str = "cpu", compute_type: str = "int8") -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model = None
        self._failed = False

    @property
    def enabled(self) -> bool:
        return bool(self.model_name) and not self._failed

    def _load(self):
        from faster_whisper import WhisperModel

        log.info("Loading Whisper model %s (%s/%s)…", self.model_name, self.device, self.compute_type)
        return WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)

    def _run(self, audio: bytes) -> str:
        segments, _info = self._model.transcribe(BytesIO(audio), vad_filter=True)
        return " ".join(seg.text for seg in segments).strip()

    async def transcribe(self, audio: bytes) -> str | None:
        """Return transcript text, or None if ASR is unavailable/fails."""
        if not self.enabled:
            return None
        try:
            if self._model is None:
                self._model = await asyncio.to_thread(self._load)
            return await asyncio.to_thread(self._run, audio)
        except Exception as exc:  # noqa: BLE001
            log.warning("ASR failed (%s); voice scanning disabled", exc)
            self._failed = True
            return None
