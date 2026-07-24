# ADR-0012 — Visión por computador como fuente, no como capa

**Estado:** Aceptado

## Contexto
¿Agregar visión (OCR de etiquetas, detección de cajas apiladas) rompe la arquitectura?

## Decisión
**No.** La visión es un adaptador más dentro de `contexts/resolucion/adapters/`, y una `fuente` más en `count_event`.

## Qué cambia al agregarla
```
contexts/resolucion/adapters/vision.py    <- NUEVO. Devuelve ResolucionResult
contexts/resolucion/graph/nodes.py        <- 1 rama: si fuente == FOTO, usar vision
```

## Qué NO cambia
- `contracts/` — ya tiene `Fuente.FOTO`, `confianza`, `utterance`.
- `contracts/events.py` — `count_event` no gana ni una columna.
- `contexts/conteo/` — el dominio nunca se entera de por dónde entró el conteo.
- `apps/api` — mismo endpoint `/v1/resolver`, distinto payload.
- El schema de base de datos — cero migraciones.

## Por qué funciona
Es el pago del diseño de dos rutas (ADR-0007): la visión entra por la ruta asistida, produce `Candidato[]` igual que la voz, y converge en el mismo `RegistrarConteoCmd`. **La cámara es un sensor, no un modelo de dominio.**

## Nota de realidad
YOLO sobre cajas apiladas da conteo aproximado, no exacto. Se usa como *sugerencia de cantidad* que el operario confirma — nunca como valor autoritativo. Emite `confianza` y el dominio la trata como cualquier otra ruta asistida.
