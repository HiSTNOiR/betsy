# Unified Configuration System

The configuration system provides a hierarchical approach to managing application settings, allowing for core configurations to be extended by feature-specific configurations. This document outlines the structure and components of the unified configuration system.

## Core Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/base.py | ConfigurationBase | Abstract base class for all configurations |
| config/base.py | ConfigurationBase.load | Load configuration from source |
| config/base.py | ConfigurationBase.save | Save configuration to source |
| config/base.py | ConfigurationBase.get | Get configuration value |
| config/base.py | ConfigurationBase.set | Set configuration value |
| config/base.py | ConfigurationBase.has | Check if configuration exists |
| config/base.py | ConfigurationBase.remove | Remove configuration value |
| config/base.py | ConfigurationBase.clear | Clear all configuration |
| config/base.py | ConfigurationBase.merge | Merge with another configuration |
| config/base.py | ConfigurationBase.validate | Validate configuration values |
| config/base.py | ConfigurationBase.get_schema | Get configuration schema |

## Configuration Manager

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/manager.py | ConfigurationManager | Manager for all configurations |
| config/manager.py | ConfigurationManager.initialise | Initialise configuration system |
| config/manager.py | ConfigurationManager.shutdown | Shut down configuration system |
| config/manager.py | ConfigurationManager.register | Register configuration |
| config/manager.py | ConfigurationManager.get_config | Get configuration by name |
| config/manager.py | ConfigurationManager.load_all | Load all configurations |
| config/manager.py | ConfigurationManager.save_all | Save all configurations |
| config/manager.py | ConfigurationManager.validate_all | Validate all configurations |
| config/manager.py | ConfigurationManager.get_defaults | Get default configurations |
| config/manager.py | get_manager | Get singleton manager instance |
| config/manager.py | get_config | Get configuration by name |
| config/manager.py | register_config | Register configuration |

## Environment Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/environment.py | EnvironmentConfiguration | Configuration from environment variables |
| config/environment.py | EnvironmentConfiguration.load | Load from environment |
| config/environment.py | EnvironmentConfiguration.get_required | Get required environment variable |
| config/environment.py | EnvironmentConfiguration.get_optional | Get optional environment variable |
| config/environment.py | EnvironmentConfiguration.as_dict | Get all as dictionary |
| config/environment.py | env_bool | Convert environment value to boolean |
| config/environment.py | env_int | Convert environment value to integer |
| config/environment.py | env_float | Convert environment value to float |
| config/environment.py | env_list | Convert environment value to list |
| config/environment.py | env_dict | Convert environment value to dictionary |

## File Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/file.py | FileConfiguration | Configuration from file |
| config/file.py | FileConfiguration.load | Load from file |
| config/file.py | FileConfiguration.save | Save to file |
| config/file.py | FileConfiguration.get_file_path | Get configuration file path |
| config/file.py | FileConfiguration.watch | Watch file for changes |
| config/file.py | FileConfiguration.unwatch | Stop watching file |
| config/file.py | YAMLConfiguration | Configuration from YAML file |
| config/file.py | JSONConfiguration | Configuration from JSON file |
| config/file.py | INIConfiguration | Configuration from INI file |
| config/file.py | TOMLConfiguration | Configuration from TOML file |
| config/file.py | DotEnvConfiguration | Configuration from .env file |

## Memory Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/memory.py | MemoryConfiguration | In-memory configuration |
| config/memory.py | MemoryConfiguration.load | Load from dictionary |
| config/memory.py | MemoryConfiguration.save | Save to dictionary |
| config/memory.py | MemoryConfiguration.reset | Reset to initial state |
| config/memory.py | MemoryConfiguration.copy | Create copy of configuration |
| config/memory.py | MemoryConfiguration.snapshot | Create snapshot of current state |
| config/memory.py | MemoryConfiguration.restore | Restore from snapshot |

## Database Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/database.py | DatabaseConfiguration | Configuration from database |
| config/database.py | DatabaseConfiguration.load | Load from database |
| config/database.py | DatabaseConfiguration.save | Save to database |
| config/database.py | DatabaseConfiguration.get_repository | Get configuration repository |
| config/database.py | DatabaseConfiguration.create_table | Create configuration table |
| config/database.py | DatabaseConfiguration.drop_table | Drop configuration table |
| config/database.py | DatabaseConfiguration.reload | Reload from database |

## Configuration Schema and Validation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/schema.py | ConfigurationSchema | Schema for configuration validation |
| config/schema.py | ConfigurationSchema.validate | Validate configuration against schema |
| config/schema.py | ConfigurationSchema.get_defaults | Get default values from schema |
| config/schema.py | ConfigurationSchema.to_dict | Convert schema to dictionary |
| config/schema.py | ConfigurationSchema.from_dict | Create schema from dictionary |
| config/schema.py | SchemaField | Field definition for schema |
| config/schema.py | SchemaField.validate | Validate value against field |
| config/schema.py | StringField | String field definition |
| config/schema.py | IntegerField | Integer field definition |
| config/schema.py | FloatField | Float field definition |
| config/schema.py | BooleanField | Boolean field definition |
| config/schema.py | ListField | List field definition |
| config/schema.py | DictionaryField | Dictionary field definition |
| config/schema.py | EnumField | Enumeration field definition |

