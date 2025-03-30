import unittest
from unittest.mock import patch, MagicMock, call

import importlib
import logging

from bot.core.lifecycle.hooks import (
    register_config_hooks,
    register_logging_hooks,
    register_error_hooks,
    register_database_hooks,
    register_platform_hooks,
    register_command_hooks,
    register_feature_hooks,
    register_all_hooks,
    register_hook,
    HookType,
    HookDependency,
    mark_initialised,
    is_initialised,
    _import_module_safely,
    _validate_hook_dependencies,
)


class TestLifecycleHooks(unittest.TestCase):
    """Test the lifecycle hooks registration functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock LifecycleManager for testing
        self.mock_manager = MagicMock()

        # Capture logging
        self.log_capture = MagicMock()
        self.logger_patch = patch(
            'bot.core.lifecycle.hooks.logger', self.log_capture)
        self.logger_patch.start()

        # Reset initialised modules tracking
        patch('bot.core.lifecycle.hooks._initialised_modules', set()).start()
        patch('bot.core.lifecycle.hooks._registered_hooks', {
            hook_type: set() for hook_type in HookType
        }).start()

        # Mock register_hook to actually register hooks in _registered_hooks
        original_register_hook = register_hook

        def side_effect_register_hook(*args, **kwargs):
            result = original_register_hook(*args, **kwargs)
            return result

        self.register_hook_patch = patch(
            'bot.core.lifecycle.hooks.register_hook', side_effect=side_effect_register_hook)
        self.register_hook_patch.start()

    def tearDown(self):
        """Tear down test fixtures."""
        # Stop patches
        patch.stopall()

    @patch('bot.core.lifecycle.hooks._import_module_safely')
    def test_register_config_hooks(self, mock_import):
        """Test registration of configuration hooks."""
        # Given
        mock_config = MagicMock()
        mock_config_module = MagicMock()
        mock_config_module.get_config.return_value = mock_config
        mock_import.return_value = mock_config_module

        # When
        with patch('bot.core.lifecycle.hooks.register_hook') as mock_register_hook:
            # Check logging - need to verify this BEFORE executing the callback
            # which will generate additional log messages
            register_config_hooks(self.mock_manager)
            self.log_capture.debug.assert_called_with(
                'Registered configuration lifecycle hooks')

            # Then
            # Verify register_hook was called with the correct parameters
            mock_register_hook.assert_called_once()
            call_args = mock_register_hook.call_args

            self.assertEqual(call_args[1]['manager'], self.mock_manager)
            self.assertEqual(call_args[1]['name'], 'load_config')
            self.assertEqual(call_args[1]['hook_type'], HookType.INITIALISE)
            self.assertEqual(call_args[1]['priority'], 10)

            # Execute the callback to verify it works
            callback = call_args[1]['callback']
            callback()

            # Verify config.load() was called
            mock_config.load.assert_called_once()

            # Verify initialised marker was set
            self.assertTrue(is_initialised('config'))

    @patch('bot.core.lifecycle.hooks._import_module_safely')
    def test_register_logging_hooks(self, mock_import):
        """Test registration of logging hooks."""
        # Given
        mock_config = MagicMock()
        mock_config.get.side_effect = lambda k, default=None: {
            'log_level': 'INFO', 'log_file': 'test.log'}.get(k, default)

        mock_config_module = MagicMock()
        mock_config_module.get_config.return_value = mock_config

        mock_logging_module = MagicMock()
        mock_setup_logging = MagicMock()
        mock_logging_module.setup_logging = mock_setup_logging

        mock_import.side_effect = lambda module: {
            'bot.core.config': mock_config_module,
            'bot.core.logging': mock_logging_module
        }.get(module)

        # Mark config as initialised for dependency
        mark_initialised('config')

        # When
        with patch('bot.core.lifecycle.hooks.register_hook') as mock_register_hook:
            # Check logging first, before executing the callback
            register_logging_hooks(self.mock_manager)
            self.log_capture.debug.assert_called_with(
                'Registered logging lifecycle hooks')

            # Then
            # Verify register_hook was called with the correct parameters
            mock_register_hook.assert_called_once()
            call_args = mock_register_hook.call_args

            self.assertEqual(call_args[1]['manager'], self.mock_manager)
            self.assertEqual(call_args[1]['name'], 'configure_logging')
            self.assertEqual(call_args[1]['hook_type'], HookType.INITIALISE)
            self.assertEqual(call_args[1]['priority'], 20)

            # Execute the callback to verify it works
            callback = call_args[1]['callback']
            callback()

            # Verify setup_logging was called with correct parameters
            mock_setup_logging.assert_called_once_with(
                level='INFO',
                log_file='test.log',
                console=True,
                file_rotation=True
            )

            # Verify initialised marker was set
            self.assertTrue(is_initialised('logging'))


class TestHookUtils(unittest.TestCase):
    """Test the hook utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Capture logging
        self.log_capture = MagicMock()
        self.logger_patch = patch(
            'bot.core.lifecycle.hooks.logger', self.log_capture)
        self.logger_patch.start()

        # Reset internal module state to avoid test interference
        patch('bot.core.lifecycle.hooks._registered_hooks', {
            hook_type: set() for hook_type in HookType
        }).start()
        patch('bot.core.lifecycle.hooks._initialised_modules', set()).start()

    def tearDown(self):
        """Tear down test fixtures."""
        # Stop patches
        patch.stopall()

    def test_import_module_safely(self):
        """Test safe module import."""
        # Test successful import
        with patch('importlib.import_module') as mock_import:
            mock_module = MagicMock()
            mock_import.return_value = mock_module

            result = _import_module_safely('valid.module')
            self.assertEqual(result, mock_module)
            mock_import.assert_called_once_with('valid.module')

        # Test ImportError
        with patch('importlib.import_module', side_effect=ImportError('Module not found')):
            result = _import_module_safely('invalid.module')
            self.assertIsNone(result)
            self.log_capture.warning.assert_called_with(
                'Module invalid.module not available: Module not found')

        # Test other exception
        with patch('importlib.import_module', side_effect=Exception('Unknown error')):
            result = _import_module_safely('error.module')
            self.assertIsNone(result)
            self.log_capture.error.assert_called_with(
                'Error importing module error.module: Unknown error', exc_info=True)

    def test_validate_hook_dependencies(self):
        """Test hook dependency validation."""
        # Manually register a hook for dependency testing
        from bot.core.lifecycle.hooks import _registered_hooks
        _registered_hooks[HookType.INITIALISE].add('existing_hook')

        # Test with no dependencies
        result = _validate_hook_dependencies('test_hook', HookType.INITIALISE)
        self.assertTrue(result)

        # Test with valid dependency
        valid_dep = HookDependency('existing_hook')
        result = _validate_hook_dependencies(
            'test_hook', HookType.INITIALISE, [valid_dep])
        self.assertTrue(result)

        # Test with invalid dependency
        invalid_dep = HookDependency('non_existing_hook')
        result = _validate_hook_dependencies(
            'test_hook', HookType.INITIALISE, [invalid_dep])
        self.assertFalse(result)
        self.log_capture.warning.assert_called_with(
            "Hook test_hook depends on non_existing_hook (type: INITIALISE), which is not registered."
        )

        # Test with mixed dependencies
        mixed_deps = [valid_dep, invalid_dep]
        result = _validate_hook_dependencies(
            'test_hook', HookType.INITIALISE, mixed_deps)
        self.assertFalse(result)

    def test_mark_and_check_initialised(self):
        """Test module initialisation marking and checking."""
        # Check before marking
        self.assertFalse(is_initialised('test_module'))

        # Mark as initialised
        mark_initialised('test_module')

        # Check after marking
        self.assertTrue(is_initialised('test_module'))
        self.log_capture.debug.assert_called_with(
            'Module test_module marked as initialised')

    def test_register_hook(self):
        """Test hook registration."""
        # Create a mock manager and callback
        mock_manager = MagicMock()
        mock_callback = MagicMock()

        # Test basic registration (INITIALISE type)
        result = register_hook(
            manager=mock_manager,
            name="test_hook",
            callback=mock_callback,
            hook_type=HookType.INITIALISE,
            priority=50
        )
        self.assertTrue(result)
        mock_manager.register_initialise_hook.assert_called_once_with(
            name="test_hook", callback=mock_callback, priority=50
        )

        # Test conditional registration - condition True
        mock_manager.reset_mock()
        def condition_true(): return True
        result = register_hook(
            manager=mock_manager,
            name="conditional_hook",
            callback=mock_callback,
            condition=condition_true
        )
        self.assertTrue(result)
        mock_manager.register_initialise_hook.assert_called_once()

        # Test conditional registration - condition False
        mock_manager.reset_mock()
        def condition_false(): return False
        result = register_hook(
            manager=mock_manager,
            name="conditional_hook",
            callback=mock_callback,
            condition=condition_false
        )
        self.assertFalse(result)
        mock_manager.register_initialise_hook.assert_not_called()

        # Test START hook type
        mock_manager.reset_mock()
        result = register_hook(
            manager=mock_manager,
            name="start_hook",
            callback=mock_callback,
            hook_type=HookType.START
        )
        self.assertTrue(result)
        mock_manager.register_start_hook.assert_called_once()

        # Test STOP hook type
        mock_manager.reset_mock()
        result = register_hook(
            manager=mock_manager,
            name="stop_hook",
            callback=mock_callback,
            hook_type=HookType.STOP
        )
        self.assertTrue(result)
        mock_manager.register_stop_hook.assert_called_once()

        # Test SHUTDOWN hook type
        mock_manager.reset_mock()
        result = register_hook(
            manager=mock_manager,
            name="shutdown_hook",
            callback=mock_callback,
            hook_type=HookType.SHUTDOWN
        )
        self.assertTrue(result)
        mock_manager.register_shutdown_hook.assert_called_once()

        # Test ERROR hook type
        mock_manager.reset_mock()
        result = register_hook(
            manager=mock_manager,
            name="error_hook",
            callback=mock_callback,
            hook_type=HookType.ERROR
        )
        self.assertTrue(result)
        mock_manager.register_error_hook.assert_called_once()

        # Test failed dependency validation
        with patch('bot.core.lifecycle.hooks._validate_hook_dependencies', return_value=False):
            mock_manager.reset_mock()
            result = register_hook(
                manager=mock_manager,
                name="dep_hook",
                callback=mock_callback,
                dependencies=[HookDependency("missing_hook")]
            )
            self.assertFalse(result)
            mock_manager.register_initialise_hook.assert_not_called()
