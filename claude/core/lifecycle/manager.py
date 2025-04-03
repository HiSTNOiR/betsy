import logging
import signal
import sys
import time
import threading
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type
from bot.core.errors import BotError
logger = logging.getLogger(__name__)


class LifecycleState(Enum):
    INITIALISING = auto()
    INITIALISED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    STOPPED = auto()
    ERROR = auto()


class LifecycleError(BotError):
    pass


class LifecycleHook:
    def __init__(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ):
        self.name = name
        self.callback = callback
        self.priority = priority

    def __lt__(self, other: 'LifecycleHook') -> bool:
        return self.priority < other.priority


class LifecycleManager:
    def __init__(self, shutdown_event: Optional[threading.Event] = None, stop_timeout: float = 5.0):
        self._state = LifecycleState.INITIALISING
        self._initialise_hooks: List[LifecycleHook] = []
        self._start_hooks: List[LifecycleHook] = []
        self._stop_hooks: List[LifecycleHook] = []
        self._shutdown_hooks: List[LifecycleHook] = []
        self._error_hooks: List[LifecycleHook] = []
        self._shutdown_event = shutdown_event or threading.Event()
        self._stop_timeout = stop_timeout
        self._fallback_error_handler = self._default_error_handler

    @property
    def state(self) -> LifecycleState:
        return self._state

    def register_initialise_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        hook = LifecycleHook(name, callback, priority)
        self._initialise_hooks.append(hook)
        self._initialise_hooks.sort()
        logger.debug(
            f"Registered initialise hook: {name} (priority: {priority})")

    def register_start_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        hook = LifecycleHook(name, callback, priority)
        self._start_hooks.append(hook)
        self._start_hooks.sort()
        logger.debug(f"Registered start hook: {name} (priority: {priority})")

    def register_stop_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        hook = LifecycleHook(name, callback, priority)
        self._stop_hooks.append(hook)
        self._stop_hooks.sort()
        logger.debug(f"Registered stop hook: {name} (priority: {priority})")

    def register_shutdown_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        hook = LifecycleHook(name, callback, priority)
        self._shutdown_hooks.append(hook)
        self._shutdown_hooks.sort()
        logger.debug(
            f"Registered shutdown hook: {name} (priority: {priority})")

    def register_error_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        hook = LifecycleHook(name, callback, priority)
        self._error_hooks.append(hook)
        self._error_hooks.sort()
        logger.debug(f"Registered error hook: {name} (priority: {priority})")

    def set_fallback_error_handler(self, handler: Callable[[Exception], None]) -> None:
        self._fallback_error_handler = handler
        logger.debug("Set fallback error handler")

    def _default_error_handler(self, exception: Exception) -> None:
        logger.critical(
            f"Unhandled error in lifecycle manager: {str(exception)}",
            exc_info=True
        )

    def initialise(self) -> None:
        if self._state != LifecycleState.INITIALISING:
            error_msg = f"Cannot initialise from state: {self._state}"
            logger.error(error_msg)
            raise LifecycleError(error_msg)
        logger.info("Initialising application")
        try:
            self._execute_initialise_hooks()
            self._state = LifecycleState.INITIALISED
            logger.info("Application initialised")
        except Exception as e:
            self._state = LifecycleState.ERROR
            logger.error(
                f"Error initialising application: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error initialising application: {str(e)}") from e

    def _execute_initialise_hooks(self) -> None:
        for hook in self._initialise_hooks:
            logger.debug(f"Executing initialise hook: {hook.name}")
            hook.callback()

    def start(self) -> None:
        if self._state != LifecycleState.INITIALISED:
            error_msg = f"Cannot start from state: {self._state}"
            logger.error(error_msg)
            raise LifecycleError(error_msg)
        logger.info("Starting application")
        self._state = LifecycleState.STARTING
        try:
            self._execute_start_hooks()
            self._state = LifecycleState.RUNNING
            logger.info("Application started")
            self._setup_signal_handlers()
        except Exception as e:
            self._state = LifecycleState.ERROR
            logger.error(
                f"Error starting application: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error starting application: {str(e)}") from e

    def _execute_start_hooks(self) -> None:
        for hook in self._start_hooks:
            logger.debug(f"Executing start hook: {hook.name}")
            hook.callback()

    def stop(self) -> None:
        if self._state not in (LifecycleState.RUNNING, LifecycleState.ERROR):
            error_msg = f"Cannot stop from state: {self._state}"
            logger.error(error_msg)
            raise LifecycleError(error_msg)
        logger.info("Stopping application")
        self._state = LifecycleState.STOPPING
        try:
            self._execute_stop_hooks_with_timeout()
            self._state = LifecycleState.STOPPED
            logger.info("Application stopped")
        except Exception as e:
            self._state = LifecycleState.ERROR
            logger.error(
                f"Error stopping application: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error stopping application: {str(e)}") from e

    def _execute_stop_hooks_with_timeout(self) -> None:
        if not self._stop_hooks:
            logger.debug("No stop hooks to execute")
            return
        stop_thread = threading.Thread(
            target=self._execute_stop_hooks,
            name="StopHooksThread"
        )
        stop_thread.daemon = True
        logger.debug(
            f"Executing stop hooks with timeout of {self._stop_timeout} seconds")
        start_time = time.time()
        stop_thread.start()
        stop_thread.join(timeout=self._stop_timeout)
        if stop_thread.is_alive():
            elapsed = time.time() - start_time
            logger.warning(
                f"Stop hooks did not complete within timeout ({elapsed:.2f}s). "
                f"Continuing with shutdown anyway."
            )

    def _execute_stop_hooks(self) -> None:
        for hook in self._stop_hooks:
            try:
                logger.debug(f"Executing stop hook: {hook.name}")
                hook.callback()
            except Exception as e:
                logger.error(
                    f"Error in stop hook {hook.name}: {str(e)}", exc_info=True)
                raise

    def shutdown(self) -> None:
        logger.info("Shutting down application")
        try:
            self._execute_shutdown_hooks()
            logger.info("Application shutdown complete")
        except Exception as e:
            logger.error(
                f"Error during application shutdown: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error during application shutdown: {str(e)}") from e

    def _execute_shutdown_hooks(self) -> None:
        for hook in self._shutdown_hooks:
            logger.debug(f"Executing shutdown hook: {hook.name}")
            hook.callback()

    def run(self) -> None:
        try:
            self._run_initialise()
            self._run_start()
            self._run_wait_for_shutdown()
            self._run_stop()
            self._run_shutdown()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self._handle_run_exception()
        except Exception as e:
            logger.error(f"Error in application run: {str(e)}", exc_info=True)
            self._handle_run_exception(e)

    def _run_initialise(self) -> None:
        self.initialise()

    def _run_start(self) -> None:
        self.start()
        logger.info("Application running, press Ctrl+C to exit")

    def _run_wait_for_shutdown(self) -> None:
        while not self._shutdown_event.is_set():
            self._shutdown_event.wait(0.1)

        logger.info("Shutdown requested")

    def _run_stop(self) -> None:
        if self._state in (LifecycleState.RUNNING, LifecycleState.STARTING):
            self.stop()

    def _run_shutdown(self) -> None:
        self.shutdown()

    def _handle_run_exception(self, exception: Optional[Exception] = None) -> None:
        if self._state in (LifecycleState.RUNNING, LifecycleState.STARTING):
            self.stop()
        self.shutdown()
        sys.exit(1)

    def request_shutdown(self) -> None:
        logger.info("Shutdown requested")
        self._shutdown_event.set()

    def _setup_signal_handlers(self) -> None:
        def signal_handler(sig, frame):
            logger.info(f"Received signal: {sig}")
            self.request_shutdown()
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _execute_error_hooks(self) -> None:
        error_count = 0
        total_hooks = len(self._error_hooks)
        for hook in self._error_hooks:
            try:
                logger.debug(f"Executing error hook: {hook.name}")
                hook.callback()
            except Exception as e:
                error_count += 1
                logger.error(
                    f"Error in error hook {hook.name}: {str(e)}", exc_info=True)
        if error_count == total_hooks and total_hooks > 0:
            logger.warning("All error hooks failed, using fallback handler")
            try:
                self._fallback_error_handler(Exception("Error hooks failed"))
            except Exception as e:
                logger.critical(
                    f"Fallback error handler failed: {str(e)}", exc_info=True)


_lifecycle_manager = LifecycleManager()


def get_lifecycle_manager() -> LifecycleManager:
    return _lifecycle_manager
