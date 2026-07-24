# ADR-0004 — Escaneo de ubicación como poda de catálogo

**Estado:** Aceptado

## Contexto
El catálogo global tiene 936 referencias únicas. Buscar "agua" contra el global devuelve agua, aguardiente, aguacate y agujas desechables (ver `context/03-hallazgos.md` P-03).

Además, el maestro de bodegas **ya está duplicado consigo mismo**: `caf. Velas` vs `caf.velas`, `movil fonda` vs `movil fonda suministros`, y un `paqueadero` con typo (P-08). Teclear o elegir de una lista de texto libre reproduce esa suciedad.

## Decisión
La bodega/ubicación **se escanea**, no se teclea. El `bodega_id` resultante poda el catálogo **antes** de cualquier búsqueda o embedding.

## Consecuencias
- Un kiosco maneja 56 referencias, no 936: **reducción de 16x del espacio de búsqueda, gratis**.
- Es el desambiguador más potente del sistema y no cuesta un solo token de LLM.
- `CREATE INDEX ON catalogo (bodega_id)` no es opcional.
- Prohibido `LIKE '%...%'` sobre el catálogo global.

## Consecuencia operativa
Requiere etiquetas de código de barras en las ubicaciones. Costo trivial, y es el mismo gesto que ya hace el operario.
