"""Nodos del grafo (ruta asistida). Cada nodo SOLO llama use_cases/ (ADR-0007):
nunca el matcher directo, nunca un repositorio, nunca una politica, nunca el ERP.

FIJATE: ningun nodo hace `if fuente == FOTO`. La fuente se resuelve en el registry de
adapters. Por eso agregar vision no toco este archivo — es la prueba de ADR-0012.
"""
from __future__ import annotations

from contracts.dtos import RegistrarConteoCmd
from ..use_cases.resolver_expresion import ResolverExpresionCmd, resolver_expresion
from .state import ResolverState


def resolviendo(state: ResolverState) -> ResolverState:
    r = resolver_expresion(ResolverExpresionCmd(
        bodega_id=state["bodega_id"], fuente=state["fuente"], entrada=state["entrada"]))
    state["resolucion"] = r
    state["pregunta"] = r.pregunta
    if not r.requiere_desambiguacion and r.candidatos:
        state["candidato"] = r.candidatos[0]   # sin empate: candidato unico
    return state


def necesita_desambiguar(state: ResolverState) -> str:
    return "desambiguando" if state["resolucion"].requiere_desambiguacion else "esperando_cantidad"


def desambiguando(state: ResolverState) -> ResolverState:
    # El operario toca un boton grande (uno de los candidatos). En runtime esa eleccion
    # vuelve como un turno nuevo; el front la deja en state['candidato'].
    return state


def esperando_cantidad(state: ResolverState) -> ResolverState:
    # Unico punto donde vision aporta un extra: una cantidad sugerida a confirmar con +/-.
    # Si no vino de foto, cantidad_sugerida es None y el operario la teclea desde cero.
    return state


def emitiendo_comando(state: ResolverState) -> ResolverState:
    c = state["candidato"]
    state["comando"] = RegistrarConteoCmd(
        session_id=state.get("session_id", ""),
        bodega_id=state["bodega_id"],
        ubicacion=state.get("ubicacion"),
        sku=c.sku,
        utterance=state.get("utterance"),
        cantidad=state["cantidad"],
        unidad=c.unidad_esperada,
        packaging=None,
        fuente=state["fuente"],
        confianza=c.confianza,
        operator_id=state.get("operator_id", ""),
        device_id=state.get("device_id", ""),
        event_id=state.get("event_id", ""),
    )
    return state
