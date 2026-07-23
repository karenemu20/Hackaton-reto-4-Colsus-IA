# Propuesta de valor — v1 (borrador inicial)

> Versión inicial, previa a la fase de refinamiento con el equipo. El archivo de slides está en [`Propuesta_de_Valor_V1.pptx`](./Reto4_Propuesta_de_Valor.pptx).

**Tagline:** Que lo que se cuenta entre limpio al sistema, desde la primera vez.

## Para quién

El equipo de costos que hace la toma física de inventario, bodega por bodega (48 bodegas hoy), en hoteles y parques de Colsubsidio.

## Problema

El ERP ya es sólido y conoce productos, bodegas y costos; el error nace en el paso manual de capturar y transcribir el conteo.

## Solución

Captura por voz o conversación que reconoce producto, cantidad y unidad sin ambigüedad (5 kg ≠ 5 g).

## Diferenciador

Detecta anomalías contra el histórico antes de guardar: si el patrón dice 9 cajas y hoy dicen 90, pregunta antes de dejarlo pasar.

## Flujo del MVP

1. **Captura** — voz o conversación del conteo
2. **Reconocimiento** — producto, cantidad y unidad, sin ambigüedad
3. **Validación** — contra catálogo e histórico por bodega
4. **Alerta de anomalía** — si se desvía del patrón, pregunta antes de guardar
5. **Registro limpio** — listo para alimentar el ERP

El canal es libre: agente de WhatsApp, app móvil o widget web.

## Alcance del prototipo

**Incluido:**
- Captura conversacional del conteo (voz o texto)
- Validación en tiempo real contra el catálogo
- Detección de anomalías vs. histórico por bodega
- (Bonus) Reporte: contado vs. sistema y descuadres

**Fuera de alcance (definido por el reto):**
- Reemplazar el sistema actual de inventario
- Integración real con el ERP actual
- Compras a proveedores o pasarelas de pago
- Pedidos de cocina, recetas o menús

## Cronograma

| Día | Modalidad | Foco |
|---|---|---|
| Mié 22 | En línea | Cerrar alcance y arquitectura del reto |
| Jue 23 | En línea | Arrancar el pipeline base (captura de voz → reconocimiento) |
| Vie 24 | Presencial | Prototipo funcional completo: validación + detección de anomalías |
| Sáb 25 | Presencial | Testing a fondo y correcciones |
| Dom 26 | Presencial | Presentación final |

## Lo que queremos demostrar

- Menos diferencias entre lo contado y lo registrado en el sistema.
- Anomalías detectadas antes de guardar, no después del cierre de mes.
