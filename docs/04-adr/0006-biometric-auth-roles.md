# ADR-0006 — Biometría para autenticación y relevo de turno

**Estado:** Aceptado

## Contexto
El operario tiene las manos ocupadas, guantes, y trabaja en frío y humedad. Una contraseña en un móvil sujeto al brazo es fricción pura, y en la práctica termina en una sesión compartida entre varias personas — lo que destruye la trazabilidad del conteo.

## Decisión
Autenticación **biométrica** (huella / rostro del dispositivo). La sesión de conteo tiene un operario identificado en cada evento, no en la sesión.

## Consecuencias
- `count_event.operator_id` va **por evento**, no por sesión: un relevo a mitad de bodega no rompe la atribución.
- El agregado `ConteoSesion` soporta cambio de operario sin cerrar y reabrir.
- Habilita `SUPERVISOR_APPROVAL` como acción requerida: el supervisor autentica en el mismo dispositivo, en el sitio.
- Auditoría real de overrides: quién dijo "estoy seguro" y cuándo.

## Duda abierta
¿El manager que abre la sesión es una persona distinta del operario que cuenta, en la operación real de Colsubsidio? Sin confirmar. Afecta al ciclo de vida de `ConteoSesion`. Registrada en `docs/02-event-storming/hotspots.md`.
