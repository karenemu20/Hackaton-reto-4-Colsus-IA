# Restricciones y supuestos

## Fuera de alcance (dicho por Colsubsidio)
- Reemplazar el sistema actual de inventario.
- **Integración real con el ERP.** No hay endpoints, no hay credenciales, no sabemos cuál ERP es.
- Compras a proveedores o pasarelas de pago.
- Pedidos de cocina, recetas o menús.

## Supuestos que asumimos (y hay que decirlos en el pitch)
- **S-01** El ERP expone una API de solo lectura: catálogo por bodega + stock al corte. La mockeamos en `plataforma/erp/` sembrada con los CSV reales. El *seam* es explícito y está marcado en el diagrama.
- **S-02** La salida del sistema es un archivo/endpoint de conteo limpio. **Nada escribe al ERP.**
- **S-03** Hay conectividad en la bodega durante el demo. Offline queda diferido, pero el seam está listo: `event_id` lo genera el dispositivo (UUID) → el sync es idempotente por construcción. (ADR-0010)
- **S-04** No hay serie histórica: un solo corte. La detección de anomalía usa el stock del corte + orden de magnitud, no promedio móvil.

## Restricciones del operario (esto manda sobre la elegancia técnica)
- Puede tener dificultad para leer. Nombre grande, foto si existe, SKU visible.
- Tiene las dos manos ocupadas. Móvil en el brazo con velcro; lector de anillo si hay.
- Trabaja en frío y humedad. Nada de gestos finos ni targets pequeños.
- El español regional rompe el STT. **La voz nunca puede ser obligatoria.**

## Restricción del equipo
5 personas, 48 horas. Todo lo que no se demuestra en 3 minutos va a la lámina de arquitectura, no al código.
