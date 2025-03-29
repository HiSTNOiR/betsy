"""
Main application entry point for the bot.

This module provides the main application class and entry point for running the bot.
"""

from bot.core.lifecycle import (
    LifecycleManager,
    get_lifecycle_manager,
    register_all_hooks,
)
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path if needed
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)


# Set up logger for this module
logger = logging.getLogger(__name__)


class BetsyBot:
    """
    Main bot application class.

    This class initialises and runs the bot, handling the application lifecycle.
    """

    def __init__(self, env_file: str = None):
        """
        Initialize the bot application.

        Args:
            env_file (str): Path to environment file.
        """
        self._env_file = env_file
        self._lifecycle = get_lifecycle_manager()

    def _setup_environment(self) -> None:
        """Set up the application environment."""
        # Set environment variables
        if self._env_file:
            os.environ['ENV_FILE'] = self._env_file

    def run(self) -> None:
        """Run the bot application."""
        try:
            # Set up environment
            self._setup_environment()

            # Register all lifecycle hooks
            register_all_hooks(self._lifecycle)

            # Run the application
            self._lifecycle.run()

        except Exception as e:
            logger.critical(
                f"Critical error in application: {str(e)}", exc_info=True)
            sys.exit(1)


def main() -> None:
    """Main entry point for the bot application."""
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(
        description="Betsy Bot - Twitch bot with extensive features")
    parser.add_argument(
        "--env",
        dest="env_file",
        default=None,
        help="Path to environment file"
    )

    args = parser.parse_args()

    # Run the bot
    bot = BetsyBot(env_file=args.env_file)
    bot.run()


if __name__ == "__main__":
    main()
