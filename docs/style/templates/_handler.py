import logging
from core.logging import get_logger
from core.errors import handle_error, NetworkError
from event_bus.bus import EventBus

class GenericSender:
   def __init__(self, event_bus: EventBus, platform: str):
       self.logger = get_logger(f"{platform}_sender")
       self.event_bus = event_bus
       self.platform = platform

   async def send_message(self, target: str, message: str):
       try:
           self.logger.info(f"Sending message to {target} via {self.platform}")
       except Exception as e:
           handle_error(NetworkError(f"Failed to send {self.platform} message: {e}"))

   def subscribe(self):
       self.event_bus.subscribe(f"{self.platform}_message", self.send_message)

    # EXAMPLE IMPLEMENTATION
