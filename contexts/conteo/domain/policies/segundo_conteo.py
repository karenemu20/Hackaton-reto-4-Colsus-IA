"""El override siempre gana, pero siempre cuesta un recuento.
(glosario: Override, Segundo conteo · hotspot H-03)

Invariante de conteo/CLAUDE.md: 'El override del operario siempre gana, siempre se
audita, y siempre dispara SECOND_COUNT.' Ese invariante se AFIRMABA pero no se
GARANTIZABA en codigo: solo `anomalia_magnitud` sugeria SECOND_COUNT, y solo cuando
ella misma disparaba. Un override sobre un conteo que no disparo anomalia (p.ej. una
unidad rara que el operario fuerza) no generaba recuento -> hueco entre invariante y
codigo. Esta politica lo cierra: si hay `override_motivo`, hay segundo conteo, venga
de la ruta que venga.

H-03: el costo de mentir con "estoy seguro" es tener que recontar. La auditoria por
`operator_id` deja la senal para vigilar la tasa de override por operario.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from contracts.policy_result import PolicyResult, Severity, RequiredAction

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx


class SegundoConteo:
    nombre = "segundo_conteo"

    def aplica(self, ctx: "ConteoCtx") -> bool:
        return bool(ctx.override_motivo)

    def evaluar(self, ctx: "ConteoCtx") -> PolicyResult:
        return PolicyResult(
            ok=True,                       # el override GANA: el conteo se acepta
            policy=self.nombre,
            severity=Severity.WARN,
            message="Registrado. Queda un recuento pendiente para confirmar.",
            required_actions=[RequiredAction.SECOND_COUNT],
            evidence={"tipo": "OVERRIDE", "motivo": ctx.override_motivo,
                      "operator_id": ctx.operator_id},
        )
