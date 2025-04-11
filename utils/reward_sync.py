import time

from typing import Dict, Any, List, Optional, Tuple

from core.logging import get_logger
from core.errors import handle_error, TwitchError
from core.config import config
from db.database import db
from utils.reward_service import reward_service
from utils.twitch_api_client import twitch_api

logger = get_logger("reward_sync")


class RewardSynchronizer:
    def __init__(self):
        self.broadcaster_id = config.get('CHANNEL_ID')
        if not self.broadcaster_id:
            logger.warning("CHANNEL_ID not configured in config")

    def sync_all_rewards(self) -> Tuple[int, int, int]:
        """
        Fetches all rewards from Twitch API and synchronizes them with the database.
        Returns a tuple of (added, updated, failed) counts.
        """
        if not self.broadcaster_id:
            logger.error("Cannot sync rewards: CHANNEL_ID not configured")
            return (0, 0, 0)

        try:
            # Get rewards from Twitch API
            api_rewards = twitch_api.get_channel_rewards(self.broadcaster_id)
            if not api_rewards:
                logger.warning(
                    "No rewards found via Twitch API or failed to fetch")
                return (0, 0, 0)

            # Get existing rewards from our database
            db_rewards = reward_service.get_all_rewards()
            db_rewards_dict = {r['reward_id']: r for r in db_rewards}

            added = 0
            updated = 0
            failed = 0

            # Process each reward from the API
            for api_reward in api_rewards:
                reward_id = api_reward["id"]

                # Map API reward to our database format
                db_reward_data = {
                    "reward_id": reward_id,
                    "name": api_reward["title"],
                    "description": api_reward.get("prompt", ""),
                    "cost": api_reward["cost"],
                    "is_enabled": api_reward.get("is_enabled", True),
                    "background_color": api_reward.get("background_color", ""),
                    "is_user_input_required": api_reward.get("is_user_input_required", False),
                    "user_input_prompt": api_reward.get("user_input_prompt", ""),
                    "auto_fulfill": api_reward.get("is_auto_fulfilled", True)
                }

                # If exists in DB, preserve handler_type and config
                if reward_id in db_rewards_dict:
                    existing = db_rewards_dict[reward_id]
                    db_reward_data["handler_type"] = existing.get(
                        "handler_type", "default")
                    db_reward_data["handler_config"] = existing.get(
                        "handler_config")
                    db_reward_data["action_sequence_id"] = existing.get(
                        "action_sequence_id")
                else:
                    db_reward_data["handler_type"] = "default"

                # Save to database
                if reward_service.register_reward(db_reward_data):
                    if reward_id in db_rewards_dict:
                        updated += 1
                        logger.info(
                            f"Updated reward: {db_reward_data['name']} (ID: {reward_id})")
                    else:
                        added += 1
                        logger.info(
                            f"Added new reward: {db_reward_data['name']} (ID: {reward_id})")
                else:
                    failed += 1
                    logger.error(
                        f"Failed to save reward: {db_reward_data['name']} (ID: {reward_id})")

            return (added, updated, failed)

        except Exception as e:
            handle_error(e, {"context": "sync_all_rewards"})
            return (0, 0, 0)

    def setup_auto_sync(self, interval_minutes: int = 60) -> None:
        """
        Sets up automatic synchronization of rewards at specified intervals.
        This would typically be called when the bot starts.
        """
        if interval_minutes < 5:
            interval_minutes = 5  # Minimum 5 minutes to avoid rate limiting

        # This would be implemented with threading or scheduling
        # For now just log the intent
        logger.info(f"Would set up auto-sync every {interval_minutes} minutes")


# Singleton instance
reward_sync = RewardSynchronizer()
