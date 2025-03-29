# Project Architecture

This document outlines the project architecture to eliminate duplication, establish clear component boundaries, and implement proper separation of concerns.

## Core Package

The `core` package provides essential system components with well-defined responsibilities.

### Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| core/config/manager.py | ConfigManager | Central configuration manager |
| core/config/manager.py | ConfigManager.get | Get configuration value |
| core/config/manager.py | ConfigManager.set | Set configuration value |
| core/config/manager.py | ConfigManager.register_source | Register configuration source |
| core/config/sources/base.py | ConfigSource | Base class for configuration sources |
| core/config/sources/environment.py | EnvironmentSource | Environment variable configuration |
| core/config/sources/file.py | FileSource | File-based configuration |
| core/config/sources/memory.py | MemorySource | In-memory configuration |
| core/config/sources/database.py | DatabaseSource | Database-backed configuration |

### Logging

| Module | Class/Function | Description |
|--------|----------------|-------------|
| core/logging/manager.py | LogManager | Central logging manager |
| core/logging/manager.py | LogManager.get_logger | Get logger for module |
| core/logging/manager.py | LogManager.set_level | Set logging level |
| core/logging/handlers/console.py | ConsoleHandler | Console log handler |
| core/logging/handlers/file.py | FileHandler | File log handler |
| core/logging/formatters.py | StandardFormatter | Standard log formatter |

### Error Handling

| Module | Class/Function | Description |
|--------|----------------|-------------|
| core/errors/base.py | BotError | Base exception for all bot errors |
| core/errors/handler.py | ErrorHandler | Global error handler |
| core/errors/handler.py | ErrorHandler.handle | Handle error with context |
| core/errors/handler.py | ErrorHandler.register_handler | Register error handler |

### Event System

| Module | Class/Function | Description |
|--------|----------------|-------------|
| core/events/dispatcher.py | EventDispatcher | Central event dispatcher |
| core/events/dispatcher.py | EventDispatcher.subscribe | Subscribe to event type |
| core/events/dispatcher.py | EventDispatcher.publish | Publish event |
| core/events/base.py | Event | Base class for all events |
| core/events/base.py | Event.get_type | Get event type |
| core/events/base.py | Event.get_data | Get event data |

### Application Lifecycle

| Module | Class/Function | Description |
|--------|----------------|-------------|
| core/lifecycle/manager.py | LifecycleManager | Application lifecycle manager |
| core/lifecycle/manager.py | LifecycleManager.initialise | Initialise application |
| core/lifecycle/manager.py | LifecycleManager.start | Start application |
| core/lifecycle/manager.py | LifecycleManager.stop | Stop application |
| core/lifecycle/manager.py | LifecycleManager.register_hook | Register lifecycle hook |

## Utils Package

The `utils` package provides generic utility functions used throughout the application.

### Text Processing

| Module | Class/Function | Description |
|--------|----------------|-------------|
| utils/text/formatting.py | format_number | Format number with separators |
| utils/text/formatting.py | format_duration | Format time duration |
| utils/text/formatting.py | format_datetime | Format datetime |
| utils/text/formatting.py | format_list | Format list as string |
| utils/text/parsing.py | parse_command | Parse command from text |
| utils/text/parsing.py | parse_args | Parse arguments from text |
| utils/text/parsing.py | extract_mentions | Extract user mentions |

### Data Handling

| Module | Class/Function | Description |
|--------|----------------|-------------|
| utils/data/validation.py | validate_type | Validate value type |
| utils/data/validation.py | validate_range | Validate value in range |
| utils/data/validation.py | validate_not_empty | Validate value not empty |
| utils/data/conversion.py | safe_int | Safely convert to integer |
| utils/data/conversion.py | safe_float | Safely convert to float |
| utils/data/conversion.py | safe_bool | Safely convert to boolean |

### Security

| Module | Class/Function | Description |
|--------|----------------|-------------|
| utils/security/sanitisation.py | sanitise_input | Sanitise user input |
| utils/security/sanitisation.py | sanitise_filename | Sanitise filename |
| utils/security/sanitisation.py | sanitise_path | Sanitise file path |
| utils/security/crypto.py | generate_token | Generate secure token |
| utils/security/crypto.py | hash_password | Hash password securely |
| utils/security/crypto.py | verify_password | Verify password hash |

### Time Management

| Module | Class/Function | Description |
|--------|----------------|-------------|
| utils/time/datetime.py | get_current_timestamp | Get current timestamp |
| utils/time/datetime.py | get_utc_now | Get current UTC time |
| utils/time/datetime.py | to_utc | Convert to UTC time |
| utils/time/calculation.py | time_difference | Calculate time difference |
| utils/time/calculation.py | add_time | Add time delta |
| utils/time/formatting.py | format_relative_time | Format relative time |

### Collections

