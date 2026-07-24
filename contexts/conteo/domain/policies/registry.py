"""Registro de politicas. AGREGAR UNA REGLA = 1 archivo + 1 linea aqui.

Nada mas. Ni FastAPI, ni el grafo, ni el frontend, ni el schema.
Ese es el requisito #1 del proyecto: reglas a velocidad de luz frente al operario.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from contracts.policy_result import PolicyResult
from .anomalia_magnitud import DetectarAnomaliaMagnitud
from .cero_forzado import CeroForzadoAlCerrar
from .validar_unidad import ValidarUnidad
from .segundo_conteo import SegundoConteo

if TYPE_CHECKING:
    from ..conteo_ctx import ConteoCtx

POLITICAS = [
    DetectarAnomaliaMagnitud(),
    ValidarUnidad(),
    CeroForzadoAlCerrar(),
    SegundoConteo(),
    # <-- nueva regla aqui. Una linea.
]


def evaluar(ctx: "ConteoCtx") -> list[PolicyResult]:
    """ctx es el RegistrarConteoCmd enriquecido -> ConteoCtx (domain/conteo_ctx.py).
    El agregado lo construye y llama esto."""
    return [p.evaluar(ctx) for p in POLITICAS if p.aplica(ctx)]
