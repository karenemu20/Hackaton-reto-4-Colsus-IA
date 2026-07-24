# Hackaton-reto-4-Colsus-IA (inventory-ai)

Prototipo para el Reto 4 (Toma de Inventarios) del Hackathon Colsubsidio x 30X. Captura conversacional por voz y foto que reconoce producto, cantidad y unidad, valida contra el catálogo real de bodegas y detecta anomalías antes de guardar, para que el conteo físico entre limpio al sistema desde la primera vez.

## Arranque

```bash
python3 plataforma/erp/seed.py       # verifica los datos reales
docker compose up -d               # postgres + pgvector
psql $DB < plataforma/db/schema.sql
```

## Cómo leer este repo

1. `CLAUDE.md` — los invariantes. Empieza aquí.
2. `context/00-reto.md` y `context/03-hallazgos.md` — el problema y la evidencia.
3. `ARCHITECTURE.md` — el mapa en una página.
4. `docs/` — el porqué (storytelling, event storming, ADRs). Para humanos.

## Reparto (5 personas)

| Persona | Carpeta | Sin solapamiento |
|---|---|---|
| 1 | `contexts/conteo/` | sesión, políticas, cero forzado |
| 2 | `contexts/resolucion/` | grafo, embeddings, desambiguación |
| 3 | `contexts/calidad_dato/` | eventos, reconciliación, hotspots |
| 4 | `apps/mobile/` | UI operario, botones grandes, scan |
| 5 | `apps/api/` + `plataforma/` | endpoints, ERP mock, db |

**Hora 1 es de una sola persona:** congelar `contracts/` y escribir los `CLAUDE.md`. Hasta que eso exista, los otros 4 no arrancan — si arrancan, a la hora 6 hay cinco arquitecturas.
