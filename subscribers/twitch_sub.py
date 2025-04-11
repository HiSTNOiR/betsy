from typing import Dict, Any

from event_bus.bus import event_bus
from core.logging import get_logger
from core.errors import handle_error, NetworkError
from core.config import config
from publishers.twitch_pub import twitch_pub

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

        self.event_bus.subscribe("twitch_message", self._handle_message)
        self.event_bus.subscribe("twitch_ready", self._handle_ready)
        self.event_bus.subscribe("twitch_join", self._handle_join)
        self.event_bus.subscribe("twitch_part", self._handle_part)
        self.event_bus.subscribe(
            "twitch_subscription", self._handle_subscription)
        self.event_bus.subscribe("send_twitch_message", self._send_message)

        logger.info("Twitch handler subscribed to events")

    def _handle_message(self, data: Dict[str, Any]):
        try:
            author = data.get("author", {})
            username = author.get("name", "unknown")
            content = data.get("content", "")
            logger.info(f"[{username}]: {content}")

            # Additional message processing logic can be added here
        except Exception as e:
            handle_error(e, {"event": "twitch_message", "data": data})

    def _handle_ready(self, data: Dict[str, Any]):
        try:
            bot_user = data.get("bot_user", "unknown")
            logger.info(f"Twitch bot ready: {bot_user}")

            # Optional: Send a startup message to channel
            # if self.channel:
            #     self._send_message(
            #         {"channel": self.channel, "content": f"I'm live, bitches!"})
        except Exception as e:
            handle_error(e, {"event": "twitch_ready", "data": data})

    def _handle_join(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", "unknown")
            user = data.get("user", "unknown")
            logger.debug(f"User joined: {user} in {channel}")
        except Exception as e:
            handle_error(e, {"event": "twitch_join", "data": data})

    def _handle_part(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", "unknown")
            user = data.get("user", "unknown")
            logger.debug(f"User left: {user} from {channel}")
        except Exception as e:
            handle_error(e, {"event": "twitch_part", "data": data})

    def _handle_subscription(self, data: Dict[str, Any]):
        try:
            logger.info(f"New subscription event: {data}")
        except Exception as e:
            handle_error(e, {"event": "twitch_subscription", "data": data})

    def _send_message(self, data: Dict[str, Any]):
        try:
            channel = data.get("channel", self.channel)
            content = data.get("content", "")

            if not channel or not content:
                logger.warning(
                    "Cannot send message: missing channel or content")
                return

            result = twitch_pub.send_message(channel, content)
            if not result:
                logger.warning(f"Failed to send message to {channel}")
        except Exception as e:
            handle_error(NetworkError(f"Failed to send Twitch message: {str(e)}"),
                         {"channel": data.get("channel"), "content": data.get("content")})


# Singleton instance
twitch_sub = TwitchEventHandler(event_bus)
