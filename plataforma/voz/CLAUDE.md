# plataforma/voz/

Cliente ElevenLabs: STT (micrófono → texto) y TTS (texto → speaker). ADR-0014.

## Invariantes
- **La API key vive solo aquí** (desde `plataforma/config/settings.py`, que la lee del entorno).
  Nunca en el cliente, nunca en el repo. En Docker se inyecta por `.env`.
- **`sintetizar` solo vocaliza mensajes seguros.** `PolicyResult.message` y las preguntas del
  resolver nunca contienen la cantidad del ERP (ADR-0001). Prohibido pasar a `sintetizar`
  cualquier texto derivado de `stock_corte`. El sistema habla, pero nunca canta el número.
- **El STT no decide** (ADR-0007): solo transcribe. La validación la hace el dominio.
- La voz sigue siendo **secundaria** (ADR-0003): ningún flujo se completa solo por voz.

## Cómo lo consume el resto
`apps/api` compone el flujo: `transcribir` (audio del navegador) → `resolver_expresion` →
`sintetizar` (para que el sistema pregunte en voz alta). El dominio no importa este módulo.
