from typing import Dict, Any, Optional, List
from datetime import datetime

from core.logging import get_logger
from core.errors import handle_error, TwitchError
from db.database import db
from event_bus.bus import event_bus

logger = get_logger("channel_points_service")


class ChannelPointsService:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._registered_handlers = {}

    def register_handler(self, reward_id: str, handler_func):
        self._registered_handlers[reward_id] = handler_func
        logger.info(f"Registered handler for reward ID: {reward_id}")

    def handle_redemption(self, redemption_data: Dict[str, Any]) -> bool:
        try:
            # Extract key data
            user = redemption_data.get("user", {})
            username = user.get("name", "unknown")
            reward = redemption_data.get("reward", {})
            reward_id = reward.get("id", "")
            reward_title = reward.get("title", "Unknown Reward")
            user_input = redemption_data.get("input", "")

            logger.info(
                f"Processing redemption: {username} redeemed '{reward_title}' (ID: {reward_id})")

            # Record the redemption in our database
            from utils.reward_service import reward_service
            reward_service.record_redemption(redemption_data)

            # Check for registered handler
            if reward_id in self._registered_handlers:
                logger.info(f"Found custom handler for reward ID: {reward_id}")
                return self._registered_handlers[reward_id](redemption_data)

            # Check for action sequence in database
            action_sequence_id = self._get_action_sequence_id(reward_id)
            if action_sequence_id:
                logger.info(
                    f"Found action sequence {action_sequence_id} for reward {reward_title}")

                # Trigger the action sequence
                self.event_bus.publish("trigger_action_sequence", {
                    "action_sequence_id": action_sequence_id,
                    "source": "channel_point",
                    "user": username,
                    "data": {
                        "reward_title": reward_title,
                        "reward_id": reward_id,
                        "user_input": user_input
                    }
                })
                return True

            logger.info(f"No handler found for reward ID: {reward_id}")
            return False

        except Exception as e:
            handle_error(e, {"redemption_data": redemption_data})
            return False

    def _get_action_sequence_id(self, reward_id: str) -> Optional[int]:
        try:
            reward_action = db.fetchone(
                "SELECT action_sequence_id FROM twitch_rewards WHERE reward_id = ?",
                (reward_id,)
            )

            if reward_action and reward_action.get('action_sequence_id'):
                return reward_action['action_sequence_id']
            return None

        except Exception as e:
            logger.error(f"Error getting action sequence ID: {e}")
            return None


# Singleton instance
channel_points_service = ChannelPointsService(event_bus)
