"""El puerto que hace intercambiables a voz, texto y foto."""
from __future__ import annotations
from typing import Protocol
from contracts.dtos import ResolucionResult


class Resolver(Protocol):
    """Toda fuente de la ruta asistida implementa esto. Cada una recibe una entrada CRUDA
    distinta (string de voz/texto, bytes de imagen) y devuelve el MISMO ResolucionResult.

    Esa igualdad de SALIDA es la costura entera: como los tres producen `Candidato[]`,
    el grafo y el dominio no distinguen por donde entro el conteo. Agregar una fuente es
    agregar un Resolver; nada aguas abajo cambia (ADR-0012).
    """
    fuente: str

    def resolver(self, bodega_id: str, entrada: object) -> ResolucionResult: ...
