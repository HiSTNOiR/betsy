"""
Lifecycle hooks for the bot.

This module provides predefined lifecycle hooks for the application.
"""

import logging
import sys
from typing import Callable, Dict, List, Optional

from bot.core.lifecycle.manager import LifecycleManager, get_lifecycle_manager

# Set up logger for this module
logger = logging.getLogger(__name__)


def register_config_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register configuration-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.config import get_config

    def load_config() -> None:
        """Load configuration from environment variables and .env file."""
        config = get_config()
        config.load()
        logger.info("Configuration loaded")

    manager.register_initialise_hook(
        name="load_config",
        callback=load_config,
        priority=10  # Load configuration early in the initialisation process
    )

    logger.debug("Registered configuration lifecycle hooks")


def register_logging_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register logging-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.config import get_config
    from bot.core.logging import setup_logging

    def configure_logging() -> None:
        """Configure logging based on configuration."""
        config = get_config()
        log_level = config.get("log_level", "INFO")
        log_file = config.get("log_file", None)

        setup_logging(
            level=log_level,
            log_file=log_file,
            console=True,
            file_rotation=True
        )

        logger.info(f"Logging configured with level: {log_level}")

    manager.register_initialise_hook(
        name="configure_logging",
        callback=configure_logging,
        priority=20  # Configure logging after configuration is loaded
    )

    logger.debug("Registered logging lifecycle hooks")


def register_error_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register error-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.errors import register_default_handlers

    def setup_error_handling() -> None:
        """Set up error handling."""
        register_default_handlers()
        logger.info("Error handling configured")

    manager.register_initialise_hook(
        name="setup_error_handling",
        callback=setup_error_handling,
        priority=30  # Set up error handling after logging is configured
    )

    logger.debug("Registered error lifecycle hooks")


def register_database_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register database-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.config import get_config

    def initialise_database() -> None:
        """Initialise the database connection."""
        config = get_config()
        if config.get_bool("db_enabled", False):
            try:
                # Importing here to avoid unnecessary imports if database is disabled
                from bot.db.connection import initialise_db_connection
                initialise_db_connection()
                logger.info("Database connection initialised")
            except ImportError:
                logger.warning("Database module not available")
        else:
            logger.info("Database disabled, skipping initialisation")

    def close_database() -> None:
        """Close the database connection."""
        config = get_config()
        if config.get_bool("db_enabled", False):
            try:
                # Importing here to avoid unnecessary imports if database is disabled
                from bot.db.connection import close_db_connection
                close_db_connection()
                logger.info("Database connection closed")
            except ImportError:
                logger.warning("Database module not available")
        else:
            logger.info("Database disabled, skipping shutdown")

    manager.register_initialise_hook(
        name="initialise_database",
        callback=initialise_database,
        priority=40  # Initialise database after configuration, logging, and error handling
    )

    manager.register_shutdown_hook(
        name="close_database",
        callback=close_database,
        priority=20  # Close database early in the shutdown process
    )

    logger.debug("Registered database lifecycle hooks")


