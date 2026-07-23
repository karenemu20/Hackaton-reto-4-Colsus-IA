# Mockups de diseño — guía de qué construir vs. qué es visión a futuro

> Los mockups (`dashboard.jpeg`, `Mockupsv1.jpeg`) son referencia visual y de marca. No todo lo que aparece ahí es alcance del hackathon — ver la tabla.

| Elemento del mockup | Veredicto | Nota |
|---|---|---|
| Botones Hablar / Tomar foto / Escribir | ✅ Construir tal cual | Es el flujo core de captura |
| Flujo de 5 pasos (Captura → Entiende → Valida → Confirma → Guarda) | ✅ Construir tal cual | Coincide exacto con el MVP acordado en `propuesta-valor-v1.md` |
| KPI cards (precisión, registros hoy, alertas activas, diferencia vs sistema) | ✅ Construir | Cálculos directos sobre la base de datos |
| "Top alertas de hoy" | ✅ Construir | Se alimenta de la detección de anomalías |
| Comparativo vs sistema (donut chart) | ✅ Construir | Chart.js, el dato ya está disponible |
| Escanear código QR / código de barras | ⏸ Aplazar | Modalidad extra, no crítica para la demo |
| Subir archivo (PDF/XLS/JPG) | ⏸ Aplazar | Es importación masiva, una feature distinta a la captura conversacional |
| "Actividad en tiempo real" | ⚠️ Simplificar | Lista que se refresca al cargar la página, no un feed en vivo con websockets |
| Digital Twin — mapa de bodega con zonas de colores | ⚠️ Simplificar fuerte | Reemplazar por tabla/lista con badge Normal/Atención/Crítico por bodega. Es la pieza más cara de construir y la que menos aporta a que el prototipo funcione |
| "Insights Colsus IA Brain" (recomendaciones tipo patrones de merma) | ⚠️ Simplificar | Precalcular 1-2 insights reales contra el Excel una sola vez y mostrarlos fijos, no un motor en vivo |

**Regla general:** todo lo que es lectura/cálculo directo de datos ya guardados (KPIs, alertas, gráficos simples) es barato de construir. Todo lo que implica una visualización custom elaborada (mapa de bodega) o un motor de inteligencia adicional (insights) es caro — se muestra en el pitch como visión de producto, no se construye para la demo.
