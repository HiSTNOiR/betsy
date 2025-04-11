import json
import os

from typing import Dict, Any, List
from datetime import datetime

from core.logging import get_logger
from core.errors import handle_error, ConfigError
from core.config import config
from db.database import db
from utils.reward_service import reward_service

logger = get_logger("reward_config")


def load_reward_config():
    try:
        config_path = config.get_path(
            'REWARD_CONFIG_PATH', 'config/rewards.json')

        if not os.path.exists(config_path):
            logger.info(f"Reward configuration file not found: {config_path}")
            return

        with open(config_path, 'r') as f:
            config_data = json.load(f)

        # Process handlers first
        if "handlers" in config_data:
            for handler in config_data["handlers"]:
                register_handler_from_config(handler)

        # Then process rewards
        if "rewards" in config_data:
            for reward in config_data["rewards"]:
                register_reward_from_config(reward)

        logger.info(f"Loaded reward configuration from {config_path}")
    except Exception as e:
        handle_error(ConfigError(
            f"Failed to load reward configuration: {str(e)}"))


def register_handler_from_config(handler_config: Dict[str, Any]):
    try:
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in handler_config:
                logger.warning(
                    f"Handler config missing required field: {field}")
                return

        handler_name = handler_config["name"]

        # Check if handler already exists
        existing = db.fetchone(
            "SELECT * FROM reward_handlers WHERE handler_name = ?",
            (handler_name,)
        )

        current_time = datetime.now().isoformat()

        if existing:
            # Update existing handler
            db.execute(
                "UPDATE reward_handlers SET handler_description = ?, enabled = ?, config_schema = ? WHERE handler_name = ?",
                (
                    handler_config["description"],
                    handler_config.get("enabled", True),
                    json.dumps(handler_config.get("config_schema", {})),
                    handler_name
                )
            )
            logger.info(f"Updated handler: {handler_name}")
        else:
            # Create new handler
            db.execute(
                "INSERT INTO reward_handlers (handler_name, handler_description, enabled, config_schema, date_added) VALUES (?, ?, ?, ?, ?)",
                (
                    handler_name,
                    handler_config["description"],
                    handler_config.get("enabled", True),
                    json.dumps(handler_config.get("config_schema", {})),
                    current_time
                )
            )
            logger.info(f"Registered new handler: {handler_name}")
    except Exception as e:
        handle_error(e, {"context": "register_handler_from_config",
                     "handler_config": handler_config})


def register_reward_from_config(reward_config: Dict[str, Any]):
    try:
        # We don't have reward_id in config since this is assigned by Twitch
        # Instead, we'll use the name to check for existing rewards
        name = reward_config.get("name")
        if not name:
            logger.warning("Reward config missing name")
            return

        # Check if a reward with this name exists
        existing = db.fetchone(
            "SELECT * FROM twitch_rewards WHERE name = ?",
            (name,)
        )

        if existing:
            # Update the existing reward with data from config
            update_data = {
                "description": reward_config.get("description", existing.get("description", "")),
                "cost": reward_config.get("cost", existing.get("cost", 0)),
                "is_enabled": reward_config.get("enabled", existing.get("is_enabled", True)),
                "handler_type": reward_config.get("handler_type", existing.get("handler_type", "default")),
                "auto_fulfill": reward_config.get("auto_fulfill", existing.get("auto_fulfill", True)),
            }

            if "handler_config" in reward_config:
                update_data["handler_config"] = json.dumps(
                    reward_config["handler_config"])

            if "action_sequence_id" in reward_config:
                update_data["action_sequence_id"] = reward_config["action_sequence_id"]

            reward_service.update_reward(existing["reward_id"], update_data)
            logger.info(f"Updated reward from config: {name}")
        else:
            # This is a new reward, but we can't create it without Twitch API integration
            # We could store it as a "template" to create via the API later
            logger.info(
                f"New reward in config: {name} (would need to be created via Twitch API)")
    except Exception as e:
        handle_error(
            e, {"context": "register_reward_from_config", "reward_config": reward_config})


def save_reward_config():
    try:
        config_path = config.get_path(
            'REWARD_CONFIG_PATH', 'config/rewards.json')

        # Get all rewards and handlers
        rewards = reward_service.get_all_rewards()
        handlers = db.fetchall("SELECT * FROM reward_handlers")

        # Create config structure
        config_data = {
            "handlers": [],
            "rewards": []
        }

        # Add handlers
        for handler in handlers:
            handler_data = {
                "name": handler["handler_name"],
                "description": handler["handler_description"],
                "enabled": bool(handler["enabled"])
            }

            if handler["config_schema"]:
                try:
                    handler_data["config_schema"] = json.loads(
                        handler["config_schema"])
                except json.JSONDecodeError:
                    pass

            config_data["handlers"].append(handler_data)

        # Add rewards
        for reward in rewards:
            reward_data = {
                "name": reward["name"],
                "description": reward.get("description", ""),
                "cost": reward["cost"],
                "enabled": bool(reward.get("is_enabled", True)),
                "handler_type": reward.get("handler_type", "default"),
                "auto_fulfill": bool(reward.get("auto_fulfill", True))
            }

            if reward.get("handler_config"):
                try:
                    reward_data["handler_config"] = json.loads(
                        reward["handler_config"])
                except json.JSONDecodeError:
                    pass

            if reward.get("action_sequence_id"):
                reward_data["action_sequence_id"] = reward["action_sequence_id"]

            config_data["rewards"].append(reward_data)

        # Save to file
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)

        logger.info(f"Saved reward configuration to {config_path}")
        return True
    except Exception as e:
        handle_error(e, {"context": "save_reward_config"})
        return False
