# Event Storming

**Pendiente de copiar desde `inventory-count-docs/02-event-storming/`.**

Contenido esperado: `01-big-picture/`, `02-process-level/`, `03-design-level/`, `domain-events.md`, `commands.md`, `policies.md`, `read-models.md`, `external-systems.md`, `assets/`.

`hotspots.md` ya está aquí y **es más reciente** — no lo sobrescribas al copiar.

## Convención de colores
naranja = evento de dominio · azul = comando · lila = política · verde = read model · rosa = sistema externo · amarillo = actor · **rojo = hotspot**

## Trazas que deben cuadrar con el código
| Este doc | Debe corresponder a |
|---|---|
| `domain-events.md` | `contracts/events.py` |
| `policies.md` | `contexts/conteo/domain/policies/*.py` (uno a uno) |
| `read-models.md` | vistas en `plataforma/db/schema.sql` |
| `03-ddd/bounded-contexts.md` | carpetas en `contexts/` |

Si un post-it existe y el archivo no, es alcance no implementado. Al revés, es código que nadie modeló.
