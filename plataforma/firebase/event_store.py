"""Log de eventos append-only sobre Firestore. ADR-0015.

Decidido por el lead: Firebase para ir rapido (deploy, realtime, Firebase Auth). Firestore
es el LADO DE ESCRITURA: count_event, eventos de calidad, sesiones. Postgres + pgvector
queda como espejo READ-ONLY del ERP + embeddings (busqueda semantica), NO del log.

El invariante de ADR-0005 SOBREVIVE intacto: append-only, nunca update, nunca delete;
corregir = emitir otro evento. Y el de ADR-0010: el doc id de Firestore ES el `event_id`
generado en el device -> el sync es idempotente por construccion (escribir el mismo id dos
veces no duplica).

Frontera limpia (por eso NO es el anti-patron de 'dos maestros', P-08/P-10):
  - Firestore: EVENTOS (lo que escribimos nosotros).
  - Postgres : REFERENCIA del ERP (lo que solo leemos) + embeddings.
Ningun dato vive en las dos. La reconciliacion cruza ambos en `contexts/calidad_dato`.
"""
from __future__ import annotations
from typing import Protocol


class EventStore(Protocol):
    """Puerto del log. `conteo` escribe por aqui; nunca conoce Firestore directamente."""
    def append(self, evento) -> None: ...              # nunca update/delete (ADR-0005)
    def por_sesion(self, session_id: str) -> list: ...


class FirestoreEventStore:
    """STUB en memoria para el esqueleto. Real: firebase_admin.firestore,
    coleccion 'count_event', `doc(evento.event_id).set(...)` -> idempotente por event_id."""

    def __init__(self) -> None:
        self._eventos: list = []

    def append(self, evento) -> None:
        # idempotente: si ya existe ese event_id, no se duplica (como el set() de Firestore)
        if any(getattr(e, "event_id", None) == getattr(evento, "event_id", None)
               for e in self._eventos):
            return
        self._eventos.append(evento)

    def por_sesion(self, session_id: str) -> list:
        return [e for e in self._eventos if getattr(e, "session_id", None) == session_id]
