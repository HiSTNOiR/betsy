"""
Unit tests for the lifecycle manager.

This module tests the functionality of the LifecycleManager class,
including hook registration, state transitions, and error handling.
"""

import unittest
from unittest.mock import Mock, patch, call
import threading
import time
import signal
import logging

from bot.core.lifecycle.manager import (
    LifecycleManager,
    LifecycleState,
    LifecycleError,
    LifecycleHook,
    get_lifecycle_manager
)


# Suppress logging during tests to reduce output
class SuppressLogging:
    """Context manager to suppress logging temporarily."""

    def __init__(self, logger_name='bot.core.lifecycle.manager'):
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level

    def __enter__(self):
        # Above CRITICAL to suppress all
        self.logger.setLevel(logging.CRITICAL + 1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.original_level)


class TestLifecycleHook(unittest.TestCase):
    """Test the LifecycleHook class."""

    def test_hook_creation(self):
        """Test that hooks can be created with proper attributes."""
        callback = Mock()
        hook = LifecycleHook("test_hook", callback, 50)
        self.assertEqual(hook.name, "test_hook")
        self.assertEqual(hook.callback, callback)
        self.assertEqual(hook.priority, 50)

    def test_hook_comparison(self):
        """Test hook comparison for sorting by priority."""
        hook1 = LifecycleHook("hook1", Mock(), 10)
        hook2 = LifecycleHook("hook2", Mock(), 20)
        hook3 = LifecycleHook("hook3", Mock(), 5)

        # Lower priority value means higher priority (sorts earlier)
        self.assertTrue(hook1 < hook2)
        self.assertTrue(hook3 < hook1)
        self.assertTrue(hook3 < hook2)