| Module | Class/Function | Description |
|--------|----------------|-------------|
| utils/collections/cache.py | LRUCache | Least Recently Used Cache |
| utils/collections/cache.py | ExpiringCache | Cache with expiry |
| utils/collections/queue.py | PriorityQueue | Priority-based queue |
| utils/collections/dict.py | deep_merge | Deep merge dictionaries |
| utils/collections/dict.py | flatten_dict | Flatten nested dictionary |

## Database Package

The `database` package handles all database operations with a unified approach.

### Connection Management

| Module | Class/Function | Description |
|--------|----------------|-------------|
| database/connection.py | DatabaseConnection | Database connection manager |
| database/connection.py | get_connection | Get database connection |
| database/connection.py | with_connection | Connection context manager |
| database/connection.py | with_transaction | Transaction context manager |

### Repository Pattern

| Module | Class/Function | Description |
|--------|----------------|-------------|
| database/repository/base.py | Repository | Base repository class |
| database/repository/base.py | Repository.find | Find entity by ID |
| database/repository/base.py | Repository.find_all | Find all entities |
| database/repository/base.py | Repository.save | Save entity |
| database/repository/base.py | Repository.delete | Delete entity |

### Schema Management

| Module | Class/Function | Description |
|--------|----------------|-------------|
| database/schema/manager.py | SchemaManager | Schema management |
| database/schema/manager.py | SchemaManager.create_schema | Create database schema |
| database/schema/manager.py | SchemaManager.migrate | Apply migrations |
| database/schema/migrations.py | Migration | Base migration class |

## Platform Package

The `platform` package provides a unified interface to external services.

### Twitch Integration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| platform/twitch/client.py | TwitchClient | Twitch API client |
| platform/twitch/client.py | TwitchClient.connect | Connect to Twitch |
| platform/twitch/client.py | TwitchClient.send_message | Send chat message |
| platform/twitch/events.py | register_twitch_events | Register Twitch events |
| platform/twitch/auth.py | TwitchAuth | Twitch authentication |

### OBS Integration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| platform/obs/client.py | OBSClient | OBS WebSocket client |
| platform/obs/client.py | OBSClient.connect | Connect to OBS WebSocket |
| platform/obs/client.py | OBSClient.switch_scene | Switch to scene |
| platform/obs/client.py | OBSClient.set_source_visibility | Set source visibility |
| platform/obs/actions.py | OBSActionExecutor | Execute OBS actions |

## Commands Package

The `commands` package handles command registration, parsing, and execution.

### Command Framework

| Module | Class/Function | Description |
|--------|----------------|-------------|
| commands/handler.py | CommandHandler | Process commands |
| commands/handler.py | CommandHandler.handle | Handle command message |
| commands/handler.py | CommandHandler.register | Register command |
| commands/base.py | Command | Base command class |
| commands/base.py | Command.execute | Execute command |
| commands/context.py | CommandContext | Command execution context |

### Command Processing

| Module | Class/Function | Description |
|--------|----------------|-------------|
| commands/parser.py | CommandParser | Parse command text |
| commands/parser.py | CommandParser.parse | Parse command and args |
| commands/args.py | ArgumentParser | Parse command arguments |
| commands/args.py | ArgumentParser.parse | Parse argument string |

### Command Decorators

| Module | Class/Function | Description |
|--------|----------------|-------------|
| commands/decorators.py | command | Command decorator |
| commands/decorators.py | argument | Argument decorator |
| commands/decorators.py | cooldown | Cooldown decorator |
| commands/decorators.py | permission | Permission decorator |

## Middleware Package

The `middleware` package provides request processing pipelines.

### Middleware Framework

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/base.py | Middleware | Base middleware class |
| middleware/base.py | Middleware.process | Process request |
| middleware/pipeline.py | MiddlewarePipeline | Execute middleware chain |
| middleware/pipeline.py | MiddlewarePipeline.add | Add middleware to pipeline |
| middleware/pipeline.py | MiddlewarePipeline.process | Process through pipeline |

### Command Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/command/permission.py | PermissionMiddleware | Check command permissions |
| middleware/command/cooldown.py | CooldownMiddleware | Handle command cooldowns |
| middleware/command/logging.py | LoggingMiddleware | Log command execution |
| middleware/command/validation.py | ValidationMiddleware | Validate command input |
| middleware/command/error.py | ErrorMiddleware | Handle command errors |

### Event Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/event/logging.py | LoggingMiddleware | Log event processing |
| middleware/event/validation.py | ValidationMiddleware | Validate event data |
| middleware/event/filtering.py | FilteringMiddleware | Filter events |
| middleware/event/error.py | ErrorMiddleware | Handle event errors |

## Feature Packages

Each feature is a self-contained package with a consistent structure.

### Feature Base

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/base.py | Feature | Base feature class |
| features/base.py | Feature.initialise | Initialise feature |
| features/base.py | Feature.shutdown | Shut down feature |
| features/base.py | Feature.is_enabled | Check if feature is enabled |
| features/base.py | Feature.register_components | Register feature components |

