"""Saltar != cero. En el dataset real no hay UN SOLO cero y hay 79 negativos (P-02).
Sin esta regla, el descuadre es ruido."""
from __future__ import annotations
from typing import TYPE_CHECKING
from contracts.policy_result import PolicyResult, Severity, RequiredAction

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx


class CeroForzadoAlCerrar:
    nombre = "cero_forzado"

    def aplica(self, ctx: "ConteoCtx") -> bool:
        return ctx.cerrando_ubicacion

    def evaluar(self, ctx: "ConteoCtx") -> PolicyResult:
        faltantes = ctx.esperados_no_contados
        if not faltantes:
            return PolicyResult.passed(self.nombre)
        return PolicyResult(
            ok=False,                      # BLOQUEA el cierre hasta responder
            policy=self.nombre,
            severity=Severity.BLOCK,
            message=f"Faltan {len(faltantes)} referencias en esta ubicacion. Es 0 o te faltaron?",
            required_actions=[RequiredAction.CONFIRM_ZERO],
            evidence={"faltantes": faltantes[:20]},
        )
