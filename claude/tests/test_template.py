import unittest
import sys
import os
from unittest import TestCase
from unittest.mock import (
    patch, MagicMock, mock_open, Mock
)
from bot.core.app import BetsyBot, main
unittest.main.__defaults__ = (None, True, [], False)


class TestBetsyBot(TestCase):
    def setUp(self):
        if 'ENV_FILE' in os.environ:
            del os.environ['ENV_FILE']

    def test_init_without_env_file(self):
        bot = BetsyBot()
        self.assertIsNotNone(bot._lifecycle)
        self.assertIsNone(bot._env_file)

    def test_init_with_env_file(self):
        env_file_path = "/path/to/test/.env"
        bot = BetsyBot(env_file=env_file_path)
        self.assertIsNotNone(bot._lifecycle)
        self.assertEqual(bot._env_file, env_file_path)

    @patch('bot.core.app.register_all_hooks')
    @patch('bot.core.lifecycle.LifecycleManager.run')
    def test_run_success(self, mock_lifecycle_run, mock_register_hooks):
        bot = BetsyBot()
        bot.run()
        self.assertTrue(mock_register_hooks.called)
        self.assertTrue(mock_lifecycle_run.called)

    @patch('bot.core.app.register_all_hooks')
    @patch('bot.core.lifecycle.LifecycleManager.run')
    @patch('sys.exit')
    def test_run_with_exception(self, mock_sys_exit, mock_lifecycle_run, mock_register_hooks):
        bot = BetsyBot()
        mock_lifecycle_run.side_effect = Exception("Test runtime error")
        bot.run()
        mock_sys_exit.assert_called_once_with(1)

    def test_setup_environment_with_env_file(self):
        env_file_path = "/path/to/test/.env"
        bot = BetsyBot(env_file=env_file_path)
        bot._setup_environment()
        self.assertEqual(os.environ.get('ENV_FILE'), env_file_path)

    def test_setup_environment_without_env_file(self):
        bot = BetsyBot()
        bot._setup_environment()
        self.assertNotIn('ENV_FILE', os.environ)


class TestMainFunction(TestCase):
    @patch('bot.core.app.BetsyBot')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_default_args(self, mock_parse_args, mock_bot_class):
        mock_bot_instance = mock_bot_class.return_value
        mock_bot_instance.run = MagicMock()
        mock_parse_args.return_value = Mock(env_file=None)
        main()
        mock_bot_class.assert_called_once_with(env_file=None)
        mock_bot_instance.run.assert_called_once()

    @patch('bot.core.app.BetsyBot')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_custom_env_file(self, mock_parse_args, mock_bot_class):
        custom_env_path = "/custom/path/to/.env"
        mock_bot_instance = mock_bot_class.return_value
        mock_bot_instance.run = MagicMock()
        mock_parse_args.return_value = Mock(env_file=custom_env_path)
        main()
        mock_bot_class.assert_called_once_with(env_file=custom_env_path)
        mock_bot_instance.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
