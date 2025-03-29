# Commands Package Structure and Components

The `commands` package provides the framework for defining, registering, and executing chat commands within the Twitch bot. It handles command parsing, validation, permissions, cooldowns, and execution within the application. This document outlines the structure and purpose of each module within the `commands` package.

## Command Base Framework
| Module | Function | Description |
|--------|----------|-------------|
| base.py | Command | Base class for all commands |
| base.py | Command.execute | Execute command with given context |
| base.py | Command.can_execute | Check if command can be executed |
| base.py | Command.get_help | Get help text for command |
| base.py | Command.get_usage | Get usage instruction for command |
| base.py | Command.get_aliases | Get command aliases |
| base.py | Command.has_permission | Check if user has permission to use command |
| base.py | Command.has_cooldown | Check if command is on cooldown |
| base.py | Command.get_cooldown | Get cooldown information for command |
| base.py | CommandGroup | Container for related commands |
| base.py | CommandGroup.add_command | Add sub-command to group |
| base.py | CommandGroup.remove_command | Remove sub-command from group |
| base.py | CommandGroup.get_commands | Get all sub-commands |

## Command Context
| Module | Function | Description |
|--------|----------|-------------|
| context.py | CommandContext | Context object for command execution |
| context.py | CommandContext.reply | Send reply to command sender |
| context.py | CommandContext.send | Send message to chat |
| context.py | CommandContext.get_args | Get command arguments |
| context.py | CommandContext.get_user | Get user who sent command |
| context.py | CommandContext.get_channel | Get channel where command was sent |
| context.py | CommandContext.get_platform | Get platform where command was sent |
| context.py | CommandContext.get_command | Get command being executed |
| context.py | CommandContext.is_broadcaster | Check if sender is broadcaster |
| context.py | CommandContext.is_moderator | Check if sender is moderator |
| context.py | CommandContext.is_vip | Check if sender is VIP |
| context.py | CommandContext.is_subscriber | Check if sender is subscriber |

## Command Registry
| Module | Function | Description |
|--------|----------|-------------|
| registry.py | CommandRegistry | Registry for all commands |
| registry.py | CommandRegistry.register | Register command with registry |
| registry.py | CommandRegistry.unregister | Unregister command from registry |
| registry.py | CommandRegistry.get_command | Get command by name |
| registry.py | CommandRegistry.get_all_commands | Get all registered commands |
| registry.py | CommandRegistry.get_commands_for_user | Get commands available to user |
| registry.py | CommandRegistry.get_commands_by_category | Get commands by category |
| registry.py | CommandRegistry.get_command_aliases | Get all registered aliases |
| registry.py | CommandRegistry.clear | Clear all registered commands |
| registry.py | get_registry | Get singleton registry instance |
| registry.py | register_command | Register command with global registry |
| registry.py | unregister_command | Unregister command from global registry |
| registry.py | get_command | Get command from global registry |

## Command Handler
| Module | Function | Description |
|--------|----------|-------------|
| handler.py | CommandHandler | Handles command dispatching from messages |
| handler.py | CommandHandler.handle_message | Parse message and handle command |
| handler.py | CommandHandler.execute_command | Execute command with parsed arguments |
| handler.py | CommandHandler.get_command | Get command by name or alias |
| handler.py | CommandHandler.register_command | Register command with handler |
| handler.py | CommandHandler.unregister_command | Unregister command from handler |
| handler.py | CommandHandler.register_middleware | Register command middleware |
| handler.py | CommandHandler.set_prefix | Set command prefix |
| handler.py | CommandHandler.get_prefix | Get command prefix |
| handler.py | get_handler | Get singleton handler instance |
| handler.py | handle_message | Handle message with global handler |
| handler.py | execute_command | Execute command with global handler |

