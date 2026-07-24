# El reto — Hackathon Colsubsidio x 30X, Reto Hotelería

## El problema

Cada fin de mes, en las bodegas de hoteles y parques de Colsubsidio, el equipo de costos hace la toma física: bodega por bodega, producto por producto, anotando en papel. Ese papel viaja a otra persona que lo digita, y a otra que revisa.

El ERP ya es sólido: conoce productos, bodegas, unidades y costos. **El error nace en el paso manual** — cuando alguien captura lo que contó y otro lo transcribe. Ahí "9 cajas" termina como "90", la caligrafía se lee mal, gramos se confunden con kilos, y el físico no cuadra con el sistema.

**Misión:** quitarle fricción y error a la toma física, para que lo contado entre limpio al sistema desde la primera vez.

## Qué debe lograr una buena solución

- Reemplazar o complementar "papel + digitar" con captura más natural y menos propensa a error.
- Reconocer producto, cantidad y unidad sin ambigüedad ("cinco kilos de harina" ≠ cinco gramos).
- **Detectar anomalías antes de guardar** usando el patrón de esa bodega.
- Validar contra el catálogo existente en tiempo real.
- *(Suma puntos)* Reportes: contado vs. sistema, dónde hay diferencias, **dónde se repiten los descuadres**.

El medio es libre: WhatsApp, app móvil, widget web o algo nuevo.

## Nuestra tesis

El día de conteo no mide stock. **Instrumenta, por primera vez, dónde está roto el dato maestro que nadie gobierna.** Cada conteo emite eventos de calidad de dato (`MISSING_SKU`, `NAME_VARIANT`, `UNIT_MISMATCH`, `STALE_SYSTEM_STOCK`) que son el backlog del MDM que Colsubsidio no tiene — generado solo, sin un proyecto de 18 meses.

Ver `03-hallazgos.md`: el 18% del inventario ya no tiene código y hay 79 existencias negativas. La evidencia está en su propio archivo.