### Feature Manager

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/manager.py | FeatureManager | Feature management |
| features/manager.py | FeatureManager.load_feature | Load feature |
| features/manager.py | FeatureManager.enable_feature | Enable feature |
| features/manager.py | FeatureManager.disable_feature | Disable feature |
| features/manager.py | FeatureManager.get_feature | Get feature by name |

### Points Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/points/feature.py | PointsFeature | Points system feature |
| features/points/manager.py | PointsManager | Points management |
| features/points/manager.py | PointsManager.add_points | Add points to user |
| features/points/manager.py | PointsManager.remove_points | Remove points from user |
| features/points/manager.py | PointsManager.transfer_points | Transfer points between users |
| features/points/repository.py | PointsRepository | Points data access |
| features/points/commands.py | PointsCommand | Points command |
| features/points/commands.py | GiveCommand | Give points command |
| features/points/middleware.py | PointsTransactionMiddleware | Points transaction handling |

### Shop Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/shop/feature.py | ShopFeature | Shop system feature |
| features/shop/manager.py | ShopManager | Shop management |
| features/shop/manager.py | ShopManager.buy_item | Buy item for user |
| features/shop/manager.py | ShopManager.get_item | Get item details |
| features/shop/manager.py | ShopManager.list_items | List available items |
| features/shop/items/base.py | ShopItem | Base item class |
| features/shop/items/weapon.py | Weapon | Weapon item |
| features/shop/items/armour.py | Armour | Armour item |
| features/shop/repository.py | ShopRepository | Shop data access |
| features/shop/commands.py | ShopCommand | Shop command |
| features/shop/commands.py | BuyCommand | Buy item command |
| features/shop/middleware.py | ShopTransactionMiddleware | Shop transaction handling |

### Inventory Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/inventory/feature.py | InventoryFeature | Inventory system feature |
| features/inventory/manager.py | InventoryManager | Inventory management |
| features/inventory/manager.py | InventoryManager.add_item | Add item to inventory |
| features/inventory/manager.py | InventoryManager.remove_item | Remove item from inventory |
| features/inventory/manager.py | InventoryManager.get_inventory | Get user's inventory |
| features/inventory/repository.py | InventoryRepository | Inventory data access |
| features/inventory/commands.py | InventoryCommand | Inventory command |
| features/inventory/commands.py | GearCommand | Show gear command |
| features/inventory/middleware.py | InventoryTransactionMiddleware | Inventory transaction handling |

### Duel Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/duel/feature.py | DuelFeature | Duel system feature |
| features/duel/manager.py | DuelManager | Duel management |
| features/duel/manager.py | DuelManager.challenge | Create duel challenge |
| features/duel/manager.py | DuelManager.accept | Accept duel challenge |
| features/duel/manager.py | DuelManager.reject | Reject duel challenge |
| features/duel/calculator.py | DuelCalculator | Calculate duel outcome |
| features/duel/environment.py | EnvironmentManager | Manage duel environments |
| features/duel/repository.py | DuelRepository | Duel data access |
| features/duel/commands.py | DuelCommand | Duel command |
| features/duel/commands.py | AcceptCommand | Accept duel command |
| features/duel/middleware.py | DuelTransactionMiddleware | Duel transaction handling |

### DOMT Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/domt/feature.py | DOMTFeature | Deck of Many Things feature |
| features/domt/manager.py | DOMTManager | DOMT management |
| features/domt/manager.py | DOMTManager.draw_card | Draw card from deck |
| features/domt/manager.py | DOMTManager.reset_deck | Reset deck |
| features/domt/manager.py | DOMTManager.apply_effect | Apply card effect |
| features/domt/cards.py | Card | Card implementation |
| features/domt/effects.py | CardEffect | Card effect implementation |
| features/domt/repository.py | DOMTRepository | DOMT data access |
| features/domt/commands.py | CardCommand | Card command |
| features/domt/middleware.py | DOMTTransactionMiddleware | DOMT transaction handling |

### OBS Actions Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/obs_actions/feature.py | OBSActionsFeature | OBS actions feature |
| features/obs_actions/manager.py | ActionManager | Action management |
| features/obs_actions/manager.py | ActionManager.execute_action | Execute single action |
| features/obs_actions/manager.py | ActionManager.execute_sequence | Execute action sequence |
| features/obs_actions/manager.py | ActionManager.register_trigger | Register action trigger |
| features/obs_actions/actions/base.py | Action | Base action class |
| features/obs_actions/actions/scene.py | SceneAction | Scene action |
| features/obs_actions/actions/source.py | SourceAction | Source action |
| features/obs_actions/repository.py | ActionRepository | Action data access |
| features/obs_actions/commands.py | ActionCommand | Action command |
| features/obs_actions/triggers.py | ActionTrigger | Action trigger handler |
