# ADR-0003 — Botones primero, voz secundaria

**Estado:** Aceptado — **el STT on-device fue reemplazado por ElevenLabs (ADR-0014).** El
invariante de este ADR (voz secundaria, botones primero, nunca obligatoria) sigue vigente;
solo cambió *dónde* corre el STT.

## Contexto
El reto sugiere voz como captura natural. La experiencia previa con dispositivos Zebra en bodega muestra lo contrario: el español regional colombiano rompe el STT, y el ruido de bodega empeora el WER. Una solución que **requiere** voz falla frente al operario real.

## Decisión
La UI se opera con **botones grandes y escaneo**. La voz es entrada secundaria, local-first (Web Speech API en el dispositivo, ADR-0011). **Ningún flujo puede completarse solo por voz.**

## Consecuencias
- Target táctil mínimo 64px: el operario tiene las manos ocupadas, frío y humedad.
- La voz entra por la ruta asistida (ADR-0007), nunca por la ruta crítica.
- El STT corre en el cliente: el audio nunca viaja, y funciona sin señal.
- En el demo, la voz se muestra como capacidad — no como el camino principal.

## Alternativa descartada
*Voz como modalidad primaria*: es el error que hace que estas soluciones se abandonen en semana dos.
