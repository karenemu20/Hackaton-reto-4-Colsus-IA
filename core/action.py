from __future__ import annotations

from typing import Any, Callable

import structlog

logger = structlog.get_logger(__name__)

class ActionEngine:
    def __init__(self) -> None:
        self.TOOL_REGISTRY: dict[str, Callable[..., str]] = {
            "consultar_saldo": self.consultar_saldo,
            "responder_texto": self.responder_texto,
            "crear_ticket": self.crear_ticket,
        }

    def consultar_saldo(self, user_id: str) -> str:
        return "Tu saldo es $150.000"

    def responder_texto(self, message: str) -> str:
        return message

    def crear_ticket(self, problema: str) -> str:
        logger.info("ticket_created", problema=problema) # log extra para ver el problema
        return "Ticket #12345 creado"

    def execute(self, action_name: str, params: dict[str, Any]) -> str:
        if action_name == "pedir_ayuda":
            message = params.get("message", "Necesito ayuda para resolver esta solicitud.")
            output = self.responder_texto(message)
            logger.info("action_done", action_executed="pedir_ayuda") # QUITÉ event=
            return output

        tool = self.TOOL_REGISTRY.get(action_name)
        if not tool:
            output = "No pude ejecutar esa acción"
            logger.info("action_done", action_executed="accion_desconocida") # QUITÉ event=
            return output

        output = tool(**params)
        logger.info("action_done", action_executed=action_name) # QUITÉ event=
        return output
