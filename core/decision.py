from __future__ import annotations

from core.reasoning import Decision
import structlog

logger = structlog.get_logger(__name__)


class DecisionEngine:
    def __init__(self, threshold: float = 0.8) -> None:
        self.threshold = threshold

    def review(self, llm_decision: Decision) -> Decision:
        if llm_decision.confidence > self.threshold:
            logger.info(
                "decision_done",
                approved=True,
                action=llm_decision.action,
                confidence=llm_decision.confidence,
            )
            return llm_decision

        fallback = Decision(
            action="pedir_ayuda",
            params={"message": "No tengo suficiente confianza para ejecutar una acción automática."},
            confidence=llm_decision.confidence,
            reasoning=(
                f"Confianza {llm_decision.confidence:.2f} por debajo del umbral "
                f"{self.threshold:.2f}. Se deriva a pedir_ayuda."
            ),
        )
        logger.info(
            "decision_done",
            approved=False,
            action=fallback.action,
            confidence=fallback.confidence,
        )
        return fallback
