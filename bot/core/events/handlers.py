"""
Global event handlers for the bot.

This module provides predefined event handlers for common scenarios and system events.
"""

import logging
from typing import cast
from bot.core.events.base import (
    CoreEventType, ErrorEvent, Event, EventHandler, EventPriority, EventType
)
from bot.core.errors import get_error_handler, ErrorContext

# Set up logger for this module
logger = logging.getLogger(__name__)


class LoggingEventHandler(EventHandler):
    """
    Event handler that logs all events.

    This handler can be used for debugging or monitoring the event system.
    """

    def __init__(self, level: int = logging.DEBUG):
        """
        Initialize the logging event handler.

        Args:
            level (int): Log level to use.
        """
        self._level = level

    @property
    def event_types(self) -> set[EventType]:
        """
        Get the event types this handler can handle.

        The logging handler handles all event types.

        Returns:
            set[EventType]: Empty set (handles all events).
        """
        return set()  # Empty set means it handles all events

    @property
    def priority(self) -> EventPriority:
        """
        Get the priority of this handler.

        The logging handler should run before other handlers.

        Returns:
            EventPriority: High priority.
        """
        return EventPriority.HIGH

    async def handle_event(self, event: Event) -> None:
        """
        Handle an event by logging it.

        Args:
            event (Event): The event to handle.
        """
        logger.log(self._level, f"Event received: {event.name} from {event.source or 'unknown'} "
                   f"with data: {event.data}")


class ErrorEventHandler(EventHandler):
    """
    Event handler for error events.

    This handler logs errors and can forward them to the global error handler.
    """

    def __init__(self):
        """Initialize the error event handler."""
        pass

    @property
    def event_types(self) -> set[EventType]:
        """
        Get the event types this handler can handle.

        Returns:
            set[EventType]: Set containing only the ERROR event type.
        """
        return {CoreEventType.ERROR}

    @property
    def priority(self) -> EventPriority:
        """
        Get the priority of this handler.

        The error handler should run with highest priority.

        Returns:
            EventPriority: Highest priority.
        """
        return EventPriority.HIGHEST

    async def handle_event(self, event: Event) -> None:
        """
        Handle an error event.

        Args:
            event (Event): The error event to handle.
        """
        try:
            # Check if event is an instance of ErrorEvent first
            if not isinstance(event, ErrorEvent):
                logger.warning(
                    f"Non-ErrorEvent received in ErrorEventHandler: {event.name}")
                return

            # Try to cast to an ErrorEvent
            error_event = cast(ErrorEvent, event)

            # Log the error
            logger.error(f"Error event received from {event.source or 'unknown'}: "
                         f"{error_event.data.get('error', 'Unknown error')}")

            # Forward to the global error handler
            error_handler = get_error_handler()
            exception = error_event.exception

            if exception:
                context = ErrorContext(
                    error=exception,
                    source=event.source or "event_system",
                    context=error_event.error_context,
                    traceback_info=error_event.data.get("traceback", "")
                )

                error_handler.handle(exception, context)
        except Exception as e:
            # If something goes wrong while handling the error event,
            # log it but don't create another error event to avoid loops
            logger.error(
                f"Error handling error event: {str(e)}", exc_info=True)


class LifecycleEventHandler(EventHandler):
    """
    Event handler for lifecycle events.

    This handler logs lifecycle events and can perform additional actions when the system
    changes state.
    """

    def __init__(self):
        """Initialize the lifecycle event handler."""
        self._lifecycle_states = {
            CoreEventType.INITIALISING,
            CoreEventType.INITIALISED,
            CoreEventType.STARTING,
            CoreEventType.STARTED,
            CoreEventType.STOPPING,
            CoreEventType.STOPPED,
            CoreEventType.SHUTDOWN
        }

    @property
    def event_types(self) -> set[EventType]:
        """
        Get the event types this handler can handle.

        Returns:
            set[EventType]: Set of lifecycle event types.
        """
        return self._lifecycle_states

    @property
    def priority(self) -> EventPriority:
        """
        Get the priority of this handler.

        The lifecycle handler should run with normal priority.

        Returns:
            EventPriority: Normal priority.
        """
        return EventPriority.NORMAL

    async def handle_event(self, event: Event) -> None:
        """
        Handle a lifecycle event.

        Args:
            event (Event): The lifecycle event to handle.
        """
        logger.info(
            f"Lifecycle event: {event.name} from {event.source or 'unknown'}")

        # Perform actions based on the lifecycle state
        if event.type == CoreEventType.INITIALISING:
            logger.info("System is initialising")
        elif event.type == CoreEventType.INITIALISED:
            logger.info("System initialisation complete")
        elif event.type == CoreEventType.STARTING:
            logger.info("System is starting")
        elif event.type == CoreEventType.STARTED:
            logger.info("System startup complete")
        elif event.type == CoreEventType.STOPPING:
            logger.info("System is stopping")
        elif event.type == CoreEventType.STOPPED:
            logger.info("System has stopped")
        elif event.type == CoreEventType.SHUTDOWN:
            logger.info("System is shutting down")


def register_global_handlers() -> None:
    """
    Register global event handlers.

    This function registers the default event handlers with the event dispatcher.
    """
    from bot.core.events.dispatcher import get_event_dispatcher

    dispatcher = get_event_dispatcher()

    # Register logging handler at DEBUG level
    dispatcher.register_handler(LoggingEventHandler(logging.DEBUG))

    # Register error handler
    dispatcher.register_handler(ErrorEventHandler())

    # Register lifecycle handler
    dispatcher.register_handler(LifecycleEventHandler())

    logger.info("Global event handlers registered")
