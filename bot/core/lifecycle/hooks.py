"""
Lifecycle hooks for the bot.

This module provides predefined lifecycle hooks for the application.
"""

import importlib
import logging
import sys
from enum import Enum, auto
from typing import Callable, Dict, List, Optional, Set, Tuple, Any, Union, Type

from bot.core.lifecycle.manager import LifecycleManager, get_lifecycle_manager

# Set up logger for this module
logger = logging.getLogger(__name__)


class HookType(Enum):
    """Types of lifecycle hooks."""
    INITIALISE = auto()
    START = auto()
    STOP = auto()
    SHUTDOWN = auto()
    ERROR = auto()


class HookDependency:
    """Defines a dependency between hooks."""

    def __init__(self, hook_name: str, hook_type: HookType = HookType.INITIALISE):
        """
        Initialize a hook dependency.

        Args:
            hook_name (str): Name of the hook that is required.
            hook_type (HookType): Type of the hook.
        """
        self.hook_name = hook_name
        self.hook_type = hook_type


# Registry to track registered hooks for dependency resolution
_registered_hooks: Dict[HookType, Set[str]] = {
    hook_type: set() for hook_type in HookType
}

# Initialisation sequence tracking
_initialised_modules: Set[str] = set()


def _import_module_safely(module_path: str) -> Optional[Any]:
    """
    Import a module safely, handling ImportError and other exceptions.

    Args:
        module_path (str): Dot-notation path to the module to import.

    Returns:
        Optional[Any]: The imported module, or None if import failed.
    """
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        logger.warning(f"Module {module_path} not available: {str(e)}")
        return None
    except Exception as e:
        logger.error(
            f"Error importing module {module_path}: {str(e)}", exc_info=True)
        return None


def _validate_hook_dependencies(
    hook_name: str,
    hook_type: HookType,
    dependencies: List[HookDependency] = None
) -> bool:
    """
    Validate that all dependencies for a hook are satisfied.

    Args:
        hook_name (str): Name of the hook.
        hook_type (HookType): Type of the hook.
        dependencies (List[HookDependency]): List of dependencies.

    Returns:
        bool: True if all dependencies are satisfied, False otherwise.
    """
    if not dependencies:
        return True

    for dependency in dependencies:
        if dependency.hook_name not in _registered_hooks[dependency.hook_type]:
            logger.warning(
                f"Hook {hook_name} depends on {dependency.hook_name} "
                f"(type: {dependency.hook_type.name}), which is not registered."
            )
            return False

    return True


