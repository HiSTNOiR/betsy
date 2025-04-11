import json

from typing import Dict, Any, Optional, List
from datetime import datetime

from core.logging import get_logger
from core.errors import handle_error, ValidationError, TwitchError
from db.database import db
from event_bus.bus import event_bus
from utils.channel_points_service import channel_points_service

logger = get_logger("reward_service")


class RewardService:
    def __init__(self):
        self.handlers = {}
        self._load_handlers()

    def _load_handlers(self):
        try:
            handlers = db.fetchall(
                "SELECT * FROM reward_handlers WHERE enabled = 1")
            for handler in handlers:
                self.handlers[handler['handler_name']] = handler
                logger.info(
                    f"Loaded reward handler: {handler['handler_name']}")
        except Exception as e:
            logger.error(f"Error loading reward handlers: {e}")

    def get_all_rewards(self) -> List[Dict[str, Any]]:
        try:
            return db.fetchall("SELECT * FROM twitch_rewards ORDER BY cost ASC")
        except Exception as e:
            handle_error(e, {"context": "get_all_rewards"})
            return []

    def get_reward(self, reward_id: str) -> Optional[Dict[str, Any]]:
        try:
            return db.fetchone("SELECT * FROM twitch_rewards WHERE reward_id = ?", (reward_id,))
        except Exception as e:
            handle_error(e, {"context": "get_reward", "reward_id": reward_id})
            return None

    def register_reward(self, reward_data: Dict[str, Any]) -> bool:
        try:
            required_fields = ["reward_id", "name", "cost"]
            for field in required_fields:
                if field not in reward_data:
                    raise ValidationError(f"Missing required field: {field}")

            reward_id = reward_data["reward_id"]
            existing = self.get_reward(reward_id)

            current_time = datetime.now().isoformat()

            if existing:
                # Update existing reward
                fields = []
                values = []
                for key, value in reward_data.items():
                    if key != "reward_id" and hasattr(existing, key):
                        fields.append(f"{key} = ?")
                        values.append(value)

                values.append(current_time)
                values.append(reward_id)

                query = f"UPDATE twitch_rewards SET {', '.join(fields)}, last_updated = ? WHERE reward_id = ?"
                db.execute(query, values)
                logger.info(
                    f"Updated reward {reward_data['name']} (ID: {reward_id})")
            else:
                # Insert new reward
                reward_data["date_added"] = current_time
                reward_data["last_updated"] = current_time
                reward_data["total_uses"] = 0

                fields = ", ".join(reward_data.keys())
                placeholders = ", ".join(["?" for _ in reward_data])

                query = f"INSERT INTO twitch_rewards ({fields}) VALUES ({placeholders})"
                db.execute(query, list(reward_data.values()))
                logger.info(
                    f"Registered new reward {reward_data['name']} (ID: {reward_id})")

                # Register with channel_points_service if has a handler_type
                if "handler_type" in reward_data and reward_data["handler_type"] != "default":
                    self.register_handler(
                        reward_id, reward_data["handler_type"], reward_data.get("handler_config"))

            return True
        except Exception as e:
            handle_error(e, {"context": "register_reward",
                         "reward_data": reward_data})
            return False

    def update_reward(self, reward_id: str, update_data: Dict[str, Any]) -> bool:
        try:
            existing = self.get_reward(reward_id)
            if not existing:
                logger.warning(
                    f"Attempted to update non-existent reward: {reward_id}")
                return False

            fields = []
            values = []
            for key, value in update_data.items():
                if key != "reward_id" and key != "id":
                    fields.append(f"{key} = ?")
                    values.append(value)

            if not fields:
                return True  # Nothing to update

            current_time = datetime.now().isoformat()
            fields.append("last_updated = ?")
            values.append(current_time)
            values.append(reward_id)

            query = f"UPDATE twitch_rewards SET {', '.join(fields)} WHERE reward_id = ?"
            db.execute(query, values)

            logger.info(f"Updated reward {existing['name']} (ID: {reward_id})")

            # Update handler if handler_type changed
            if "handler_type" in update_data:
                if update_data["handler_type"] != existing.get("handler_type", "default"):
                    self.register_handler(
                        reward_id, update_data["handler_type"], update_data.get("handler_config"))

            return True
        except Exception as e:
            handle_error(e, {"context": "update_reward",
                         "reward_id": reward_id, "update_data": update_data})
            return False

    def delete_reward(self, reward_id: str) -> bool:
        try:
            existing = self.get_reward(reward_id)
            if not existing:
                logger.warning(
                    f"Attempted to delete non-existent reward: {reward_id}")
                return False

            db.execute(
                "DELETE FROM twitch_rewards WHERE reward_id = ?", (reward_id,))
            logger.info(f"Deleted reward {existing['name']} (ID: {reward_id})")

            # Unregister from channel_points_service
            if reward_id in channel_points_service._registered_handlers:
                del channel_points_service._registered_handlers[reward_id]

            return True
        except Exception as e:
            handle_error(
                e, {"context": "delete_reward", "reward_id": reward_id})
            return False

    def register_handler(self, reward_id: str, handler_type: str, handler_config: Optional[Dict[str, Any]] = None) -> bool:
        try:
            if handler_type == "default":
                # Use default handler (just triggers the action sequence)
                if reward_id in channel_points_service._registered_handlers:
                    del channel_points_service._registered_handlers[reward_id]
                return True

            if handler_type == "custom" and handler_config:
                # Parse the handler configuration
                config = handler_config if isinstance(
                    handler_config, dict) else json.loads(handler_config)

                # Create a custom handler function
                def custom_handler(redemption_data):
                    try:
                        # Extract data from redemption
                        user = redemption_data.get("user", {})
                        username = user.get("name", "unknown")
                        user_input = redemption_data.get("input", "")
                        reward = redemption_data.get("reward", {})
                        reward_title = reward.get("title", "Unknown Reward")

                        # Process based on config
                        if "message_template" in config:
                            message = config["message_template"]
                            message = message.replace("{username}", username)
                            message = message.replace("{input}", user_input)
                            message = message.replace("{reward}", reward_title)

                            # Send message to chat
                            channel = redemption_data.get("channel", "")
                            if channel:
                                event_bus.publish("send_twitch_message", {
                                    "channel": channel,
                                    "content": message
                                })

                        # Trigger action sequence if configured
                        if "action_sequence_id" in config:
                            event_bus.publish("trigger_action_sequence", {
                                "action_sequence_id": config["action_sequence_id"],
                                "source": "channel_point",
                                "user": username,
                                "data": {
                                    "reward_title": reward_title,
                                    "reward_id": reward_id,
                                    "user_input": user_input
                                }
                            })

                        return True
                    except Exception as e:
                        logger.error(
                            f"Error in custom handler for {reward_id}: {e}")
                        return False

                # Register the custom handler
                channel_points_service.register_handler(
                    reward_id, custom_handler)
                logger.info(
                    f"Registered custom handler for reward ID: {reward_id}")
                return True

            # For other handler types, we'd have a similar approach
            logger.warning(f"Unsupported handler type: {handler_type}")
            return False
        except Exception as e:
            handle_error(e, {"context": "register_handler",
                         "reward_id": reward_id, "handler_type": handler_type})
            return False

    def record_redemption(self, redemption_data: Dict[str, Any]) -> bool:
        try:
            user = redemption_data.get("user", {})
            user_id = user.get("id", "")
            username = user.get("name", "unknown")
            reward = redemption_data.get("reward", {})
            reward_id = reward.get("id", "")
            reward_title = reward.get("title", "Unknown Reward")
            user_input = redemption_data.get("input", "")

            if not user_id or not reward_id:
                logger.warning(
                    "Missing user_id or reward_id in redemption data")
                return False

            current_time = datetime.now().isoformat()

            # Check if the user exists in our database
            user_exists = db.fetchone(
                "SELECT 1 FROM users WHERE twitch_user_id = ?", (user_id,))

            # If user doesn't exist, create them
            if not user_exists:
                logger.info(
                    f"Creating new user record for {username} (ID: {user_id})")
                db.execute(
                    "INSERT INTO users (twitch_user_id, twitch_username, rank, points, date_added, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, username, "viewer", 0, current_time, current_time)
                )

            # Now record the redemption
            try:
                db.execute(
                    "INSERT INTO reward_redemptions (reward_id, user_id, redeemed_at, user_input) VALUES (?, ?, ?, ?)",
                    (reward_id, user_id, current_time, user_input)
                )

                db.execute(
                    "UPDATE twitch_rewards SET total_uses = total_uses + 1 WHERE reward_id = ?",
                    (reward_id,)
                )

                logger.info(
                    f"Recorded redemption of {reward_title} by {username}")
                return True
            except Exception as e:
                logger.error(f"Error inserting redemption record: {e}")
                return False

        except Exception as e:
            handle_error(e, {"context": "record_redemption",
                         "redemption_data": redemption_data})
            return False

    def get_user_redemptions(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            return db.fetchall(
                """
                SELECT r.*, t.name as reward_name, t.cost 
                FROM reward_redemptions r
                JOIN twitch_rewards t ON r.reward_id = t.reward_id
                WHERE r.user_id = ?
                ORDER BY r.redeemed_at DESC
                LIMIT ?
                """,
                (user_id, limit)
            )
        except Exception as e:
            handle_error(
                e, {"context": "get_user_redemptions", "user_id": user_id})
            return []

    def create_reward_via_api(self, channel_id: str, reward_data: Dict[str, Any]) -> Optional[str]:
        try:
            # This would call the Twitch API to create the reward
            # We'd need to implement this using the appropriate Twitch API client/authorization

            # For now, just log the attempt
            logger.info(
                f"Would create reward via API: {reward_data.get('title', 'Unnamed')} for channel {channel_id}")

            # Placeholder for reward ID that would be returned by the API
            api_reward_id = None

            # In a real implementation, we'd:
            # 1. Call the Twitch API to create the reward
            # 2. Get back the reward ID
            # 3. Store it in our database
            # 4. Register any handlers

            return api_reward_id
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to create reward via API: {str(e)}"))
            return None


# Singleton instance
reward_service = RewardService()
