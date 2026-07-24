# contexts/conteo/

Sesión de conteo, captura, políticas de dominio, cierre de ubicación, relevo.
**Es el corazón. Todo lo demás lo alimenta o lo consume.**

## Invariantes — no negociables
- **NUNCA leer `stock_corte` para mostrarlo.** Se usa solo para evaluar anomalía dentro del dominio, y el mensaje al operario jamás contiene el número. (ADR-0001)
- `count_event` es append-only. Si escribes un `UPDATE`, está mal.
- Toda política devuelve `PolicyResult`, nunca `bool`. (ADR-0008)
- Toda política recibe un **`ConteoCtx`** (`domain/conteo_ctx.py`), nunca un dict ni el DTO crudo. El caso de uso enriquece el `RegistrarConteoCmd` con `esperado_erp`, `unidad_esperada`, `nombre_resuelto` y el estado de cierre **antes** de llamar `registry.evaluar`.
- **`nombre_resuelto` guarda SIEMPRE `nombre_norm`, nunca `nombre_raw`.** Las proyecciones `cobertura` y `reconciliacion` (`plataforma/db/schema.sql`) unen por `nombre_resuelto = nombre_norm`. Si guardas el raw, la reconciliación devuelve NULL en silencio: descuadre falso, no error. (P-05)
- NUNCA `import contexts.resolucion`. Solo `contracts/`. (ADR-0009)
- El override del operario **siempre gana**, siempre se audita, y siempre dispara `SECOND_COUNT`. Lo garantiza la política `SegundoConteo`, no un `if` suelto.

## Políticas
Implementadas: `DetectarAnomaliaMagnitud` · `ValidarUnidad` · `CeroForzadoAlCerrar` · `SegundoConteo`.
Pendientes: `ValidarCantidad` · `ConfirmarEmpaque`.

`DetectarAnomaliaMagnitud` y `CeroForzadoAlCerrar` son las dos del demo. `SegundoConteo` cierra el invariante del override (antes se afirmaba sin código que lo garantizara).

## Antes de tocar esto
`context/03-hallazgos.md` P-02 (no hay ceros, hay 79 negativos) y P-07 (mediana 12).
