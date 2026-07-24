# plataforma/erp/

Anti-corruption layer hacia el ERP. **Es un seam, no una integración.** (ADR-0002, S-01)

## Invariantes
- **READ ONLY.** Cero escrituras. La salida del sistema es un archivo/endpoint de conteo limpio.
- Todo lo que sale de aquí ya viene traducido a nuestro lenguaje ubicuo. Nombres del ERP no cruzan la frontera.
- `seed.py` siembra con los CSV reales. Nunca con datos inventados.

Verifica el estado real cuando dudes:
```bash
python3 plataforma/erp/seed.py
```
