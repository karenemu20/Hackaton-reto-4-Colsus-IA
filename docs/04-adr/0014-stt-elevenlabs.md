# ADR-0014 — Voz por ElevenLabs: STT (Scribe) + TTS

**Estado:** Aceptado (decisión del lead) — **modifica ADR-0003 y ADR-0011**

## Contexto
ADR-0003/0011 fijaron STT **on-device** (Web Speech API) para que el audio no viajara y
funcionara sin señal. Realidad del hackathon: hay créditos de ElevenLabs, el demo tiene wifi
(S-03), y ElevenLabs Scribe da mejor precisión en español que Web Speech. El lead prioriza
que funcione y rápido.

## Decisión
El STT de la ruta asistida lo hace **ElevenLabs Scribe** (nube). El audio se transcribe en
el servidor/servicio y de ahí sigue como texto al `matcher`.

**Lo que NO cambia (el corazón de ADR-0003 sobrevive):** la voz es **secundaria**. Botones y
escaneo primero; **ningún flujo se completa solo por voz**. La voz entra solo por la ruta
asistida (ADR-0007), nunca por la crítica.

## Consecuencias
- El audio ahora **sí viaja** y la voz **exige señal**. Aceptado: el demo tiene wifi (S-03) y
  la voz es opcional — si no hay señal, el operario usa botones/escaneo y no se bloquea nada.
- Arquitectónicamente es **gratis**: ElevenLabs es un `Transcriptor` (puerto) dentro de
  `contexts/resolucion/adapters/voz_elevenlabs.py`. Devuelve texto → converge en el mismo
  `Candidato[]` que texto y foto. Cero cambios aguas abajo (misma prueba que ADR-0012).
- La `ELEVENLABS_API_KEY` vive en `plataforma/config`, nunca en el cliente.
- El STT nunca decide: solo transcribe (ADR-0007 intacto).

## TTS — el sistema también habla
Se añade **salida de voz** (ElevenLabs TTS): el sistema lee en voz alta la pregunta del
resolver ("¿Cuál aguardiente?") y los `PolicyResult.message`, por el speaker del teléfono.

**Seguro por diseño respecto al conteo ciego (ADR-0001):** `sintetizar` solo vocaliza textos
que ya se garantizaban sin la cantidad del ERP — `pregunta` y `PolicyResult.message` nunca la
contienen. El sistema habla, pero **nunca canta el número del sistema**. Prohibido pasar a
`sintetizar` cualquier texto derivado de `stock_corte`.

- Requiere HTTPS en el cliente: el micrófono del navegador solo va en contexto seguro
  (`https://` o `localhost`). Ver `docs/00-overview/despliegue.md`.
- La voz de salida es un extra, no un requisito: si no hay créditos/señal, la UI sigue con
  texto y botones (ADR-0003).

## Alternativa descartada
*Mantener Web Speech on-device*: mejor para offline, pero peor precisión en español regional
y no aprovecha los créditos. Reversible: cambiar el `Transcriptor` por uno on-device es una
línea en el registry, sin tocar nada más.
