# Revisión de diseño — 2026-07-23

Registro de una revisión completa del repo hecha con IA (Claude, sesión de arquitectura).
**Propósito:** dejar como contexto lo que se analizó, se encontró y se resolvió, para que
la siguiente sesión que revise no parta de cero. No es narrativa de pitch; es memoria técnica.

Alcance: el repo completo cabe holgadamente en contexto (~1.400 líneas de sustancia +
2 CSV de 1.406 filas). Se leyó TODO, no un resumen: los 12 ADRs, los 9 hotspots, los
contratos, las 3 políticas implementadas, el schema, el seed y todos los `CLAUDE.md`.

## Estado del repo al momento de revisar

Es un **esqueleto de hora 1**: ~90% decisión, ~10% implementación. Contratos congelados +
3 políticas de `conteo` (`anomalia_magnitud`, `cero_forzado`, `validar_unidad`) + schema +
seed. `resolucion`, `calidad_dato`, `apps/api`, `apps/mobile`, `plataforma/auth|config` están
vacíos o solo con su `CLAUDE.md`. Esto es coherente con su propia tesis ("hora 1 es de una
sola persona: congelar `contracts/` y escribir los `CLAUDE.md`").

## Veredicto de arquitectura

Las tres decisiones portantes (estructura por contexto, LangGraph acotado, log append-only)
están **bien elegidas y son estables frente a cambio**. El análisis detallado y las pruebas
de estrés están en `decisiones-portantes.md`. Resumen: ninguna cambia por un descuido; las
tres solo cambiarían por disparadores explícitos y con señal temprana.

## Fortalezas confirmadas

1. **Screaming architecture (por contexto, no por capa)** bien justificada y no cosmética.
2. **`contracts/` congelado como mecanismo de coordinación**, no como carpeta técnica. El
   mejor insight del repo: con 5 personas el fallo modal no es el código, es que a la hora 6
   cada uno inventó su propio contrato.
3. **Conteo ciego aplicado mecánicamente en 4 capas** (ADR-0001, schema, política, API, mobile).
4. **`PolicyResult` con `required_actions` en vez de `bool`** (ADR-0008): separa reglas que
   validan de reglas que cambian la conversación. Evita que la lógica se infiltre en el grafo.
5. **`event_id` generado en el device** (ADR-0010): una columna compra offline idempotente.
6. **Diseño anclado a evidencia**: cada patología P-01…P-10 trae su comando de verificación.
   La arquitectura es un corolario de los datos, no de opiniones.

## Incertidumbre declarada y bien gestionada (los hotspots)

El repo es honesto con su propia incertidumbre — los 9 hotspots son eso. Los dos más
relevantes para el demo:
- **H-02** (`ubicacion` sub-bodega es un invento, no está en el dato de Colsubsidio): es la
  asunción más frágil. El cero forzado por ubicación se apoya en granularidad que puede no
  existir. Mitigado (nullable → cierre por bodega). **Debe decirse en el pitch.**
- **H-04** (umbral de anomalía sin serie histórica): el "9 vs 90" que pide el reto requiere
  historia; hay un solo corte. Mitigado con factor 5x + orden de magnitud. Honesto, pero es
  lo más débil frente al jurado.

## Hallazgos nuevos de esta revisión

Tres eran contratos IMPLÍCITOS — el mismo fallo que `contracts/` existe para prevenir, pero
fuera de `contracts/`:

1. **`ctx` de las políticas no tenía tipo.** Las políticas leen `ctx.esperado_erp`,
   `ctx.unidad_esperada`, `ctx.cerrando_ubicacion`, `ctx.esperados_no_contados` — campos que
   NO están en `RegistrarConteoCmd`. El "comando enriquecido" no existía como tipo. Con 5
   personas, cada una lo iba a enriquecer distinto.
2. **Invariante `nombre_resuelto == nombre_norm` sin declarar.** Las vistas `cobertura` y
   `reconciliacion` unen por ahí. Si el conteo guarda `nombre_raw`, la reconciliación
   devuelve NULL en silencio: descuadre falso, no error. Seam de bug latente.
3. **`override → SECOND_COUNT` se afirmaba pero no se garantizaba en código.** Solo
   `anomalia_magnitud` sugería `SECOND_COUNT`, y solo cuando ella disparaba. Un override
   sobre un conteo sin anomalía no generaba recuento.

Dos observaciones menores (no bugs, decisiones a hacer explícitas):
4. **`anomalia_magnitud.aplica()` se desactiva sin `esperado_erp`** → justo los ítems sin
   SKU (18%) no reciben chequeo de anomalía. Es correcto (sin línea base no hay anomalía; es
   `MISSING_SKU`), pero no estaba dicho. Ahora comentado en el código.
5. **Reparto de 5 personas asimétrico:** la persona 5 (`apps/api` + `plataforma/` entero) es la
   porción más pesada y el punto del que dependen las otras 4. La persona 2 (`resolucion`:
   LangGraph + pgvector) carga el riesgo técnico más alto. Sugerencia: sacar `plataforma/auth`
   (biometría, demo-nice, no bloquea) del camino crítico y poner apoyo en `resolucion`.

## Qué se resolvió en esta sesión

- **`contexts/conteo/domain/conteo_ctx.py`** (NUEVO): define `ConteoCtx` frozen y tipado —
  el comando enriquecido, con el invariante ADR-0001 (`esperado_erp` nunca cruza a HTTP)
  documentado. Vive en `conteo/domain`, NO en `contracts/` (es interno al contexto y
  `contracts/` está congelado).
- **`contexts/conteo/domain/policies/segundo_conteo.py`** (NUEVO): política que garantiza
  `override → SECOND_COUNT`, auditando `operator_id` + `motivo`. Registrada en `registry.py`.
- **`base.py`, `registry.py` y las 3 políticas**: firmas tipadas con `ConteoCtx`
  (vía `TYPE_CHECKING`, sin acople en runtime).
- **`plataforma/db/schema.sql`**: comentado el invariante de escritura `nombre_resuelto == nombre_norm`.
- **`contexts/conteo/CLAUDE.md`**: añadidos los invariantes de `ConteoCtx` y `nombre_resuelto`;
  lista de políticas actualizada (implementadas vs. pendientes).
- **`docs/00-overview/`** (carpeta antes vacía): este registro + `README.md` (mapa de
  carpetas/onboarding) + `decisiones-portantes.md` (las 3 decisiones + prueba de estrés).

Ninguna de estas resoluciones tocó `contracts/` (congelado) ni contradijo un ADR.

## Qué queda abierto para el equipo

- **`contracts/` — evaluar si `ConteoCtx` debería vivir ahí.** Se dejó en `conteo/domain`
  por ahora porque es interno al contexto. Si `apps/api` acaba construyéndolo, revisar si el
  enriquecimiento cruza frontera. **Decisión de las 5 personas, no de un agente.**
- Los hotspots ABIERTOS (H-01, H-02, H-05, H-07, H-08, H-09) siguen abiertos: son preguntas
  a Colsubsidio o riesgos declarados para el pitch, no deuda de código.
- Dependencia del repo externo `inventory-count-docs` (storytelling y event-storming
  "pendientes de copiar"). Recomendación: copiarlo ya o declararlo out-of-scope; tener dos
  fuentes documentales que pueden divergir es deuda que nadie pagará a la hora 30.
- Políticas pendientes: `ValidarCantidad`, `ConfirmarEmpaque`.

## Para la próxima sesión que revise

Empieza por `docs/00-overview/README.md`, luego `decisiones-portantes.md`, luego este
registro. Los invariantes globales están en el `CLAUDE.md` raíz; los específicos, en el
`CLAUDE.md` de cada carpeta. Si algo del código contradice un invariante, el invariante gana
y es un bug del código, no del invariante.
