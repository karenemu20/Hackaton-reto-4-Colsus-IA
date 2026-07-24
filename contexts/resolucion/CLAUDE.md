# contexts/resolucion/

Expresión (voz/texto/foto) → candidatos de referencia. **LangGraph vive aquí y solo aquí.**

## Invariantes — no negociables
- **Podar el catálogo por `bodega_id` ANTES de embeddings. Siempre.** Es 16x de reducción y sale gratis. (P-03)
- Nunca `LIKE '%agua%'` sobre el catálogo global: devuelve agua, aguardiente, aguacate y agujas.
- El LLM interpreta lenguaje. **NUNCA decide si un conteo es válido** ni aplica una regla. (ADR-0007)
- Un nodo del grafo solo llama `use_cases/`. Nunca repositorios, nunca políticas, nunca el ERP.
- Empate entre candidatos → **devolver el atributo distintivo como pregunta**, no elegir el top-1. (P-04)
- Comparar sobre `nombre_norm`. Mostrar `nombre_raw`. (P-05)
- NUNCA `import contexts.conteo`. Solo `contracts/`.

## El grafo (ruta asistida únicamente)
`esperando_producto → resolviendo → desambiguando → esperando_cantidad → confirmando → emitiendo_comando`

La ruta rápida (scan → botones) **no pasa por aquí**. Si la haces pasar, metes latencia de LLM en el 80% de los conteos.

## Antes de tocar esto
`context/03-hallazgos.md` P-03, P-04, P-05. ADR-0007.