## Application Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/app.py | ApplicationConfiguration | Core application configuration |
| config/app.py | ApplicationConfiguration.get_bot_settings | Get bot settings |
| config/app.py | ApplicationConfiguration.get_twitch_settings | Get Twitch settings |
| config/app.py | ApplicationConfiguration.get_obs_settings | Get OBS settings |
| config/app.py | ApplicationConfiguration.get_database_settings | Get database settings |
| config/app.py | ApplicationConfiguration.get_log_settings | Get logging settings |
| config/app.py | ApplicationConfiguration.get_command_settings | Get command settings |
| config/app.py | ApplicationConfiguration.get_event_settings | Get event settings |

## Feature Configurations

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/features/points.py | PointsConfiguration | Points system configuration |
| config/features/points.py | PointsConfiguration.get_message_points | Get points for messages |
| config/features/points.py | PointsConfiguration.get_lurker_points | Get points for lurking |
| config/features/points.py | PointsConfiguration.get_bits_ratio | Get bits to points ratio |
| config/features/points.py | PointsConfiguration.get_gift_multiplier | Get gift multiplier |
| config/features/shop.py | ShopConfiguration | Shop system configuration |
| config/features/shop.py | ShopConfiguration.get_discount_rate | Get discount rate |
| config/features/shop.py | ShopConfiguration.get_max_modifications | Get max modifications |
| config/features/shop.py | ShopConfiguration.get_durability_settings | Get durability settings |
| config/features/duel.py | DuelConfiguration | Duel system configuration |
| config/features/duel.py | DuelConfiguration.get_min_amount | Get minimum stake amount |
| config/features/duel.py | DuelConfiguration.get_max_amount | Get maximum stake amount |
| config/features/duel.py | DuelConfiguration.get_timeout_seconds | Get challenge timeout |
| config/features/duel.py | DuelConfiguration.get_underdog_win_chance | Get underdog win chance |
| config/features/domt.py | DOMTConfiguration | DOMT system configuration |
| config/features/domt.py | DOMTConfiguration.get_bits_cost | Get bits cost for drawing |
| config/features/domt.py | DOMTConfiguration.get_card_count | Get total card count |
| config/features/obs_actions.py | OBSActionsConfiguration | OBS actions configuration |
| config/features/obs_actions.py | OBSActionsConfiguration.get_default_scene | Get default scene |
| config/features/obs_actions.py | OBSActionsConfiguration.get_animation_fps | Get animation FPS |
| config/features/easter_eggs.py | EasterEggsConfiguration | Easter eggs configuration |
| config/features/easter_eggs.py | EasterEggsConfiguration.get_emote_combo_settings | Get emote combo settings |
| config/features/easter_eggs.py | EasterEggsConfiguration.get_timing_streak_settings | Get timing streak settings |

## Configuration Providers

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/providers/base.py | ConfigurationProvider | Base class for configuration providers |
| config/providers/base.py | ConfigurationProvider.get_configuration | Get configuration from provider |
| config/providers/env.py | EnvironmentProvider | Provider from environment variables |
| config/providers/file.py | FileProvider | Provider from configuration files |
| config/providers/memory.py | MemoryProvider | Provider from in-memory storage |
| config/providers/database.py | DatabaseProvider | Provider from database |
| config/providers/default.py | DefaultProvider | Provider for default values |
| config/providers/composite.py | CompositeProvider | Provider combining multiple sources |
| config/providers/factory.py | ProviderFactory | Factory for creating providers |
| config/providers/factory.py | create_provider | Create provider instance |
| config/providers/registry.py | ProviderRegistry | Registry for providers |
| config/providers/registry.py | register_provider | Register provider with registry |

## Configuration Utilities

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/utils.py | merge_configurations | Merge multiple configurations |
| config/utils.py | deep_merge | Deep merge of configuration dictionaries |
| config/utils.py | flatten_dict | Flatten nested dictionary |
| config/utils.py | unflatten_dict | Unflatten dictionary to nested structure |
| config/utils.py | dict_to_config | Convert dictionary to configuration object |
| config/utils.py | config_to_dict | Convert configuration to dictionary |
| config/utils.py | mask_sensitive | Mask sensitive configuration values |
| config/utils.py | interpolate_values | Interpolate variables in configuration |
| config/utils.py | validate_config | Validate configuration against schema |
| config/utils.py | get_config_differences | Get differences between configurations |

## Configuration Events

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/events.py | ConfigurationEvent | Base class for configuration events |
| config/events.py | ConfigurationLoadedEvent | Event for configuration loaded |
| config/events.py | ConfigurationSavedEvent | Event for configuration saved |
| config/events.py | ConfigurationChangedEvent | Event for configuration changed |
| config/events.py | ConfigurationResetEvent | Event for configuration reset |
| config/events.py | ConfigurationValidationEvent | Event for configuration validation |
| config/events.py | publish_config_event | Publish configuration event |
| config/events.py | subscribe_to_config_events | Subscribe to configuration events |

## Configuration Initialisation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| config/initialisation.py | initialise_configuration | Initialise configuration system |
| config/initialisation.py | register_configurations | Register all configurations |
| config/initialisation.py | register_providers | Register all providers |
| config/initialisation.py | load_configurations | Load all configurations |
| config/initialisation.py | validate_configurations | Validate all configurations |
| config/initialisation.py | setup_watchers | Set up configuration file watchers |
| config/initialisation.py | shutdown_configuration | Shutdown configuration system |