## Command Parser
| Module | Function | Description |
|--------|----------|-------------|
| parser.py | CommandParser | Parse commands from messages |
| parser.py | CommandParser.parse | Parse message into command and arguments |
| parser.py | CommandParser.extract_command | Extract command name from message |
| parser.py | CommandParser.extract_arguments | Extract arguments from message |
| parser.py | CommandParser.split_arguments | Split argument string into arguments |
| parser.py | CommandParser.parse_quoted_arguments | Parse arguments with quotes |
| parser.py | CommandParser.is_command | Check if message is a command |
| parser.py | CommandParser.set_prefix | Set command prefix |
| parser.py | CommandParser.get_prefix | Get command prefix |
| parser.py | parse_command | Parse command with global parser |
| parser.py | extract_command_name | Extract command name with global parser |
| parser.py | is_command | Check if message is a command with global parser |

## Command Decorators
| Module | Function | Description |
|--------|----------|-------------|
| decorators.py | command | Decorator to create command |
| decorators.py | group | Decorator to create command group |
| decorators.py | cooldown | Decorator to add cooldown to command |
| decorators.py | permission | Decorator to add permission requirement |
| decorators.py | aliases | Decorator to add aliases to command |
| decorators.py | description | Decorator to add description to command |
| decorators.py | usage | Decorator to add usage information |
| decorators.py | category | Decorator to assign command to category |
| decorators.py | hidden | Decorator to mark command as hidden |
| decorators.py | before_command | Decorator for hook before command execution |
| decorators.py | after_command | Decorator for hook after command execution |
| decorators.py | error_handler | Decorator for command error handler |

## Argument Parsing
| Module | Function | Description |
|--------|----------|-------------|
| arguments.py | ArgumentParser | Parser for command arguments |
| arguments.py | ArgumentParser.add_argument | Add argument definition |
| arguments.py | ArgumentParser.parse_args | Parse arguments string |
| arguments.py | ArgumentParser.print_help | Get help text for arguments |
| arguments.py | Argument | Definition of command argument |
| arguments.py | Argument.validate | Validate argument value |
| arguments.py | Argument.convert | Convert argument to expected type |
| arguments.py | StringArgument | Argument for string values |
| arguments.py | IntegerArgument | Argument for integer values |
| arguments.py | FloatArgument | Argument for float values |
| arguments.py | BooleanArgument | Argument for boolean values |
| arguments.py | UserArgument | Argument for user references |
| arguments.py | RemainingArgument | Argument for remaining text |
| arguments.py | OptionalArgument | Wrapper for optional arguments |

## Command Permissions
| Module | Function | Description |
|--------|----------|-------------|
| permissions.py | PermissionLevel | Enum for permission levels |
| permissions.py | PermissionChecker | Check command permissions |
| permissions.py | PermissionChecker.check | Check if user has required permission |
| permissions.py | PermissionChecker.get_level | Get permission level for user |
| permissions.py | PermissionDeniedError | Error raised when permission denied |
| permissions.py | check_permission | Check permission with global checker |
| permissions.py | broadcaster_only | Permission checker for broadcaster |
| permissions.py | moderator_only | Permission checker for moderator or above |
| permissions.py | vip_only | Permission checker for VIP or above |
| permissions.py | subscriber_only | Permission checker for subscriber or above |
| permissions.py | permission_level | Permission checker for specific level |
| permissions.py | custom_permission | Permission checker with custom function |

## Command Cooldowns
| Module | Function | Description |
|--------|----------|-------------|
| cooldowns.py | CooldownManager | Manager for command cooldowns |
| cooldowns.py | CooldownManager.add_cooldown | Add cooldown for command/user |
| cooldowns.py | CooldownManager.check_cooldown | Check if command/user is on cooldown |
| cooldowns.py | CooldownManager.reset_cooldown | Reset cooldown for command/user |
| cooldowns.py | CooldownManager.get_remaining | Get remaining cooldown time |
| cooldowns.py | CooldownBucket | Container for cooldown state |
| cooldowns.py | CooldownBucket.update | Update bucket state |
| cooldowns.py | CooldownBucket.get_retry_after | Get time until cooldown expires |
| cooldowns.py | Cooldown | Cooldown definition |
| cooldowns.py | Cooldown.calculate_retry | Calculate retry time |
| cooldowns.py | BucketType | Enum for cooldown bucket types |
| cooldowns.py | CommandOnCooldownError | Error raised when command on cooldown |

