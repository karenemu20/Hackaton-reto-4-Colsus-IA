"""El 9-vs-90. Mediana del catalogo = 12 (ver context/03-hallazgos.md P-07)."""
from __future__ import annotations
from typing import TYPE_CHECKING
from contracts.policy_result import PolicyResult, Severity, RequiredAction

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx


class DetectarAnomaliaMagnitud:
    nombre = "anomalia_magnitud"
    FACTOR = 5  # umbral por item, nunca global

    def aplica(self, ctx: "ConteoCtx") -> bool:
        # Sin referencia del corte (item sin SKU / no matcheado) NO hay anomalia posible:
        # ese caso es MISSING_SKU en calidad_dato, no un descuadre de magnitud. Decidido
        # a proposito: no inventamos una linea base que no existe (P-01, H-04).
        return ctx.esperado_erp is not None and ctx.esperado_erp > 0

    def evaluar(self, ctx: "ConteoCtx") -> PolicyResult:
        ratio = ctx.cantidad / ctx.esperado_erp
        if 1 / self.FACTOR <= ratio <= self.FACTOR:
            return PolicyResult.passed(self.nombre)
        return PolicyResult(
            ok=True,                       # NO bloquea: el operario siempre puede ganar
            policy=self.nombre,
            severity=Severity.WARN,
            # INVARIANTE ADR-0001: el mensaje NUNCA contiene ctx.esperado_erp
            message="Ese numero no coincide con lo que tenemos. Como lo contaste?",
            required_actions=[
                RequiredAction.CONFIRM_PACKAGING,   # casi siempre es empaque, no conteo
                RequiredAction.OFFER_ALTERNATIVES,
                RequiredAction.SECOND_COUNT,        # si hace override, se recuenta
            ],
            evidence={"ratio": round(ratio, 2), "tipo": "MAGNITUDE_ANOMALY"},
        )
