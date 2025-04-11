import threading
import time
import asyncio

from twitchio.ext import commands

from typing import Dict, Any, Callable, List, Optional

from utils.platform_connections import PlatformConnection, SingletonMeta
from utils.string_utils import sanitise_for_logging
from utils.user_service import enrich_user_data
from core.config import config, ConfigurationError
from core.logging import get_logger
from core.errors import NetworkError, TwitchError, handle_error

logger = get_logger("twitch_pub")


class TwitchConnector(PlatformConnection, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()
        self.token = config.get('TMI_TOKEN')
        self.client_id = config.get('CLIENT_ID')
        self.nick = config.get('BOT_NICK')
        self.channel = config.get('CHANNEL')
        self.prefix = config.get('BOT_PREFIX', '!')

        self.bot = None
        self.thread = None
        self.enabled = config.get_boolean('TWITCH_ENABLED', True)
        self.event_callbacks: Dict[str, List[Callable]] = {}
        self.message_callbacks: List[Callable] = []
        self._lock = threading.Lock()
        self._ready = threading.Event()

    def _connect(self):
        if not self.enabled:
            logger.info("Twitch connectivity is disabled")
            return

        if not self.token or not self.nick or not self.channel:
            error_msg = "Missing required Twitch configuration"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        with self._lock:
            if self.is_connected():
                logger.info("Already connected to Twitch")
                return

            try:
                # Create a Bot instance from twitchio.ext.commands
                class Bot(commands.Bot):
                    def __init__(self, parent):
                        self.parent = parent
                        super().__init__(
                            token=parent.token,
                            prefix=parent.prefix,
                            initial_channels=[parent.channel]
                        )

                    async def event_ready(self):
                        logger.info(f"Twitch Bot ready | {self.nick}")
                        self.parent.connection = self
                        self.parent._ready.set()
                        self.parent.trigger_event(
                            "ready", {"bot_user": self.nick})

                    async def event_message(self, message):
                        if message.echo:
                            return

                        logger.info(
                            f"[{message.author.name}]: {message.content}")

                        # Check if this message is actually a channel point redemption
                        # This extracts the custom-reward-id from the message tags if present
                        custom_reward_id = None
                        if hasattr(message, 'tags') and message.tags:
                            custom_reward_id = message.tags.get(
                                'custom-reward-id')

                        message_data = {
                            "author": {
                                "id": message.author.id,
                                "name": message.author.name,
                                "display_name": message.author.display_name,
                                "is_mod": message.author.is_mod,
                                "is_subscriber": message.author.is_subscriber,
                                "badges": message.author.badges
                            },
                            "content": message.content,
                            "channel": message.channel.name,
                            "id": message.id,
                            "timestamp": time.time()
                        }

                        # Enrich with database information (for things like bot_admin)
                        message_data["author"] = enrich_user_data(
                            message_data["author"])

                        # Check if this is a channel point redemption
                        if custom_reward_id:
                            logger.info(
                                f"🟪 DETECTED CHANNEL POINT REDEMPTION - Reward ID: {custom_reward_id}")

                            # Create the channel point redemption event data
                            redemption_data = {
                                "user": message_data["author"],
                                "channel": message_data["channel"],
                                "reward": {
                                    "id": custom_reward_id,
                                    "title": "Unknown Reward",  # We don't have the title from just the message
                                    "cost": 0,  # We don't have the cost from just the message
                                    "prompt": ""
                                },
                                "input": message_data["content"],
                                "status": "fulfilled",
                                "timestamp": message_data["timestamp"]
                            }

                            # Trigger both the message event and the channel point redemption event
                            self.parent.trigger_message(message_data)
                            self.parent.trigger_event(
                                "channel_point_redemption", redemption_data)
                        else:
                            # Regular message, just trigger the message event
                            self.parent.trigger_message(message_data)

                    async def event_subscription(self, event):
                        subscription_data = {
                            "user": {
                                "id": event.user.id,
                                "name": event.user.name,
                                "display_name": event.user.display_name
                            },
                            "channel": event.channel.name,
                            "sub_plan": event.sub_plan,
                            "message": event.message,
                            "is_gift": event.is_gift,
                            "months": event.cumulative_months,
                            "timestamp": time.time()
                        }
                        self.parent.trigger_event(
                            "subscription", subscription_data)

                    async def event_subscription_gift(self, event):
                        recipients = []
                        if hasattr(event, "recipients") and event.recipients:
                            recipients = [{
                                "id": user.id,
                                "name": user.name,
                                "display_name": user.display_name
                            } for user in event.recipients]

                        gift_data = {
                            "gifter": {
                                "id": event.user.id,
                                "name": event.user.name,
                                "display_name": event.user.display_name
                            },
                            "channel": event.channel.name,
                            "count": event.count,
                            "sub_plan": event.sub_plan,
                            "recipients": recipients,
                            "timestamp": time.time()
                        }
                        self.parent.trigger_event(
                            "subscription_gift", gift_data)

                    async def event_bits(self, event):
                        bits_data = {
                            "user": {
                                "id": event.user.id,
                                "name": event.user.name,
                                "display_name": event.user.display_name
                            },
                            "bits_used": event.bits_used,
                            "total_bits": event.total_bits,
                            "message": event.message,
                            "channel": event.channel.name,
                            "timestamp": time.time()
                        }
                        self.parent.trigger_event("bits", bits_data)

                    async def event_follow(self, event):
                        follow_data = {
                            "user": {
                                "id": event.user.id,
                                "name": event.user.name,
                                "display_name": event.user.display_name
                            },
                            "channel": event.channel.name,
                            "timestamp": time.time()
                        }
                        self.parent.trigger_event("follow", follow_data)

                    async def event_raid(self, event):
                        raid_data = {
                            "raider": {
                                "id": event.raider.id,
                                "name": event.raider.name,
                                "display_name": event.raider.display_name
                            },
                            "channel": event.channel.name,
                            "viewer_count": event.viewer_count,
                            "timestamp": time.time()
                        }
                        self.parent.trigger_event("raid", raid_data)

                    async def event_channel_points_custom_reward_redemption_add(self, data):
                        try:
                            # Extract user information
                            user_data = {
                                "id": data.user.id if hasattr(data, 'user') and hasattr(data.user, 'id') else "unknown",
                                "name": data.user.name if hasattr(data, 'user') and hasattr(data.user, 'name') else "unknown",
                                "display_name": data.user.display_name if hasattr(data, 'user') and hasattr(data.user, 'display_name') else "unknown"
                            }

                            # Extract reward information
                            reward_data = {
                                "id": data.reward.id if hasattr(data, 'reward') and hasattr(data.reward, 'id') else "unknown",
                                "title": data.reward.title if hasattr(data, 'reward') and hasattr(data.reward, 'title') else "Unknown Reward",
                                "cost": data.reward.cost if hasattr(data, 'reward') and hasattr(data.reward, 'cost') else 0,
                                "prompt": data.reward.prompt if hasattr(data, 'reward') and hasattr(data.reward, 'prompt') else ""
                            }

                            # Create the channel point redemption event data
                            redemption_data = {
                                "user": user_data,
                                "channel": data.broadcaster.name if hasattr(data, 'broadcaster') and hasattr(data.broadcaster, 'name') else "unknown",
                                "reward": reward_data,
                                "input": data.input if hasattr(data, 'input') else "",
                                "status": "fulfilled",
                                "timestamp": time.time()
                            }

                            # Log the redemption
                            logger.info(
                                f"Channel point redemption: {user_data['name']} redeemed {reward_data['title']} (ID: {reward_data['id']})")

                            # Trigger the event
                            self.parent.trigger_event(
                                "channel_point_redemption", redemption_data)
                        except Exception as e:
                            logger.error(
                                f"Error processing channel point event: {e}")

                # Create the bot instance
                self.bot = Bot(self)

                # Start the bot in a separate thread
                self.thread = threading.Thread(
                    target=self._run_bot, daemon=True, name="TwitchThread")
                self.thread.start()
                logger.info(f"Twitch bot thread started: {self.thread.name}")

            except Exception as e:
                error_msg = f"Failed to connect to Twitch: {str(e)}"
                logger.error(error_msg)
                raise TwitchError(error_msg)

    def _run_bot(self):
        logger.info("Starting Twitch bot...")
        try:
            self.bot.run()
        except Exception as e:
            error_message = f"Twitch bot error: {str(e)}"
            logger.error(error_message)
            handle_error(NetworkError(error_message))
            self._ready.clear()

            if self.enabled:
                logger.info("Attempting to reconnect...")
                time.sleep(5)
                self._reconnect()

    def _reconnect(self):
        with self._lock:
            if self.bot:
                try:
                    self._disconnect_internal()
                except Exception as e:
                    logger.error(f"Error during disconnect: {str(e)}")

            try:
                self._connect()
            except Exception as e:
                logger.error(f"Reconnection failed: {str(e)}")

    def _disconnect_internal(self):
        if self.bot:
            try:
                if hasattr(self.bot, 'loop') and self.bot.loop:
                    asyncio.run_coroutine_threadsafe(
                        self.bot.close(), self.bot.loop)
            except Exception as e:
                logger.error(f"Error in bot close: {str(e)}")

        self.bot = None
        self.connection = None
        self._ready.clear()

    def _disconnect(self):
        with self._lock:
            if not self.bot:
                return

            try:
                logger.info("Disconnecting from Twitch...")
                self._disconnect_internal()
                logger.info("Disconnected from Twitch")
            except Exception as e:
                error_msg = f"Error disconnecting from Twitch: {str(e)}"
                logger.error(error_msg)
                raise NetworkError(error_msg)

    def is_connected(self):
        return self.bot is not None and self._ready.is_set()

    def register_event_callback(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type not in self.event_callbacks:
                self.event_callbacks[event_type] = []
            self.event_callbacks[event_type].append(callback)
            logger.debug(f"Registered event callback for {event_type}")

    def register_message_callback(self, callback: Callable):
        with self._lock:
            self.message_callbacks.append(callback)
            logger.debug("Registered message callback")

    def trigger_event(self, event_type: str, data: Any = None):
        callbacks = []
        with self._lock:
            if event_type in self.event_callbacks:
                callbacks = self.event_callbacks[event_type].copy()

        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in event callback: {str(e)}")

    def trigger_message(self, message: Any):
        callbacks = []
        with self._lock:
            callbacks = self.message_callbacks.copy()

        for callback in callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in message callback: {str(e)}")

    def send_message(self, channel: str, content: str) -> bool:
        if not self.is_connected():
            logger.error("Cannot send message: not connected to Twitch")
            return False

        try:
            # Use the Bot's loop to send the message
            ch = self.bot.get_channel(channel)
            if not ch:
                logger.error(f"Channel {channel} not found")
                return False

            asyncio.run_coroutine_threadsafe(
                ch.send(content),
                self.bot.loop
            )
            logger.info(
                f"Sent message to {channel}: {sanitise_for_logging(content)}")
            return True
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False


# Singleton instance
twitch_pub = TwitchConnector()
