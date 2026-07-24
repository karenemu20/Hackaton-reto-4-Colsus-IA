# ADR-0009 — Monolito modular por contexto, un solo paquete desplegable

**Estado:** Aceptado

## Contexto
Tres ejes que se estaban confundiendo como si fueran uno:
- **Monorepo** (un repo Git) → sí, con 5 personas y 48 horas no hay discusión.
- **Monolito modular** (un desplegable) → sí.
- **Agrupación por capa vs. por contexto** → aquí estaba el error.

La propuesta original agrupaba por capa (`application/ agent/ domain/ infrastructure/ shared/` como paquetes separados).

## Decisión
Un solo paquete desplegable, con las **fronteras como carpetas por contexto de negocio**. Las capas viven dentro de cada contexto.

## Consecuencias
- El cambio de negocio (que es el que no conocemos aún) queda contenido en una carpeta.
- **Con 5 personas: un dueño por contexto, casi cero merge conflicts.** Con capas, los 5 editan las mismas 4 carpetas.
- Mismo import graph que multi-paquete, sin fricción de packaging.
- El aislamiento real lo da una regla, no la estructura: *un contexto nunca importa a otro, solo `contracts/`*.

## Consecuencia negativa aceptada
Nada impide físicamente un import cruzado. Se mitiga con `import-linter` en CI si sobra tiempo; si no, con revisión y el `CLAUDE.md` de cada carpeta.
