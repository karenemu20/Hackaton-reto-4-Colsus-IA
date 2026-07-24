"""STUB de ElevenLabs Scribe para el esqueleto/demo. SUSTITUIR por la llamada real.

Real (ejemplo):
    import requests
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text",
                      headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
                      files={"file": audio}, data={"model_id": "scribe_v1"})
    return r.json()["text"]

Aqui simula un audio donde el operario dijo 'aguardiente' pero el STT lo devolvio garbleado
como 'agardiente' — el error tipico del espanol regional en bodega (P-05, motivo de ADR-0003).
Sirve para demostrar que la busqueda semantica lo recupera igual.
"""
from __future__ import annotations


class ElevenLabsStubSTT:
    def transcribir(self, audio: object) -> str:
        return "agardiente"
