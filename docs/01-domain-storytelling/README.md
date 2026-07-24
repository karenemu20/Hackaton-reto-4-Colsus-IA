# Domain Storytelling

Cómo trabaja el dominio, contado como historias. **Notación:** actor → *actividad numerada* →
work object. Cada historia es un recorrido real, no una pantalla. Si una historia y el código
se contradicen, gana la historia (o se corrige la historia con el equipo).

Cada historia enlaza a su ADR y a las patologías del dato (`context/03-hallazgos.md`) que la
justifican — para que nadie "mejore" un flujo rompiendo el porqué.

## Historias

| # | Historia | Toca |
|---|---|---|
| [01](stories/01-happy-path-mensual.md) | Toma mensual, camino feliz (scan → botones) | ruta rápida, ADR-0004 |
| [02](stories/02-conteo-ciego-y-anomalia.md) | Conteo ciego y anomalía 9-vs-90 | ADR-0001, P-07 |
| [03](stories/03-cero-forzado-al-cerrar.md) | Cero forzado al cerrar la ubicación | P-02, cero_forzado |
| [04](stories/04-captura-por-voz.md) | Captura por voz: el operario habla, el sistema responde | ADR-0014, P-03/P-04/P-05 |

Pendientes (menor prioridad para el demo): granel y pesables, desajuste de empaque, relevo de
turno, apertura por manager con biometría (ADR-0006).

## Convención con event storming
Cada *actividad* de una historia debe tener su comando/evento en `docs/02-event-storming/`.
Si una historia menciona algo que no está modelado, es alcance nuevo — se discute, no se cuela.
