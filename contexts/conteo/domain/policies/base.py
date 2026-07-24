from __future__ import annotations
from typing import Protocol, TYPE_CHECKING
from contracts.policy_result import PolicyResult

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx


class Politica(Protocol):
    """Contrato de toda regla de negocio. Dos metodos, nada mas.

    aplica()  -> decide si esta regla toca este contexto (barato, sin IO)
    evaluar() -> devuelve PolicyResult, NUNCA bool (ADR-0008)

    `ctx` es SIEMPRE un ConteoCtx (domain/conteo_ctx.py), no un dict ni el DTO crudo.
    """
    nombre: str

    def aplica(self, ctx: "ConteoCtx") -> bool: ...
    def evaluar(self, ctx: "ConteoCtx") -> PolicyResult: ...
