# ADR-0010 — Offline diferido, seam listo

**Estado:** Aceptado (alcance hackathon)

## Contexto
Las bodegas de Piscilago no garantizan cobertura. Pero implementar sync bidireccional real en 48 horas mata el demo.

## Decisión
Offline **diferido**. Pero el seam queda construido:
- `event_id` es un UUID generado **en el dispositivo**, no en la base → el sync es idempotente por construcción.
- `count_event.sync_state` existe desde el día 1 (`local` | `synced`).
- El log es append-only → sincronizar es solo insertar lo que falta.

## Consecuencias
- Para el demo hay wifi (supuesto S-01, se dice explícito en el pitch).
- Migrar a offline real no requiere cambiar el modelo de datos: se agrega la cola local y el reintento.
- **Si `event_id` lo generara la base, no habría offline posible sin rediseñar el schema.** Esa columna es la decisión que importa.

## Alternativa descartada
*Implementar offline completo*: 12+ horas de las 48, contra un riesgo que en el demo no se materializa.
