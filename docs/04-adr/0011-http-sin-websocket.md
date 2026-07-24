# ADR-0011 — HTTP plano, sin WebSocket

**Estado:** Aceptado (alcance hackathon) — **matizado por ADR-0015.** El **dashboard** usa
realtime de Firestore (hay push del server). El **flujo de conteo** sigue siendo HTTP
request/response e idempotente por `event_id`. El STT dejó de ser on-device (ADR-0014).

## Contexto
Se planteó WebSocket para la conversación por voz con el agente.

## Decisión
Todo el flujo es HTTP request/response. Sin WS.

## Razones
1. **El flujo ya es request/response.** Enunciado → candidatos → confirmación → guardar. No hay push del servidor al cliente; el operario siempre inicia.
2. **El STT es del lado del cliente.** Web Speech API transcribe en el dispositivo y envía texto. El audio nunca viaja. Esto además es local-first y resuelve el español regional mejor que un round-trip.
3. **WS rompe el seam de offline.** Una conexión persistente no encola: si se cae, se pierde el turno. Un POST con `event_id` del device reintenta solo. (ADR-0010)
4. **Costo de reconexión.** En una bodega con señal intermitente, el manejo de reconexión y estado del socket cuesta más horas de las que tenemos, y falla justo en el demo.

## Cuándo sí valdría
Streaming token-a-token de la respuesta del LLM. Pero el resolver devuelve una lista de candidatos, no prosa: no hay nada que streamear. Y SSE resolvería ese caso sin socket bidireccional.

## Consecuencia
Latencia percibida sube ~100ms en la ruta asistida. Irrelevante: la ruta rápida (80% de los conteos) ni pasa por ahí.
