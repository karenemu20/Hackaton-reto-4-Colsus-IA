"""STUB de vision para el esqueleto/demo. SUSTITUIR por el adapter real de YOLO + OCR.

Simula lo que devolveria el pipeline real al fotografiar una botella de agua en la
estanteria: leyo la etiqueta 'AGUA BOTELLA' y estimo ~24 unidades (una bandeja).
Cambiar esta clase por el detector real no toca ningun otro archivo.
"""
from __future__ import annotations
from .vision import Deteccion


class DetectorStub:
    def detectar(self, imagen: object) -> Deteccion:
        return Deteccion(etiqueta="AGUA BOTELLA", cantidad_sugerida=24, confianza=0.83)
