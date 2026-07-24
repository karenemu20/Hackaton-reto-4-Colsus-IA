# apps/mobile/ — React + Vite + Tailwind

UI del operario. Móvil en el brazo con velcro, dos manos ocupadas, frío y humedad.

## Invariantes — no negociables
- **NUNCA renderizar la cantidad del ERP.** Si llega en una respuesta, es bug del backend: repórtalo, no lo pintes. (ADR-0001)
- **Botones grandes primero.** Target mínimo 64px. La voz es un botón más, nunca obligatoria. Ningún flujo se completa solo por voz. (ADR-0003)
- El operario puede leer con dificultad: nombre grande, SKU visible, foto si existe.
- **`event_id` lo genera el front** con `crypto.randomUUID()` antes de enviar. Nunca lo pide al backend.
- El front no decide reglas. Renderiza `acciones_requeridas`. Un componente por `RequiredAction`.
- Feedback: verde + sonido cuando cuadra; ámbar cuando hay que confirmar. Nunca rojo acusatorio.

## Arranque
```bash
npm create vite@latest . -- --template react-ts
npm i && npm i -D tailwindcss
```
Mockea `API_CONTRACT.md` con MSW o un `fetch` falso y arranca sin esperar al backend.

## Pantallas (en orden de prioridad para el demo)
1. Conteo — scan/voz/texto → producto grande → cantidad con +/- → guardar
2. Desambiguación — botones grandes de candidatos
3. Anomalía — opciones sin revelar el número + "Estoy seguro"
4. Cierre de ubicación — el cero forzado
5. Reporte — reconciliación + eventos de calidad + hotspots
