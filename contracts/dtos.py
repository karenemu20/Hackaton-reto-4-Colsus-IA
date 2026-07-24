"""DTOs de frontera. Lo unico que cruza entre contextos y hacia apps/api."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Candidato:
    """Salida del resolver. NUNCA incluye stock del ERP (conteo ciego, ADR-0001)."""
    sku: str | None
    nombre: str              # nombre_raw, como se ve en la estanteria
    unidad_esperada: str
    confianza: float
    atributo_distintivo: str | None = None  # "basmati" vs "" -> la pregunta a hacer


@dataclass(frozen=True)
class ResolucionResult:
    candidatos: list[Candidato]
    requiere_desambiguacion: bool
    pregunta: str | None = None


@dataclass(frozen=True)
class RegistrarConteoCmd:
    session_id: str
    bodega_id: str
    ubicacion: str | None
    sku: str | None
    utterance: str | None
    cantidad: float
    unidad: str
    packaging: str | None
    fuente: str
    confianza: float | None
    operator_id: str
    device_id: str
    event_id: str            # lo trae el device
    override_motivo: str | None = None


@dataclass(frozen=True)
class RegistrarConteoResult:
    aceptado: bool
    policy_results: list = field(default_factory=list)
    acciones_requeridas: list[str] = field(default_factory=list)
