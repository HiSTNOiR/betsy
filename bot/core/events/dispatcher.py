"""
Event dispatcher for the bot.

This module provides the EventDispatcher class, which manages event handlers and dispatches
events to the appropriate handlers.
"""

import asyncio
import logging
import traceback
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast

from bot.core.events.base import (
    Event, EventError, EventFilter, EventFilterError, EventHandler,
    EventHandlerError, EventPriority, EventType
)

# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variable for type hinting
T = TypeVar('T', bound=Event)


class EventDispatcher:
    """
    Central event dispatcher for the application.

    The dispatcher manages event handlers and filters, and dispatches events to the
    appropriate handlers based on event type.
    """

    def __init__(self):
        """Initialize the event dispatcher."""
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._generic_handlers: List[EventHandler] = []
        self._filters: List[EventFilter] = []
        self._event_queue: asyncio.Queue[Event] = asyncio.Queue()
        self._processing_task: Optional[asyncio.Task] = None
        self._is_processing = False
        self._lock = asyncio.Lock()  # For thread safety

    async def start_processing(self) -> None:
        """Start processing events from the queue."""
        if self._is_processing:
            logger.warning("Event processing is already running")
            return

        self._is_processing = True
        self._processing_task = asyncio.create_task(self._process_events())
        logger.info("Event processing started")

    async def stop_processing(self) -> None:
        """Stop processing events."""
        if not self._is_processing:
            logger.warning("Event processing is not running")
            return

        self._is_processing = False
        if self._processing_task is not None:
            await self._processing_task
            self._processing_task = None
        logger.info("Event processing stopped")

    async def _process_events(self) -> None:
        """Process events from the queue."""
        logger.debug("Event processor started")
        try:
            while self._is_processing:
                try:
                    # Get the next event from the queue with a timeout
                    # This allows checking _is_processing regularly
                    event = await asyncio.wait_for(self._event_queue.get(), 0.1)

                    # Process the event
                    await self._handle_event(event)

                    # Mark the task as done
                    self._event_queue.task_done()
                except asyncio.TimeoutError:
                    # No event in the queue, check _is_processing and continue
                    continue
                except asyncio.CancelledError:
                    # Task was cancelled
                    break
                except Exception as e:
                    logger.error(
                        f"Error processing event: {str(e)}", exc_info=True)
        except Exception as e:
            logger.error(
                f"Fatal error in event processor: {str(e)}", exc_info=True)
            self._is_processing = False
        finally:
            logger.debug("Event processor stopped")

    async def publish(self, event: Event) -> None:
        """
        Publish an event to be processed.

        Args:
            event (Event): The event to publish.
        """
        await self._event_queue.put(event)
        logger.debug(f"Event published: {event.name}")

    async def publish_now(self, event: Event) -> None:
        """
        Publish and process an event immediately, bypassing the queue.

        Args:
            event (Event): The event to publish and process.
        """
        await self._handle_event(event)
        logger.debug(
            f"Event published and processed immediately: {event.name}")

    async def _handle_event(self, event: Event) -> None:
        """
        Handle an event by dispatching it to registered handlers.

        Args:
            event (Event): The event to handle.
        """
        # Apply filters
        filtered_event = await self._apply_filters(event)
        if filtered_event is None:
            logger.debug(f"Event filtered out: {event.name}")
            return

        # Get handlers for this event type
        handlers = self._get_handlers_for_event(filtered_event)

        if not handlers:
            logger.debug(f"No handlers for event: {filtered_event.name}")
            return

        # Sort handlers by priority
        sorted_handlers = sorted(handlers, key=lambda h: h.priority.value)

        # Process the event with each handler
        for handler in sorted_handlers:
            try:
                if filtered_event.cancelled:
                    logger.debug(f"Event cancelled: {filtered_event.name}")
                    break

                await handler.handle_event(filtered_event)

                if not filtered_event.propagate:
                    logger.debug(
                        f"Event propagation stopped: {filtered_event.name}")
                    break
            except Exception as e:
                error = EventHandlerError(handler, filtered_event, e)
                logger.error(str(error), exc_info=True)
                # Publish an error event, but don't raise to allow other handlers to run
                await self.publish(Event(
                    type=event.event_type_enum.ERROR,
                    source="event_dispatcher",
                    data={
                        "handler": handler.__class__.__name__,
                        "event": filtered_event.name,
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    }
                ))

    async def _apply_filters(self, event: Event) -> Optional[Event]:
        """
        Apply all registered filters to an event.

        Args:
            event (Event): The event to filter.

        Returns:
            Optional[Event]: The filtered event or None if the event should be dropped.
        """
        current_event = event

        for event_filter in self._filters:
            try:
                current_event = event_filter.filter_event(current_event)
                if current_event is None:
                    return None
            except Exception as e:
                error = EventFilterError(event_filter, event, e)
                logger.error(str(error), exc_info=True)
                # Continue with the original event

        return current_event

    def _get_handlers_for_event(self, event: Event) -> List[EventHandler]:
        """
        Get all handlers for a specific event.

        Args:
            event (Event): The event to get handlers for.

        Returns:
            List[EventHandler]: List of handlers for the event.
        """
        handlers: List[EventHandler] = []

        # Add specific handlers for this event type
        if event.type in self._handlers:
            handlers.extend(self._handlers[event.type])

        # Add generic handlers
        handlers.extend(self._generic_handlers)

        return handlers

    def register_handler(self, handler: EventHandler) -> None:
        """
        Register an event handler.

        Args:
            handler (EventHandler): The handler to register.
        """
        if not handler.event_types:
            # Register as a generic handler (handles all events)
            self._generic_handlers.append(handler)
            logger.debug(
                f"Registered generic handler: {handler.__class__.__name__}")
            return

        # Register for specific event types
        for event_type in handler.event_types:
            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(handler)
            logger.debug(
                f"Registered handler {handler.__class__.__name__} for event type: {event_type.name}")

    def unregister_handler(self, handler: EventHandler) -> None:
        """
        Unregister an event handler.

        Args:
            handler (EventHandler): The handler to unregister.
        """
        # Remove from generic handlers
        if handler in self._generic_handlers:
            self._generic_handlers.remove(handler)
            logger.debug(
                f"Unregistered generic handler: {handler.__class__.__name__}")

        # Remove from specific handlers
        for event_type, handlers in list(self._handlers.items()):
            if handler in handlers:
                handlers.remove(handler)
                logger.debug(
                    f"Unregistered handler {handler.__class__.__name__} from event type: {event_type.name}")

                # Remove the event type entry if no handlers remain
                if not handlers:
                    del self._handlers[event_type]

    def register_filter(self, event_filter: EventFilter) -> None:
        """
        Register an event filter.

        Args:
            event_filter (EventFilter): The filter to register.
        """
        self._filters.append(event_filter)
        logger.debug(
            f"Registered event filter: {event_filter.__class__.__name__}")

    def unregister_filter(self, event_filter: EventFilter) -> None:
        """
        Unregister an event filter.

        Args:
            event_filter (EventFilter): The filter to unregister.
        """
        if event_filter in self._filters:
            self._filters.remove(event_filter)
            logger.debug(
                f"Unregistered event filter: {event_filter.__class__.__name__}")

    def clear_handlers(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
        self._generic_handlers.clear()
        logger.debug("Cleared all event handlers")

    def clear_filters(self) -> None:
        """Clear all registered filters."""
        self._filters.clear()
        logger.debug("Cleared all event filters")

    def get_queue_size(self) -> int:
        """
        Get the current size of the event queue.

        Returns:
            int: Number of events in the queue.
        """
        return self._event_queue.qsize()


# Singleton instance of the event dispatcher
_event_dispatcher = EventDispatcher()


def get_event_dispatcher() -> EventDispatcher:
    """
    Get the singleton event dispatcher instance.

    Returns:
        EventDispatcher: Singleton event dispatcher instance.
    """
    return _event_dispatcher
