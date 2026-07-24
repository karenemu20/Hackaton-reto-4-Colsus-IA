"""Estado del grafo de la ruta asistida (LangGraph)."""
from __future__ import annotations
from typing import TypedDict
from contracts.dtos import Candidato, ResolucionResult


class ResolverState(TypedDict, total=False):
    # --- entrada ---
    session_id: str
    bodega_id: str
    fuente: str                    # voz | manual | foto
    entrada: object                # str (voz/texto) | bytes (foto)
    operator_id: str
    device_id: str
    event_id: str
    ubicacion: str | None
    utterance: str | None

    # --- identidad del producto: la llena 'resolviendo', IGUAL para toda fuente ---
    resolucion: ResolucionResult
    candidato: Candidato           # el elegido tras desambiguar, o el unico
    pregunta: str | None

    # --- cantidad ---
    cantidad_sugerida: float | None  # SOLO vision la trae; el operario la confirma
    cantidad: float

    # --- salida ---
    comando: object                # RegistrarConteoCmd, listo para cruzar a conteo
