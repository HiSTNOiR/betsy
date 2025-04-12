from typing import Dict, Any, Tuple

from core.logging import get_logger
from core.errors import handle_error, TwitchError
from core.config import config
from utils.reward_service import reward_service
from utils.twitch_api_client import twitch_api

logger = get_logger("reward_sync")


class RewardSynchronizer:
    def __init__(self):
        self.broadcaster_id = config.get('CHANNEL_ID')

    def sync_all_rewards(self) -> Tuple[int, int, int]:
        if not self.broadcaster_id:
            logger.error("Cannot sync rewards: CHANNEL_ID not configured")
            return (0, 0, 0)

        try:
            api_rewards = twitch_api.get_channel_rewards(self.broadcaster_id)
            if not api_rewards:
                return (0, 0, 0)

            added, updated, failed = 0, 0, 0

            for api_reward in api_rewards:
                reward_data = self._transform_reward_data(api_reward)

                if reward_service.register_reward(reward_data):
                    if reward_service.get_reward(reward_data['reward_id']):
                        updated += 1
                    else:
                        added += 1
                else:
                    failed += 1

            return (added, updated, failed)

        except Exception as e:
            handle_error(TwitchError(f"Reward sync failed: {str(e)}"))
            return (0, 0, 0)

    def _transform_reward_data(self, api_reward: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "reward_id": api_reward["id"],
            "name": api_reward["title"],
            "description": api_reward.get("prompt", ""),
            "cost": api_reward["cost"],
            "is_enabled": api_reward.get("is_enabled", True),
            "background_color": api_reward.get("background_color", ""),
            "is_user_input_required": api_reward.get("is_user_input_required", False),
            "user_input_prompt": api_reward.get("user_input_prompt", ""),
            "auto_fulfill": api_reward.get("is_auto_fulfilled", True)
        }


reward_sync = RewardSynchronizer()
