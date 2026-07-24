"""Cliente ElevenLabs — STT (Scribe) y TTS. ADR-0014.

Una sola dependencia: `requests` (ya en el entorno). Aquí viven las DOS llamadas HTTP a
ElevenLabs; la API key nunca sale de aquí hacia el cliente.

- `transcribir(audio)` : micrófono del navegador -> texto (entra a la ruta asistida).
- `sintetizar(texto)`  : el sistema HABLA por el speaker del teléfono.

Conteo ciego (ADR-0001): `sintetizar` solo vocaliza textos que ya son seguros —
`PolicyResult.message` y las preguntas del resolver NUNCA contienen la cantidad del ERP.
El sistema puede hablar libremente porque esos mensajes se diseñaron sin el número. No
pasar a `sintetizar` nada derivado de `stock_corte`.
"""
from __future__ import annotations
import requests

from ..config import settings

_STT_URL = "https://api.elevenlabs.io/v1/speech-to-text"
_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
_TIMEOUT = 60


def transcribir(audio: bytes, filename: str = "audio.webm") -> str:
    if not settings.tiene_elevenlabs():
        raise RuntimeError("ELEVENLABS_API_KEY ausente: configúrala en el .env")
    resp = requests.post(
        _STT_URL,
        headers={"xi-api-key": settings.ELEVENLABS_API_KEY},
        data={"model_id": settings.ELEVENLABS_STT_MODEL, "language_code": "spa"},
        files={"file": (filename, audio)},
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return (resp.json().get("text") or "").strip()


def sintetizar(texto: str) -> bytes:
    if not settings.tiene_elevenlabs():
        raise RuntimeError("ELEVENLABS_API_KEY ausente: configúrala en el .env")
    resp = requests.post(
        _TTS_URL.format(voice_id=settings.ELEVENLABS_VOICE_ID),
        headers={"xi-api-key": settings.ELEVENLABS_API_KEY, "accept": "audio/mpeg"},
        json={
            "text": texto,
            "model_id": settings.ELEVENLABS_TTS_MODEL,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        },
        timeout=_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.content
