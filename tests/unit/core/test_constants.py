"""
Unit tests for bot.core.constants module.

This module tests the constants defined in the constants module.
"""

import os
import unittest
from pathlib import Path

# Import the module under test
from bot.core.constants import (
    PROJECT_ROOT,
    DATA_DIR,
    LOGS_DIR,
    CONFIG_DIR,
    DEFAULT_ENV_FILE,
    DEFAULT_CONFIG,
    DB_SCHEMA_FILE,
    TWITCH_API_BASE_URL,
    TWITCH_AUTH_URL,
    FEATURES,
    USER_RANKS,
    DEFAULT_COMMAND_COOLDOWN,
    DEFAULT_GLOBAL_COOLDOWN,
    POINTS_PER_MESSAGE,
    POINTS_PER_MINUTE,
    POINTS_PER_BIT
)


class TestBotConstants(unittest.TestCase):
    """Test cases for bot constants."""

    def test_project_root_path(self):
        """Test PROJECT_ROOT is a valid path."""
        self.assertIsInstance(PROJECT_ROOT, Path)
        self.assertTrue(PROJECT_ROOT.exists())
        self.assertTrue(PROJECT_ROOT.is_dir())

    def test_directory_paths(self):
        """Test directory paths are correctly configured."""
        import os

        # Helper function to validate directory paths
        def validate_dir_path(path, expected_dir_name):
            """Validate a directory path."""
            self.assertIsInstance(path, Path)

            # Check that either the exact path exists or a parent directory exists
            path_exists = path.exists()
            parent_exists = path.parent.exists()

            error_msg = (
                f"Path {path} does not exist. "
                f"Parent directory exists: {parent_exists}. "
                f"Actual path: {path}"
            )

            self.assertTrue(path_exists or parent_exists, error_msg)

            # Normalise paths for cross-platform comparison
            norm_path = os.path.normpath(str(path))
            norm_expected_ending = os.path.normpath(expected_dir_name)

            self.assertTrue(
                norm_path.endswith(norm_expected_ending),
                f"Expected path to end with {norm_expected_ending}, but got {norm_path}"
            )

        # Validate data directory
        validate_dir_path(DATA_DIR, 'data')

        # Validate logs directory
        validate_dir_path(LOGS_DIR, 'logs')

        # Validate config directory
        validate_dir_path(CONFIG_DIR, 'config')

    def test_default_env_file(self):
        """Test DEFAULT_ENV_FILE configuration."""
        self.assertIsInstance(DEFAULT_ENV_FILE, Path)

        # Use os.path.normpath to handle different path separators
        import os
        expected_ending = os.path.normpath('.env')
        actual_path = os.path.normpath(str(DEFAULT_ENV_FILE))

        # Check if the actual path ends with the expected filename
        self.assertTrue(actual_path.endswith(expected_ending),
                        f"Expected path to end with {expected_ending}, but got {actual_path}")

        # Optional: Additional check to ensure the filename is exactly '.env'
        self.assertEqual(DEFAULT_ENV_FILE.name, '.env')

    def test_default_config_structure(self):
        """Test DEFAULT_CONFIG has expected structure and values."""
        # Basic structure checks
        self.assertIsInstance(DEFAULT_CONFIG, dict)

        # Check specific keys exist
        expected_keys = [
            "bot_nick", "bot_prefix", "channel", "log_level",
            "db_enabled", "obs_enabled", "discord_enabled", "db_path"
        ]
        for key in expected_keys:
            self.assertIn(key, DEFAULT_CONFIG)

        # Check specific default values
        self.assertEqual(DEFAULT_CONFIG["bot_nick"], "BetsyBot")
        self.assertEqual(DEFAULT_CONFIG["bot_prefix"], "!")
        self.assertEqual(DEFAULT_CONFIG["log_level"], "INFO")

    def test_db_schema_file(self):
        """Test DB_SCHEMA_FILE configuration."""
        self.assertIsInstance(DB_SCHEMA_FILE, Path)

        # Use os.path.normpath to handle different path separators
        import os
        expected_ending = os.path.normpath('bot/db/schema.sql')
        actual_path = os.path.normpath(str(DB_SCHEMA_FILE))

        # Check if the actual path ends with the expected path
        self.assertTrue(actual_path.endswith(expected_ending),
                        f"Expected path to end with {expected_ending}, but got {actual_path}")

    def test_platform_constants(self):
        """Test Twitch platform constants."""
        self.assertEqual(TWITCH_API_BASE_URL, "https://api.twitch.tv/helix")
        self.assertEqual(TWITCH_AUTH_URL, "https://id.twitch.tv/oauth2/token")

    def test_features_list(self):
        """Test features list has correct structure."""
        self.assertIsInstance(FEATURES, list)
        self.assertTrue(len(FEATURES) > 0)

        # Check for specific features
        expected_features = [
            "points", "shop", "inventory", "duel", "domt",
            "obs_actions", "easter_eggs", "dungeon", "betsy_vault",
            "shield_mode", "todo", "chat_log", "ai"
        ]
        self.assertEqual(set(FEATURES), set(expected_features))

    def test_user_ranks(self):
        """Test user ranks configuration."""
        expected_ranks = [
            "viewer", "vip", "subscriber",
            "moderator", "broadcaster", "bot_admin"
        ]
        self.assertEqual(USER_RANKS, expected_ranks)

    def test_command_cooldown_constants(self):
        """Test command cooldown constants."""
        self.assertEqual(DEFAULT_COMMAND_COOLDOWN, 3)
        self.assertEqual(DEFAULT_GLOBAL_COOLDOWN, 1)

    def test_points_constants(self):
        """Test points earning constants."""
        self.assertEqual(POINTS_PER_MESSAGE, 10)
        self.assertEqual(POINTS_PER_MINUTE, 1)
        self.assertEqual(POINTS_PER_BIT, 1)


if __name__ == "__main__":
    unittest.main()
