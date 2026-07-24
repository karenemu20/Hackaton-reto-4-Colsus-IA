"""Config por variables de entorno. En Docker/VPS se inyecta por el .env (nunca en el repo)."""
from __future__ import annotations
import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # multilingüe
ELEVENLABS_STT_MODEL = os.environ.get("ELEVENLABS_STT_MODEL", "scribe_v1")
ELEVENLABS_TTS_MODEL = os.environ.get("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")


def tiene_elevenlabs() -> bool:
    return bool(ELEVENLABS_API_KEY)
