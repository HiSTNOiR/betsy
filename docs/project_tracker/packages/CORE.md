# Core Package Structure and Components

The `core` package serves as the foundation of the Twitch bot application, containing essential components that power the entire system. This document outlines the structure and purpose of each module within the `core` package.

## Configuration Management
| Module | Function | Description |
|--------|----------|-------------|
| config/config.py | load_config | Load configuration from .env file |
| config/config.py | get_config | Get singleton configuration instance |
| config/config.py | Config.get | Get specific configuration value |
| config/config.py | Config.reload | Reload configuration from environment |
| config/config.py | Config._get_required_env | Get required environment variable |
| config/config.py | Config._get_env | Get environment variable with default |
| config/constants.py | BOT_VERSION | Bot version number |
| config/constants.py | MESSAGE_QUEUE_SIZE | Maximum size for message queue |
| config/constants.py | DEFAULT_COMMAND_PREFIX | Default prefix for commands |
| config/constants.py | MessagePriority | Enum for message priority levels |
| config/constants.py | DuelState | Enum for duel states |
| config/constants.py | ItemType | Enum for item types |
| config/constants.py | ERROR_MESSAGES | Dictionary of error message templates |
| config/constants.py | SUCCESS_MESSAGES | Dictionary of success message templates |
| config/environment.py | is_development | Check if running in development environment |
| config/environment.py | is_production | Check if running in production environment |
| config/environment.py | is_testing | Check if running in testing environment |
| config/environment.py | get_environment | Get current environment name |

## Error Handling
| Module | Function | Description |
|--------|----------|-------------|
| errors.py | BotError | Base exception for all bot-related errors |
| errors.py | ConfigError | Exception for configuration errors |
| errors.py | DatabaseError | Exception for database errors |
| errors.py | TwitchError | Exception for Twitch API errors |
| errors.py | OBSError | Exception for OBS WebSocket errors |
| errors.py | PermissionError | Exception for permission-related errors |
| errors.py | CommandError | Exception for command-related errors |
| errors.py | ValidationError | Exception for validation errors |
| errors.py | ThrottlingError | Exception for throttling-related errors |
| errors.py | CooldownError | Exception for cooldown-related errors |
| errors.py | FeatureDisabledError | Exception when feature is disabled |
| errors.py | ItemNotFoundError | Exception when item is not found |
| errors.py | handle_error | Global error handler function |
| errors.py | format_exception | Format exception with traceback for logging |

## Logging System
| Module | Function | Description |
|--------|----------|-------------|
| logging.py | setup_logging | Set up logging configuration |
| logging.py | get_logger | Get logger instance for module |
| logging.py | LoggingContext | Context manager for temporarily changing log level |
| logging.py | set_debug_mode | Enable or disable debug mode logging |
| logging.py | rotate_logs | Rotate log files based on size or time |
| logging.py | clean_old_logs | Remove log files older than specified days |
| logging.py | log_exception | Log exception with full traceback |
| logging.py | log_command | Log command execution with sanitised arguments |
| logging.py | log_event | Log event occurrence |
| logging.py | configure_file_logging | Configure file-based logging |
| logging.py | configure_console_logging | Configure console-based logging |

## Bot Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_bot | Initialise bot components |
| initialisation.py | load_features | Load enabled features |
| initialisation.py | setup_database | Set up database connection |
| initialisation.py | connect_platforms | Connect to Twitch and OBS |
| initialisation.py | register_commands | Register command handlers |
| initialisation.py | register_events | Register event handlers |
| initialisation.py | verify_environment | Verify environment configuration |
| initialisation.py | check_dependencies | Check required dependencies |
| initialisation.py | initialise_state | Initialise application state |

## Application State Management
| Module | Function | Description |
|--------|----------|-------------|
| state.py | BotState | Singleton class for global application state |
| state.py | get_state | Get singleton state instance |
| state.py | BotState.set | Set state value |
| state.py | BotState.get | Get state value |
| state.py | BotState.delete | Delete state value |
| state.py | BotState.clear | Clear all state values |
| state.py | BotState.has | Check if state has value |
| state.py | StatefulMixin | Mixin for stateful classes |
| state.py | create_namespace | Create isolated state namespace |
| state.py | load_persistent_state | Load persistent state from storage |
| state.py | save_persistent_state | Save persistent state to storage |

## Command Framework
| Module | Function | Description |
|--------|----------|-------------|
| commands/base.py | Command | Base class for all commands |
| commands/base.py | Command.execute | Execute command with given context |
| commands/base.py | Command.can_execute | Check if command can be executed |
| commands/base.py | Command.get_help | Get help text for command |
| commands/base.py | Command.get_usage | Get usage instructions for command |
| commands/base.py | CommandContext | Context object for command execution |
| commands/registry.py | CommandRegistry | Registry for all commands |
| commands/registry.py | register_command | Register command with registry |
| commands/registry.py | get_command | Get command by name |
| commands/registry.py | get_all_commands | Get all registered commands |
| commands/registry.py | get_commands_for_user | Get commands available to user |
| commands/handler.py | handle_command | Handle command from message |
| commands/handler.py | parse_command | Parse command from message |
| commands/handler.py | execute_command | Execute command with arguments |
| commands/handler.py | get_command_help | Get help for command |

