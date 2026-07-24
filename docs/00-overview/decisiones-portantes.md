# Decisiones portantes — y por qué no van a cambiar por un descuido

Tres decisiones sostienen todo el repo. La preocupación legítima no es si son "buenas"
en abstracto, sino: **¿las elegimos bien, y aguantan cambios que hoy no vemos?**

El método de este documento: para cada decisión, la enunciamos EXPLÍCITA, decimos por qué
es la correcta *aquí* (anclada a los datos y al reto), y la sometemos a una **prueba de
estrés** — escenarios de cambio futuro. Si la arquitectura los absorbe sin reestructurar,
la decisión es estable. Al final de cada una: **qué SÍ la haría cambiar** (el disparador
honesto, para que no nos tome por sorpresa).

Estas tres deciden el 90% del riesgo. Todo lo demás es reversible.

---

## Decisión 1 · Monorepo + monolito modular + organización POR CONTEXTO

Se confunden tres ejes como si fueran uno. Los separamos (ADR-0009):

| Eje | Elección | Por qué |
|---|---|---|
| **Repo** | Monorepo (un solo repo Git) | 5 personas, 48h. No hay discusión. |
| **Despliegue** | Monolito modular (un desplegable) | Mismo grafo de imports que multi-paquete, sin fricción de packaging. |
| **Agrupación** | **Por contexto de negocio, NO por capa** | ← Aquí es donde la mayoría se equivoca. |

**Enunciado explícito:** un repo, un desplegable, con las **fronteras como carpetas por
contexto** (`conteo`, `resolucion`, `calidad_dato`). Las capas (`domain/ use_cases/
adapters/`) viven DENTRO de cada contexto, no como paquetes hermanos.

**Por qué es la correcta aquí:** el cambio que vamos a sufrir no es tecnológico (cambiar
Postgres), es de negocio — una regla nueva, una bodega que cuenta distinto, un modo de
captura nuevo. Ese cambio es *vertical*. Con capas toca 4 carpetas / 4 PRs / 4 conflictos.
Con contextos toca una carpeta, un dueño.

### Prueba de estrés — escenarios que ya contemplamos

| Cambio futuro | Qué toca | ¿Reestructura? |
|---|---|---|
| Regla nueva ("lote en refrigerados") | 1 archivo en `conteo/domain/policies/` + 1 línea | No |
| Modo de captura nuevo (visión/OCR) | 1 adapter en `resolucion/` (ADR-0012) | No |
| Cambiar Postgres por otra DB | `plataforma/db` + adapters. Dominio intacto | No |
| Escala 8 → 48 → 200 bodegas | Cero cambios de arquitectura (P-09): es dato, no estructura | No |
| Sacar `resolucion` como microservicio (6 meses) | Posible SIN tocar `conteo`, porque el único acople es `contracts/` | No |
| Sumar una 6.ª persona al equipo | Un contexto nuevo o un dueño más. No compite por las mismas carpetas | No |

El aislamiento real **no lo dan las carpetas** — lo da una regla: *un contexto nunca
importa a otro, solo `contracts/`*. Esa regla es lo que hace reversible casi todo.

### Qué SÍ la haría cambiar
- Que dos contextos necesiten **estado transaccional fuerte compartido**. No es el caso:
  se comunican por eventos append-only, no por una transacción común.
- Que el equipo crezca a decenas de personas y un contexto se vuelva cuello de botella
  → se extrae a servicio. **El diseño ya lo permite; no es un rediseño, es un corte por la
  costura que ya existe.**

**Riesgo aceptado (ADR-0009):** nada FÍSICO impide un import cruzado. Mitigación:
`import-linter` en CI si sobra tiempo; si no, revisión + el `CLAUDE.md` de cada carpeta.

**Veredicto:** bien elegida. El eje que importa —por contexto vs. por capa— es el correcto,
y es precisamente el que suele equivocarse. No cambia por un descuido; cambiaría solo por
un cambio explícito de escala o de acoplamiento, y ambos tienen señal temprana.

---

## Decisión 2 · LangGraph SOLO en la ruta asistida

**Enunciado explícito:** LangGraph vive en `contexts/resolucion/graph/` y **solo se activa
con entrada ambigua** (voz, texto libre, foto). La **ruta rápida** (escaneo → botones, el
~80% de los conteos) **no lo atraviesa**. El LLM interpreta lenguaje a candidatos; **nunca**
decide si un conteo es válido ni aplica una regla. (ADR-0007)

