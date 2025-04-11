import requests
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from core.logging import get_logger
from core.errors import handle_error, TwitchError, NetworkError
from core.config import config

logger = get_logger("twitch_api")


class TwitchAPIClient:
    def __init__(self):
        self.client_id = config.get('CLIENT_ID')
        self.client_secret = config.get('CLIENT_SECRET')
        self.broadcaster_token = None
        self.token_expires_at = 0

    def _ensure_token(self):
        current_time = time.time()

        if self.broadcaster_token and current_time < self.token_expires_at - 60:
            return

        try:
            # Get a new token
            response = requests.post(
                "https://id.twitch.tv/oauth2/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                    "scope": "channel:read:redemptions channel:manage:redemptions"
                }
            )

            if response.status_code != 200:
                raise TwitchError(
                    f"Failed to get access token: {response.text}")

            data = response.json()
            self.broadcaster_token = data["access_token"]
            self.token_expires_at = current_time + data["expires_in"]

            logger.info("Acquired new Twitch API token")
        except Exception as e:
            handle_error(NetworkError(f"Failed to get Twitch token: {str(e)}"))
            raise

    def get_channel_rewards(self, broadcaster_id: str) -> List[Dict[str, Any]]:
        try:
            self._ensure_token()

            url = f"https://api.twitch.tv/helix/channel_points/custom_rewards"
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.broadcaster_token}"
            }
            params = {
                "broadcaster_id": broadcaster_id
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                raise TwitchError(
                    f"Failed to get channel rewards: {response.text}")

            data = response.json()
            return data.get("data", [])
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to get channel rewards: {str(e)}"))
            return []

    def create_custom_reward(self, broadcaster_id: str, reward_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            self._ensure_token()

            url = f"https://api.twitch.tv/helix/channel_points/custom_rewards"
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.broadcaster_token}",
                "Content-Type": "application/json"
            }
            params = {
                "broadcaster_id": broadcaster_id
            }

            # Transform our internal data model to Twitch API format
            twitch_reward_data = {
                "title": reward_data.get("name", "Custom Reward"),
                "cost": reward_data.get("cost", 1000),
                "prompt": reward_data.get("description", "")
            }

            # Handle optional fields
            if "is_enabled" in reward_data:
                twitch_reward_data["is_enabled"] = reward_data["is_enabled"]

            if "background_color" in reward_data:
                twitch_reward_data["background_color"] = reward_data["background_color"]

            if "is_user_input_required" in reward_data:
                twitch_reward_data["is_user_input_required"] = reward_data["is_user_input_required"]

            if "user_input_prompt" in reward_data:
                twitch_reward_data["user_input_prompt"] = reward_data["user_input_prompt"]

            if "max_per_stream" in reward_data:
                twitch_reward_data["max_per_stream_setting"] = {
                    "is_enabled": True,
                    "max_per_stream": reward_data["max_per_stream"]
                }

            if "max_per_user_per_stream" in reward_data:
                twitch_reward_data["max_per_user_per_stream_setting"] = {
                    "is_enabled": True,
                    "max_per_user_per_stream": reward_data["max_per_user_per_stream"]
                }

            if "global_cooldown_seconds" in reward_data:
                twitch_reward_data["global_cooldown_setting"] = {
                    "is_enabled": True,
                    "global_cooldown_seconds": reward_data["global_cooldown_seconds"]
                }

            if "auto_fulfill" in reward_data:
                twitch_reward_data["is_auto_fulfilled"] = reward_data["auto_fulfill"]

            response = requests.post(
                url, headers=headers, params=params, json=twitch_reward_data)

            if response.status_code != 200:
                raise TwitchError(
                    f"Failed to create custom reward: {response.text}")

            data = response.json()
            if not data.get("data") or len(data["data"]) == 0:
                raise TwitchError("No reward data returned from API")

            return data["data"][0]
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to create custom reward: {str(e)}"))
            return None

    def update_custom_reward(self, broadcaster_id: str, reward_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            self._ensure_token()

            url = f"https://api.twitch.tv/helix/channel_points/custom_rewards"
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.broadcaster_token}",
                "Content-Type": "application/json"
            }
            params = {
                "broadcaster_id": broadcaster_id,
                "id": reward_id
            }

            # Transform our internal data model to Twitch API format
            twitch_update_data = {}

            if "name" in update_data:
                twitch_update_data["title"] = update_data["name"]

            if "cost" in update_data:
                twitch_update_data["cost"] = update_data["cost"]

            if "description" in update_data:
                twitch_update_data["prompt"] = update_data["description"]

            if "is_enabled" in update_data:
                twitch_update_data["is_enabled"] = update_data["is_enabled"]

            if "background_color" in update_data:
                twitch_update_data["background_color"] = update_data["background_color"]

            if "is_user_input_required" in update_data:
                twitch_update_data["is_user_input_required"] = update_data["is_user_input_required"]

            if "user_input_prompt" in update_data:
                twitch_update_data["user_input_prompt"] = update_data["user_input_prompt"]

            if "max_per_stream" in update_data:
                twitch_update_data["max_per_stream_setting"] = {
                    "is_enabled": True,
                    "max_per_stream": update_data["max_per_stream"]
                }

            if "max_per_user_per_stream" in update_data:
                twitch_update_data["max_per_user_per_stream_setting"] = {
                    "is_enabled": True,
                    "max_per_user_per_stream": update_data["max_per_user_per_stream"]
                }

            if "global_cooldown_seconds" in update_data:
                twitch_update_data["global_cooldown_setting"] = {
                    "is_enabled": True,
                    "global_cooldown_seconds": update_data["global_cooldown_seconds"]
                }

            if "auto_fulfill" in update_data:
                twitch_update_data["is_auto_fulfilled"] = update_data["auto_fulfill"]

            response = requests.patch(
                url, headers=headers, params=params, json=twitch_update_data)

            if response.status_code != 200:
                raise TwitchError(
                    f"Failed to update custom reward: {response.text}")

            data = response.json()
            if not data.get("data") or len(data["data"]) == 0:
                raise TwitchError("No reward data returned from API")

            return data["data"][0]
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to update custom reward: {str(e)}"))
            return None

    def delete_custom_reward(self, broadcaster_id: str, reward_id: str) -> bool:
        try:
            self._ensure_token()

            url = f"https://api.twitch.tv/helix/channel_points/custom_rewards"
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.broadcaster_token}"
            }
            params = {
                "broadcaster_id": broadcaster_id,
                "id": reward_id
            }

            response = requests.delete(url, headers=headers, params=params)

            if response.status_code != 204:
                raise TwitchError(
                    f"Failed to delete custom reward: {response.text}")

            return True
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to delete custom reward: {str(e)}"))
            return False

    def update_redemption_status(self, broadcaster_id: str, reward_id: str, redemption_id: str, status: str) -> bool:
        try:
            self._ensure_token()

            url = f"https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions"
            headers = {
                "Client-ID": self.client_id,
                "Authorization": f"Bearer {self.broadcaster_token}",
                "Content-Type": "application/json"
            }
            params = {
                "broadcaster_id": broadcaster_id,
                "reward_id": reward_id,
                "id": redemption_id
            }

            data = {
                "status": status  # "FULFILLED" or "CANCELED"
            }

            response = requests.patch(
                url, headers=headers, params=params, json=data)

            if response.status_code != 200:
                raise TwitchError(
                    f"Failed to update redemption status: {response.text}")

            return True
        except Exception as e:
            handle_error(TwitchError(
                f"Failed to update redemption status: {str(e)}"))
            return False


# Singleton instance
twitch_api = TwitchAPIClient()
