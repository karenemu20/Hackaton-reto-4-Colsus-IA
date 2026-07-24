"""kilos vs gramos. Ojo P-06: el ERP mismo tiene 'Unidad' con decimales
(HUEVOS DE GALLINA 2809.5). No validar contra el maestro, validar la CAPTURA."""
from __future__ import annotations
from typing import TYPE_CHECKING
from contracts.policy_result import PolicyResult, Severity, RequiredAction

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx


class ValidarUnidad:
    nombre = "validar_unidad"
    CONTABLES = {"Unidad", "Portion"}

    def aplica(self, ctx: "ConteoCtx") -> bool:
        return ctx.unidad is not None

    def evaluar(self, ctx: "ConteoCtx") -> PolicyResult:
        if ctx.unidad_esperada and ctx.unidad != ctx.unidad_esperada:
            return PolicyResult(
                ok=True, policy=self.nombre, severity=Severity.WARN,
                message=f"Este item se lleva en {ctx.unidad_esperada}. Confirmas?",
                required_actions=[RequiredAction.CONFIRM_UNIT],
                evidence={"tipo": "UNIT_MISMATCH", "dicho": ctx.unidad,
                          "maestro": ctx.unidad_esperada},
            )
        if ctx.unidad in self.CONTABLES and ctx.cantidad % 1 != 0 and ctx.fuente != "scan":
            return PolicyResult(
                ok=True, policy=self.nombre, severity=Severity.WARN,
                message="Contaste una fraccion de una unidad contable. Es correcto?",
                required_actions=[RequiredAction.CONFIRM_UNIT],
                evidence={"tipo": "UNIT_MISMATCH", "cantidad": ctx.cantidad},
            )
        return PolicyResult.passed(self.nombre)
