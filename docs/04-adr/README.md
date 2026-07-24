# ADRs

Formato MADR. Estos son el **porqué**. Los `CLAUDE.md` son el **qué está prohibido**.
Un agente obedece los CLAUDE.md; un humano audita los ADR.

| # | Decisión | Estado |
|---|---|---|
| [0001](0001-blind-count.md) | Conteo ciego: nunca mostrar la cantidad del ERP | Aceptado |
| [0002](0002-erp-read-only-adapter-seam.md) | ERP como adaptador de solo lectura (seam explícito) | Aceptado |
| [0003](0003-buttons-first-voice-as-output.md) | Botones primero, voz secundaria | Aceptado (STT → ADR-0014) |
| [0004](0004-location-scan-as-catalog-scoping.md) | Escaneo de ubicación como poda de catálogo | Aceptado |
| [0005](0005-event-log-append-only.md) | El log de eventos es el registro de verdad | Aceptado (motor → ADR-0015) |
| [0006](0006-biometric-auth-roles.md) | Biometría para autenticación y relevo | Aceptado |
| [0007](0007-langgraph-solo-ruta-asistida.md) | LangGraph solo en la ruta asistida | Aceptado |
| [0008](0008-policy-result-acciones.md) | PolicyResult con acciones requeridas, no booleano | Aceptado |
| [0009](0009-monolito-por-contexto.md) | Monolito modular por contexto, un desplegable | Aceptado |
| [0010](0010-offline-diferido-seam-listo.md) | Offline diferido con seam listo | Aceptado |
| [0011](0011-http-sin-websocket.md) | HTTP plano, sin WebSocket | Aceptado (matizado por 0015) |
| [0012](0012-vision-como-fuente.md) | Visión por computador como fuente, no como capa | Aceptado |
| [0013](0013-stack-congelado-y-alcance.md) | Stack congelado y alcance del hackathon | Aceptado |
| [0014](0014-stt-elevenlabs.md) | Voz por ElevenLabs: STT + TTS | Aceptado |
| [0015](0015-firebase-plano-datos.md) | Firestore escritura + Postgres referencia | Aceptado |

## Si el repo `inventory-count-docs` ya tiene 0001–0006

Reconcíliense antes de mezclar. Dos cosas a revisar:

1. **El 0005 original mezclaba dos decisiones**: log append-only + local-first. Aquí quedaron separados — 0005 es solo el log, y local-first pasó a **0010 (offline diferido)**. Si dejan la versión vieja, contradice a 0010 y un agente va a intentar implementar sync completo.
2. **La versión de aquel repo gana en contenido** si es más detallada. Estos seis se reconstruyeron a partir de las decisiones tomadas, no se copiaron del original.