class TestLifecycleManager(unittest.TestCase):
    """Test the LifecycleManager class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.manager = LifecycleManager()
        # Clear any signal handlers that might be set by other tests
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

    def test_initial_state(self):
        """Test the initial state of the lifecycle manager."""
        self.assertEqual(self.manager.state, LifecycleState.INITIALISING)
        self.assertFalse(self.manager._shutdown_event.is_set())
        self.assertEqual(len(self.manager._initialise_hooks), 0)
        self.assertEqual(len(self.manager._start_hooks), 0)
        self.assertEqual(len(self.manager._stop_hooks), 0)
        self.assertEqual(len(self.manager._shutdown_hooks), 0)
        self.assertEqual(len(self.manager._error_hooks), 0)

    def test_register_initialise_hook(self):
        """Test registering initialisation hooks."""
        callback1 = Mock()
        callback2 = Mock()
        callback3 = Mock()

        # Register hooks with different priorities
        self.manager.register_initialise_hook("hook1", callback1, 30)
        self.manager.register_initialise_hook("hook2", callback2, 10)
        self.manager.register_initialise_hook("hook3", callback3, 20)

        # Check if hooks are registered in priority order
        self.assertEqual(len(self.manager._initialise_hooks), 3)
        self.assertEqual(self.manager._initialise_hooks[0].name, "hook2")
        self.assertEqual(self.manager._initialise_hooks[1].name, "hook3")
        self.assertEqual(self.manager._initialise_hooks[2].name, "hook1")

    def test_register_start_hook(self):
        """Test registering start hooks."""
        callback1 = Mock()
        callback2 = Mock()

        # Register hooks with different priorities
        self.manager.register_start_hook("hook1", callback1, 20)
        self.manager.register_start_hook("hook2", callback2, 10)

        # Check if hooks are registered in priority order
        self.assertEqual(len(self.manager._start_hooks), 2)
        self.assertEqual(self.manager._start_hooks[0].name, "hook2")
        self.assertEqual(self.manager._start_hooks[1].name, "hook1")

    def test_register_stop_hook(self):
        """Test registering stop hooks."""
        callback1 = Mock()
        callback2 = Mock()

        # Register hooks with different priorities
        self.manager.register_stop_hook("hook1", callback1, 20)
        self.manager.register_stop_hook("hook2", callback2, 10)

        # Check if hooks are registered in priority order
        self.assertEqual(len(self.manager._stop_hooks), 2)
        self.assertEqual(self.manager._stop_hooks[0].name, "hook2")
        self.assertEqual(self.manager._stop_hooks[1].name, "hook1")

    def test_register_shutdown_hook(self):
        """Test registering shutdown hooks."""
        callback1 = Mock()
        callback2 = Mock()

        # Register hooks with different priorities
        self.manager.register_shutdown_hook("hook1", callback1, 20)
        self.manager.register_shutdown_hook("hook2", callback2, 10)

        # Check if hooks are registered in priority order
        self.assertEqual(len(self.manager._shutdown_hooks), 2)
        self.assertEqual(self.manager._shutdown_hooks[0].name, "hook2")
        self.assertEqual(self.manager._shutdown_hooks[1].name, "hook1")

    def test_register_error_hook(self):
        """Test registering error hooks."""
        callback1 = Mock()
        callback2 = Mock()

        # Register hooks with different priorities
        self.manager.register_error_hook("hook1", callback1, 20)
        self.manager.register_error_hook("hook2", callback2, 10)

        # Check if hooks are registered in priority order
        self.assertEqual(len(self.manager._error_hooks), 2)
        self.assertEqual(self.manager._error_hooks[0].name, "hook2")
        self.assertEqual(self.manager._error_hooks[1].name, "hook1")

    def test_initialise(self):
        """Test the initialise method."""
        # Register initialisation hooks
        hook1 = Mock()
        hook2 = Mock()
        hook3 = Mock()

        self.manager.register_initialise_hook("hook1", hook1, 30)
        self.manager.register_initialise_hook("hook2", hook2, 10)
        self.manager.register_initialise_hook("hook3", hook3, 20)

        # Call initialise
        with SuppressLogging():
            self.manager.initialise()

        # Check if all hooks were called in the correct order
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_called_once()

        # Check if the state was updated
        self.assertEqual(self.manager.state, LifecycleState.INITIALISED)

    def test_initialise_error(self):
        """Test error handling during initialisation."""
        # Register hooks, one of which will fail
        hook1 = Mock()
        hook2 = Mock(side_effect=Exception("Test exception"))
        hook3 = Mock()

        self.manager.register_initialise_hook("hook1", hook1, 10)
        self.manager.register_initialise_hook("hook2", hook2, 20)
        self.manager.register_initialise_hook("hook3", hook3, 30)

        # Register error hook
        error_hook = Mock()
        self.manager.register_error_hook("error_hook", error_hook)

        # Call initialise, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.initialise()

        # Check if hooks were called up to the failing one
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_not_called()

        # Check if error hook was called
        error_hook.assert_called_once()

        # Check if the state was updated to ERROR
        self.assertEqual(self.manager.state, LifecycleState.ERROR)

    def test_initialise_invalid_state(self):
        """Test initialisation from invalid state."""
        # Set state to something other than INITIALISING
        self.manager._state = LifecycleState.INITIALISED

        # Call initialise, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.initialise()

    def test_start(self):
        """Test the start method."""
        # Set state to INITIALISED to allow starting
        self.manager._state = LifecycleState.INITIALISED

        # Register start hooks
        hook1 = Mock()
        hook2 = Mock()
        hook3 = Mock()

        self.manager.register_start_hook("hook1", hook1, 30)
        self.manager.register_start_hook("hook2", hook2, 10)
        self.manager.register_start_hook("hook3", hook3, 20)

        # Mock _setup_signal_handlers to prevent actual signal handler registration
        with SuppressLogging(), patch.object(self.manager, '_setup_signal_handlers') as mock_setup:
            # Call start
            self.manager.start()

            # Check if all hooks were called in the correct order
            hook1.assert_called_once()
            hook2.assert_called_once()
            hook3.assert_called_once()

            # Check if _setup_signal_handlers was called
            mock_setup.assert_called_once()

            # Check if the state was updated
            self.assertEqual(self.manager.state, LifecycleState.RUNNING)

    def test_start_error(self):
        """Test error handling during start."""
        # Set state to INITIALISED to allow starting
        self.manager._state = LifecycleState.INITIALISED

        # Register hooks, one of which will fail
        hook1 = Mock()
        hook2 = Mock(side_effect=Exception("Test exception"))
        hook3 = Mock()

        self.manager.register_start_hook("hook1", hook1, 10)
        self.manager.register_start_hook("hook2", hook2, 20)
        self.manager.register_start_hook("hook3", hook3, 30)

        # Register error hook
        error_hook = Mock()
        self.manager.register_error_hook("error_hook", error_hook)

        # Call start, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.start()

        # Check if hooks were called up to the failing one
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_not_called()

        # Check if error hook was called
        error_hook.assert_called_once()

        # Check if the state was updated to ERROR
        self.assertEqual(self.manager.state, LifecycleState.ERROR)

    def test_start_invalid_state(self):
        """Test starting from invalid state."""
        # Set state to something other than INITIALISED
        self.manager._state = LifecycleState.RUNNING

        # Call start, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.start()

    def test_stop(self):
        """Test the stop method."""
        # Set state to RUNNING to allow stopping
        self.manager._state = LifecycleState.RUNNING

        # Register stop hooks
        hook1 = Mock()
        hook2 = Mock()
        hook3 = Mock()

        self.manager.register_stop_hook("hook1", hook1, 30)
        self.manager.register_stop_hook("hook2", hook2, 10)
        self.manager.register_stop_hook("hook3", hook3, 20)

        # Call stop
        with SuppressLogging():
            self.manager.stop()

        # Check if all hooks were called in the correct order
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_called_once()

        # Check if the state was updated
        self.assertEqual(self.manager.state, LifecycleState.STOPPED)

    def test_stop_from_error_state(self):
        """Test stopping from ERROR state."""
        # Set state to ERROR
        self.manager._state = LifecycleState.ERROR

        # Register stop hooks
        hook1 = Mock()
        self.manager.register_stop_hook("hook1", hook1)

        # Call stop
        with SuppressLogging():
            self.manager.stop()

        # Check if hook was called
        hook1.assert_called_once()

        # Check if the state was updated
        self.assertEqual(self.manager.state, LifecycleState.STOPPED)

    def test_stop_error(self):
        """Test error handling during stop."""
        # Set state to RUNNING to allow stopping
        self.manager._state = LifecycleState.RUNNING

        # Register hooks, one of which will fail
        hook1 = Mock()
        hook2 = Mock(side_effect=Exception("Test exception"))
        hook3 = Mock()

        self.manager.register_stop_hook("hook1", hook1, 10)
        self.manager.register_stop_hook("hook2", hook2, 20)
        self.manager.register_stop_hook("hook3", hook3, 30)

        # Register error hook
        error_hook = Mock()
        self.manager.register_error_hook("error_hook", error_hook)

        # Call stop, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.stop()

        # Check if hooks were called up to the failing one
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_not_called()

        # Check if error hook was called
        error_hook.assert_called_once()

        # Check if the state was updated to ERROR
        self.assertEqual(self.manager.state, LifecycleState.ERROR)

    def test_stop_invalid_state(self):
        """Test stopping from invalid state."""
        # Set state to something other than RUNNING or ERROR
        self.manager._state = LifecycleState.INITIALISED

        # Call stop, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.stop()

    def test_shutdown(self):
        """Test the shutdown method."""
        # Register shutdown hooks
        hook1 = Mock()
        hook2 = Mock()
        hook3 = Mock()

        self.manager.register_shutdown_hook("hook1", hook1, 30)
        self.manager.register_shutdown_hook("hook2", hook2, 10)
        self.manager.register_shutdown_hook("hook3", hook3, 20)

        # Call shutdown
        with SuppressLogging():
            self.manager.shutdown()

        # Check if all hooks were called in the correct order
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_called_once()

    def test_shutdown_error(self):
        """Test error handling during shutdown."""
        # Register hooks, one of which will fail
        hook1 = Mock()
        hook2 = Mock(side_effect=Exception("Test exception"))
        hook3 = Mock()

        self.manager.register_shutdown_hook("hook1", hook1, 10)
        self.manager.register_shutdown_hook("hook2", hook2, 20)
        self.manager.register_shutdown_hook("hook3", hook3, 30)

        # Register error hook
        error_hook = Mock()
        self.manager.register_error_hook("error_hook", error_hook)

        # Call shutdown, should raise LifecycleError
        with SuppressLogging(), self.assertRaises(LifecycleError):
            self.manager.shutdown()

        # Check if hooks were called up to the failing one
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_not_called()

        # Check if error hook was called
        error_hook.assert_called_once()

    def test_request_shutdown(self):
        """Test requesting shutdown."""
        # Call request_shutdown
        with SuppressLogging():
            self.manager.request_shutdown()

        # Check if shutdown event is set
        self.assertTrue(self.manager._shutdown_event.is_set())

    def test_signal_handler(self):
        """Test signal handler registration."""
        # Set state to RUNNING to ensure we can register signal handlers
        self.manager._state = LifecycleState.INITIALISED

        # Mock signal.signal to capture handler registration
        with SuppressLogging(), patch('signal.signal') as mock_signal:
            # Call start to register signal handlers
            with patch.object(self.manager, '_execute_start_hooks'):
                self.manager.start()

            # Check if signal.signal was called for SIGINT and SIGTERM
            self.assertEqual(mock_signal.call_count, 2)
            mock_signal.assert_has_calls([
                call(signal.SIGINT, mock_signal.call_args[0][1]),
                call(signal.SIGTERM, mock_signal.call_args[0][1])
            ])

    def test_execute_error_hooks(self):
        """Test execution of error hooks."""
        # Register error hooks
        hook1 = Mock()
        hook2 = Mock(side_effect=Exception("Error in error hook"))
        hook3 = Mock()

        self.manager.register_error_hook("hook1", hook1, 30)
        self.manager.register_error_hook("hook2", hook2, 10)
        self.manager.register_error_hook("hook3", hook3, 20)

        # Mock the fallback handler to verify it gets called
        mock_fallback = Mock()
        self.manager.set_fallback_error_handler(mock_fallback)

        # Call _execute_error_hooks
        with SuppressLogging():
            self.manager._execute_error_hooks()

        # Check if all hooks were called in priority order
        hook1.assert_called_once()
        hook2.assert_called_once()
        hook3.assert_called_once()

        # Since not all error hooks failed, fallback should not be called
        mock_fallback.assert_not_called()

    def test_fallback_error_handler(self):
        """Test fallback error handler when all hooks fail."""
        # Register error hooks that all fail
        hook1 = Mock(side_effect=Exception("Error 1"))
        hook2 = Mock(side_effect=Exception("Error 2"))

        self.manager.register_error_hook("hook1", hook1, 10)
        self.manager.register_error_hook("hook2", hook2, 20)

        # Mock the fallback handler to verify it gets called
        mock_fallback = Mock()
        self.manager.set_fallback_error_handler(mock_fallback)

        # Call _execute_error_hooks
        with SuppressLogging():
            self.manager._execute_error_hooks()

        # Since all error hooks failed, fallback should be called
        mock_fallback.assert_called_once()

    def test_run(self):
        """Test the run method."""
        # Create mock methods for each of the run stages
        with SuppressLogging(), \
                patch.object(self.manager, '_run_initialise') as mock_initialise, \
                patch.object(self.manager, '_run_start') as mock_start, \
                patch.object(self.manager, '_run_wait_for_shutdown') as mock_wait, \
                patch.object(self.manager, '_run_stop') as mock_stop, \
                patch.object(self.manager, '_run_shutdown') as mock_shutdown:

            # Call run
            self.manager.run()

            # Check that all stage methods were called exactly once
            mock_initialise.assert_called_once()
            mock_start.assert_called_once()
            mock_wait.assert_called_once()
            mock_stop.assert_called_once()
            mock_shutdown.assert_called_once()

    def test_run_with_error(self):
        """Test run method with an error during initialisation."""
        # Mock _run_initialise to raise an exception
        with SuppressLogging(), \
                patch.object(self.manager, '_run_initialise', side_effect=Exception("Test exception")), \
                patch.object(self.manager, '_handle_run_exception') as mock_handle_exception:

            # Call run
            self.manager.run()

            # Check that the exception handler was called
            mock_handle_exception.assert_called_once()

    def test_run_with_keyboard_interrupt(self):
        """Test run method with keyboard interrupt during start."""
        # Mock _run_start to raise KeyboardInterrupt
        with SuppressLogging(), \
                patch.object(self.manager, '_run_initialise') as mock_initialise, \
                patch.object(self.manager, '_run_start', side_effect=KeyboardInterrupt()), \
                patch.object(self.manager, '_handle_run_exception') as mock_handle_exception:

            # Call run
            self.manager.run()

            # Check that initialise was called and exception handler was called
            mock_initialise.assert_called_once()
            mock_handle_exception.assert_called_once()

    def test_handle_run_exception(self):
        """Test the exception handling during run."""
        # Mock stop and shutdown methods
        with SuppressLogging(), \
                patch.object(self.manager, 'stop') as mock_stop, \
                patch.object(self.manager, 'shutdown') as mock_shutdown, \
                patch('sys.exit') as mock_exit:

            # Set state to RUNNING to test stop is called
            self.manager._state = LifecycleState.RUNNING

            # Call _handle_run_exception
            self.manager._handle_run_exception(Exception("Test exception"))

            # Check that stop and shutdown were called
            mock_stop.assert_called_once()
            mock_shutdown.assert_called_once()
            mock_exit.assert_called_once_with(1)


class TestLifecycleManagerSingleton(unittest.TestCase):
    """Test the lifecycle manager singleton instance."""

    def test_get_lifecycle_manager(self):
        """Test getting the singleton lifecycle manager instance."""
        manager1 = get_lifecycle_manager()
        manager2 = get_lifecycle_manager()

        # Should return the same instance
        self.assertIs(manager1, manager2)


if __name__ == '__main__':
    unittest.main()