Esta es la decisión donde más pesa tu preocupación ("que no cambie porque no tuvimos algo
en cuenta"). El error clásico es poner el grafo en la columna vertebral
(`FastAPI → Application → LangGraph → Domain`) y descubrir a la hora 20 que todo depende del
LLM. Lo evitamos acotándolo a un contexto y a una ruta.

### Prueba de estrés — lo que SÍ contemplamos

| "¿Y si...?" | Respuesta | ¿Rompe la decisión? |
|---|---|---|
| ...el LLM se cae o hay rate limit | La ruta rápida (80%) no depende de él; el conteo sigue. La asistida degrada a texto/botones | No |
| ...queremos streaming de la respuesta | El resolver devuelve una LISTA de candidatos, no prosa. No hay nada que streamear. Si algún día sí → SSE, no WebSocket (ADR-0011) | No |
| ...agregamos visión / OCR de etiquetas | Un adapter más que produce `Candidato[]`; el grafo gana 1 rama (ADR-0012). Mismo patrón | No |
| ...el diálogo se vuelve multi-turno complejo | Para eso ES LangGraph (FSM con estado de diálogo). Ya está en el lugar correcto | No |
| ...quieren que el agente "decida" el conteo | **NO.** Ese es el invariante que ADR-0007 protege: el dominio decide, la IA interpreta. Cambiarlo sería decisión de producto, no descuido técnico | No (por diseño) |
| ...se cae la señal a mitad de diálogo | El estado conversacional en el servidor no bloquea el conteo: la ruta rápida no lo usa, y el POST con `event_id` del device reintenta solo | No |

El invariante frágil está declarado: *"un nodo del grafo que importa `domain/policies` es
el que se viola en la hora 20"*. Mitigación: los nodos solo llaman `use_cases/`, nunca
políticas ni repositorios ni el ERP.

### Qué SÍ la haría cambiar
- Que el **80% dejara de ser escaneo** — p. ej. bodegas sin códigos de barras en la
  ubicación, o productos sin código. Ahí la ruta rápida se encoge y el LLM entra al camino
  crítico. **Pero eso es un cambio de supuesto** (ligado a H-02), y se detecta observando
  el ratio scan/asistido, no por sorpresa.

**Veredicto:** bien elegida y, sobre todo, **bien acotada**. La decisión clave no es "usar
LangGraph"; es "acotarlo a un contexto y a una ruta". Ese acotamiento es lo que impide que
un cambio no previsto lo mande a la columna vertebral.

---

## Decisión 3 · El modelo de datos es un log append-only + proyecciones

**Enunciado explícito:** el registro de verdad es la secuencia **append-only** de
`count_event`. Nunca `UPDATE`, nunca `DELETE`; corregir = emitir otro evento. `cobertura`
y `reconciliacion` son **proyecciones reconstruibles** del log. `event_id` lo genera el
**dispositivo** (UUID). `sku` es nullable y string. `ubicacion` es nullable.
(ADR-0005, ADR-0010)

Es event-sourcing-lite. La pregunta que importa: **¿soporta los cambios que vienen?**

### Prueba de estrés — evolvabilidad

| Cambio / necesidad futura | Cómo lo absorbe el modelo | ¿Migración? |
|---|---|---|
| Corregir un conteo | Nuevo evento, no `UPDATE`. La historia queda | No |
| Relevo de turno a media bodega | Hereda un log, no un estado; `operator_id` va por evento (ADR-0006) | No |
| Segundo conteo / override | Acompaña al primero, no lo sobrescribe. La comparación *es* el dato | No |
| Offline real algún día | `event_id` del device + append-only = sync idempotente. `sync_state` ya existe (ADR-0010) | **No — y esa es la decisión que importa** |
| Nueva proyección (productividad por operario) | Es un `VIEW`/consulta sobre el log | No |
| Ítem sin código (18%, P-01) | `sku` nullable → es `MISSING_SKU`, no un error | No |
| Dos rangos de SKU / dos ERPs (P-10) | `sku` es string, sin aritmética; conviven | No |
| Sin serie histórica hoy (H-04) | Cada evento es un punto: la serie se construye sola. El modelo ya la soporta, faltan datos | No |
| Nueva unidad, nuevo tipo de evento de calidad | Enum + fila; sin cambio estructural | No |
| Granularidad sub-bodega incierta (H-02) | `ubicacion` nullable: si no existe, cierre por bodega. Absorbe ambos mundos | No |

### Costos aceptados a sabiendas
- Toda lectura de "cantidad actual" es una agregación sobre el log. Irrelevante a esta
  escala. Si algún día fueran millones de eventos/día → se **materializan** las proyecciones
  (snapshots). Eso es evolución estándar de event sourcing, **no un rediseño**.

### El único punto frágil — y ya está cerrado
No es el modelo: es un **invariante de escritura**. `count_event.nombre_resuelto` debe
guardar `nombre_norm`, no `nombre_raw`, porque las vistas unen por ahí. Si se guarda el raw,
la reconciliación devuelve NULL en silencio (descuadre falso, no error). Documentado en
`plataforma/db/schema.sql`, `contexts/conteo/CLAUDE.md` y `conteo/domain/conteo_ctx.py`.

**Veredicto:** es el activo **más fuerte** del repo para absorber cambio. La decisión de más
apalancamiento es una sola columna —`event_id` generado en el device— que compra offline
idempotente sin implementar sync. Si esa columna la generara la base, no habría offline
posible sin rediseñar el schema.

---

## Resumen para el pitch

Las tres decisiones comparten una misma forma: **el punto de extensión está aislado y el
cambio queda contenido.** Una regla nueva = una carpeta. Un modo de captura nuevo = un
adapter. Un dato corregido = un evento más. Ninguno de los tres obliga a reestructurar, y
los tres únicos disparadores reales de cambio (acoplamiento transaccional, que el 80% deje
de ser escaneo, y volumen de millones de eventos) tienen **señal temprana medible** — no
nos tomarían por sorpresa.
