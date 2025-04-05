import asyncio
import threading

import twitchio
from twitchio.ext import commands

from core.config import config
from core.logging import get_logger
from core.errors import TwitchError, handle_error
from utils.platform_connections import PlatformConnection

class TwitchReader(PlatformConnection):
    def __init__(self):
        super().__init__()
        self.logger = get_logger("twitch_reader")
        self.enabled = config.get_boolean('TWITCH_ENABLED', False)
       
        try:
            self.bot_nick = config.get('BOT_NICK')
            self.bot_token = config.get('TMI_TOKEN')
            self.channels = config.get_list('CHANNEL')
            self.bot_prefix = config.get('BOT_PREFIX', '!')
           
            if not all([self.bot_nick, self.bot_token, self.channels]):
                raise TwitchError("Missing Twitch configuration")
        except Exception as e:
            handle_error(TwitchError(f"Twitch configuration error: {e}"))
            self.enabled = False

    def _connect(self):
        if not self.enabled:
            self.logger.warning("Twitch connection is disabled")
            return False
        
        try:
            self.connection = commands.Bot(
                token=self.bot_token,
                nick=self.bot_nick,
                prefix=self.bot_prefix,
                initial_channels=self.channels
            )
           
            self._register_default_events()
           
            connection_thread = threading.Thread(target=self._run_bot, daemon=True)
            connection_thread.start()
            
            return True
        except Exception as e:
            error_msg = f"Twitch connection failed: {e}"
            self.logger.error(error_msg)
            handle_error(TwitchError(error_msg))
            return False

    def _run_bot(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.connection.start())
        except Exception as e:
            error_msg = f"Twitch bot run error: {e}"
            self.logger.error(error_msg)
            handle_error(TwitchError(error_msg))

    def _register_default_events(self):
        @self.connection.event()
        async def event_ready():
            self.logger.info(f"Twitch bot connected as {self.connection.nick}")
            self.logger.info(f"Connected to channels: {', '.join(self.channels)}")

        @self.connection.event()
        async def event_message(message):
            if not message.echo:
                self.logger.debug(f"Message from {message.author.name}: {message.content}")

        @self.connection.event()
        async def event_error(error):
            self.logger.error(f"Twitch bot error: {error}")
            handle_error(TwitchError(f"Twitch bot encountered an error: {error}"))

    def _disconnect(self):
        if self.connection:
            try:
                asyncio.run(self.connection.close())
                self.logger.info("Twitch bot disconnected")
            except Exception as e:
                error_msg = f"Error disconnecting Twitch bot: {e}"
                self.logger.error(error_msg)
                handle_error(TwitchError(error_msg))

twitch_reader = TwitchReader()