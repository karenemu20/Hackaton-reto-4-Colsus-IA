# Lenguaje ubicuo

Usar estos términos en código, commits y UI. Si aparece un sinónimo, es un bug de comunicación.

| Término | Definición |
|---|---|
| **Bodega** | ubicación física con catálogo propio. 48 declaradas. Se **escanea**, no se teclea |
| **Referencia** | un ítem del catálogo. Tiene nombre y unidad; el SKU es opcional |
| **Corte** | foto del stock del ERP en un instante. Nuestro único corte es el del xlsx |
| **Conteo ciego** | contar sin ver la cantidad del sistema. Invariante del proyecto |
| **Cero forzado** | confirmación explícita al cerrar una ubicación de que un ítem esperado está en 0 y no fue saltado |
| **Saltar ≠ cero** | el error #1 de las tomas físicas: un ítem sin anotar es un hueco silencioso |
| **Empaque / packaging** | cajas × unidades. Origen real del 9-vs-90, que casi nunca es error de conteo |
| **Override** | el operario dice "estoy seguro" contra la anomalía. Siempre gana, siempre queda auditado, dispara segundo conteo |
| **Segundo conteo** | recuento disparado por override o anomalía. No sobrescribe el primero, lo acompaña |
| **Relevo** | traspaso de sesión a medias entre operarios sin perder avance |
| **Cobertura** | proyección de qué se contó vs. qué se esperaba por ubicación |
| **Descuadre** | diferencia contado vs. corte del ERP |
| **Hotspot** | descuadre que **se repite** en el mismo ítem o bodega. Lo que el reto premia |
| **Evento de calidad de dato** | señal de que el maestro está roto: `MISSING_SKU`, `NAME_VARIANT`, `UNIT_MISMATCH`, `STALE_SYSTEM_STOCK`, `MAGNITUDE_ANOMALY`, `MASTER_DATA_DUPLICATE` |
| **Resolver** | expresión (voz/texto/foto) → candidatos de referencia, dentro del scope de la bodega |
| **Ruta rápida** | scan → botones. Determinística, sin LLM |
| **Ruta asistida** | voz/texto/foto → LangGraph → desambiguación |
