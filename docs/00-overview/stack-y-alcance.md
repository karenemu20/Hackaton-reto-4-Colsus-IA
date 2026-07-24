# Stack y alcance — decisión congelada

Este documento resume el stack y el alcance ya **decididos** (ADR-0013, 0014, 0015). Es el
"hablamos el mismo idioma" para las 5 personas. Si algo aquí te sorprende, la fuente es el
ADR citado, no este resumen.

## Regla de gobernanza (la que evita las 5 arquitecturas)

> **Toda herramienta del stack apunta a un ADR, o se convierte en uno.**

Un nombre en una lista no es una decisión. Si quieres meter algo nuevo que contradice un ADR,
se escribe el ADR que lo reemplaza y se convence a las 5 personas. Así entró ElevenLabs
(ADR-0014) y así entró Firebase (ADR-0015): con su razón y sus consecuencias escritas, no
como un ítem suelto en un chat.

## El stack (congelado, ADR-0013)

| Capa | Herramienta | ADR |
|---|---|---|
| Backend / orquestación | Python + FastAPI | — |
| Lógica de IA (ruta asistida) | LangGraph, solo en `resolucion` | 0007 |
| Visión | YOLO + OCR, como adapter | 0012 |
| Voz (STT) | **ElevenLabs Scribe** | 0014 |
| Referencia + búsqueda semántica | Postgres + pgvector (espejo ERP, read-only) | 0002, 0015 |
| Escritura / realtime / auth | **Firebase** (Firestore + Auth) | 0015 |
| Frontend | React PWA mobile-first — **un solo framework** | — |

## Cómo caben ElevenLabs y Firebase sin romper la arquitectura

La clave es que **ninguno de los dos toca el dominio**. Entran por costuras que ya existían:

- **ElevenLabs** es un `Transcriptor` (puerto) dentro de `resolucion/adapters/voz_elevenlabs.py`.
  Convierte audio → texto y de ahí sigue el mismo `matcher` que texto y foto. Es una fuente
  más de la ruta asistida: **1 adapter + 1 línea en el registry**, cero cambios aguas abajo.
  La voz sigue siendo secundaria (ADR-0003): botones primero, nunca obligatoria.

- **Firebase** entra por una **frontera de responsabilidad sin datos compartidos** (ADR-0015):
  Firestore guarda **eventos** (lo que escribimos, append-only), Postgres guarda **referencia
  del ERP** (lo que solo leemos) + embeddings. Ningún dato vive en los dos → **no es** el
  problema de "dos maestros" (P-08). `conteo` escribe contra el puerto `EventStore`, no contra
  Firestore directo: intercambiable por Postgres si algún día se unifica.

## Lo que se cedió (dicho explícito, para el pitch)

- El audio de voz **ahora viaja** y la voz **exige señal** (ADR-0014). Mitigado: demo con wifi
  (S-03) y voz opcional. Si no hay señal → botones/escaneo, nada se bloquea.
- El **dashboard** usa realtime de Firestore, así que ahí sí hay push del server (ADR-0015
  matiza ADR-0011). El **flujo de conteo** sigue request/response e idempotente por `event_id`.

## Lo que NO construimos (sigue firme)

Un "AIOS Core / Cerebro genérico" como componente. El invariante ADR-0007 manda: **el dominio
decide, la IA interpreta**. "Colsus Brain IA" es el nombre de pitch; la reusabilidad se
**muestra** en los seams (contracts, ERP ACL, adapters de voz/visión), no se **programa** como
un mega-módulo este fin de semana. (ADR-0013)

## El árbol de decisión sigue igual

Dónde va tu código no cambió: ver `docs/00-overview/README.md`. Voz, texto y foto son
adapters de `resolucion`; las reglas viven en `conteo`; la escritura va por `plataforma/firebase`;
la referencia y la semántica por Postgres. El dominio no se entera de nada de esto.
