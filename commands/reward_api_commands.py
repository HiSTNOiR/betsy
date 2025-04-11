import json

from typing import Dict, Any

from commands.base import BaseCommand
from utils.reward_service import reward_service
from utils.twitch_api_client import twitch_api
from core.config import config


class RewardCreateCommand(BaseCommand):
    name = "reward-create"
    description = "Create a new channel point reward"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        parts = args.split(" ", 2)
        if len(parts) < 2:
            self.send_message(
                channel, f"@{user.get('name')}, usage: !reward-create <name> <cost> [description]")
            return

        reward_name = parts[0]

        try:
            cost = int(parts[1])
            if cost < 1:
                self.send_message(
                    channel, f"@{user.get('name')}, cost must be at least 1 point.")
                return
        except ValueError:
            self.send_message(
                channel, f"@{user.get('name')}, cost must be a number.")
            return

        description = parts[2] if len(parts) > 2 else ""

        # Get broadcaster ID
        broadcaster_id = config.get('CHANNEL_ID')
        if not broadcaster_id:
            self.send_message(
                channel, f"@{user.get('name')}, broadcaster ID not configured.")
            return

        # Create the reward via Twitch API
        reward_data = {
            "name": reward_name,
            "cost": cost,
            "description": description,
            "is_enabled": True,
            "auto_fulfill": True
        }

        api_response = twitch_api.create_custom_reward(
            broadcaster_id, reward_data)

        if not api_response:
            self.send_message(
                channel, f"@{user.get('name')}, failed to create reward via Twitch API.")
            return

        # Register the reward in our database
        db_reward_data = {
            "reward_id": api_response["id"],
            "name": api_response["title"],
            "description": api_response.get("prompt", ""),
            "cost": api_response["cost"],
            "is_enabled": api_response.get("is_enabled", True),
            "background_color": api_response.get("background_color", ""),
            "is_user_input_required": api_response.get("is_user_input_required", False),
            "user_input_prompt": api_response.get("user_input_prompt", ""),
            "auto_fulfill": api_response.get("is_auto_fulfilled", True),
            "handler_type": "default"
        }

        reward_service.register_reward(db_reward_data)

        self.send_message(
            channel, f"@{user.get('name')}, created new reward: {reward_name} ({cost} points)")


class RewardDeleteCommand(BaseCommand):
    name = "reward-delete"
    description = "Delete a channel point reward"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        if not args:
            self.send_message(
                channel, f"@{user.get('name')}, please provide a reward name or ID.")
            return

        # Try to find by name first
        rewards = reward_service.get_all_rewards()
        matching_reward = None

        for reward in rewards:
            if reward['name'].lower() == args.lower() or reward['reward_id'] == args:
                matching_reward = reward
                break

        if not matching_reward:
            self.send_message(
                channel, f"@{user.get('name')}, no reward found with name or ID: {args}")
            return

        # Get broadcaster ID
        broadcaster_id = config.get('CHANNEL_ID')
        if not broadcaster_id:
            self.send_message(
                channel, f"@{user.get('name')}, broadcaster ID not configured.")
            return

        # Delete via Twitch API
        result = twitch_api.delete_custom_reward(
            broadcaster_id, matching_reward['reward_id'])

        if not result:
            self.send_message(
                channel, f"@{user.get('name')}, failed to delete reward via Twitch API.")
            return

        # Delete from our database
        reward_service.delete_reward(matching_reward['reward_id'])

        self.send_message(
            channel, f"@{user.get('name')}, deleted reward: {matching_reward['name']}")


class RewardImportCommand(BaseCommand):
    name = "reward-import"
    description = "Import channel point rewards from Twitch"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        # Get broadcaster ID
        broadcaster_id = config.get('CHANNEL_ID')
        if not broadcaster_id:
            self.send_message(
                channel, f"@{user.get('name')}, broadcaster ID not configured.")
            return

        # Get rewards from Twitch API
        api_rewards = twitch_api.get_channel_rewards(broadcaster_id)

        if not api_rewards:
            self.send_message(
                channel, f"@{user.get('name')}, no rewards found or failed to retrieve rewards from Twitch API.")
            return

        imported_count = 0
        for api_reward in api_rewards:
            db_reward_data = {
                "reward_id": api_reward["id"],
                "name": api_reward["title"],
                "description": api_reward.get("prompt", ""),
                "cost": api_reward["cost"],
                "is_enabled": api_reward.get("is_enabled", True),
                "background_color": api_reward.get("background_color", ""),
                "is_user_input_required": api_reward.get("is_user_input_required", False),
                "user_input_prompt": api_reward.get("user_input_prompt", ""),
                "auto_fulfill": api_reward.get("is_auto_fulfilled", True),
                "handler_type": "default"
            }

            if reward_service.register_reward(db_reward_data):
                imported_count += 1

        self.send_message(
            channel, f"@{user.get('name')}, imported {imported_count} rewards from Twitch.")


class RewardExportCommand(BaseCommand):
    name = "reward-export"
    description = "Export rewards configuration to file"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        from config.reward_config import save_reward_config

        if save_reward_config():
            self.send_message(
                channel, f"@{user.get('name')}, successfully exported rewards configuration to file.")
        else:
            self.send_message(
                channel, f"@{user.get('name')}, failed to export rewards configuration.")
