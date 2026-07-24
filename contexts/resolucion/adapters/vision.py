"""VISION POR COMPUTADOR — el adapter que agrega la foto. ADR-0012.

La camara es un SENSOR, no un modelo de dominio. Este adapter hace UNA sola cosa que voz
y texto no hacen: convierte una imagen en TEXTO (etiqueta, via OCR) y, opcionalmente, en
una CANTIDAD sugerida (deteccion de cajas apiladas, via YOLO). A partir de ese texto,
reutiliza EXACTAMENTE el mismo `matcher` que voz y texto -> converge en el mismo
ResolucionResult / Candidato[].

Nota de realidad (ADR-0012): YOLO sobre cajas apiladas da un conteo APROXIMADO. Se usa
como sugerencia que el operario confirma con +/-, nunca como valor autoritativo. Por eso
la cantidad sugerida viaja en el estado del grafo, no en el Candidato ni en count_event.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from contracts.dtos import ResolucionResult
from ..domain import matcher


@dataclass(frozen=True)
class Deteccion:
    etiqueta: str                     # texto leido de la etiqueta (OCR)
    cantidad_sugerida: float | None   # de la deteccion de cajas (YOLO). Aproximada
    confianza: float


class Detector(Protocol):
    """Puerto de vision. La implementacion real es YOLO + OCR (Tesseract/PaddleOCR);
    es swappeable sin tocar nada mas. `detectar` NUNCA decide el conteo: solo propone texto."""
    def detectar(self, imagen: object) -> Deteccion: ...


class VisionResolver:
    fuente = "foto"

    def __init__(self, detector: "Detector") -> None:
        self._detector = detector

    def resolver(self, bodega_id: str, entrada: object) -> ResolucionResult:
        det = self._detector.detectar(entrada)            # imagen -> texto. LO UNICO nuevo
        return matcher.resolver(bodega_id, det.etiqueta)  # de aqui: identico a voz/texto

    def cantidad_sugerida(self, entrada: object) -> float | None:
        # Extra SOLO de vision, consumido en el paso 'esperando_cantidad'. El operario
        # confirma con +/-; jamas se guarda sin confirmar.
        return self._detector.detectar(entrada).cantidad_sugerida