## Event System
| Module | Function | Description |
|--------|----------|-------------|
| events/base.py | Event | Base class for all events |
| events/base.py | EventData | Data container for event data |
| events/base.py | EventListener | Interface for event listeners |
| events/base.py | EventHandler | Handler for event callbacks |
| events/registry.py | EventRegistry | Registry for event handlers |
| events/registry.py | register_event | Register event handler |
| events/registry.py | unregister_event | Unregister event handler |
| events/registry.py | get_handlers | Get handlers for event type |
| events/dispatcher.py | EventDispatcher | Dispatches events to handlers |
| events/dispatcher.py | dispatch_event | Dispatch event to registered handlers |
| events/types.py | ChatMessageEvent | Event for chat messages |
| events/types.py | BitsEvent | Event for bits donations |
| events/types.py | RewardEvent | Event for channel point redemptions |
| events/types.py | SubscriptionEvent | Event for subscriptions |
| events/types.py | FollowEvent | Event for new followers |
| events/types.py | StreamEvent | Event for stream state changes |

## Feature Management
| Module | Function | Description |
|--------|----------|-------------|
| features/base.py | Feature | Base class for all features |
| features/base.py | Feature.initialise | Initialise feature |
| features/base.py | Feature.shutdown | Shut down feature |
| features/base.py | Feature.is_enabled | Check if feature is enabled |
| features/base.py | Feature.get_commands | Get commands provided by feature |
| features/base.py | Feature.get_event_handlers | Get event handlers for feature |
| features/registry.py | FeatureRegistry | Registry for all features |
| features/registry.py | register_feature | Register feature with registry |
| features/registry.py | get_feature | Get feature by name |
| features/registry.py | get_all_features | Get all registered features |
| features/registry.py | get_enabled_features | Get all enabled features |
| features/loader.py | load_feature | Load feature by name |
| features/loader.py | unload_feature | Unload feature by name |
| features/loader.py | reload_feature | Reload feature by name |
| features/loader.py | discover_features | Discover available features |

## Bot Management
| Module | Function | Description |
|--------|----------|-------------|
| bot.py | Bot | Main bot class |
| bot.py | Bot.start | Start the bot |
| bot.py | Bot.stop | Stop the bot |
| bot.py | Bot.restart | Restart the bot |
| bot.py | Bot.handle_message | Handle incoming message |
| bot.py | Bot.send_message | Send message to chat |
| bot.py | Bot.handle_event | Handle event from platform |
| bot.py | Bot.register_command | Register command handler |
| bot.py | Bot.register_event_handler | Register event handler |
| bot.py | Bot.load_feature | Load feature dynamically |
| bot.py | Bot.unload_feature | Unload feature dynamically |
| bot.py | Bot.reload_feature | Reload feature dynamically |
| bot.py | Bot.get_user | Get user from database |
| bot.py | Bot.check_permissions | Check user permissions |

## Service Container
| Module | Function | Description |
|--------|----------|-------------|
| services/container.py | ServiceContainer | Container for service instances |
| services/container.py | register_service | Register service with container |
| services/container.py | get_service | Get service instance |
| services/container.py | has_service | Check if service is registered |
| services/container.py | initialise_services | Initialise all registered services |
| services/container.py | shutdown_services | Shut down all registered services |
| services/base.py | Service | Base class for all services |
| services/base.py | Service.initialise | Initialise service |
| services/base.py | Service.shutdown | Shut down service |
| services/base.py | ServiceDependency | Decorator for service dependencies |
| services/providers.py | ServiceProvider | Interface for service providers |
| services/providers.py | DatabaseServiceProvider | Provider for database service |
| services/providers.py | TwitchServiceProvider | Provider for Twitch service |
| services/providers.py | OBSServiceProvider | Provider for OBS service |

## Platform Integration Framework
| Module | Function | Description |
|--------|----------|-------------|
| platforms/base.py | Platform | Base class for platform integrations |
| platforms/base.py | Platform.connect | Connect to platform |
| platforms/base.py | Platform.disconnect | Disconnect from platform |
| platforms/base.py | Platform.is_connected | Check if platform is connected |
| platforms/base.py | Platform.send_message | Send message to platform |
| platforms/base.py | PlatformEvent | Base class for platform events |
| platforms/base.py | PlatformMessage | Base class for platform messages |
| platforms/registry.py | PlatformRegistry | Registry for platform integrations |
| platforms/registry.py | register_platform | Register platform with registry |
| platforms/registry.py | get_platform | Get platform by name |
| platforms/registry.py | get_all_platforms | Get all registered platforms |
| platforms/manager.py | PlatformManager | Manager for platform connections |
| platforms/manager.py | connect_all | Connect to all platforms |
| platforms/manager.py | disconnect_all | Disconnect from all platforms |
| platforms/manager.py | get_connection | Get connection to platform |

