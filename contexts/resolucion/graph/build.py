"""Ensambla la FSM con LangGraph. LangGraph vive SOLO aqui (ADR-0007).
La ruta rapida (scan -> botones) NO construye este grafo: no paga latencia de LLM.

Estados (contexts/resolucion/CLAUDE.md):
  resolviendo -> [desambiguando] -> esperando_cantidad -> emitiendo_comando
"""
from __future__ import annotations
from langgraph.graph import StateGraph, END

from .state import ResolverState
from . import nodes


def construir_grafo():
    g = StateGraph(ResolverState)
    g.add_node("resolviendo", nodes.resolviendo)
    g.add_node("desambiguando", nodes.desambiguando)
    g.add_node("esperando_cantidad", nodes.esperando_cantidad)
    g.add_node("emitiendo_comando", nodes.emitiendo_comando)

    g.set_entry_point("resolviendo")
    g.add_conditional_edges("resolviendo", nodes.necesita_desambiguar, {
        "desambiguando": "desambiguando",
        "esperando_cantidad": "esperando_cantidad",
    })
    g.add_edge("desambiguando", "esperando_cantidad")
    g.add_edge("esperando_cantidad", "emitiendo_comando")
    g.add_edge("emitiendo_comando", END)
    return g.compile()
