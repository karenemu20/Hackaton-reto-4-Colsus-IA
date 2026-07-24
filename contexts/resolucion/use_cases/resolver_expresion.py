"""Caso de uso que llama el nodo del grafo. Un nodo NUNCA llama al matcher ni a un adapter
directo: llama esto (ADR-0007). Y este caso de uso NO sabe por que fuente entro el conteo:
elige el resolver por `fuente` y devuelve ResolucionResult. La fuente muere aqui."""
from __future__ import annotations
from dataclasses import dataclass

from contracts.dtos import ResolucionResult
from ..adapters.registry import RESOLVERS


@dataclass(frozen=True)
class ResolverExpresionCmd:
    bodega_id: str
    fuente: str
    entrada: object          # str (voz/texto) | bytes (foto). El resolver sabe leerla


def resolver_expresion(cmd: ResolverExpresionCmd) -> ResolucionResult:
    resolver = RESOLVERS.get(cmd.fuente)
    if resolver is None:
        raise ValueError(f"fuente sin resolver: {cmd.fuente}")
    return resolver.resolver(cmd.bodega_id, cmd.entrada)
