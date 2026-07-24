# ADR-0007 — LangGraph solo en la ruta asistida

**Estado:** Aceptado

## Contexto
La propuesta inicial ponía LangGraph en la columna vertebral: `FastAPI → Application → LangGraph → Domain`. Contradicción interna: el mismo documento declaraba el problema "predominantemente determinístico" y rechazaba multiagente/ReAct, pero metía un framework de grafos para orquestar cinco estados.

## Decisión
LangGraph vive **dentro de `contexts/resolucion/graph/`** y solo se activa cuando la entrada es ambigua (voz, texto libre, foto). La ruta rápida (scan → botones) no lo atraviesa.

## Consecuencias
- El 80% de los conteos no paga latencia de LLM.
- La FSM garantiza que el LLM nunca decide: interpreta y propone candidatos.
- Un nodo del grafo solo puede llamar `use_cases/`. Si importa `domain/policies`, la arquitectura ya se rompió — **este es el invariante que se viola en la hora 20 del hackathon.**
- El estado conversacional en el servidor no bloquea el conteo si se cae la señal.

## Alternativas descartadas
- *LangGraph como orquestador de sesión*: acopla el conteo a la disponibilidad del LLM.
- *Sin LangGraph, FSM a mano*: pierde el manejo de estado del diálogo en desambiguación multi-turno.
