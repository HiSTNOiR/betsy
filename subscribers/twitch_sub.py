from typing import Dict, Any

from event_bus.bus import event_bus
from core.logging import get_logger
from core.config import config
from publishers.twitch_pub import twitch_pub
from utils.channel_points_service import channel_points_service

logger = get_logger("twitch_sub")


class TwitchEventHandler:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.channel = config.get('CHANNEL', '')
        self.enabled = config.get_boolean('TWITCH_ENABLED', True)

    def subscribe(self):
        if not self.enabled:
            logger.info("Twitch handler is disabled")
            return

        subscriptions = {
            "twitch_message": self._handle_message,
            "twitch_ready": self._handle_ready,
            "twitch_join": self._handle_join,
            "twitch_part": self._handle_part,
            "twitch_subscription": self._handle_subscription,
            "twitch_subscription_gift": self._handle_subscription_gift,
            "twitch_bits": self._handle_bits,
            "twitch_follow": self._handle_follow,
            "twitch_raid": self._handle_raid,
            "twitch_channel_point_redemption": self._handle_channel_point_redemption,
            "send_twitch_message": self._send_message
        }

        for event, handler in subscriptions.items():
            self.event_bus.subscribe(event, handler)

        logger.info("Twitch handler subscribed to events")

    def _handle_channel_point_redemption(self, data: Dict[str, Any]):
        try:
            user = data.get("user", {})
            reward = data.get("reward", {})
            channel_points_service.handle_redemption(data)
        except Exception as e:
            from core.errors import handle_error
            handle_error(
                e, {"event": "channel_point_redemption", "data": data})

    def _send_message(self, data: Dict[str, Any]):
        channel = data.get("channel", self.channel)
        content = data.get("content", "")
        twitch_pub.send_message(channel, content)

    def _handle_message(self, data: Dict[str, Any]):
        logger.info(
            f"[{data.get('author', {}).get('name', 'unknown')}]: {data.get('content', '')}")

    def _handle_ready(self, data: Dict[str, Any]):
        logger.info(f"Twitch bot ready: {data.get('bot_user', 'unknown')}")

    def _handle_join(self, data: Dict[str, Any]):
        logger.debug(
            f"User joined: {data.get('user', 'unknown')} in {data.get('channel', 'unknown')}")

    def _handle_part(self, data: Dict[str, Any]):
        logger.debug(
            f"User left: {data.get('user', 'unknown')} from {data.get('channel', 'unknown')}")

    def _handle_subscription(self, data: Dict[str, Any]):
        user = data.get("user", {})
        username = user.get("name", "unknown")
        sub_plan = data.get("sub_plan", "")

        logger.info(f"Subscription: {username} subscribed with {sub_plan}")

    def _handle_subscription_gift(self, data: Dict[str, Any]):
        gifter = data.get("gifter", {})
        gifter_name = gifter.get("name", "unknown")
        count = data.get("count", 1)

        logger.info(f"Sub Gift: {gifter_name} gifted {count} subs")

    def _handle_bits(self, data: Dict[str, Any]):
        user = data.get("user", {})
        username = user.get("name", "unknown")
        bits_used = data.get("bits_used", 0)

        logger.info(f"Bits: {username} cheered {bits_used} bits")

    def _handle_follow(self, data: Dict[str, Any]):
        user = data.get("user", {})
        username = user.get("name", "unknown")

        logger.info(f"Follow: {username} followed the channel")

    def _handle_raid(self, data: Dict[str, Any]):
        raider = data.get("raider", {})
        raider_name = raider.get("name", "unknown")
        viewer_count = data.get("viewer_count", 0)

        logger.info(f"Raid: {raider_name} raided with {viewer_count} viewers")


twitch_sub = TwitchEventHandler(event_bus)
