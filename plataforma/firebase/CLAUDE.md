# plataforma/firebase/

Firestore + Firebase Auth. **El lado de ESCRITURA del sistema.** (ADR-0015)

## Invariantes
- **Append-only.** `count_event` es una colección donde solo se agrega. Nunca update, nunca
  delete. Corregir = otro evento. (ADR-0005 sigue vigente)
- **El doc id ES el `event_id` del device** (UUID). Escribir el mismo dos veces es idempotente
  → offline sync gratis. (ADR-0010) Nunca dejes que Firestore genere el id.
- **Firestore guarda EVENTOS, no referencia.** El catálogo y el stock del ERP viven en
  Postgres (read-only) — no los copies aquí. Dos stores, cero datos compartidos: esa frontera
  es lo que evita el problema de "dos maestros" (P-08).
- **`conteo` nunca importa Firestore.** Escribe contra el puerto `EventStore` (`event_store.py`).
  El adapter Firestore es una implementación, intercambiable por Postgres si algún día se unifica.
- Firebase Auth da la identidad del operario; `operator_id` sigue yendo **por evento** (ADR-0006).

## Realtime
Los listeners de Firestore alimentan el dashboard del pitch en vivo. Eso es lo único que
ADR-0011 (sin WebSocket) cede: el **dashboard** puede recibir push. El **flujo de conteo**
sigue siendo request/response e idempotente por `event_id` — no depende del socket.
