from event_bus.bus import EventBus
from publishers.twitch_reader import twitch_reader
from subscribers.twitch_handler import create_twitch_handler
from core.config import config
from core.logging import get_logger

logger = get_logger("main")

def main():
    event_bus = EventBus()
    
    if config.get_boolean('TWITCH_ENABLED', False):
        twitch_handler = create_twitch_handler(event_bus)
        twitch_reader._connect()

if __name__ == "__main__":
    main()