# Bounded Contexts

**Tres contextos, no cuatro.** (ver hotspot H-06)

| Contexto | Carpeta | Responsabilidad | Comandos propios |
|---|---|---|---|
| **Conteo** | `contexts/conteo/` | sesión, captura, políticas, cierre, relevo | sí |
| **Resolución Semántica** | `contexts/resolucion/` | expresión → candidatos, dentro del scope de bodega | sí |
| **Calidad de Dato** | `contexts/calidad_dato/` | eventos de calidad, hotspots | sí |

**Reconciliación NO es un contexto.** No tiene comandos ni invariantes propios: solo lee el log y el corte. Es una proyección en `contexts/calidad_dato/projections/`.

## Relaciones (context map)
```
Conteo ──(publica count_event)──▶ Calidad de Dato
Conteo ──(consume Candidato)───▶ Resolución Semántica
Ambos ──(ACL, read-only)───────▶ ERP  [plataforma/erp]
```

**Regla de aislamiento:** un contexto nunca importa a otro. Solo `contracts/`. (ADR-0009)