## Command Errors
| Module | Function | Description |
|--------|----------|-------------|
| errors.py | CommandError | Base exception for command errors |
| errors.py | CommandNotFoundError | Error when command not found |
| errors.py | ArgumentParsingError | Error when parsing arguments |
| errors.py | MissingRequiredArgumentError | Error when required argument missing |
| errors.py | TooManyArgumentsError | Error when too many arguments provided |
| errors.py | InvalidArgumentError | Error when argument is invalid |
| errors.py | CommandExecutionError | Error during command execution |
| errors.py | PermissionDeniedError | Error when permission denied |
| errors.py | CommandOnCooldownError | Error when command on cooldown |
| errors.py | CommandDisabledError | Error when command is disabled |
| errors.py | handle_command_error | Handle command error with appropriate response |
| errors.py | format_error_message | Format error message for user |

## Built-In Commands
| Module | Function | Description |
|--------|----------|-------------|
| builtins/help.py | HelpCommand | Command to show help information |
| builtins/help.py | HelpCommand.execute | Execute help command |
| builtins/help.py | HelpCommand.get_command_help | Get help for specific command |
| builtins/help.py | HelpCommand.get_all_commands | Get list of all commands |
| builtins/help.py | format_command_help | Format help text for command |
| builtins/help.py | format_command_list | Format list of commands |
| builtins/admin.py | AdminCommandGroup | Group for admin commands |
| builtins/admin.py | EnableCommand | Command to enable other command |
| builtins/admin.py | DisableCommand | Command to disable other command |
| builtins/admin.py | ReloadCommand | Command to reload command or module |
| builtins/admin.py | ShutdownCommand | Command to shutdown bot |
| builtins/admin.py | RestartCommand | Command to restart bot |
| builtins/utility.py | PingCommand | Simple ping command |
| builtins/utility.py | UptimeCommand | Command to show bot uptime |
| builtins/utility.py | VersionCommand | Command to show bot version |

## Command Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | CommandHook | Base class for command hooks |
| hooks.py | CommandHook.run | Run hook function |
| hooks.py | BeforeCommandHook | Hook that runs before command |
| hooks.py | AfterCommandHook | Hook that runs after command |
| hooks.py | ErrorHook | Hook that runs on command error |
| hooks.py | HookManager | Manager for command hooks |
| hooks.py | HookManager.add_before_hook | Add hook before command |
| hooks.py | HookManager.add_after_hook | Add hook after command |
| hooks.py | HookManager.add_error_hook | Add hook for command error |
| hooks.py | HookManager.run_before_hooks | Run all before hooks |
| hooks.py | HookManager.run_after_hooks | Run all after hooks |
| hooks.py | HookManager.run_error_hooks | Run all error hooks |

## Command Factory
| Module | Function | Description |
|--------|----------|-------------|
| factory.py | CommandFactory | Factory for creating commands |
| factory.py | CommandFactory.create_command | Create command instance |
| factory.py | CommandFactory.create_from_function | Create command from function |
| factory.py | CommandFactory.create_from_class | Create command from class |
| factory.py | CommandFactory.register_command_type | Register custom command type |
| factory.py | create_command | Create command with global factory |
| factory.py | create_from_function | Create command from function with global factory |
| factory.py | create_from_class | Create command from class with global factory |
| factory.py | register_command_type | Register command type with global factory |

## Command Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | CommandManager | Manager for command registration and execution |
| manager.py | CommandManager.initialise | Initialise command system |
| manager.py | CommandManager.shutdown | Shutdown command system |
| manager.py | CommandManager.register_command | Register command |
| manager.py | CommandManager.unregister_command | Unregister command |
| manager.py | CommandManager.handle_message | Handle message for commands |
| manager.py | CommandManager.get_command | Get command by name |
| manager.py | CommandManager.get_all_commands | Get all registered commands |
| manager.py | CommandManager.execute_command | Execute command |
| manager.py | CommandManager.register_hook | Register command hook |
| manager.py | get_manager | Get singleton manager instance |
| manager.py | initialise | Initialise command system with global manager |
| manager.py | shutdown | Shutdown command system with global manager |

