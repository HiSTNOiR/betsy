import threading
import time
import asyncio
import signal
import sys

from core.config import config
from core.logging import get_logger
from core.errors import handle_error, BetsyError
from event_bus.bus import event_bus
from event_bus.registry import event_registry
from publishers.twitch_pub import twitch_pub
from subscribers.twitch_sub import twitch_sub
from utils.reward_service import reward_service
from utils.reward_sync import reward_sync
from utils.channel_points_service import channel_points_service
from processors.command_parser import command_parser
from commands import command_registry
from events.twitch import *

logger = get_logger("main")


class BetsyBot:
    def __init__(self):
        self.running = False
        self._setup_signal_handlers()
        self._register_events()

    def _setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum=None, frame=None):
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)

    def _register_events(self):
        event_registry.register_event("twitch_ready", TwitchReadyEvent)
        event_registry.register_event("twitch_message", TwitchMessageEvent)
        event_registry.register_event("twitch_join", TwitchJoinEvent)
        event_registry.register_event("twitch_part", TwitchPartEvent)
        event_registry.register_event(
            "twitch_subscription", TwitchSubscriptionEvent)
        event_registry.register_event("twitch_bits", TwitchBitsEvent)
        event_registry.register_event("twitch_follow", TwitchFollowEvent)
        event_registry.register_event("twitch_raid", TwitchRaidEvent)
        event_registry.register_event(
            "twitch_subscription_gift", TwitchSubscriptionGiftEvent)
        event_registry.register_event(
            "twitch_channel_point_redemption", TwitchChannelPointRedemptionEvent)
        event_registry.register_event(
            "send_twitch_message", SendTwitchMessageEvent)

    def start(self):
        try:
            logger.info("Starting Betsy...")
            self.running = True
            command_parser.set_prefix(config.get('BOT_PREFIX', '!'))

            if config.get_boolean('TWITCH_ENABLED', True):
                self._setup_twitch_events()

            twitch_sub.subscribe()
            event_bus.subscribe("bot_shutdown", lambda _: self.shutdown())

            while self.running:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.shutdown()
                    break

        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            handle_error(BetsyError(f"Error starting bot: {str(e)}"))
            self.shutdown()

    def _setup_twitch_events(self):
        twitch_pub.register_event_callback("ready",
                                           lambda data: event_registry.create_and_publish_event("twitch_ready", data))
        twitch_pub.register_message_callback(self._handle_twitch_message)
        twitch_pub.register_event_callback("join",
                                           lambda data: event_registry.create_and_publish_event("twitch_join", data))
        twitch_pub.register_event_callback("part",
                                           lambda data: event_registry.create_and_publish_event("twitch_part", data))
        twitch_pub.register_event_callback("subscription",
                                           lambda data: event_registry.create_and_publish_event("twitch_subscription", data))
        twitch_pub.register_event_callback("bits",
                                           lambda data: event_registry.create_and_publish_event("twitch_bits", data))
        twitch_pub.register_event_callback("follow",
                                           lambda data: event_registry.create_and_publish_event("twitch_follow", data))
        twitch_pub.register_event_callback("raid",
                                           lambda data: event_registry.create_and_publish_event("twitch_raid", data))
        twitch_pub.register_event_callback("channel_point_redemption",
                                           lambda data: event_registry.create_and_publish_event("twitch_channel_point_redemption", data))

        twitch_pub._connect()

    def _handle_twitch_message(self, data):
        command_data = command_parser.parse_message(data)
        if command_data:
            command_parser.process_command(command_data)
        event_registry.create_and_publish_event("twitch_message", data)

    def shutdown(self):
        logger.info("Shutting down Betsy...")
        self.running = False
        twitch_pub._disconnect()


if __name__ == "__main__":
    bot = BetsyBot()
    channel_points_service.initialize(reward_service)

    if config.get_boolean('TWITCH_ENABLED', True):
        logger.info("Initial sync of Twitch rewards...")
        added, updated, failed = reward_sync.sync_all_rewards()
        logger.info(
            f"Rewards sync complete: {added} added, {updated} updated, {failed} failed")

    bot.start()
