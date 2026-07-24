"""Voz por ElevenLabs (Scribe / Speech-to-Text). Adapter de la ruta asistida. ADR-0014.

Decidido por el lead: hay creditos de ElevenLabs en la hackaton. Reemplaza el STT on-device
que planteaban ADR-0003/0011. Lo que NO cambia: la voz sigue siendo SECUNDARIA — botones
primero, ningun flujo se completa solo por voz (el corazon de ADR-0003 sobrevive).

Mismo patron que vision: audio (bytes) -> texto (ElevenLabs) -> matcher. Converge en el
mismo ResolucionResult que texto y foto. El transcriptor es un PUERTO: el stub del demo se
cambia por la llamada real a la API sin tocar nada mas.
"""
from __future__ import annotations
from typing import Protocol

from contracts.dtos import ResolucionResult
from ..domain import matcher


class Transcriptor(Protocol):
    """Puerto STT. Real = POST a ElevenLabs /v1/speech-to-text con ELEVENLABS_API_KEY.
    transcribir() NUNCA decide nada: solo convierte audio en texto (ADR-0007)."""
    def transcribir(self, audio: object) -> str: ...


class VozElevenLabsResolver:
    fuente = "voz"

    def __init__(self, transcriptor: "Transcriptor") -> None:
        self._stt = transcriptor

    def resolver(self, bodega_id: str, entrada: object) -> ResolucionResult:
        texto = self._stt.transcribir(entrada)          # audio -> texto. LO UNICO nuevo
        return matcher.resolver(bodega_id, texto)       # de aqui: identico a texto/foto
