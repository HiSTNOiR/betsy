import json

from datetime import datetime
from typing import Dict, Any, Optional, List, Callable

from core.logging import get_logger
from core.errors import handle_error, ValidationError
from db.database import db
from event_bus.bus import event_bus

logger = get_logger("reward_service")


class RewardService:
    def __init__(self):
        self.handlers = {}
        self._handler_factory = None

    def set_handler_factory(self, factory):
        self._handler_factory = factory

    def get_reward(self, reward_id: str) -> Optional[Dict[str, Any]]:
        return db.fetchone("SELECT * FROM twitch_rewards WHERE reward_id = ?", (reward_id,))

    def register_reward(self, reward_data: Dict[str, Any]) -> bool:
        try:
            required_fields = ["reward_id", "name", "cost"]
            for field in required_fields:
                if field not in reward_data:
                    raise ValidationError(f"Missing required field: {field}")

            reward_id = reward_data["reward_id"]
            existing = self.get_reward(reward_id)
            current_time = datetime.now().isoformat()

            reward_data.update({
                "date_added": current_time,
                "last_updated": current_time,
                "total_uses": 0 if not existing else existing.get("total_uses", 0),
                "handler_type": existing.get("handler_type", "default") if existing else "default"
            })

            query = self._build_upsert_query(reward_data, existing)
            db.execute(query["query"], query["values"])

            self._handle_reward_registration(reward_data)
            return True
        except Exception as e:
            handle_error(
                e, {"context": "register_reward", "data": reward_data})
            return False

    def _build_upsert_query(self, reward_data: Dict[str, Any], existing: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if existing:
            fields = [f"{k} = ?" for k in reward_data.keys() if k !=
                      "reward_id"]
            query = f"UPDATE twitch_rewards SET {', '.join(fields)} WHERE reward_id = ?"
            values = list(reward_data.values())[
                :-1] + [reward_data["reward_id"]]
        else:
            fields = ", ".join(reward_data.keys())
            placeholders = ", ".join(["?" for _ in reward_data])
            query = f"INSERT INTO twitch_rewards ({fields}) VALUES ({placeholders})"
            values = list(reward_data.values())

        return {"query": query, "values": values}

    def _handle_reward_registration(self, reward_data: Dict[str, Any]):
        current_time = datetime.now().isoformat()
        reward_data["date_added"] = current_time
        reward_data["last_updated"] = current_time

        if self._handler_factory:
            reward_id = reward_data["reward_id"]
            handler_type = reward_data.get("handler_type", "default")
            handler_config = reward_data.get("handler_config")
            self._handler_factory(reward_id, handler_type, handler_config)

    def record_redemption(self, redemption_data: Dict[str, Any]) -> bool:
        try:
            user = redemption_data.get("user", {})
            user_id = user.get("id", "")
            username = user.get("name", "unknown")
            reward = redemption_data.get("reward", {})
            reward_id = reward.get("id", "")

            if not user_id or not reward_id:
                logger.warning(
                    "Missing user_id or reward_id in redemption data")
                return False

            current_time = datetime.now().isoformat()

            self._ensure_user_exists(user_id, username, current_time)
            self._insert_redemption_record(reward_id, user_id, current_time,
                                           redemption_data.get("input", ""))
            return True
        except Exception as e:
            handle_error(e, {"redemption_data": redemption_data})
            return False

    def _ensure_user_exists(self, user_id: str, username: str, current_time: str):
        user_exists = db.fetchone(
            "SELECT 1 FROM users WHERE twitch_user_id = ?", (user_id,))
        if not user_exists:
            db.execute(
                "INSERT INTO users (twitch_user_id, twitch_username, rank, points, date_added, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, username, "viewer", 0, current_time, current_time)
            )

    def _insert_redemption_record(self, reward_id: str, user_id: str, current_time: str, user_input: str):
        db.execute(
            "INSERT INTO reward_redemptions (reward_id, user_id, redeemed_at, user_input) VALUES (?, ?, ?, ?)",
            (reward_id, user_id, current_time, user_input)
        )
        db.execute(
            "UPDATE twitch_rewards SET total_uses = total_uses + 1 WHERE reward_id = ?",
            (reward_id,)
        )


reward_service = RewardService()
