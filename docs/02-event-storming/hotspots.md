# Hotspots 🔴

Los "picos" del taller: tensiones sin resolver, dudas que afectan el modelo, conflictos entre lo que creemos y lo que dice el dato.

**Regla:** un hotspot no se borra, se resuelve con un ADR o se acepta como riesgo declarado en el pitch.

---

## H-01 · ¿El manager que abre la sesión es distinto del operario que cuenta?
**Estado:** ABIERTO — nadie de Colsubsidio lo ha confirmado.
**Afecta:** ciclo de vida de `ConteoSesion`, ADR-0006.
**Si son la misma persona:** la sesión es del operario, el relevo es simple.
**Si son distintas:** hay un rol de apertura/cierre, y `abierta_por ≠ operator_id` de los eventos. Ya lo modelamos así por si acaso — es reversible, no al revés.
**Cómo se resuelve:** una pregunta al equipo de costos. Si no hay acceso, se asume lo segundo y se declara como supuesto.

---

## H-02 · No existe granularidad de ubicación por debajo de la bodega
**Estado:** ABIERTO — **y es una invención nuestra.**
El dataset solo tiene bodega. `count_event.ubicacion` (`estante-4`) **no existe en el dato de Colsubsidio**. Nos la inventamos para que funcione el cero forzado por ubicación.
**Riesgo:** si en la operación real no hay estantes marcados, el cierre por ubicación no tiene dónde apoyarse y el cero forzado tiene que ser por bodega completa — que es mucho menos útil (una bodega tiene 200+ referencias).
**Mitigación actual:** `ubicacion` es nullable. Si no existe, el cierre es por bodega.
**Hay que decirlo en el pitch.** Es la asunción más frágil del diseño.

---

## H-03 · El override abusivo degrada la señal
**Estado:** MITIGADO SIN PROBAR.
Si el operario aprende que "Estoy seguro" salta la fricción, lo usa siempre y el sistema pierde su valor.
**Mitigación:** el override dispara `SECOND_COUNT` obligatorio y queda auditado con `operator_id`. El costo de mentir es recontar.
**Sin probar:** no sabemos si eso alcanza. Un operario apurado puede recontar mal a propósito.
**Métrica a vigilar:** tasa de override por operario. Si uno supera al resto por mucho, es señal — de mal entrenamiento o de un ítem realmente mal catalogado.

---

## H-04 · Umbral de anomalía con un solo corte
**Estado:** RIESGO ACEPTADO para el demo.
El reto pide detectar que "normalmente hay 9 cajas y hoy alguien reporta 90". Eso requiere **serie histórica**. Tenemos un solo corte.
**Lo que hacemos:** factor 5x contra el stock del corte + orden de magnitud (mediana 12, P-07).
**Lo que NO podemos decir:** "aprende el patrón de la bodega". Sería mentir al jurado.
**Lo que SÍ podemos decir:** "el sistema genera desde el día uno la serie que hoy no existe — cada conteo es un punto".
**Cómo se resuelve de verdad:** dos meses de tomas físicas. No hay atajo.

---

## H-05 · ¿Cómo se cuenta algo que no tiene código? (252 filas, 18%)
**Estado:** ABIERTO — decisión de producto pendiente.
El operario encuentra `AGUA WAIRA SABORIZADA` (2.844 unidades) que no tiene SKU.
**Opción A:** se registra con `sku=NULL` y `utterance` crudo. El evento `MISSING_SKU` va al backlog del MDM. *(implementado)*
**Opción B:** el operario crea la referencia en el momento. Rápido, pero **multiplica la basura del maestro** — el problema que estamos tratando de exponer.
**Inclinación:** A. Que el sistema no deje crear maestro es una feature, no una carencia.
**Pero:** si el conteo no puede guardarse sin código, el operario abandona. Por eso `sku` es nullable.

---

## H-06 · ¿Reconciliación es un bounded context o un read model?
**Estado:** RESUELTO — read model.
El doc de DDD listaba cuatro contextos (Conteo · Resolución · Reconciliación · Calidad de Dato) y solo hay tres carpetas.
**Decisión:** Reconciliación no tiene comandos propios ni invariantes — solo lee el log y el corte. Es una proyección dentro de `contexts/calidad_dato/projections/`.
**Acción:** corregir `03-ddd/bounded-contexts.md`, no crear la carpeta.

---

## H-07 · Dos rangos de SKU conviviendo: ¿son dos ERPs?
**Estado:** ABIERTO — impacto bajo, pero afecta el discurso.
Suministros usa 8 dígitos (`95026919`). A&B usa 4-5 (`7290`). Son numeraciones distintas en el mismo archivo (P-10).
**Hipótesis:** dos maestros o dos módulos que alguien consolidó a mano en Excel.
**Si es cierto:** refuerza la tesis del proyecto — el maestro ya está fragmentado y nadie lo gobierna. Es munición para el pitch.
**Riesgo si nos equivocamos:** afirmarlo sin confirmar y que el jurado lo desmienta. Presentarlo como observación, no como hecho.

---

## H-08 · 48 bodegas declaradas, 8 con datos
**Estado:** ABIERTO.
¿Las otras 40 existen y no nos las dieron, o el maestro de bodegas tiene entradas muertas?
Dado que el propio listado tiene duplicados y un typo (`paqueadero`), la segunda hipótesis es plausible.
**Impacto:** es el argumento de escala del pitch ("esto es una unidad de negocio de 48"). Si 20 son fantasmas, el argumento se debilita.
**Mitigación:** decir "48 bodegas declaradas en su maestro" — literal y verificable. No decir "48 bodegas operando".

---

## H-09 · `Portion` como unidad de medida (22 filas)
**Estado:** ABIERTO — posible fuga de alcance.
Una unidad `Portion` implica pre-porcionados o recetas. El reto **excluye explícitamente** recetas y menús.
**Duda:** ¿el operario cuenta porciones físicas, o es una conversión contable del ERP?
**Por ahora:** se trata como cualquier otra unidad. Si aparece en el demo, no se explica.
