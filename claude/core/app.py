from bot.core.lifecycle import (
    LifecycleManager,
    get_lifecycle_manager,
    register_all_hooks,
)
import logging
import os
import sys
from pathlib import Path
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)
logger = logging.getLogger(__name__)


class BetsyBot:
    def __init__(self, env_file: str = None):
        self._env_file = env_file
        self._lifecycle = get_lifecycle_manager()

    def _setup_environment(self) -> None:
        if self._env_file:
            os.environ['ENV_FILE'] = self._env_file

    def run(self) -> None:
        try:
            self._setup_environment()
            register_all_hooks(self._lifecycle)
            self._lifecycle.run()
        except Exception as e:
            logger.critical(
                f"Critical error in application: {str(e)}", exc_info=True)
            sys.exit(1)


def main() -> None:
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
    bot = BetsyBot(env_file=args.env_file)
    bot.run()


if __name__ == "__main__":
    main()
