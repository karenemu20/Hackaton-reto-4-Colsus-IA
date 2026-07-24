from __future__ import annotations

import json
from typing import Any

import redis
import structlog

logger = structlog.get_logger(__name__)


class MemoryEngine:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_history(self, user_id: str) -> list[dict[str, Any]]:
        key = f"history:{user_id}"
        raw = self.redis.get(key)
        history = json.loads(raw) if raw else []
        logger.info("memory_loaded", user_id=user_id, history_len=len(history))
        return history

    def save(self, user_id: str, user_msg: str, ai_msg: str) -> None:
        key = f"history:{user_id}"
        history = self.get_history(user_id)
        history.append({"user": user_msg, "ai": ai_msg})
        trimmed = history[-10:]
        self.redis.set(key, json.dumps(trimmed, ensure_ascii=False))
        logger.info("memory_saved", user_id=user_id, history_len=len(trimmed))
