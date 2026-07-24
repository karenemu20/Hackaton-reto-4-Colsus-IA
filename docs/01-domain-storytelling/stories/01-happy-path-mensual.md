# 01 · Toma mensual — camino feliz (ruta rápida)

**Actores:** Operario · Dispositivo (PDA/celular con velcro) · ERP (espejo read-only).
**Es el 80% de los conteos.** No pasa por el LLM (ADR-0007).

1. El **operario** llega a una estantería y **escanea** el código de la **ubicación**.
2. El **dispositivo** poda el **catálogo** a esa bodega — de 936 referencias a ~56 (P-03, ADR-0004).
3. El **operario** **escanea** el código de barras del **producto**.
4. El **dispositivo** muestra el **producto** en grande: nombre tal cual la estantería
   (`nombre_raw`), foto si existe, SKU visible (P-05).
5. El **operario** ajusta la **cantidad** con botones grandes `+ / −` y toca **Guardar**.
6. El **dispositivo** genera un **`event_id` (UUID)** y emite un **`ConteoRegistrado`** al log
   (append-only, ADR-0005). Feedback verde + sonido.
7. El **operario** repite desde (3) para el siguiente producto.

**Por qué así:** el operario tiene las manos ocupadas, frío y humedad; botones de 64px y
escaneo, nunca gestos finos (ADR-0003). El `event_id` del device hace el guardado idempotente
y deja listo el offline (ADR-0010).

**Dónde vive:** ruta rápida en `apps/mobile` + `apps/api` → `contexts/conteo`. No toca `resolucion`.
