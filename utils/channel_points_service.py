from typing import Dict, Any, Optional, Callable

from core.logging import get_logger
from core.errors import handle_error
from event_bus.bus import event_bus

logger = get_logger("channel_points_service")


class ChannelPointsService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._registered_handlers = {}
        self._reward_service = None

    def initialize(self, reward_service):
        self._reward_service = reward_service
        reward_service.set_handler_factory(self._register_reward_handler)

    def _register_reward_handler(self, reward_id: str, handler_type: str, handler_config: Optional[Dict[str, Any]] = None):
        if handler_type == "default":
            self.register_handler(reward_id, self._default_handler)
        elif handler_type == "custom":
            self.register_handler(
                reward_id, self._create_custom_handler(handler_config))

    def _default_handler(self, redemption_data: Dict[str, Any]) -> bool:
        reward_id = redemption_data.get("reward", {}).get("id", "")
        reward = self._reward_service.get_reward(reward_id)
        action_sequence_id = reward.get("action_sequence_id")

        if action_sequence_id:
            self.event_bus.publish("trigger_action_sequence", {
                "action_sequence_id": action_sequence_id,
                "source": "channel_point",
                "user": redemption_data.get("user", {}).get("name", "unknown"),
                "data": redemption_data
            })
            return True
        return False

    def _create_custom_handler(self, handler_config: Optional[Dict[str, Any]]) -> Callable:
        def custom_handler(redemption_data: Dict[str, Any]) -> bool:
            try:
                config = handler_config or {}

                if "message_template" in config:
                    self._send_custom_message(redemption_data, config)

                if "action_sequence_id" in config:
                    self.event_bus.publish("trigger_action_sequence", {
                        "action_sequence_id": config["action_sequence_id"],
                        "source": "channel_point",
                        "user": redemption_data.get("user", {}).get("name", "unknown"),
                        "data": redemption_data
                    })

                return True
            except Exception as e:
                logger.error(f"Custom handler error: {e}")
                return False
        return custom_handler

    def _send_custom_message(self, redemption_data: Dict[str, Any], config: Dict[str, Any]):
        user = redemption_data.get("user", {})
        reward = redemption_data.get("reward", {})

        message = config["message_template"]
        message = message.replace("{username}", user.get("name", "unknown"))
        message = message.replace(
            "{reward}", reward.get("title", "Unknown Reward"))

        self.event_bus.publish("send_twitch_message", {
            "channel": redemption_data.get("channel", ""),
            "content": message
        })

    def register_handler(self, reward_id: str, handler_func: Callable):
        self._registered_handlers[reward_id] = handler_func
        logger.info(f"Registered handler for reward ID: {reward_id}")

    def handle_redemption(self, redemption_data: Dict[str, Any]) -> bool:
        try:
            reward = redemption_data.get("reward", {})
            reward_id = reward.get("id", "")

            self._ensure_reward_exists(reward)

            if not self._reward_service.record_redemption(redemption_data):
                return False

            handler = self._registered_handlers.get(reward_id)
            return handler(redemption_data) if handler else False

        except Exception as e:
            handle_error(e, {"redemption_data": redemption_data})
            return False

    def _ensure_reward_exists(self, reward: Dict[str, Any]):
        if not self._reward_service.get_reward(reward.get("id", "")):
            reward_data = {
                "reward_id": reward.get("id", ""),
                "name": reward.get("title", "Unknown Reward"),
                "description": reward.get("prompt", ""),
                "cost": reward.get("cost", 0),
                "is_enabled": True,
                "handler_type": "default"
            }
            self._reward_service.register_reward(reward_data)


channel_points_service = ChannelPointsService(event_bus)
