import asyncio
import logging
import traceback
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast
from bot.core.events.base import (
    Event, EventError, EventFilter, EventFilterError, EventHandler,
    EventHandlerError, EventPriority, EventType
)
logger = logging.getLogger(__name__)
T = TypeVar('T', bound=Event)


class EventDispatcher:
    def __init__(self):
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._generic_handlers: List[EventHandler] = []
        self._filters: List[EventFilter] = []
        self._event_queue: asyncio.Queue[Event] = asyncio.Queue()
        self._processing_task: Optional[asyncio.Task] = None
        self._is_processing = False

    async def start_processing(self) -> None:
        if self._is_processing:
            logger.warning("Event processing is already running")
            return
        self._is_processing = True
        self._processing_task = asyncio.create_task(self._process_events())
        logger.info("Event processing started")

    async def stop_processing(self) -> None:
        if not self._is_processing:
            logger.warning("Event processing is not running")
            return
        self._is_processing = False
        if self._processing_task is not None:
            await self._processing_task
            self._processing_task = None
        logger.info("Event processing stopped")

    async def _process_events(self) -> None:
        logger.debug("Event processor started")
        try:
            while self._is_processing:
                try:
                    event = await asyncio.wait_for(self._event_queue.get(), 0.1)
                    await self._handle_event(event)
                    self._event_queue.task_done()
                except asyncio.TimeoutError:
                    continue
                except asyncio.CancelledError:
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
        await self._event_queue.put(event)
        logger.debug(f"Event published: {event.name}")

    async def publish_now(self, event: Event) -> None:
        await self._handle_event(event)
        logger.debug(
            f"Event published and processed immediately: {event.name}")

    async def _handle_event(self, event: Event) -> None:
        filtered_event = await self._apply_filters(event)
        if filtered_event is None:
            logger.debug(f"Event filtered out: {event.name}")
            return
        handlers = self._get_handlers_for_event(filtered_event)
        if not handlers:
            logger.debug(f"No handlers for event: {filtered_event.name}")
            return
        sorted_handlers = sorted(handlers, key=lambda h: h.priority.value)
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
        current_event = event
        for event_filter in self._filters:
            try:
                current_event = event_filter.filter_event(current_event)
                if current_event is None:
                    return None
            except Exception as e:
                error = EventFilterError(event_filter, event, e)
                logger.error(str(error), exc_info=True)
        return current_event

    def _get_handlers_for_event(self, event: Event) -> List[EventHandler]:
        handlers: List[EventHandler] = []
        if event.type in self._handlers:
            handlers.extend(self._handlers[event.type])
        handlers.extend(self._generic_handlers)
        return sorted(handlers, key=lambda h: h.priority.value)

    def register_handler(self, handler: EventHandler) -> None:
        if not handler.event_types:
            self._generic_handlers.append(handler)
            logger.debug(
                f"Registered generic handler: {handler.__class__.__name__}")
            return
        for event_type in handler.event_types:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            self._handlers[event_type].append(handler)
            logger.debug(
                f"Registered handler {handler.__class__.__name__} for event type: {event_type.name}")

    def unregister_handler(self, handler: EventHandler) -> None:
        if handler in self._generic_handlers:
            self._generic_handlers.remove(handler)
            logger.debug(
                f"Unregistered generic handler: {handler.__class__.__name__}")
        for event_type, handlers in list(self._handlers.items()):
            if handler in handlers:
                handlers.remove(handler)
                logger.debug(
                    f"Unregistered handler {handler.__class__.__name__} from event type: {event_type.name}")
                if not handlers:
                    del self._handlers[event_type]

    def register_filter(self, event_filter: EventFilter) -> None:
        self._filters.append(event_filter)
        logger.debug(
            f"Registered event filter: {event_filter.__class__.__name__}")

    def unregister_filter(self, event_filter: EventFilter) -> None:
        if event_filter in self._filters:
            self._filters.remove(event_filter)
            logger.debug(
                f"Unregistered event filter: {event_filter.__class__.__name__}")

    def clear_handlers(self) -> None:
        self._handlers.clear()
        self._generic_handlers.clear()
        logger.debug("Cleared all event handlers")

    def clear_filters(self) -> None:
        self._filters.clear()
        logger.debug("Cleared all event filters")

    def get_queue_size(self) -> int:
        return self._event_queue.qsize()


_event_dispatcher = EventDispatcher()


def get_event_dispatcher() -> EventDispatcher:
    return _event_dispatcher
