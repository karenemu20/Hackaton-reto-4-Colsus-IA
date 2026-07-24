# 00 · Overview — empieza aquí (5 min)

Si eres una de las 5 personas y no sabes dónde va tu código, esta página lo resuelve.
Léela entera antes de escribir nada. Es corta a propósito.

## La idea en una frase

No construimos "una app de inventario". Instrumentamos, por primera vez, **dónde está
roto el dato maestro** de Colsubsidio. Cada conteo emite eventos de calidad de dato que
son el backlog de un MDM que hoy no existe. Eso es el diferencial del pitch, no la voz.
(ver `context/00-reto.md`)

## Cómo está organizado el repo (y por qué NO por capas)

Organizado **por contexto de negocio**, no por capa técnica. Las capas
(`domain/ use_cases/ adapters/`) viven DENTRO de cada contexto.

```
contracts/          CONGELADO. Lo único que dos contextos comparten. No lo tocas.
contexts/
  conteo/           sesión, políticas, cierre, relevo   ← el corazón
  resolucion/       expresión → candidatos. LangGraph vive aquí y SOLO aquí
  calidad_dato/     eventos de calidad, hotspots, reconciliación (read-only)
plataforma/           erp (ACL read-only), db, auth, config
apps/
  api/              FastAPI. routing y nada más. Cero lógica
  mobile/           UI del operario. Botones grandes primero
context/            el problema real y los datos. Solo lectura, no lo edites
docs/               el porqué (este overview, ADRs, event storming)
```

**La razón** (ADR-0009): el cambio que vamos a sufrir es *de negocio* y es vertical —
"requerir lote en refrigerados" toca UNA carpeta (`conteo/domain/policies/`), no cuatro.
Con capas, los 5 editan las mismas 4 carpetas y a la hora 6 hay merge conflicts en todo.

## ¿Dónde va MI código? (árbol de decisión)

- ¿Es una **regla** sobre un conteo (cantidad, unidad, empaque, cero, override)?
  → `contexts/conteo/domain/policies/` — 1 archivo + 1 línea en `registry.py`. Nada más.
- ¿Interpreta **lenguaje** (voz/texto/foto) para proponer qué producto es?
  → `contexts/resolucion/`. Si tocas el LLM o el grafo, es aquí. Solo aquí.
- ¿Cuenta **descuadres, hotspots o eventos de calidad de dato**?
  → `contexts/calidad_dato/`. Solo lee el log; nunca escribe `count_event`.
- ¿Es un **endpoint** HTTP?
  → `apps/api/`. Validar entrada → llamar un caso de uso → serializar. Tres líneas.
- ¿Es **pantalla** del operario?
  → `apps/mobile/`. Mockea `apps/mobile/API_CONTRACT.md` y arranca sin esperar al backend.
- ¿Habla con el **ERP o la base**?
  → `plataforma/`. El ERP es un ACL de solo lectura sembrado con los CSV reales.
- ¿Es una **forma que cruza entre contextos** (evento, DTO)?
  → `contracts/`. Está CONGELADO. Si lo necesitas cambiar, **paras y avisas a las 5 personas.**

## La regla de aislamiento (la que de verdad importa)

> **Un contexto NUNCA importa a otro contexto. Solo `contracts/`.**

`contexts/conteo` no puede `import contexts.resolucion`. Se hablan por `contracts/`.
Esto es lo que permite sacar `resolucion` como servicio aparte en 6 meses sin tocar
`conteo`. Las carpetas no dan ese aislamiento; esta regla sí. (ADR-0009)

## Orden de lectura

1. **Esta página.**
2. `CLAUDE.md` (raíz) — los invariantes globales, no negociables.
3. `context/00-reto.md` + `context/03-hallazgos.md` — el problema y la evidencia real.
4. `ARCHITECTURE.md` — el mapa en una página con el diagrama de las dos rutas.
5. El `CLAUDE.md` de TU carpeta — antes de escribir en ella.
6. `docs/00-overview/decisiones-portantes.md` — por qué la arquitectura no va a cambiar.
7. `docs/04-adr/` — el detalle de cada decisión (para auditar, no para memorizar).

## Las dos verdades que más se violan a la hora 20

1. **Conteo ciego** (ADR-0001): la cantidad del ERP NUNCA se muestra al operario. Ni como
   sugerencia, ni placeholder, ni tooltip. Si aparece en una respuesta HTTP, es bug bloqueante.
2. **El dominio decide, la IA interpreta** (ADR-0007): un LLM nunca valida un conteo ni
   aplica una regla. Solo resuelve lenguaje a candidatos.
