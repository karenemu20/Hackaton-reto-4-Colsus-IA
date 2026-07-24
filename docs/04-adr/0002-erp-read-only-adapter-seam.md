# ADR-0002 — ERP como adaptador de solo lectura (seam explícito)

**Estado:** Aceptado

## Contexto
El reto excluye explícitamente la integración real con el ERP. No hay endpoints, credenciales, ni sabemos cuál ERP es. Pero la solución no tiene sentido si no se apoya en el catálogo existente.

## Decisión
`plataforma/erp/` es un **anti-corruption layer de solo lectura**, sembrado con los CSV reales del corte. Expone catálogo por bodega y stock al corte. **Nada escribe al ERP.** La salida del sistema es un archivo/endpoint de conteo limpio.

## Consecuencias
- Los nombres del ERP no cruzan la frontera: todo sale traducido al lenguaje ubicuo.
- El seam se marca en el diagrama del pitch: *"aquí entra su ERP real, y nada más cambia"*.
- Cambiar de ERP o soportar varios = un adaptador nuevo, cero cambios en `contexts/`.

## Nota de credibilidad
Esta decisión es un argumento ante el jurado, no una limitación: demuestra que la solución **alimenta** el ERP en vez de competir con él, que es literalmente lo que pidió Colsubsidio.
