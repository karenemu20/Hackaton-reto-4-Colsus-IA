from __future__ import annotations

import os
from typing import Any, TypedDict

from langchain_core.language_models import FakeListLLM
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger(__name__)


class Decision(BaseModel):
    action: str = Field(description="Action to execute")
    params: dict[str, Any] = Field(default_factory=dict, description="Tool parameters")
    confidence: float = Field(ge=0.0, le=1.0, description="Decision confidence")
    reasoning: str = Field(description="Short explanation of the decision")


class ReasoningState(TypedDict):
    canonical_json: dict[str, Any]
    history: list[dict[str, Any]]
    decision: Decision


def _create_llm(model: str = "gpt-4o"):
    provider = os.environ.get("LLM_PROVIDER", "gemini").strip().lower()

    if provider == "gemini":
        gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if gemini_key:
            from langchain_google_genai import ChatGoogleGenerativeAI

            gemini_model = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")
            return ChatGoogleGenerativeAI(
                model=gemini_model,
                temperature=0,
                google_api_key=gemini_key,
            )
        logger.warning(
            "no_gemini_key",
            message="GEMINI_API_KEY/GOOGLE_API_KEY not set. Using FakeListLLM for testing.",
        )
    elif provider == "openai":
        from langchain_openai import ChatOpenAI

        openai_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_ADMIN_KEY")
        if openai_key:
            return ChatOpenAI(model=model, temperature=0)
        logger.warning(
            "no_openai_key",
            message="OPENAI_API_KEY not set. Using FakeListLLM for testing.",
        )
    else:
        logger.warning(
            "unknown_llm_provider",
            message="LLM_PROVIDER must be 'gemini' or 'openai'. Using FakeListLLM for testing.",
            provider=provider,
        )

    return FakeListLLM(
        responses=[
            '{"action": "responder_texto", "params": {"message": "Hola, ¿en qué puedo ayudarte?"}, "confidence": 0.95, "reasoning": "No se detectó una acción específica, se responde con un saludo."}'
        ]
    )


class ReasoningEngine:
    def __init__(self, model: str = "gpt-4o") -> None:
        self.llm = _create_llm(model=model)
        self.parser = PydanticOutputParser(pydantic_object=Decision)
        self.graph = self._build_graph()

    def _build_graph(self):
        prompt = ChatPromptTemplate.from_template(
            """
Eres el motor de razonamiento de un agente.
Debes decidir UNA acción usando SOLO estas tools disponibles:
- consultar_saldo(user_id: str)
- responder_texto(message: str)

Reglas:
1) Si el usuario pregunta por saldo, usa action="consultar_saldo" y params={{"user_id":"<user_id>"}}.
2) Si no aplica consultar_saldo, usa action="responder_texto" y params={{"message":"<texto>"}}.
3) confidence debe ser un número entre 0 y 1.
4) reasoning debe explicar en una frase por qué elegiste la acción.
5) Devuelve SOLO JSON válido según el formato.

Historial: {history}
Entrada canónica: {canonical_json}

{format_instructions}
            """.strip()
        )
        chain = prompt | self.llm | self.parser

        def reason_node(state: ReasoningState) -> ReasoningState:
            decision = chain.invoke(
                {
                    "history": state["history"],
                    "canonical_json": state["canonical_json"],
                    "format_instructions": self.parser.get_format_instructions(),
                }
            )
            logger.info(
                "reasoning_done",
                action=decision.action,
                confidence=decision.confidence,
            )
            return {**state, "decision": decision}

        builder = StateGraph(ReasoningState)
        builder.add_node("reason_node", reason_node)
        builder.add_edge(START, "reason_node")
        builder.add_edge("reason_node", END)
        return builder.compile()

    def think(self, canonical_json: dict[str, Any], history: list[dict[str, Any]]) -> Decision:
        result = self.graph.invoke(
            {"canonical_json": canonical_json, "history": history, "decision": Decision(action="responder_texto", params={"message": ""}, confidence=0.0, reasoning="") }
        )
        return result["decision"]