def register_platform_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register platform-related lifecycle hooks.

    Initialises and shuts down platform connections (Twitch, OBS, Discord).

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.config import get_config

    def initialise_twitch() -> None:
        """Initialise the Twitch platform."""
        config = get_config()
        try:
            # Importing here to avoid unnecessary imports if platform is not used
            from bot.platforms.twitch import initialise_twitch_client

            bot_nick = config.get("bot_nick", required=True)
            channel = config.get("channel", required=True)
            tmi_token = config.get("tmi_token", required=True)
            client_id = config.get("client_id", required=True)

            initialise_twitch_client(
                bot_nick=bot_nick,
                channel=channel,
                tmi_token=tmi_token,
                client_id=client_id
            )

            logger.info("Twitch platform initialised")
        except ImportError:
            logger.warning("Twitch module not available")
        except Exception as e:
            logger.error(
                f"Error initialising Twitch platform: {str(e)}", exc_info=True)

    def initialise_obs() -> None:
        """Initialise the OBS platform."""
        config = get_config()
        if config.get_bool("obs_enabled", False):
            try:
                # Importing here to avoid unnecessary imports if platform is disabled
                from bot.platforms.obs import initialise_obs_client

                obs_host = config.get("obs_host", "localhost")
                obs_port = config.get_int("obs_port", 4455)
                obs_password = config.get("obs_password", "")

                initialise_obs_client(
                    host=obs_host,
                    port=obs_port,
                    password=obs_password
                )

                logger.info("OBS platform initialised")
            except ImportError:
                logger.warning("OBS module not available")
            except Exception as e:
                logger.error(
                    f"Error initialising OBS platform: {str(e)}", exc_info=True)
        else:
            logger.info("OBS platform disabled, skipping initialisation")

    def initialise_discord() -> None:
        """Initialise the Discord platform."""
        config = get_config()
        if config.get_bool("discord_enabled", False):
            try:
                # Importing here to avoid unnecessary imports if platform is disabled
                from bot.platforms.discord import initialise_discord_client

                discord_token = config.get("discord_token", "")
                discord_channel_id = config.get("discord_channel_id", "")

                if discord_token and discord_channel_id:
                    initialise_discord_client(
                        token=discord_token,
                        channel_id=discord_channel_id
                    )

                    logger.info("Discord platform initialised")
                else:
                    logger.warning(
                        "Discord platform enabled but token or channel ID missing")
            except ImportError:
                logger.warning("Discord module not available")
            except Exception as e:
                logger.error(
                    f"Error initialising Discord platform: {str(e)}", exc_info=True)
        else:
            logger.info("Discord platform disabled, skipping initialisation")

    def shutdown_platforms() -> None:
        """Shutdown all platform connections."""
        config = get_config()

        # Shutdown Twitch
        try:
            from bot.platforms.twitch import shutdown_twitch_client
            shutdown_twitch_client()
            logger.info("Twitch platform shutdown complete")
        except ImportError:
            logger.debug("Twitch module not available for shutdown")
        except Exception as e:
            logger.error(
                f"Error shutting down Twitch platform: {str(e)}", exc_info=True)

        # Shutdown OBS if enabled
        if config.get_bool("obs_enabled", False):
            try:
                from bot.platforms.obs import shutdown_obs_client
                shutdown_obs_client()
                logger.info("OBS platform shutdown complete")
            except ImportError:
                logger.debug("OBS module not available for shutdown")
            except Exception as e:
                logger.error(
                    f"Error shutting down OBS platform: {str(e)}", exc_info=True)

        # Shutdown Discord if enabled
        if config.get_bool("discord_enabled", False):
            try:
                from bot.platforms.discord import shutdown_discord_client
                shutdown_discord_client()
                logger.info("Discord platform shutdown complete")
            except ImportError:
                logger.debug("Discord module not available for shutdown")
            except Exception as e:
                logger.error(
                    f"Error shutting down Discord platform: {str(e)}", exc_info=True)

    # Register initialisation hooks
    manager.register_initialise_hook(
        name="initialise_twitch",
        callback=initialise_twitch,
        priority=50  # Initialise Twitch after database
    )

    manager.register_initialise_hook(
        name="initialise_obs",
        callback=initialise_obs,
        priority=51  # Initialise OBS after Twitch
    )

    manager.register_initialise_hook(
        name="initialise_discord",
        callback=initialise_discord,
        priority=52  # Initialise Discord after OBS
    )

    # Register shutdown hooks
    manager.register_shutdown_hook(
        name="shutdown_platforms",
        callback=shutdown_platforms,
        priority=10  # Shutdown platforms before database
    )

    logger.debug("Registered platform lifecycle hooks")


def register_command_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register command-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    def initialise_commands() -> None:
        """Initialise the command handler and register commands."""
        try:
            # Importing here to avoid circular imports
            from bot.commands import initialise_command_handler
            initialise_command_handler()
            logger.info("Command handler initialised")
        except ImportError:
            logger.warning("Command module not available")
        except Exception as e:
            logger.error(
                f"Error initialising command handler: {str(e)}", exc_info=True)

    manager.register_initialise_hook(
        name="initialise_commands",
        callback=initialise_commands,
        priority=60  # Initialise commands after platforms
    )

    logger.debug("Registered command lifecycle hooks")


def register_feature_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register feature-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    # Import here to avoid circular imports
    from bot.core.config import get_config
    from bot.core.constants import FEATURES

    def initialise_features() -> None:
        """Initialise enabled features."""
        try:
            # Importing here to avoid circular imports
            from bot.features import initialise_feature_manager, enable_feature

            config = get_config()
            initialise_feature_manager()

            # Enable features based on configuration
            for feature in FEATURES:
                feature_enabled = config.get_bool(f"{feature}_enabled", False)
                if feature_enabled:
                    try:
                        enable_feature(feature)
                        logger.info(f"Feature enabled: {feature}")
                    except Exception as e:
                        logger.error(
                            f"Error enabling feature {feature}: {str(e)}", exc_info=True)
                else:
                    logger.debug(f"Feature disabled: {feature}")

            logger.info("Features initialised")
        except ImportError:
            logger.warning("Features module not available")
        except Exception as e:
            logger.error(
                f"Error initialising features: {str(e)}", exc_info=True)

    def shutdown_features() -> None:
        """Shutdown all active features."""
        try:
            # Importing here to avoid circular imports
            from bot.features import shutdown_feature_manager
            shutdown_feature_manager()
            logger.info("Features shutdown complete")
        except ImportError:
            logger.debug("Features module not available for shutdown")
        except Exception as e:
            logger.error(
                f"Error shutting down features: {str(e)}", exc_info=True)

    manager.register_initialise_hook(
        name="initialise_features",
        callback=initialise_features,
        priority=70  # Initialise features after commands
    )

    manager.register_shutdown_hook(
        name="shutdown_features",
        callback=shutdown_features,
        priority=5  # Shutdown features before platforms
    )

    logger.debug("Registered feature lifecycle hooks")


def register_all_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register all lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    register_config_hooks(manager)
    register_logging_hooks(manager)
    register_error_hooks(manager)
    register_database_hooks(manager)
    register_platform_hooks(manager)
    register_command_hooks(manager)
    register_feature_hooks(manager)

    logger.info("All lifecycle hooks registered")
