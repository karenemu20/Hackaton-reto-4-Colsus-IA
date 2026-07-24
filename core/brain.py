from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field
import structlog

from core.action import ActionEngine
from core.decision import DecisionEngine
from core.memory import MemoryEngine
from core.reasoning import ReasoningEngine

app = FastAPI()


class CanonicalInput(BaseModel):
    user_id: str
    timestamp: str
    input_type: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


def _configure_logging() -> None:
    if structlog.is_configured():
        return
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ]
    )


class Brain:
    def __init__(self) -> None:
        _configure_logging()
        self.logger = structlog.get_logger(__name__)
        self.memory = MemoryEngine()
        self.reasoning = ReasoningEngine()
        self.decision = DecisionEngine()
        self.action = ActionEngine()

    def run(self, canonical_json: dict[str, Any]) -> dict[str, Any]:
        canonical = CanonicalInput(**canonical_json)
        self.logger.info(
            "perception_done",
            user_id=canonical.user_id,
            input_type=canonical.input_type,
        )

        history = self.memory.get_history(canonical.user_id)
        llm_decision = self.reasoning.think(canonical.model_dump(), history)
        final_decision = self.decision.review(llm_decision)
        response = self.action.execute(final_decision.action, final_decision.params)
        self.memory.save(canonical.user_id, canonical.text, response)

        result = {
            "response": response,
            "action_executed": final_decision.action,
            "confidence": final_decision.confidence,
            "thought": final_decision.reasoning,
        }
        self.logger.info(
            "brain_done",
            user_id=canonical.user_id,
            action_executed=result["action_executed"],
            confidence=result["confidence"],
        )
        return result


_brain: Brain | None = None


def get_brain() -> Brain:
    global _brain
    if _brain is None:
        _brain = Brain()
    return _brain


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/brain")
def process(input_data: CanonicalInput) -> dict[str, Any]:
    return get_brain().run(input_data.model_dump())
