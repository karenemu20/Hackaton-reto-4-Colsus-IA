# inventory-ai — Instrucciones para agentes

Captura asistida de inventario físico. Hackathon Colsubsidio x 30X. 5 personas, 48 horas.

## Antes de escribir una sola línea

1. Lee `context/00-reto.md` (qué se pide) y `context/03-hallazgos.md` (por qué el dato está roto).
2. Lee el `CLAUDE.md` de la carpeta que vas a tocar.
3. Si tu cambio contradice un ADR de `docs/04-adr/`, **para y pregunta**. No lo resuelvas tú.

## Invariantes globales — no negociables

- **Conteo ciego.** NUNCA mostrar al operario la cantidad del ERP, ni antes ni durante el conteo. Ni como "sugerencia", ni como placeholder, ni en un tooltip. Si no coincide, se ofrecen opciones sin revelar el valor. (ADR-0001)
- **Botones primero, voz después.** La UI se opera con botones grandes y escaneo. La voz es entrada secundaria y local-first. Ningún flujo puede requerir voz para completarse. (ADR-0003)
- **El dominio decide, la IA interpreta.** Un LLM nunca determina si un conteo es válido, ni aplica una regla, ni calcula un descuadre. Solo resuelve lenguaje a candidatos. (ADR-0007)
- **`count_event` es append-only.** Nunca `UPDATE`, nunca `DELETE`. Corregir = emitir otro evento. (ADR-0005)
- **Un contexto nunca importa a otro contexto.** `contexts/conteo` no puede `import contexts.resolucion`. Solo `contracts/`. (ADR-0009)
- **El ERP es de solo lectura.** Nada escribe al ERP. La salida es un archivo/endpoint de conteo limpio. (ADR-0002)
- **`contracts/` está congelado.** Si necesitas cambiarlo, avisas a las 5 personas primero. Un agente no lo modifica solo.

## Estructura

| Carpeta | Qué vive ahí |
|---|---|
| `context/` | el origen del problema: reto, dataset real, patologías. Léelo, no lo edites |
| `contracts/` | eventos y DTOs compartidos. CONGELADO |
| `contexts/conteo/` | sesión, conteo, políticas, cero forzado, relevo |
| `contexts/resolucion/` | expresión → candidato SKU. LangGraph vive aquí |
| `contexts/calidad_dato/` | eventos de calidad, reconciliación, hotspots |
| `plataforma/` | ERP (ACL), db, auth, config |
| `apps/api` | FastAPI: routing y nada más. Cero lógica |
| `apps/mobile` | UI del operario |
| `docs/` | narrativa para humanos: storytelling, event storming, ADRs. **No la cargues entera** |

## Stack

Python 3.11 · FastAPI · PostgreSQL + pgvector · LangGraph (solo en `resolucion`) · SQLAlchemy

## Estilo

- Español en dominio y nombres de negocio (`ConteoSesion`, `bodega`, `cero_forzado`). Inglés en técnico.
- Type hints obligatorios en `contracts/` y `domain/`.
- Test por cada política de dominio. Lo demás, si sobra tiempo.
