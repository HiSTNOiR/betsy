import logging
from typing import cast
from bot.core.events.base import (
    CoreEventType, ErrorEvent, Event, EventHandler, EventPriority, EventType
)
from bot.core.errors import get_error_handler, ErrorContext
logger = logging.getLogger(__name__)


class LoggingEventHandler(EventHandler):
    def __init__(self, level: int = logging.DEBUG):
        self._level = level

    @property
    def event_types(self) -> set[EventType]:
        return set()

    @property
    def priority(self) -> EventPriority:
        return EventPriority.HIGH

    async def handle_event(self, event: Event) -> None:
        logger.log(self._level, f"Event received: {event.name} from {event.source or 'unknown'} "
                   f"with data: {event.data}")


class ErrorEventHandler(EventHandler):
    def __init__(self):
        pass

    @property
    def event_types(self) -> set[EventType]:
        return {CoreEventType.ERROR}

    @property
    def priority(self) -> EventPriority:
        return EventPriority.HIGHEST

    async def handle_event(self, event: Event) -> None:
        try:
            if not isinstance(event, ErrorEvent):
                logger.warning(
                    f"Non-ErrorEvent received in ErrorEventHandler: {event.name}")
                return
            error_event = cast(ErrorEvent, event)
            logger.error(f"Error event received from {event.source or 'unknown'}: "
                         f"{error_event.data.get('error', 'Unknown error')}")
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
            logger.error(
                f"Error handling error event: {str(e)}", exc_info=True)


class LifecycleEventHandler(EventHandler):
    def __init__(self):
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
        return self._lifecycle_states

    @property
    def priority(self) -> EventPriority:
        return EventPriority.NORMAL

    async def handle_event(self, event: Event) -> None:
        logger.info(
            f"Lifecycle event: {event.name} from {event.source or 'unknown'}")
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
    from bot.core.events.dispatcher import get_event_dispatcher
    dispatcher = get_event_dispatcher()
    dispatcher.register_handler(LoggingEventHandler(logging.DEBUG))
    dispatcher.register_handler(ErrorEventHandler())
    dispatcher.register_handler(LifecycleEventHandler())
    logger.info("Global event handlers registered")
