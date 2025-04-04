"""
Event system package for the bot.

This package provides an event system for communication between different components
of the application without direct dependencies.
"""

from bot.core.events.base import (
    Event, EventType, EventPriority, EventHandler, EventFilter,
    EventError, EventHandlerError, EventFilterError,
    CoreEventType, CoreEvent, ErrorEvent
)
from bot.core.events.dispatcher import (
    EventDispatcher, get_event_dispatcher
)
from bot.core.events.registry import (
    EventRegistry, EventRegistryError, get_event_registry
)
from bot.core.events.handlers import (
    LoggingEventHandler, ErrorEventHandler, LifecycleEventHandler,
    register_global_handlers
)

__all__ = [
    # Base classes
    "Event",
    "EventType",
    "EventPriority",
    "EventHandler",
    "EventFilter",
    "EventError",
    "EventHandlerError",
    "EventFilterError",
    "CoreEventType",
    "CoreEvent",
    "ErrorEvent",

    # Dispatcher
    "EventDispatcher",
    "get_event_dispatcher",

    # Registry
    "EventRegistry",
    "EventRegistryError",
    "get_event_registry",

    # Handlers
    "LoggingEventHandler",
    "ErrorEventHandler",
    "LifecycleEventHandler",
    "register_global_handlers",
]


async def initialise_event_system(package_paths: list[str] = None) -> None:
    """
    Initialise the event system.

    This function initialises the event registry, registers global handlers, and
    starts event processing.

    Args:
        package_paths (list[str]): List of package paths to scan for events.
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info("Initialising event system")

    # Initialise the event registry
    registry = get_event_registry()
    registry.initialise(package_paths)

    # Register global handlers
    register_global_handlers()

    # Start event processing
    dispatcher = get_event_dispatcher()
    await dispatcher.start_processing()

    logger.info("Event system initialised")


async def shutdown_event_system() -> None:
    """
    Shut down the event system.

    This function stops event processing and performs cleanup.
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info("Shutting down event system")

    # Stop event processing
    dispatcher = get_event_dispatcher()
    await dispatcher.stop_processing()

    logger.info("Event system shut down")
