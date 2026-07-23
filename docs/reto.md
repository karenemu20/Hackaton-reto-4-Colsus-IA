# Reto 4 · Captura inteligente en la toma de inventarios

_Brief oficial — Hackathon Colsubsidio × 30X_

## El problema

Cada fin de mes, en las bodegas de los hoteles y parques de Colsubsidio, el equipo de costos hace la toma física de inventario: bodega por bodega, cuenta producto por producto y va anotando lo encontrado en papel, una referencia a la vez. Ese papel viaja a otra persona, que lo digita en el sistema, y otra más lo revisa.

El sistema interno ya sabe qué productos hay en cada bodega, sus unidades y cómo cuadran los costos. La parte más robusta del proceso ya está resuelta.

El problema vive en el paso manual: cuando una persona captura lo que contó y otra tiene que transcribirlo. Ahí es donde alguien cuenta "9 cajas" y termina registrado como "90". Donde una caligrafía difícil se lee mal, donde una unidad se confunde con otra (gramos vs. kilos). Y donde después el inventario físico no cuadra con el del sistema.

**Misión:** quitarle fricción y error a la toma física de inventario, para que lo que se cuenta entre limpio al sistema desde la primera vez.

## Cómo se ve un buen resultado

No se prescribe qué construir, sino qué debería lograr una buena solución:

- Reemplaza (o complementa) el "papel + digitar" con algo más natural: voz, conversación, o cualquier forma de captura más rápida y menos propensa a error al contar.
- Reconoce productos, cantidades y unidades sin ambigüedades. Si alguien dice "cinco kilos de harina", no lo confunde con cinco gramos.
- Detecta anomalías antes de guardar. Si el patrón de esa bodega sugiere que normalmente hay 9 cajas y hoy alguien reporta 90, pregunta antes de dejarlo pasar.
- Se apoya en el catálogo de productos que Colsubsidio ya tiene para validar cada conteo en tiempo real.
- (Suma puntos) Genera reportes útiles: qué se contó vs. qué decía el sistema, dónde hay diferencias, dónde se repiten los descuadres.

El canal es libre: agente de WhatsApp, app móvil, widget web o algo distinto — lo que se evalúa es la forma de resolverlo.

## El dominio (contexto, no instrucción)

- **El error nace en el paso manual, no en el sistema.** Los ERPs de inventario de Colsubsidio son sólidos y ya conocen productos, bodegas y costos. La oportunidad está en el frente: el momento en que una persona captura lo que contó.
- **La toma física se repite bodega por bodega.** Hay varias bodegas en hoteles y parques, y en cada una se cuenta referencia por referencia. Una buena solución hace ese conteo más rápido y confiable en cualquier bodega.
- **El catálogo e histórico de inventario son un activo.** Colsubsidio ya conoce sus productos, unidades y tiene histórico de existencias por bodega. Usar eso para validar en tiempo real ("¿estás segura de que son 90 cajas y no 9?") es donde una capa de IA aporta mayor valor.
- **El endpoint es información limpia lista para el ERP.** La solución no busca reemplazar el ERP; busca alimentarlo mejor.

## Qué NO toca este reto

- Reemplazar el sistema actual de inventario.
- Integración real con el ERP actual.
- Compras a proveedores externos o pasarelas de pago.
- Pedidos de cocina, recetas o menús.

## Recursos

Ver [`recursos.md`](./recursos.md) para el detalle de los datos reales compartidos por Colsubsidio.

Carpeta oficial de recursos: https://drive.google.com/drive/folders/1VdXHqaXAW6pXc9PszMdQln0DQMGnLX0O
