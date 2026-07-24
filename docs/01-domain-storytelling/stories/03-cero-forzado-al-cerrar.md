# 03 · Cero forzado al cerrar la ubicación

**Actores:** Operario · Dispositivo · Dominio de conteo.
**Regla:** saltar ≠ cero. En el dataset real no hay UN SOLO cero, pero hay 79 negativos (P-02).

1. El **operario** termina la estantería y toca **Cerrar ubicación**.
2. El **dominio** compara lo **contado** contra lo **esperado** en esa ubicación y encuentra
   **referencias esperadas que nadie contó** (política `CeroForzadoAlCerrar`).
3. El **dispositivo** **bloquea el cierre** y pregunta, referencia por referencia:
   **"¿Este ítem está en 0, o te faltó contarlo?"** (`CONFIRM_ZERO`).
4a. El **operario** confirma **0 real** → se emite un conteo en 0 explícito. Ese 0 es un dato,
    no un hueco.
4b. El **operario** dice **"me faltó"** → vuelve a contarlo; no se cierra hasta resolverlo.
5. El **dominio** cierra la ubicación solo cuando no quedan huecos silenciosos.

**Por qué así:** un ítem sin anotar es el error #1 de las tomas físicas — un descuadre fantasma
que ensucia todo el reporte. Sin esta regla, el descuadre es ruido (P-02). Los negativos del
ERP van a `STALE_SYSTEM_STOCK`: evidencia de que el sistema miente, no de que el operario contó mal.

**Nota de honestidad (H-02):** la granularidad "por ubicación" (estante) es un supuesto nuestro
—no está en el dato de Colsubsidio. Si no hay estantes marcados, el cierre es por bodega
completa. `ubicacion` es nullable justo por esto. **Decirlo en el pitch.**

**Dónde vive:** `contexts/conteo/domain/policies/cero_forzado.py`.
