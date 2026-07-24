"""voz y texto: la entrada YA es texto.

La voz llega transcrita por el cliente (Web Speech API / STT local, ADR-0003 y ADR-0011);
el backend nunca ve audio. El texto tecleado llega tal cual. Ambos van directo al matcher.
"""
from __future__ import annotations
from contracts.dtos import ResolucionResult
from ..domain import matcher


class ExpresionResolver:
    def __init__(self, fuente: str) -> None:
        self.fuente = fuente

    def resolver(self, bodega_id: str, entrada: object) -> ResolucionResult:
        return matcher.resolver(bodega_id, str(entrada))
