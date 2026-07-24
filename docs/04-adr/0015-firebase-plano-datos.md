# ADR-0015 — Plano de datos: Firestore para escritura, Postgres para referencia

**Estado:** Aceptado (decisión del lead) — **modifica ADR-0005 y ADR-0011**

## Contexto
ADR-0005 puso el log append-only en Postgres. El lead quiere Firebase para ir rápido:
deploy inmediato, realtime para el dashboard del pitch, y Firebase Auth para la identidad
sin montar auth propia. El riesgo obvio es caer en "dos maestros" — el mismo problema que el
proyecto existe para exponer (P-08, P-10). Se evita con una **frontera de responsabilidad
sin datos compartidos**.

## Decisión
Dos stores, con datos que **no se solapan**:

| Store | Qué guarda | Modo |
|---|---|---|
| **Firestore** | `count_event`, eventos de calidad, sesiones | escritura, append-only |
| **Postgres + pgvector** | espejo del ERP (catálogo, stock del corte) + embeddings | **read-only** |

- **Firestore = lo que escribimos nosotros** (eventos). **Postgres = lo que solo leemos**
  (referencia del ERP, ADR-0002). Ningún dato vive en los dos → no hay dos fuentes de verdad
  del mismo hecho, no hay sync que conciliar. La reconciliación los cruza en
  `contexts/calidad_dato` (leer eventos de Firestore + referencia de Postgres).

**Lo que sobrevive de ADR-0005:** append-only, nunca update/delete, corregir = nuevo evento.
**Lo que sobrevive de ADR-0010:** el `doc id` de Firestore **es** el `event_id` del device
→ sync idempotente por construcción.

## Consecuencias
- `conteo` escribe contra el puerto `EventStore` (`plataforma/firebase/event_store.py`), no
  contra Firestore directo. Cambiar Firestore por Postgres luego = un adapter, cero cambios
  en el dominio.
- **Modifica ADR-0011:** los listeners de Firestore dan realtime al **dashboard** (hay push
  del server). Es lo único que se cede. El **flujo de conteo** sigue request/response e
  idempotente por `event_id` — no depende del socket, así que el seam de offline no se rompe.
- Firebase Auth da la identidad; `operator_id` sigue yendo **por evento** (ADR-0006).
- Las vistas SQL `cobertura`/`reconciliacion` de `schema.sql` quedan como la variante
  "todo-en-Postgres" (target de portabilidad). En el build del hackathon, esa agregación se
  hace en app leyendo Firestore + Postgres.

## Alternativa descartada
*Todo en Postgres (ADR-0005 puro)*: más limpio conceptualmente, pero sin realtime fácil ni
Firebase Auth, y más setup. *Todo en Firebase*: pierde pgvector, que es el motor de la
búsqueda semántica. La división por responsabilidad se queda con lo mejor de cada uno sin el
costo de sincronizarlos.
