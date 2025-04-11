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
        """Register a function to handle a specific reward ID"""
        self._registered_handlers[reward_id] = handler_func
        logger.info(f"Registered handler for reward ID: {reward_id}")

    def handle_redemption(self, redemption_data: Dict[str, Any]) -> bool:
        """Process a channel point redemption"""
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

            # Update or store reward information
            self._update_reward_info(reward_id, reward_title)

            # Check for registered handler
            if reward_id in self._registered_handlers:
                logger.info(f"Found custom handler for reward ID: {reward_id}")
                return self._registered_handlers[reward_id](redemption_data)

            # Check for action sequence in database
            action_sequence_id = self._get_action_sequence_id(reward_id)
            if action_sequence_id:
                logger.info(
                    f"Found action sequence {action_sequence_id} for reward {reward_title}")
                self._increment_usage_count(reward_id)

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

    def _update_reward_info(self, reward_id: str, title: str) -> None:
        """Store or update a reward title in the database"""
        try:
            existing = db.fetchone(
                "SELECT name FROM twitch_rewards WHERE reward_id = ?",
                (reward_id,)
            )

            if existing:
                if existing['name'] == 'Unknown Reward' or not existing['name']:
                    db.execute(
                        "UPDATE twitch_rewards SET name = ? WHERE reward_id = ?",
                        (title, reward_id)
                    )
                    logger.info(
                        f"Updated reward title for {reward_id} to '{title}'")
            else:
                current_time = datetime.now().isoformat()
                db.execute(
                    "INSERT INTO twitch_rewards (reward_id, name, total_uses, date_added) VALUES (?, ?, 1, ?)",
                    (reward_id, title, current_time)
                )
                logger.info(
                    f"Registered new reward {title} (ID: {reward_id}) in database")

        except Exception as e:
            logger.error(f"Error updating reward info: {e}")

    def _get_action_sequence_id(self, reward_id: str) -> Optional[int]:
        """Get the action sequence ID associated with a reward"""
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

    def _increment_usage_count(self, reward_id: str) -> None:
        """Increment the usage count for a reward"""
        try:
            db.execute(
                "UPDATE twitch_rewards SET total_uses = total_uses + 1 WHERE reward_id = ?",
                (reward_id,)
            )
        except Exception as e:
            logger.error(f"Error incrementing usage count: {e}")


# Singleton instance
channel_points_service = ChannelPointsService(event_bus)