## Dynamic Command Loading
| Module | Function | Description |
|--------|----------|-------------|
| loader.py | CommandLoader | Loader for commands from modules |
| loader.py | CommandLoader.load_commands | Load commands from module |
| loader.py | CommandLoader.unload_commands | Unload commands from module |
| loader.py | CommandLoader.reload_commands | Reload commands from module |
| loader.py | CommandLoader.discover_commands | Discover commands in module |
| loader.py | CommandLoader.load_builtin_commands | Load built-in commands |
| loader.py | CommandLoader.load_feature_commands | Load commands from features |
| loader.py | load_commands | Load commands with global loader |
| loader.py | unload_commands | Unload commands with global loader |
| loader.py | reload_commands | Reload commands with global loader |
| loader.py | discover_commands | Discover commands with global loader |

## Command Guards
| Module | Function | Description |
|--------|----------|-------------|
| guards.py | Guard | Base class for command guards |
| guards.py | Guard.check | Check if guard passes |
| guards.py | GuardManager | Manager for command guards |
| guards.py | GuardManager.add_guard | Add guard to command |
| guards.py | GuardManager.check_guards | Check all guards for command |
| guards.py | BroadcasterGuard | Guard for broadcaster only |
| guards.py | ModeratorGuard | Guard for moderator or above |
| guards.py | VIPGuard | Guard for VIP or above |
| guards.py | SubscriberGuard | Guard for subscriber or above |
| guards.py | RoleGuard | Guard for specific user role |
| guards.py | PermissionGuard | Guard for specific permission |
| guards.py | CooldownGuard | Guard for command cooldown |
| guards.py | GuardFailed | Exception when guard check fails |

## Command Rate Limiting
| Module | Function | Description |
|--------|----------|-------------|
| throttling.py | ThrottleManager | Manager for command throttling |
| throttling.py | ThrottleManager.throttle | Throttle command execution |
| throttling.py | ThrottleManager.check_throttle | Check if command is throttled |
| throttling.py | ThrottleManager.reset_throttle | Reset command throttle |
| throttling.py | ThrottleManager.get_retry_after | Get time until throttle expires |
| throttling.py | CommandThrottle | Throttle definition for command |
| throttling.py | CommandThrottle.update | Update throttle state |
| throttling.py | CommandThrottle.get_retry_after | Get time until throttle expires |
| throttling.py | ThrottleScope | Enum for throttle scopes |
| throttling.py | CommandThrottledError | Error when command is throttled |
| throttling.py | throttle | Throttle with global manager |
| throttling.py | check_throttle | Check throttle with global manager |

## Command Help System
| Module | Function | Description |
|--------|----------|-------------|
| help.py | HelpFormatter | Formatter for command help text |
| help.py | HelpFormatter.format_command | Format help for command |
| help.py | HelpFormatter.format_commands | Format list of commands |
| help.py | HelpFormatter.format_usage | Format command usage |
| help.py | HelpFormatter.format_arguments | Format command arguments |
| help.py | HelpFormatter.format_permission | Format permission requirements |
| help.py | HelpFormatter.format_cooldown | Format cooldown information |
| help.py | CommandHelp | Container for command help information |
| help.py | CommandHelp.get_description | Get command description |
| help.py | CommandHelp.get_usage | Get command usage |
| help.py | CommandHelp.get_examples | Get command examples |
| help.py | CommandHelp.get_aliases | Get command aliases |
| help.py | format_help | Format help with global formatter |
| help.py | format_commands | Format commands with global formatter |

## Command Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_commands | Initialise command system |
| initialisation.py | load_builtin_commands | Load built-in commands |
| initialisation.py | load_feature_commands | Load commands from features |
| initialisation.py | register_command_middleware | Register command middleware |
| initialisation.py | setup_command_hooks | Set up command hooks |
| initialisation.py | configure_commands | Configure command settings |
| initialisation.py | shutdown_commands | Shutdown command system |
| initialisation.py | reload_commands | Reload all commands |
| initialisation.py | get_command_settings | Get command settings from config |
| initialisation.py | set_command_prefix | Set command prefix |
| initialisation.py | get_command_prefix | Get command prefix |
