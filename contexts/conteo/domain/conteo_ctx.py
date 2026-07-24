"""ConteoCtx — el comando enriquecido que evaluan las politicas.

Este tipo era el SEGUNDO contrato del proyecto, y hasta ahora estaba IMPLICITO:
las politicas leen `ctx.esperado_erp`, `ctx.unidad_esperada`, `ctx.cerrando_ubicacion`,
`ctx.esperados_no_contados`... campos que NO existen en RegistrarConteoCmd
(contracts/dtos.py). Sin un tipo con nombre, cada persona iba a enriquecer con campos
distintos -> exactamente el fallo que `contracts/` existe para evitar, pero fuera de
`contracts/` y sin congelar. Este archivo lo cierra.

Por que vive aqui y NO en `contracts/`:
  - Es interno al contexto de conteo. Ninguna politica de otro contexto lo necesita.
  - No cruza fronteras -> no aplica el congelado de `contracts/` (ADR-0009).
  - `contracts/` esta congelado; un agente no lo toca. Este tipo es del dominio de conteo.

INVARIANTE ADR-0001 (conteo ciego): `esperado_erp` es el stock del corte del ERP.
Vive aqui SOLO para evaluar anomalia dentro del dominio. NUNCA cruza a la respuesta
HTTP, nunca entra en `PolicyResult.message`. Si aparece en una respuesta, es bug
bloqueante.

Quien lo construye: el caso de uso `RegistrarConteo` toma el `RegistrarConteoCmd` que
llega de apps/api y lo enriquece con:
  - `esperado_erp`     <- plataforma/erp (stock_corte de ese item+bodega)
  - `unidad_esperada`  <- plataforma/erp (catalogo)
  - `nombre_resuelto`  <- SIEMPRE nombre_norm, nunca nombre_raw (ver conteo/CLAUDE.md)
  - `cerrando_ubicacion` / `esperados_no_contados` <- estado de la sesion
...y recien entonces llama `registry.evaluar(ctx)`.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConteoCtx:
    # --- eco del RegistrarConteoCmd (contracts/dtos.py). Misma forma, mismos nombres ---
    session_id: str
    bodega_id: str
    ubicacion: str | None
    sku: str | None
    utterance: str | None
    cantidad: float
    unidad: str | None
    packaging: str | None
    fuente: str                              # scan | manual | voz | foto
    confianza: float | None
    operator_id: str
    device_id: str
    event_id: str
    override_motivo: str | None = None

    # --- enriquecimiento del dominio (lo agrega el caso de uso, no el device) ---
    esperado_erp: float | None = None        # stock del corte. NUNCA se muestra (ADR-0001)
    unidad_esperada: str | None = None       # del catalogo, para ValidarUnidad (P-06)
    nombre_resuelto: str | None = None        # SIEMPRE nombre_norm, nunca raw (P-05)

    # --- estado de sesion, solo relevante al cerrar una ubicacion ---
    cerrando_ubicacion: bool = False
    esperados_no_contados: list[str] = field(default_factory=list)
