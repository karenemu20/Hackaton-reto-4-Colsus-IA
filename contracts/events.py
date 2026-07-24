"""El log de eventos. Columna vertebral del sistema.

INVARIANTE: append-only. Nunca UPDATE, nunca DELETE.
Corregir un conteo = emitir otro evento. Ver ADR-0005.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID


class Fuente(str, Enum):
    SCAN = "scan"        # ruta rapida
    MANUAL = "manual"    # botones
    VOZ = "voz"          # ruta asistida
    FOTO = "foto"


class SyncState(str, Enum):
    LOCAL = "local"
    SYNCED = "synced"


@dataclass(frozen=True)
class ConteoRegistrado:
    """Un conteo capturado. El evento que mas se emite."""
    event_id: UUID          # generado en el DISPOSITIVO -> sync idempotente (ADR-0010)
    session_id: UUID
    ts: datetime
    operator_id: str
    bodega_id: str
    ubicacion: str | None
    sku: str | None         # NULLABLE A PROPOSITO -> 18% del maestro no tiene codigo (P-01)
    utterance: str | None   # lo que dijo/tecleo el operario, EN CRUDO. No re-derivable
    nombre_resuelto: str | None
    cantidad: float
    unidad: str
    packaging: str | None   # "caja x 24" -> el 9-vs-90
    confianza: float | None # del resolver; None si vino por scan
    override_motivo: str | None
    device_id: str
    sync_state: SyncState = SyncState.LOCAL


class TipoCalidadDato(str, Enum):
    MISSING_SKU = "MISSING_SKU"
    NAME_VARIANT = "NAME_VARIANT"
    UNIT_MISMATCH = "UNIT_MISMATCH"
    MAGNITUDE_ANOMALY = "MAGNITUDE_ANOMALY"
    STALE_SYSTEM_STOCK = "STALE_SYSTEM_STOCK"
    MASTER_DATA_DUPLICATE = "MASTER_DATA_DUPLICATE"
    AMBIGUOUS_RESOLUTION = "AMBIGUOUS_RESOLUTION"


@dataclass(frozen=True)
class EventoCalidadDato:
    """El backlog del MDM, generado solo. Este es el money shot del demo."""
    event_id: UUID
    origen_event_id: UUID | None
    ts: datetime
    tipo: TipoCalidadDato
    severidad: str
    bodega_id: str
    sku: str | None
    evidencia: dict = field(default_factory=dict)
    accion_sugerida: str = ""


@dataclass(frozen=True)
class UbicacionCerrada:
    event_id: UUID
    session_id: UUID
    ts: datetime
    ubicacion: str
    esperados_no_contados: list[str] = field(default_factory=list)  # -> CONFIRM_ZERO
