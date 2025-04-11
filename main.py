import logging
import signal
import sys
import threading
import time
import asyncio

from core.config import config
from core.logging import get_logger
from core.errors import handle_error, BetsyError
from event_bus.bus import event_bus
from event_bus.registry import event_registry
from publishers.twitch_pub import twitch_pub
from subscribers.twitch_sub import twitch_sub
from processors.command_parser import command_parser
# Import command registry (which auto-loads commands)
from commands.registry import command_registry

# Import twitch event types
from events.twitch import (
    TwitchReadyEvent,
    TwitchMessageEvent,
    TwitchJoinEvent,
    TwitchPartEvent,
    TwitchSubscriptionEvent,
    TwitchBitsEvent,
    TwitchFollowEvent,
    TwitchRaidEvent,
    TwitchSubscriptionGiftEvent,
    TwitchChannelPointRedemptionEvent,
    SendTwitchMessageEvent
)

logger = get_logger("main")


class BetsyBot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BetsyBot, cls).__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if self._initialised:
            return

        self.running = False
        self.setup_signal_handlers()
        self.register_events()
        self._initialised = True

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def register_events(self):
        # Register Twitch events
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

            # Set up command parser
            command_parser.set_prefix(config.get('BOT_PREFIX', '!'))

            # Subscribe to events
            logger.info("Setting up event subscriptions...")
            twitch_sub.subscribe()

            # Subscribe to shutdown event
            event_bus.subscribe("bot_shutdown", lambda _: self.shutdown())

            # Set up asyncio exception handling
            try:
                asyncio.get_running_loop().set_exception_handler(self._handle_async_exception)
            except RuntimeError:
                # Fallback for when no loop is running
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.set_exception_handler(self._handle_async_exception)

            # Start Twitch connection
            if config.get_boolean('TWITCH_ENABLED', True):
                logger.info("Registering Twitch event callbacks...")
                twitch_pub.register_event_callback("ready",
                                                   lambda data: event_registry.create_and_publish_event("twitch_ready", data))
                twitch_pub.register_message_callback(
                    self._handle_twitch_message)
                twitch_pub.register_event_callback("join",
                                                   lambda data: event_registry.create_and_publish_event("twitch_join", data))
                twitch_pub.register_event_callback("part",
                                                   lambda data: event_registry.create_and_publish_event("twitch_part", data))
                twitch_pub.register_event_callback("subscription",
                                                   lambda data: event_registry.create_and_publish_event("twitch_subscription", data))
                twitch_pub.register_event_callback("subscription_gift",
                                                   lambda data: event_registry.create_and_publish_event("twitch_subscription_gift", data))
                twitch_pub.register_event_callback("bits",
                                                   lambda data: event_registry.create_and_publish_event("twitch_bits", data))
                twitch_pub.register_event_callback("follow",
                                                   lambda data: event_registry.create_and_publish_event("twitch_follow", data))
                twitch_pub.register_event_callback("raid",
                                                   lambda data: event_registry.create_and_publish_event("twitch_raid", data))
                twitch_pub.register_event_callback("channel_point_redemption",
                                                   lambda data: event_registry.create_and_publish_event("twitch_channel_point_redemption", data))

                logger.info("Connecting to Twitch...")
                twitch_pub._connect()
                logger.info("Twitch connection initiated")

            # Keep the main thread alive
            while self.running:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Keyboard interrupt detected")
                    self.shutdown()
                    break

        except Exception as e:
            logger.error(f"Unhandled exception in bot startup: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            handle_error(BetsyError(f"Error starting bot: {str(e)}"))
            self.shutdown()

    def _handle_async_exception(self, loop, context):
        exception = context.get('exception')
        if isinstance(exception, asyncio.CancelledError):
            logger.warning("Asyncio task was cancelled")
        else:
            logger.error(f"Unhandled asyncio error: {context}")

    def _handle_twitch_message(self, data):
        # Process message for commands first
        command_data = command_parser.parse_message(data)
        if command_data:
            command_parser.process_command(command_data)

        # Always publish the raw message event
        # Other subscribers can decide if they want to process it
        event_registry.create_and_publish_event("twitch_message", data)

    def shutdown(self):
        logger.info("Shutting down Betsy...")
        self.running = False

        # Disconnect from Twitch
        if twitch_pub.is_connected():
            logger.info("Disconnecting from Twitch...")
            try:
                twitch_pub._disconnect()
            except Exception as e:
                logger.error(f"Error during Twitch disconnection: {str(e)}")

        logger.info("Shutdown complete")

    def handle_shutdown(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)

    def ensure_bot_admin_exists():  # ! delete meh
        from db.database import db  # TODO ^
        from datetime import datetime

        try:
            admin = db.fetchone(
                "SELECT * FROM users WHERE twitch_username = 'bob' AND rank = 'untouchable'")

            if not admin:
                admin_data = {
                    "twitch_username": "bob",
                    "rank": "untouchable",
                    "points": 100000,
                    "date_added": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat()
                }

                db.execute(
                    "INSERT INTO users (twitch_username, rank, points, date_added, last_seen) VALUES (?, ?, ?, ?, ?)",
                    [admin_data["twitch_username"], admin_data["rank"], admin_data["points"],
                        admin_data["date_added"], admin_data["last_seen"]]
                )
                logger.info("Created bot admin user 'bob'")
        except Exception as e:
            handle_error(e, {"context": "ensure_bot_admin_exists"})


if __name__ == "__main__":
    bot = BetsyBot()
    bot.start()
