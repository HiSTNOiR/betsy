import json

from typing import Dict, Any

from commands.base import BaseCommand
from utils.reward_service import reward_service


class RewardListCommand(BaseCommand):
    name = "rewards"
    description = "Lists all channel point rewards"
    permission = "moderator"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        rewards = reward_service.get_all_rewards()

        if not rewards:
            self.send_message(
                channel, f"@{user.get('name')}, no channel point rewards are configured.")
            return

        # Format basic info about each reward
        reward_list = []
        for reward in rewards:
            status = "✅" if reward.get("is_enabled", True) else "❌"
            reward_list.append(
                f"{status} {reward['name']} ({reward['cost']} points)")

        reward_str = ", ".join(reward_list)
        self.send_message(
            channel, f"@{user.get('name')}, Rewards: {reward_str}")


class RewardInfoCommand(BaseCommand):
    name = "reward"
    description = "Get detailed info about a specific reward"
    permission = "moderator"

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

        # Format detailed info
        reward_name = matching_reward['name']
        reward_id = matching_reward['reward_id']
        cost = matching_reward['cost']
        uses = matching_reward['total_uses']
        status = "Enabled" if matching_reward.get(
            "is_enabled", True) else "Disabled"
        handler = matching_reward.get("handler_type", "default")

        info = f"Reward: {reward_name} | ID: {reward_id} | Cost: {cost} | Uses: {uses} | Status: {status} | Handler: {handler}"
        self.send_message(channel, f"@{user.get('name')}, {info}")


class RewardEnableCommand(BaseCommand):
    name = "reward-enable"
    description = "Enable a reward"
    permission = "moderator"

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

        # Update the status
        result = reward_service.update_reward(
            matching_reward['reward_id'], {"is_enabled": True})

        if result:
            self.send_message(
                channel, f"@{user.get('name')}, reward '{matching_reward['name']}' has been enabled.")
        else:
            self.send_message(
                channel, f"@{user.get('name')}, failed to enable reward.")


class RewardDisableCommand(BaseCommand):
    name = "reward-disable"
    description = "Disable a reward"
    permission = "moderator"

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

        # Update the status
        result = reward_service.update_reward(
            matching_reward['reward_id'], {"is_enabled": False})

        if result:
            self.send_message(
                channel, f"@{user.get('name')}, reward '{matching_reward['name']}' has been disabled.")
        else:
            self.send_message(
                channel, f"@{user.get('name')}, failed to disable reward.")


class RewardUpdateCommand(BaseCommand):
    name = "reward-update"
    description = "Update a reward property"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        user, channel, args = self.extract_common_data(data)

        parts = args.split(" ", 2)
        if len(parts) < 3:
            self.send_message(
                channel, f"@{user.get('name')}, usage: !reward-update <name/id> <property> <value>")
            return

        reward_identifier, property_name, value = parts

        # Try to find by name first
        rewards = reward_service.get_all_rewards()
        matching_reward = None

        for reward in rewards:
            if reward['name'].lower() == reward_identifier.lower() or reward['reward_id'] == reward_identifier:
                matching_reward = reward
                break

        if not matching_reward:
            self.send_message(
                channel, f"@{user.get('name')}, no reward found with name or ID: {reward_identifier}")
            return

        # Handle different property types
        update_data = {}
        try:
            if property_name == "cost":
                cost = int(value)
                if cost < 1:
                    raise ValueError("Cost must be positive")
                update_data["cost"] = cost
            elif property_name == "name":
                update_data["name"] = value
            elif property_name == "description":
                update_data["description"] = value
            elif property_name == "handler":
                update_data["handler_type"] = value
            elif property_name == "config":
                try:
                    # Try to parse as JSON
                    config = json.loads(value)
                    update_data["handler_config"] = json.dumps(config)
                except json.JSONDecodeError:
                    self.send_message(
                        channel, f"@{user.get('name')}, invalid JSON configuration.")
                    return
            else:
                self.send_message(
                    channel, f"@{user.get('name')}, unknown property: {property_name}")
                return

            # Update the reward
            result = reward_service.update_reward(
                matching_reward['reward_id'], update_data)

            if result:
                self.send_message(
                    channel, f"@{user.get('name')}, updated {property_name} for reward '{matching_reward['name']}'.")
            else:
                self.send_message(
                    channel, f"@{user.get('name')}, failed to update reward.")
        except ValueError as e:
            self.send_message(channel, f"@{user.get('name')}, error: {str(e)}")