def register_hook(
    manager: Optional[LifecycleManager] = None,
    name: str = None,
    callback: Callable[[], None] = None,
    hook_type: HookType = HookType.INITIALISE,
    priority: int = 100,
    dependencies: List[HookDependency] = None,
    condition: Optional[Callable[[], bool]] = None
) -> bool:
    """
    Register a lifecycle hook with dependency and condition checking.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register with.
        name (str): Name of the hook.
        callback (Callable[[], None]): Hook callback function.
        hook_type (HookType): Type of the hook.
        priority (int): Priority (lower values execute first).
        dependencies (List[HookDependency]): List of hook dependencies.
        condition (Optional[Callable[[], bool]]): Optional condition that must be True
                                                for the hook to be registered.

    Returns:
        bool: True if the hook was registered, False otherwise.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    if condition is not None and not condition():
        logger.debug(f"Hook {name} not registered due to condition")
        return False

    if not _validate_hook_dependencies(name, hook_type, dependencies):
        logger.warning(f"Hook {name} not registered due to unmet dependencies")
        return False

    # Register the hook with the appropriate method
    if hook_type == HookType.INITIALISE:
        manager.register_initialise_hook(
            name=name, callback=callback, priority=priority)
    elif hook_type == HookType.START:
        manager.register_start_hook(
            name=name, callback=callback, priority=priority)
    elif hook_type == HookType.STOP:
        manager.register_stop_hook(
            name=name, callback=callback, priority=priority)
    elif hook_type == HookType.SHUTDOWN:
        manager.register_shutdown_hook(
            name=name, callback=callback, priority=priority)
    elif hook_type == HookType.ERROR:
        manager.register_error_hook(
            name=name, callback=callback, priority=priority)
    else:
        logger.error(f"Unknown hook type: {hook_type}")
        return False

    # Add to registry for dependency tracking
    _registered_hooks[hook_type].add(name)

    return True


def mark_initialised(module_name: str) -> None:
    """
    Mark a module as successfully initialised.

    Args:
        module_name (str): Name of the module.
    """
    _initialised_modules.add(module_name)
    logger.debug(f"Module {module_name} marked as initialised")


def is_initialised(module_name: str) -> bool:
    """
    Check if a module was successfully initialised.

    Args:
        module_name (str): Name of the module.

    Returns:
        bool: True if the module was initialised, False otherwise.
    """
    return module_name in _initialised_modules


def register_config_hooks(manager: Optional[LifecycleManager] = None) -> None:
    """
    Register configuration-related lifecycle hooks.

    Args:
        manager (Optional[LifecycleManager]): Lifecycle manager to register hooks with.
            If None, uses the singleton instance.
    """
    if manager is None:
        manager = get_lifecycle_manager()

    def load_config() -> None:
        """Load configuration from environment variables and .env file."""
        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if config_module:
            config = config_module.get_config()
            try:
                config.load()
                logger.info("Configuration loaded")
                mark_initialised("config")
            except Exception as e:
                logger.error(
                    f"Error loading configuration: {str(e)}", exc_info=True)
                raise

    register_hook(
        manager=manager,
        name="load_config",
        callback=load_config,
        hook_type=HookType.INITIALISE,
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

    def configure_logging() -> None:
        """Configure logging based on configuration."""
        # Make sure config is initialised first
        if not is_initialised("config"):
            logger.warning(
                "Configuration not initialised, logging may not be properly configured")

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        logging_module = _import_module_safely("bot.core.logging")

        if not config_module or not logging_module:
            logger.error("Cannot configure logging due to missing modules")
            return

        config = config_module.get_config()
        setup_logging = logging_module.setup_logging

        try:
            log_level = config.get("log_level", "INFO")
            log_file = config.get("log_file", None)

            setup_logging(
                level=log_level,
                log_file=log_file,
                console=True,
                file_rotation=True
            )

            logger.info(f"Logging configured with level: {log_level}")
            mark_initialised("logging")
        except Exception as e:
            logger.error(f"Error configuring logging: {str(e)}", exc_info=True)

    register_hook(
        manager=manager,
        name="configure_logging",
        callback=configure_logging,
        hook_type=HookType.INITIALISE,
        priority=20,  # Configure logging after configuration is loaded
        dependencies=[HookDependency("load_config")]
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

    def setup_error_handling() -> None:
        """Set up error handling."""
        # Import here to avoid circular imports
        errors_module = _import_module_safely("bot.core.errors")
        if not errors_module:
            logger.error("Cannot set up error handling due to missing module")
            return

        try:
            errors_module.register_default_handlers()
            logger.info("Error handling configured")
            mark_initialised("error_handling")
        except Exception as e:
            logger.error(
                f"Error setting up error handling: {str(e)}", exc_info=True)

    register_hook(
        manager=manager,
        name="setup_error_handling",
        callback=setup_error_handling,
        hook_type=HookType.INITIALISE,
        priority=30,  # Set up error handling after logging is configured
        dependencies=[HookDependency("configure_logging")]
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

    def initialise_database() -> None:
        """Initialise the database connection."""
        # Make sure config is initialised first
        if not is_initialised("config"):
            logger.warning(
                "Configuration not initialised, skipping database initialisation")
            return

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if not config_module:
            logger.error(
                "Cannot initialise database due to missing config module")
            return

        config = config_module.get_config()

        if not config.get_bool("db_enabled", False):
            logger.info("Database disabled, skipping initialisation")
            return

        try:
            # Importing here to avoid unnecessary imports if database is disabled
            db_module = _import_module_safely("bot.db.connection")
            if not db_module:
                logger.warning("Database module not available")
                return

            db_module.initialise_db_connection()
            logger.info("Database connection initialised")
            mark_initialised("database")
        except Exception as e:
            logger.error(
                f"Error initialising database connection: {str(e)}", exc_info=True)

    def close_database() -> None:
        """Close the database connection."""
        # Skip if database was never initialised
        if not is_initialised("database"):
            logger.info("Database was not initialised, skipping shutdown")
            return

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if not config_module:
            logger.error(
                "Cannot shut down database due to missing config module")
            return

        config = config_module.get_config()

        if not config.get_bool("db_enabled", False):
            logger.info("Database disabled, skipping shutdown")
            return

        try:
            # Importing here to avoid unnecessary imports if database is disabled
            db_module = _import_module_safely("bot.db.connection")
            if not db_module:
                logger.warning("Database module not available for shutdown")
                return

            db_module.close_db_connection()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(
                f"Error closing database connection: {str(e)}", exc_info=True)

    register_hook(
        manager=manager,
        name="initialise_database",
        callback=initialise_database,
        hook_type=HookType.INITIALISE,
        priority=40,  # Initialise database after configuration, logging, and error handling
        dependencies=[
            HookDependency("load_config"),
            HookDependency("configure_logging"),
            HookDependency("setup_error_handling")
        ]
    )

    register_hook(
        manager=manager,
        name="close_database",
        callback=close_database,
        hook_type=HookType.SHUTDOWN,
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

    def initialise_twitch() -> None:
        """Initialise the Twitch platform."""
        # Make sure config is initialised first
        if not is_initialised("config"):
            logger.warning(
                "Configuration not initialised, skipping Twitch initialisation")
            return

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if not config_module:
            logger.error(
                "Cannot initialise Twitch due to missing config module")
            return

        config = config_module.get_config()

        try:
            # Verify required configuration values
            required_configs = ['bot_nick',
                                'channel', 'tmi_token', 'client_id']
            missing_configs = [
                key for key in required_configs if not config.get(key, None)]

            if missing_configs:
                logger.error(
                    f"Missing required Twitch configuration: {', '.join(missing_configs)}")
                return

            # Importing here to avoid unnecessary imports if platform is not used
            twitch_module = _import_module_safely("bot.platforms.twitch")
            if not twitch_module:
                logger.warning("Twitch module not available")
                return

            bot_nick = config.get("bot_nick")
            channel = config.get("channel")
            tmi_token = config.get("tmi_token")
            client_id = config.get("client_id")

            twitch_module.initialise_twitch_client(
                bot_nick=bot_nick,
                channel=channel,
                tmi_token=tmi_token,
                client_id=client_id
            )

            logger.info("Twitch platform initialised")
            mark_initialised("twitch")
        except Exception as e:
            logger.error(
                f"Error initialising Twitch platform: {str(e)}", exc_info=True)

    def initialise_obs() -> None:
        """Initialise the OBS platform."""
        # Make sure config is initialised first
        if not is_initialised("config"):
            logger.warning(
                "Configuration not initialised, skipping OBS initialisation")
            return

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if not config_module:
            logger.error("Cannot initialise OBS due to missing config module")
            return

        config = config_module.get_config()

        if not config.get_bool("obs_enabled", False):
            logger.info("OBS platform disabled, skipping initialisation")
            return

        try:
            # Verify required configuration values
            obs_host = config.get("obs_host", "localhost")
            obs_port = config.get_int("obs_port", 4455)
            obs_password = config.get("obs_password", "")

            # Importing here to avoid unnecessary imports if platform is disabled
            obs_module = _import_module_safely("bot.platforms.obs")
            if not obs_module:
                logger.warning("OBS module not available")
                return

            obs_module.initialise_obs_client(
                host=obs_host,
                port=obs_port,
                password=obs_password
            )

            logger.info("OBS platform initialised")
            mark_initialised("obs")
        except Exception as e:
            logger.error(
                f"Error initialising OBS platform: {str(e)}", exc_info=True)

    def initialise_discord() -> None:
        """Initialise the Discord platform."""
        # Make sure config is initialised first
        if not is_initialised("config"):
            logger.warning(
                "Configuration not initialised, skipping Discord initialisation")
            return

        # Import here to avoid circular imports
        config_module = _import_module_safely("bot.core.config")
        if not config_module:
            logger.error(
                "Cannot initialise Discord due to missing config module")
            return

        config = config_module.get_config()

        if not config.get_bool("discord_enabled", False):
            logger.info("Discord platform disabled, skipping initialisation")
            return

        try:
            # Importing here to avoid unnecessary imports if platform is disabled
            discord_module = _import_module_safely("bot.platforms.discord")
            if not discord_module:
                logger.warning("Discord module not available")
                return

            discord_token = config.get("discord_token", "")
            discord_channel_id = config.get("discord_channel_id", "")

            if not discord_token or not discord_channel_id:
                logger.warning(
                    "Discord platform enabled but token or channel ID missing")
                return

            discord_module.initialise_discord_client(
                token=discord_token,
                channel_id=discord_channel_id
            )

            logger.info("Discord platform initialised")
            mark_initialised("discord")
        except Exception as e:
            logger.error(
                f"Error initialising Discord platform: {str(e)}", exc_info=True)

    def shutdown_platforms() -> None:
        """Shutdown all platform connections."""
        # Shutdown Twitch if it was initialised
        if is_initialised("twitch"):
            try:
                twitch_module = _import_module_safely("bot.platforms.twitch")
                if twitch_module:
                    twitch_module.shutdown_twitch_client()
                    logger.info("Twitch platform shutdown complete")
            except Exception as e:
                logger.error(
                    f"Error shutting down Twitch platform: {str(e)}", exc_info=True)

        # Shutdown OBS if it was initialised
        if is_initialised("obs"):
            try:
                obs_module = _import_module_safely("bot.platforms.obs")
                if obs_module:
                    obs_module.shutdown_obs_client()
                    logger.info("OBS platform shutdown complete")
            except Exception as e:
                logger.error(
                    f"Error shutting down OBS platform: {str(e)}", exc_info=True)

        # Shutdown Discord if it was initialised
        if is_initialised("discord"):
            try:
                discord_module = _import_module_safely("bot.platforms.discord")
                if discord_module:
                    discord_module.shutdown_discord_client()
                    logger.info("Discord platform shutdown complete")
            except Exception as e:
                logger.error(
                    f"Error shutting down Discord platform: {str(e)}", exc_info=True)

    # Register initialisation hooks
    register_hook(
        manager=manager,
        name="initialise_twitch",
        callback=initialise_twitch,
        hook_type=HookType.INITIALISE,
        priority=50,  # Initialise Twitch after database
        dependencies=[
            HookDependency("load_config"),
            HookDependency("configure_logging")
        ]
    )

    register_hook(
        manager=manager,
        name="initialise_obs",
        callback=initialise_obs,
        hook_type=HookType.INITIALISE,
        priority=51,  # Initialise OBS after Twitch
        dependencies=[
            HookDependency("load_config"),
            HookDependency("configure_logging")
        ],
        condition=lambda: get_lifecycle_manager().config.get_bool(
            "obs_enabled", False) if hasattr(get_lifecycle_manager(), "config") else False
    )

    register_hook(
        manager=manager,
        name="initialise_discord",
        callback=initialise_discord,
        hook_type=HookType.INITIALISE,
        priority=52,  # Initialise Discord after OBS
        dependencies=[
            HookDependency("load_config"),
            HookDependency("configure_logging")
        ],
        condition=lambda: get_lifecycle_manager().config.get_bool(
            "discord_enabled", False) if hasattr(get_lifecycle_manager(), "config") else False
    )

    # Register shutdown hook
    register_hook(
        manager=manager,
        name="shutdown_platforms",
        callback=shutdown_platforms,
        hook_type=HookType.SHUTDOWN,
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
            commands_module = _import_module_safely("bot.commands")
            if not commands_module:
                logger.warning("Command module not available")
                return

            commands_module.initialise_command_handler()
            logger.info("Command handler initialised")
            mark_initialised("commands")
        except Exception as e:
            logger.error(
                f"Error initialising command handler: {str(e)}", exc_info=True)

    register_hook(
        manager=manager,
        name="initialise_commands",
        callback=initialise_commands,
        hook_type=HookType.INITIALISE,
        priority=60,  # Initialise commands after platforms
        dependencies=[
            HookDependency("initialise_twitch")
        ]
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
    try:
        from bot.core.constants import FEATURES
    except ImportError:
        logger.warning("Cannot import FEATURES from bot.core.constants")
        FEATURES = []

    def initialise_features() -> None:
        """Initialise enabled features."""
        # Make sure commands are initialised first
        if not is_initialised("commands"):
            logger.warning(
                "Commands not initialised, skipping feature initialisation")
            return

        try:
            # Importing here to avoid circular imports
            features_module = _import_module_safely("bot.features")
            if not features_module:
                logger.warning("Features module not available")
                return

            config_module = _import_module_safely("bot.core.config")
            if not config_module:
                logger.error(
                    "Cannot initialise features due to missing config module")
                return

            config = config_module.get_config()
            features_module.initialise_feature_manager()

            # Enable features based on configuration
            for feature in FEATURES:
                feature_enabled = config.get_bool(f"{feature}_enabled", False)
                if feature_enabled:
                    try:
                        features_module.enable_feature(feature)
                        logger.info(f"Feature enabled: {feature}")
                        mark_initialised(f"feature:{feature}")
                    except Exception as e:
                        logger.error(
                            f"Error enabling feature {feature}: {str(e)}", exc_info=True)
                else:
                    logger.debug(f"Feature disabled: {feature}")

            logger.info("Features initialised")
            mark_initialised("features")
        except Exception as e:
            logger.error(
                f"Error initialising features: {str(e)}", exc_info=True)

    def shutdown_features() -> None:
        """Shutdown all active features."""
        # Skip if features were never initialised
        if not is_initialised("features"):
            logger.info("Features were not initialised, skipping shutdown")
            return

        try:
            # Importing here to avoid circular imports
            features_module = _import_module_safely("bot.features")
            if not features_module:
                logger.warning("Features module not available for shutdown")
                return

            features_module.shutdown_feature_manager()
            logger.info("Features shutdown complete")
        except Exception as e:
            logger.error(
                f"Error shutting down features: {str(e)}", exc_info=True)

    register_hook(
        manager=manager,
        name="initialise_features",
        callback=initialise_features,
        hook_type=HookType.INITIALISE,
        priority=70,  # Initialise features after commands
        dependencies=[
            HookDependency("initialise_commands"),
            HookDependency("load_config")
        ]
    )

    register_hook(
        manager=manager,
        name="shutdown_features",
        callback=shutdown_features,
        hook_type=HookType.SHUTDOWN,
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
