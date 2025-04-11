import asyncio

from typing import Dict, Any, List, Optional
from datetime import datetime

from core.logging import get_logger
from core.errors import handle_error, TwitchError
from db.database import db
from publishers.twitch_pub import twitch_pub

logger = get_logger("twitch_rewards")


async def fetch_channel_rewards(channel_id: str) -> List[Dict[str, Any]]:
    if not twitch_pub.is_connected() or not twitch_pub.bot:
        raise TwitchError("Not connected to Twitch")

    try:
        # Get the channel rewards
        channel = twitch_pub.bot.get_channel(channel_id)
        if not channel:
            raise TwitchError(f"Channel {channel_id} not found")

        # Placeholder
        # ? Does twitchio provide access to getting channel rewards?
        # TODO use Twitch API

        # For now, we'll return an empty list
        return []
    except Exception as e:
        handle_error(TwitchError(f"Failed to fetch channel rewards: {str(e)}"))
        return []


def register_reward_in_db(reward_id: str, name: str, action_sequence_id: Optional[int] = None) -> bool:
    try:
        existing_reward = db.fetchone(
            "SELECT * FROM twitch_rewards WHERE reward_id = ?",
            (reward_id,)
        )

        current_time = datetime.now().isoformat()

        if existing_reward:
            if action_sequence_id is not None:
                db.execute(
                    "UPDATE twitch_rewards SET name = ?, action_sequence_id = ? WHERE reward_id = ?",
                    (name, action_sequence_id, reward_id)
                )
                logger.info(f"Updated reward {name} in database")
            return True
        else:
            db.execute(
                "INSERT INTO twitch_rewards (reward_id, name, action_sequence_id, total_uses, date_added) VALUES (?, ?, ?, 0, ?)",
                (reward_id, name, action_sequence_id, current_time)
            )
            logger.info(f"Registered new reward {name} in database")
            return True
    except Exception as e:
        handle_error(e, {"reward_id": reward_id, "name": name})
        return False


def sync_rewards_with_db() -> bool:
    try:
        # Placeholder
        # TODO pending Twitch API integration
        logger.info("Channel rewards synchronization is not yet implemented")
        return True
    except Exception as e:
        handle_error(e)
        return False
