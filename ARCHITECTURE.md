# Arquitectura — una página

Monorepo · monolito modular · **organizado por contexto de negocio, no por capa**.

## Por qué no por capas

El cambio que tenemos que absorber no es tecnológico (cambiar Postgres), es **de negocio**: una regla nueva, una bodega que cuenta distinto, un modo de captura nuevo. Ese cambio es *vertical*.

- Con capas, "requerir lote en refrigerados" toca `domain/` + `application/` + `agent/` + `api/`. Cuatro carpetas, cuatro PRs, cuatro conflictos.
- Con contextos, toca `contexts/conteo/domain/policies/`. Una carpeta, un dueño.

Las capas no desaparecen: **bajan un nivel** y viven dentro de cada contexto (`domain/ use_cases/ adapters/`).

## Las dos rutas

```
RUTA RÁPIDA (determinística, sin LLM)     RUTA ASISTIDA (ambigua)
scan código · scan ubicación              voz · texto · foto
        │                                         │
producto resuelto sin duda            contexts/resolucion  (LangGraph)
        │                              podar por bodega → embeddings
botones grandes · empaque              → candidatos → desambiguar
        │                                         │
        └──────────────┬──────────────────────────┘
                       ▼
              RegistrarConteoCmd            ← contracts/dtos.py
                       ▼
              contexts/conteo               ← AQUÍ y solo aquí viven las reglas
                       ▼
              count_event (append-only)     ← contracts/events.py
                       ▼
        contexts/calidad_dato  ·  sync → Postgres  ·  ERP (ACL, read-only)
```

El dominio no sabe por qué ruta entró el conteo. **El 80% de los conteos son scan + botones y no pagan latencia de LLM.**

## Aislamiento: una sola regla

> **Un contexto nunca importa a otro contexto. Solo `contracts/`.**

Eso es lo que permite sacar `resolucion` como servicio aparte en seis meses sin tocar `conteo`. Las capas no dan ese aislamiento; esta regla sí.

## Modelo de datos: el log es la verdad

El registro de verdad es la secuencia de `count_event`, no una tabla de cantidades. Cuatro razones:

1. El **relevo de turno** hereda un log, no un estado.
2. El **override** ("estoy seguro") tiene que quedar auditado.
3. El **segundo conteo** no sobrescribe al primero, lo acompaña.
4. **Offline**: un append-only sincroniza trivialmente; un `UPDATE` genera conflictos.

`cobertura` y `reconciliacion` son proyecciones — reconstruibles del log.

## Frontera con el ERP

`plataforma/erp/` es un ACL de solo lectura, sembrado con los CSV reales del corte. Es un **seam explícito**, marcado en el diagrama del pitch: *"aquí entra su ERP real, y nada de lo demás cambia"*.
