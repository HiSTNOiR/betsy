"""
Unit tests for bot.core.lifecycle.manager module.

This module tests the lifecycle manager implementation.
"""

import asyncio
import threading
import time
import unittest
from enum import Enum, auto
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from bot.core.lifecycle.manager import (
    LifecycleManager, LifecycleState, LifecycleError, LifecycleHook
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestLifecycleHook(TestCase):
    """Test cases for LifecycleHook class."""

    def test_lifecycle_hook_creation(self):
        """Test creating a lifecycle hook."""
        # Create a mock callback
        callback = MagicMock()

        # Create a hook
        hook = LifecycleHook(name="test_hook", callback=callback, priority=50)

        # Check that it has the expected attributes
        self.assertEqual(hook.name, "test_hook")
        self.assertEqual(hook.callback, callback)
        self.assertEqual(hook.priority, 50)

    def test_lifecycle_hook_comparison(self):
        """Test that hooks are compared based on priority."""
        # Create hooks with different priorities
        hook1 = LifecycleHook(name="hook1", callback=MagicMock(), priority=10)
        hook2 = LifecycleHook(name="hook2", callback=MagicMock(), priority=20)

        # Check that hook1 is considered "less than" hook2
        self.assertLess(hook1, hook2)

        # Note: The other comparison operators are not currently implemented
        # in the LifecycleHook class, so we only test the < operator


class TestLifecycleManager(TestCase):
    """Test cases for LifecycleManager class."""

    def setUp(self):
        """Set up test environment."""
        # Create a manager for each test
        self.shutdown_event = threading.Event()
        self.manager = LifecycleManager(shutdown_event=self.shutdown_event)

    def test_initial_state(self):
        """Test that the manager starts in the INITIALISING state."""
        self.assertEqual(self.manager.state, LifecycleState.INITIALISING)

    def test_register_hooks(self):
        """Test registering hooks of different types."""
        # Create mock callbacks
        initialise_callback = MagicMock()
        start_callback = MagicMock()
        stop_callback = MagicMock()
        shutdown_callback = MagicMock()
        error_callback = MagicMock()

        # Register hooks
        self.manager.register_initialise_hook(
            "initialise", initialise_callback, 10)
        self.manager.register_start_hook("start", start_callback, 20)
        self.manager.register_stop_hook("stop", stop_callback, 30)
        self.manager.register_shutdown_hook("shutdown", shutdown_callback, 40)
        self.manager.register_error_hook("error", error_callback, 50)

        # Check that the hooks were registered
        self.assertEqual(len(self.manager._initialise_hooks), 1)
        self.assertEqual(len(self.manager._start_hooks), 1)
        self.assertEqual(len(self.manager._stop_hooks), 1)
        self.assertEqual(len(self.manager._shutdown_hooks), 1)
        self.assertEqual(len(self.manager._error_hooks), 1)

    def test_hook_sorting(self):
        """Test that hooks are sorted by priority."""
        # Register hooks with different priorities
        self.manager.register_initialise_hook("hook3", MagicMock(), 30)
        self.manager.register_initialise_hook("hook1", MagicMock(), 10)
        self.manager.register_initialise_hook("hook2", MagicMock(), 20)

        # Check that they're sorted by priority
        self.assertEqual(self.manager._initialise_hooks[0].name, "hook1")
        self.assertEqual(self.manager._initialise_hooks[1].name, "hook2")
        self.assertEqual(self.manager._initialise_hooks[2].name, "hook3")

    def test_initialise(self):
        """Test initialising the application."""
        # Register a hook
        callback = MagicMock()
        self.manager.register_initialise_hook("test", callback)

        # Initialise
        self.manager.initialise()

        # Check that the callback was called
        callback.assert_called_once()

        # Check that the state changed
        self.assertEqual(self.manager.state, LifecycleState.INITIALISED)

    def test_initialise_error(self):
        """Test error handling during initialisation."""
        # Redirect stderr during this test to suppress error output
        with patch('sys.stderr'), patch('logging.Logger.error'):
            # Register a hook that raises an exception
            callback = MagicMock(side_effect=ValueError("Test error"))
            self.manager.register_initialise_hook("test", callback)

            # Try to initialise
            with self.assertRaises(LifecycleError):
                self.manager.initialise()

            # Check that the state changed to ERROR
            self.assertEqual(self.manager.state, LifecycleState.ERROR)

    def test_start(self):
        """Test starting the application."""
        # Set up the manager in the INITIALISED state
        self.manager._state = LifecycleState.INITIALISED

        # Register a hook
        callback = MagicMock()
        self.manager.register_start_hook("test", callback)

        # Start
        self.manager.start()

        # Check that the callback was called
        callback.assert_called_once()

        # Check that the state changed
        self.assertEqual(self.manager.state, LifecycleState.RUNNING)

    def test_start_from_wrong_state(self):
        """Test that starting from a state other than INITIALISED raises an error."""
        # The manager is in INITIALISING state by default
        with self.assertRaises(LifecycleError):
            self.manager.start()

    def test_start_error(self):
        """Test error handling during start."""
        # Set up the manager in the INITIALISED state
        self.manager._state = LifecycleState.INITIALISED

        # Register a hook that raises an exception
        callback = MagicMock(side_effect=ValueError("Test error"))
        self.manager.register_start_hook("test", callback)

        # Try to start
        with self.assertRaises(LifecycleError):
            self.manager.start()

        # Check that the state changed to ERROR
        self.assertEqual(self.manager.state, LifecycleState.ERROR)

    def test_stop(self):
        """Test stopping the application."""
        # Set up the manager in the RUNNING state
        self.manager._state = LifecycleState.RUNNING

        # Register a hook
        callback = MagicMock()
        self.manager.register_stop_hook("test", callback)

        # Stop
        self.manager.stop()

        # Check that the callback was called
        callback.assert_called_once()

        # Check that the state changed
        self.assertEqual(self.manager.state, LifecycleState.STOPPED)

    def test_stop_from_wrong_state(self):
        """Test that stopping from a state other than RUNNING or ERROR raises an error."""
        # The manager is in INITIALISING state by default
        with self.assertRaises(LifecycleError):
            self.manager.stop()

    def test_stop_error(self):
        """Test error handling during stop."""
        # Set up the manager in the RUNNING state
        self.manager._state = LifecycleState.RUNNING

        # Register a hook that raises an exception
        callback = MagicMock(side_effect=ValueError("Test error"))
        self.manager.register_stop_hook("test", callback)

        # Try to stop - it should handle the exception internally
        try:
            self.manager.stop()
        except Exception:
            self.fail("stop() should not raise exceptions from hooks")

        # Even though the hook raised an exception, the state should still change
        # to STOPPED as the manager should be designed to be resilient
        self.assertEqual(self.manager.state, LifecycleState.STOPPED)

    def test_shutdown(self):
        """Test shutting down the application."""
        # Register a hook
        callback = MagicMock()
        self.manager.register_shutdown_hook("test", callback)

        # Shutdown
        self.manager.shutdown()

        # Check that the callback was called
        callback.assert_called_once()

    def test_shutdown_error(self):
        """Test error handling during shutdown."""
        # Register a hook that raises an exception
        callback = MagicMock(side_effect=ValueError("Test error"))
        self.manager.register_shutdown_hook("test", callback)

        # Try to shutdown
        with self.assertRaises(LifecycleError):
            self.manager.shutdown()

    def test_run(self):
        """Test running the application."""
        # Create mock methods
        self.manager._run_initialise = MagicMock()
        self.manager._run_start = MagicMock()
        self.manager._run_wait_for_shutdown = MagicMock()
        self.manager._run_stop = MagicMock()
        self.manager._run_shutdown = MagicMock()

        # Run
        self.manager.run()

        # Check that the methods were called
        self.manager._run_initialise.assert_called_once()
        self.manager._run_start.assert_called_once()
        self.manager._run_wait_for_shutdown.assert_called_once()
        self.manager._run_stop.assert_called_once()
        self.manager._run_shutdown.assert_called_once()

    def test_run_exception(self):
        """Test exception handling during run."""
        # Redirect stderr during this test to suppress error output
        with patch('sys.stderr'), patch('logging.Logger.error'):
            # Make _run_initialise raise an exception
            self.manager._run_initialise = MagicMock(
                side_effect=ValueError("Test error"))
            self.manager._handle_run_exception = MagicMock()

            # Try to run
            self.manager.run()

            # Check that _handle_run_exception was called
            self.manager._handle_run_exception.assert_called_once()

    def test_request_shutdown(self):
        """Test requesting a shutdown."""
        # Request shutdown
        self.manager.request_shutdown()

        # Check that the event was set
        self.assertTrue(self.shutdown_event.is_set())

    @patch("signal.signal")
    def test_setup_signal_handlers(self, mock_signal):
        """Test setting up signal handlers."""
        # Call _setup_signal_handlers
        self.manager._setup_signal_handlers()

        # Check that signal.signal was called
        self.assertEqual(mock_signal.call_count, 2)


if __name__ == "__main__":
    unittest.main()