## Plugin System
| Module | Function | Description |
|--------|----------|-------------|
| plugins/base.py | Plugin | Base class for plugins |
| plugins/base.py | Plugin.initialise | Initialise plugin |
| plugins/base.py | Plugin.shutdown | Shut down plugin |
| plugins/base.py | Plugin.get_commands | Get commands provided by plugin |
| plugins/base.py | Plugin.get_event_handlers | Get event handlers for plugin |
| plugins/registry.py | PluginRegistry | Registry for all plugins |
| plugins/registry.py | register_plugin | Register plugin with registry |
| plugins/registry.py | get_plugin | Get plugin by name |
| plugins/registry.py | get_all_plugins | Get all registered plugins |
| plugins/loader.py | load_plugin | Load plugin by name |
| plugins/loader.py | unload_plugin | Unload plugin by name |
| plugins/loader.py | reload_plugin | Reload plugin by name |
| plugins/loader.py | discover_plugins | Discover available plugins |

## Validation Framework
| Module | Function | Description |
|--------|----------|-------------|
| validation/base.py | Validator | Base class for validators |
| validation/base.py | ValidationResult | Result of validation |
| validation/base.py | validate | Function to run validation |
| validation/validators.py | StringValidator | Validator for strings |
| validation/validators.py | NumberValidator | Validator for numbers |
| validation/validators.py | BooleanValidator | Validator for booleans |
| validation/validators.py | ListValidator | Validator for lists |
| validation/validators.py | DictionaryValidator | Validator for dictionaries |
| validation/validators.py | RegexValidator | Validator using regex |
| validation/validators.py | LengthValidator | Validator for string length |
| validation/validators.py | RangeValidator | Validator for numeric range |
| validation/registry.py | ValidatorRegistry | Registry for validators |
| validation/registry.py | register_validator | Register validator with registry |
| validation/registry.py | get_validator | Get validator by name |

## Health Monitoring
| Module | Function | Description |
|--------|----------|-------------|
| health/monitor.py | HealthMonitor | Monitor system health |
| health/monitor.py | check_health | Check overall system health |
| health/monitor.py | register_check | Register health check |
| health/monitor.py | unregister_check | Unregister health check |
| health/monitor.py | get_health_status | Get health status report |
| health/checks.py | database_check | Check database connectivity |
| health/checks.py | twitch_check | Check Twitch connectivity |
| health/checks.py | obs_check | Check OBS connectivity |
| health/checks.py | memory_usage_check | Check memory usage |
| health/checks.py | disk_space_check | Check disk space |
| health/status.py | HealthStatus | Status of health check |
| health/status.py | HealthSeverity | Severity of health status |

## Background Tasks
| Module | Function | Description |
|--------|----------|-------------|
| tasks/manager.py | TaskManager | Manager for background tasks |
| tasks/manager.py | schedule_task | Schedule task for execution |
| tasks/manager.py | cancel_task | Cancel scheduled task |
| tasks/manager.py | execute_task | Execute task immediately |
| tasks/manager.py | get_scheduled_tasks | Get all scheduled tasks |
| tasks/base.py | Task | Base class for background tasks |
| tasks/base.py | ScheduledTask | Representation of scheduled task |
| tasks/base.py | PeriodicTask | Task that runs periodically |
| tasks/base.py | TaskResult | Result of task execution |
| tasks/tasks.py | database_backup | Task for database backup |
| tasks/tasks.py | log_rotation | Task for log rotation |
| tasks/tasks.py | health_check | Task for health checking |

## Main Application Entry Point
| Module | Function | Description |
|--------|----------|-------------|
| main.py | main | Main entry point function |
| main.py | parse_args | Parse command line arguments |
| main.py | setup_environment | Set up application environment |
| main.py | create_bot | Create bot instance |
| main.py | run_bot | Run bot until interrupted |
| main.py | handle_shutdown | Handle graceful shutdown |
| main.py | version | Print version information |

## Security Framework
| Module | Function | Description |
|--------|----------|-------------|
| security/sanitisation.py | sanitise_input | Sanitise user input |
| security/sanitisation.py | sanitise_command | Sanitise command input |
| security/sanitisation.py | sanitise_path | Sanitise file path |
| security/authentication.py | authenticate | Authenticate user |
| security/authentication.py | verify_token | Verify authentication token |
| security/authentication.py | generate_token | Generate authentication token |
| security/authorisation.py | authorise | Authorise user for action |
| security/authorisation.py | check_permission | Check if user has permission |
| security/authorisation.py | get_user_permissions | Get permissions for user |