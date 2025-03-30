"""
Lifecycle management for the bot.

This module provides the LifecycleManager class which manages the application's lifecycle.
"""

import logging
import signal
import sys
import time
import threading
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type

from bot.core.errors import BotError

# Set up logger for this module
logger = logging.getLogger(__name__)


class LifecycleState(Enum):
    """Possible states of the application lifecycle."""

    INITIALISING = auto()
    INITIALISED = auto()
    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    STOPPED = auto()
    ERROR = auto()


class LifecycleError(BotError):
    """Exception raised for lifecycle-related errors."""
    pass


class LifecycleHook:
    """
    Hook executed at specific points in the application lifecycle.

    Hooks are executed in priority order (lower values first).
    """

    def __init__(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ):
        """
        Initialize the lifecycle hook.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
        self.name = name
        self.callback = callback
        self.priority = priority

    def __lt__(self, other: 'LifecycleHook') -> bool:
        """
        Compare hooks based on priority.

        Args:
            other (LifecycleHook): Other hook to compare.

        Returns:
            bool: True if this hook has higher priority (lower value).
        """
        return self.priority < other.priority


class LifecycleManager:
    """
    Manages the application's lifecycle.

    This class provides methods for initialising, starting, and stopping the application,
    as well as registering hooks to be executed at specific points in the lifecycle.
    """

    def __init__(self, shutdown_event: Optional[threading.Event] = None, stop_timeout: float = 5.0):
        """
        Initialize the lifecycle manager.

        Args:
            shutdown_event (Optional[threading.Event]): Event used to signal shutdown.
                If None, a new Event is created.
            stop_timeout (float): Timeout in seconds for stopping operations.
        """
        self._state = LifecycleState.INITIALISING
        self._initialise_hooks: List[LifecycleHook] = []
        self._start_hooks: List[LifecycleHook] = []
        self._stop_hooks: List[LifecycleHook] = []
        self._shutdown_hooks: List[LifecycleHook] = []
        self._error_hooks: List[LifecycleHook] = []
        self._shutdown_event = shutdown_event or threading.Event()
        self._stop_timeout = stop_timeout

        # Last resort error handler in case all error hooks fail
        self._fallback_error_handler = self._default_error_handler

    @property
    def state(self) -> LifecycleState:
        """Get the current lifecycle state."""
        return self._state

    def register_initialise_hook(
        self,
        name: str,
        callback: Callable[[], None],
        priority: int = 100
    ) -> None:
        """
        Register a hook to be executed during initialisation.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
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
        """
        Register a hook to be executed when starting.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
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
        """
        Register a hook to be executed when stopping.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
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
        """
        Register a hook to be executed during shutdown.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
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
        """
        Register a hook to be executed on error.

        Args:
            name (str): Hook name.
            callback (Callable[[], None]): Function to execute.
            priority (int): Priority of the hook (lower values execute first).
        """
        hook = LifecycleHook(name, callback, priority)
        self._error_hooks.append(hook)
        self._error_hooks.sort()
        logger.debug(f"Registered error hook: {name} (priority: {priority})")

    def set_fallback_error_handler(self, handler: Callable[[Exception], None]) -> None:
        """
        Set a fallback error handler to use if all error hooks fail.

        Args:
            handler (Callable[[Exception], None]): Function to handle errors.
        """
        self._fallback_error_handler = handler
        logger.debug("Set fallback error handler")

    def _default_error_handler(self, exception: Exception) -> None:
        """
        Default fallback error handler.

        Args:
            exception (Exception): The exception that occurred.
        """
        logger.critical(
            f"Unhandled error in lifecycle manager: {str(exception)}",
            exc_info=True
        )

    def initialise(self) -> None:
        """
        Initialise the application.

        Executes all initialisation hooks in priority order.

        Raises:
            LifecycleError: If there is an error initialising the application.
        """
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
        """Execute all initialisation hooks in priority order."""
        for hook in self._initialise_hooks:
            logger.debug(f"Executing initialise hook: {hook.name}")
            hook.callback()

    def start(self) -> None:
        """
        Start the application.

        Executes all start hooks in priority order.

        Raises:
            LifecycleError: If there is an error starting the application.
        """
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

            # Set up signal handlers
            self._setup_signal_handlers()
        except Exception as e:
            self._state = LifecycleState.ERROR
            logger.error(
                f"Error starting application: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error starting application: {str(e)}") from e

    def _execute_start_hooks(self) -> None:
        """Execute all start hooks in priority order."""
        for hook in self._start_hooks:
            logger.debug(f"Executing start hook: {hook.name}")
            hook.callback()

    def stop(self) -> None:
        """
        Stop the application.

        Executes all stop hooks in priority order.

        Raises:
            LifecycleError: If there is an error stopping the application.
        """
        if self._state not in (LifecycleState.RUNNING, LifecycleState.ERROR):
            error_msg = f"Cannot stop from state: {self._state}"
            logger.error(error_msg)
            raise LifecycleError(error_msg)

        logger.info("Stopping application")
        self._state = LifecycleState.STOPPING

        try:
            self._execute_stop_hooks()
            self._state = LifecycleState.STOPPED
            logger.info("Application stopped")
        except Exception as e:
            self._state = LifecycleState.ERROR
            logger.error(
                f"Error stopping application: {str(e)}", exc_info=True)
            self._execute_error_hooks()
            raise LifecycleError(
                f"Error stopping application: {str(e)}") from e

    def _execute_stop_hooks(self) -> None:
        """Execute all stop hooks in priority order."""
        for hook in self._stop_hooks:
            logger.debug(f"Executing stop hook: {hook.name}")
            hook.callback()

    def shutdown(self) -> None:
        """
        Perform application shutdown.

        Executes all shutdown hooks in priority order.

        Raises:
            LifecycleError: If there is an error during shutdown.
        """
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
        """Execute all shutdown hooks in priority order."""
        for hook in self._shutdown_hooks:
            logger.debug(f"Executing shutdown hook: {hook.name}")
            hook.callback()

    def run(self) -> None:
        """
        Run the application until shutdown is requested.

        This method initialises the application, starts it, waits for a shutdown signal,
        stops the application, and performs shutdown.
        """
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
        """Initialise the application as part of the run process."""
        self.initialise()

    def _run_start(self) -> None:
        """Start the application as part of the run process."""
        self.start()
        logger.info("Application running, press Ctrl+C to exit")

    def _run_wait_for_shutdown(self) -> None:
        """Wait for shutdown signal as part of the run process."""
        while not self._shutdown_event.is_set():
            self._shutdown_event.wait(0.1)

        logger.info("Shutdown requested")

    def _run_stop(self) -> None:
        """Stop the application as part of the run process."""
        if self._state in (LifecycleState.RUNNING, LifecycleState.STARTING):
            self.stop()

    def _run_shutdown(self) -> None:
        """Perform shutdown as part of the run process."""
        self.shutdown()

    def _handle_run_exception(self, exception: Optional[Exception] = None) -> None:
        """
        Handle exceptions during the run process.

        Args:
            exception (Optional[Exception]): The exception that occurred, if any.
        """
        if self._state in (LifecycleState.RUNNING, LifecycleState.STARTING):
            self.stop()
        self.shutdown()
        sys.exit(1)

    def request_shutdown(self) -> None:
        """Request application shutdown."""
        logger.info("Shutdown requested")
        self._shutdown_event.set()

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(sig, frame):
            logger.info(f"Received signal: {sig}")
            self.request_shutdown()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _execute_error_hooks(self) -> None:
        """Execute all error hooks."""
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

        # If all error hooks fail, use fallback handler
        if error_count == total_hooks and total_hooks > 0:
            logger.warning("All error hooks failed, using fallback handler")
            try:
                self._fallback_error_handler(Exception("Error hooks failed"))
            except Exception as e:
                logger.critical(
                    f"Fallback error handler failed: {str(e)}", exc_info=True)


# Singleton instance of the error handler
_lifecycle_manager = LifecycleManager()


def get_lifecycle_manager() -> LifecycleManager:
    """
    Get the singleton lifecycle manager instance.

    Returns:
        LifecycleManager: Singleton lifecycle manager instance.
    """
    return _lifecycle_manager
