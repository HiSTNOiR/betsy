import requests
import json

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from core.logging import get_logger
from core.errors import handle_error, TwitchError
from core.config import config

logger = get_logger("twitch_api")


class TwitchAPIClient:
    def __init__(self):
        self.client_id = config.get('CLIENT_ID')
        self.broadcaster_token = config.get('BROADCASTER_TOKEN')
        self._token_cache = {
            'access_token': None,
            'expires_at': datetime.min,
            'scopes': set()
        }

    def _validate_token(self, required_scopes: List[str]) -> bool:
        if (datetime.now() < self._token_cache['expires_at'] and
                all(scope in self._token_cache['scopes'] for scope in required_scopes)):
            return True

        try:
            response = requests.get(
                "https://id.twitch.tv/oauth2/validate",
                headers={"Authorization": f"OAuth {self.broadcaster_token}"}
            )

            if response.status_code == 200:
                token_info = response.json()
                self._token_cache = {
                    'access_token': self.broadcaster_token,
                    'expires_at': datetime.now() + timedelta(hours=1),
                    'scopes': set(token_info.get('scopes', []))
                }

                missing_scopes = [
                    scope for scope in required_scopes if scope not in self._token_cache['scopes']]
                return len(missing_scopes) == 0

            return False
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False

    def get_channel_rewards(self, broadcaster_id: str) -> List[Dict[str, Any]]:
        required_scopes = ["channel:read:redemptions",
                           "channel:manage:redemptions"]

        if not self._validate_token(required_scopes):
            raise TwitchError("Insufficient token scopes")

        try:
            response = requests.get(
                "https://api.twitch.tv/helix/channel_points/custom_rewards",
                headers={
                    "Client-ID": self.client_id,
                    "Authorization": f"Bearer {self.broadcaster_token}"
                },
                params={"broadcaster_id": broadcaster_id}
            )

            return response.json().get("data", []) if response.status_code == 200 else []

        except Exception as e:
            handle_error(TwitchError(f"Rewards fetch failed: {str(e)}"))
            return []

    def create_custom_reward(self, broadcaster_id: str, reward_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                "https://api.twitch.tv/helix/channel_points/custom_rewards",
                headers={
                    "Client-ID": self.client_id,
                    "Authorization": f"Bearer {self.broadcaster_token}",
                    "Content-Type": "application/json"
                },
                params={"broadcaster_id": broadcaster_id},
                json=self._prepare_reward_payload(reward_data)
            )

            return response.json()["data"][0] if response.status_code == 200 else None

        except Exception as e:
            handle_error(TwitchError(f"Reward creation failed: {str(e)}"))
            return None

    def _prepare_reward_payload(self, reward_data: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "title": reward_data.get("name", "Custom Reward"),
            "cost": reward_data.get("cost", 1000),
            "prompt": reward_data.get("description", ""),
            "is_enabled": reward_data.get("is_enabled", True),
            "is_user_input_required": reward_data.get("is_user_input_required", False)
        }
        return {k: v for k, v in payload.items() if v is not None}


twitch_api = TwitchAPIClient()
