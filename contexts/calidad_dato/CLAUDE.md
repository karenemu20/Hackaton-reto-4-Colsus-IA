# contexts/calidad_dato/

El diferenciador del proyecto. Convierte el log de conteos en el backlog del MDM que Colsubsidio no tiene.

## Invariantes
- **Solo lee.** Nunca escribe a `count_event`. Es derivado puro.
- Todo evento lleva `evidencia` con el dato real que lo disparó — el jurado tiene que poder verificarlo.
- Reconstruible: si borras esta tabla y la regeneras del log, debe dar lo mismo.
- NUNCA importa otros contextos. Solo `contracts/`.

## Detectores
`MISSING_SKU` (P-01) · `STALE_SYSTEM_STOCK` (P-02, los 79 negativos) · `NAME_VARIANT` (P-04) · `UNIT_MISMATCH` (P-06) · `MAGNITUDE_ANOMALY` (P-07) · `MASTER_DATA_DUPLICATE` (P-08)

## Hotspots
El reto premia explícitamente *"dónde se repiten los descuadres"*. Agregación por bodega × ítem. Con un solo corte no hay serie: para el demo, el hotspot es la concentración dentro de la sesión.
