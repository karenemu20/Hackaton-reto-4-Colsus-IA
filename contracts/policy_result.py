"""Resultado de evaluar una política de dominio.

INVARIANTE: NO es booleano. Sus reglas son de dos especies:
  - las que validan            -> ok=False detiene el guardado
  - las que cambian el flujo   -> ok=True pero con required_actions

Si esto fuera bool, RequirePhoto/SecondCount/SupervisorApproval no caben,
y la lógica termina infiltrándose en el grafo. Ver ADR-0008.
"""
from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    WARN = "warn"       # se puede continuar con override auditado
    BLOCK = "block"     # no se guarda


class RequiredAction(str, Enum):
    CONFIRM_PACKAGING = "confirm_packaging"   # ¿cajas o unidades? el 9-vs-90
    CONFIRM_UNIT = "confirm_unit"
    CONFIRM_ZERO = "confirm_zero"             # saltar != cero
    REQUIRE_PHOTO = "require_photo"
    REQUIRE_LOT = "require_lot"
    SECOND_COUNT = "second_count"
    SUPERVISOR_APPROVAL = "supervisor_approval"
    OFFER_ALTERNATIVES = "offer_alternatives"  # sin revelar el valor del ERP


@dataclass(frozen=True)
class PolicyResult:
    ok: bool
    policy: str
    severity: Severity = Severity.INFO
    message: str = ""                              # texto para el operario, nunca revela el stock ERP
    required_actions: list[RequiredAction] = field(default_factory=list)
    evidence: dict = field(default_factory=dict)   # para el evento de calidad de dato

    @staticmethod
    def passed(policy: str) -> "PolicyResult":
        return PolicyResult(ok=True, policy=policy)
