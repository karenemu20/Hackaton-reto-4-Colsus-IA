# Contrato de API — para el front, ANTES de que exista el backend

Mockea esto en React y arranca ya. El backend implementa lo mismo en paralelo.
**Todo es HTTP. No hay WebSocket.** Ver decisión abajo.

## 1. Abrir sesión
`POST /v1/sesiones` → `{session_id, bodega_id, bodega_nombre, total_referencias}`
```json
{"bodega_id": "kiosco_taquilla_ayb", "operator_id": "ana", "device_id": "pda-01"}
```

## 2. Resolver (ruta asistida: voz, texto, foto)
`POST /v1/resolver`
```json
{"session_id": "...", "bodega_id": "kiosco_taquilla_ayb", "utterance": "agua", "fuente": "voz"}
```
→
```json
{"requiere_desambiguacion": true,
 "pregunta": "Cual agua?",
 "candidatos": [
   {"sku": "29018", "nombre": "AGUA BOTELLA", "unidad_esperada": "Unidad", "confianza": 0.71, "atributo_distintivo": "botella"},
   {"sku": null,    "nombre": "AGUA 280 ML",  "unidad_esperada": "Unidad", "confianza": 0.64, "atributo_distintivo": "280 ml"},
   {"sku": "29033", "nombre": "AGUA SABORIZADA  H2O", "unidad_esperada": "Unidad", "confianza": 0.52, "atributo_distintivo": "saborizada"}]}
```
> **NUNCA viene la cantidad del ERP en esta respuesta.** Si la ves, es un bug bloqueante.

## 3. Buscar por código (ruta rápida)
`GET /v1/catalogo?bodega_id=...&sku=29018` → un candidato, sin LLM, instantáneo.

## 4. Registrar conteo
`POST /v1/conteos` — **el `event_id` lo genera el front** (`crypto.randomUUID()`). Reenviar el mismo id es idempotente.
```json
{"event_id": "uuid-del-device", "session_id": "...", "bodega_id": "...", "ubicacion": "estante-4",
 "sku": "29018", "utterance": "agua botella", "cantidad": 90, "unidad": "Unidad",
 "packaging": null, "fuente": "voz", "confianza": 0.71, "operator_id": "ana", "device_id": "pda-01"}
```
→
```json
{"aceptado": true,
 "acciones_requeridas": ["confirm_packaging", "offer_alternatives", "second_count"],
 "mensajes": [{"severity": "warn", "message": "Ese numero no coincide con lo que tenemos. Como lo contaste?"}],
 "opciones": [{"label": "90 unidades sueltas", "cantidad": 90},
              {"label": "9 cajas x 10", "cantidad": 90, "packaging": "caja x 10"},
              {"label": "Estoy seguro", "override": true}]}
```

## 5. Cerrar ubicación (el cero forzado)
`POST /v1/ubicaciones/cerrar` → si hay esperados sin contar: `aceptado: false`, `acciones_requeridas: ["confirm_zero"]`, `faltantes: [...]`.

## 6. Reporte
`GET /v1/reportes/{session_id}` → `{reconciliacion: [...], eventos_calidad: [...], hotspots: [...]}`

---

## Regla de oro del front

**El front no decide nada.** Renderiza `acciones_requeridas` y muestra `mensajes`. Si mañana el backend agrega `require_photo`, el front ya sabe qué hacer porque tiene un componente por acción:

```
confirm_packaging → selector de empaque
confirm_unit      → selector de unidad
confirm_zero      → modal "es 0 o te faltó?"
offer_alternatives→ botones grandes de opciones
require_photo     → abrir cámara
second_count      → banner "recuento pendiente"
supervisor_approval → pantalla de aprobación
```

Un `switch` sobre `RequiredAction`. Regla nueva en backend = cero cambios en el front si reusa una acción existente.
