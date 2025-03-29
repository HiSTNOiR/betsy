# Feature Modularisation Structure

This document outlines a consistent approach to feature modules, ensuring proper boundaries, standardised interfaces, and well-defined dependencies. All features should follow this structure to ensure consistency and maintainability.

## Feature Base Framework

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/base.py | Feature | Abstract base class for all features |
| features/base.py | Feature.initialise | Initialise feature |
| features/base.py | Feature.shutdown | Shut down feature |
| features/base.py | Feature.is_enabled | Check if feature is enabled |
| features/base.py | Feature.get_name | Get feature name |
| features/base.py | Feature.get_description | Get feature description |
| features/base.py | Feature.get_version | Get feature version |
| features/base.py | Feature.get_dependencies | Get feature dependencies |
| features/base.py | Feature.get_commands | Get commands provided by feature |
| features/base.py | Feature.get_event_handlers | Get event handlers for feature |
| features/base.py | Feature.get_middleware | Get middleware for feature |
| features/base.py | Feature.get_config | Get feature configuration |
| features/base.py | Feature.handle_event | Handle event for feature |
| features/base.py | Feature.register_command | Register command for feature |
| features/base.py | Feature.register_event_handler | Register event handler for feature |
| features/base.py | Feature.register_middleware | Register middleware for feature |
| features/base.py | Feature.get_manager | Get feature-specific manager |
| features/base.py | Feature.validate_dependencies | Validate feature dependencies |

## Feature Manager

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/manager.py | FeatureManager | Manager for all features |
| features/manager.py | FeatureManager.initialise | Initialise feature system |
| features/manager.py | FeatureManager.shutdown | Shutdown feature system |
| features/manager.py | FeatureManager.register_feature | Register feature |
| features/manager.py | FeatureManager.get_feature | Get feature by name |
| features/manager.py | FeatureManager.load_feature | Load feature |
| features/manager.py | FeatureManager.unload_feature | Unload feature |
| features/manager.py | FeatureManager.enable_feature | Enable feature |
| features/manager.py | FeatureManager.disable_feature | Disable feature |
| features/manager.py | FeatureManager.get_enabled_features | Get all enabled features |
| features/manager.py | FeatureManager.get_all_features | Get all registered features |
| features/manager.py | FeatureManager.get_feature_dependencies | Get feature dependencies |
| features/manager.py | FeatureManager.resolve_dependencies | Resolve feature dependencies |
| features/manager.py | FeatureManager.get_dependent_features | Get features dependent on feature |
| features/manager.py | FeatureManager.validate_dependencies | Validate all feature dependencies |
| features/manager.py | get_manager | Get singleton manager instance |
| features/manager.py | register_feature | Register feature with manager |
| features/manager.py | get_feature | Get feature from manager |
| features/manager.py | enable_feature | Enable feature using manager |
| features/manager.py | disable_feature | Disable feature using manager |

## Feature Registry

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/registry.py | FeatureRegistry | Registry for all features |
| features/registry.py | FeatureRegistry.register | Register feature with registry |
| features/registry.py | FeatureRegistry.unregister | Unregister feature from registry |
| features/registry.py | FeatureRegistry.get_feature | Get feature by name |
| features/registry.py | FeatureRegistry.get_all_features | Get all registered features |
| features/registry.py | FeatureRegistry.clear | Clear all registered features |
| features/registry.py | get_registry | Get singleton registry instance |
| features/registry.py | register_feature | Register feature with registry |
| features/registry.py | unregister_feature | Unregister feature from registry |
| features/registry.py | get_feature | Get feature from registry |

## Feature Loader

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/loader.py | FeatureLoader | Loader for features |
| features/loader.py | FeatureLoader.discover_features | Discover available features |
| features/loader.py | FeatureLoader.load_feature | Load feature by name |
| features/loader.py | FeatureLoader.unload_feature | Unload feature by name |
| features/loader.py | FeatureLoader.reload_feature | Reload feature by name |
| features/loader.py | FeatureLoader.load_all_features | Load all features |
| features/loader.py | FeatureLoader.get_feature_info | Get information about feature |
| features/loader.py | FeatureLoader.get_feature_dependencies | Get feature dependencies |
| features/loader.py | get_loader | Get singleton loader instance |
| features/loader.py | discover_features | Discover features with loader |
| features/loader.py | load_feature | Load feature with loader |
| features/loader.py | unload_feature | Unload feature with loader |
| features/loader.py | reload_feature | Reload feature with loader |

## Standard Feature Structure

Each feature module should follow this standard structure:

### Core Components

| Component | Purpose |
|-----------|---------|
| `__init__.py` | Feature definition and entry point |
| `feature.py` | Main feature class implementation |
| `commands.py` | Feature-specific commands |
| `events.py` | Feature-specific event handlers |
| `models.py` | Feature-specific data models |
| `manager.py` | Feature-specific manager |
| `middleware.py` | Feature-specific middleware |
| `repository.py` | Feature-specific repository integration |
| `config.py` | Feature-specific configuration |
| `exceptions.py` | Feature-specific exceptions |
| `constants.py` | Feature-specific constants |
| `utils.py` | Feature-specific utility functions |
| `hooks.py` | Feature-specific hooks |
| `providers.py` | Feature-specific service providers |
| `initialisation.py` | Feature initialisation logic |

### Standard Feature Interface

Each feature should implement the following interface in its `feature.py` file:

```python
class MyFeature(Feature):
    """Feature description."""
    
    def __init__(self):
        self.name = "my_feature"
        self.description = "My feature description"
        self.version = "1.0.0"
        self.dependencies = ["other_feature"]  # Other features this depends on
        self.manager = None
        
    def initialise(self):
        """Initialise feature."""
        # Initialise feature-specific manager
        self.manager = get_manager()
        
        # Register commands
        self.register_commands()
        
        # Register event handlers
        self.register_event_handlers()
        
        # Register middleware
        self.register_middleware()
        
    def shutdown(self):
        """Shut down feature."""
        # Cleanup resources
        
    def is_enabled(self):
        """Check if feature is enabled."""
        return get_config().is_enabled()
        
    def get_commands(self):
        """Get commands provided by feature."""
        from .commands import get_commands
        return get_commands()
        
    def get_event_handlers(self):
        """Get event handlers for feature."""
        from .events import get_event_handlers
        return get_event_handlers()
        
    def get_middleware(self):
        """Get middleware for feature."""
        from .middleware import get_middleware
        return get_middleware()
        
    def get_manager(self):
        """Get feature-specific manager."""
        return self.manager
        
    def register_commands(self):
        """Register commands for feature."""
        from .commands import register_commands
        register_commands()
        
    def register_event_handlers(self):
        """Register event handlers for feature."""
        from .events import register_event_handlers
        register_event_handlers()
        
    def register_middleware(self):
        """Register middleware for feature."""
        from .middleware import register_middleware
        register_middleware()
```

## Feature Dependencies

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/dependencies.py | DependencyResolver | Resolver for feature dependencies |
| features/dependencies.py | DependencyResolver.resolve | Resolve feature dependencies |
| features/dependencies.py | DependencyResolver.get_load_order | Get feature load order |
| features/dependencies.py | DependencyResolver.check_circular | Check for circular dependencies |
| features/dependencies.py | DependencyResolver.validate | Validate dependency resolution |
| features/dependencies.py | DependencyGraph | Graph of feature dependencies |
| features/dependencies.py | DependencyGraph.add_node | Add node to graph |
| features/dependencies.py | DependencyGraph.add_edge | Add edge to graph |
| features/dependencies.py | DependencyGraph.has_node | Check if graph has node |
| features/dependencies.py | DependencyGraph.get_dependencies | Get dependencies for node |
| features/dependencies.py | DependencyGraph.get_dependents | Get dependents for node |
| features/dependencies.py | DependencyGraph.find_cycles | Find cycles in graph |
| features/dependencies.py | DependencyGraph.topological_sort | Sort graph topologically |
| features/dependencies.py | get_resolver | Get singleton resolver instance |
| features/dependencies.py | resolve_dependencies | Resolve dependencies with resolver |
| features/dependencies.py | get_load_order | Get load order with resolver |

## Feature Events

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/events.py | FeatureEvent | Base class for feature events |
| features/events.py | FeatureLoadedEvent | Event for feature loaded |
| features/events.py | FeatureUnloadedEvent | Event for feature unloaded |
| features/events.py | FeatureEnabledEvent | Event for feature enabled |
| features/events.py | FeatureDisabledEvent | Event for feature disabled |
| features/events.py | FeatureInitialisingEvent | Event for feature initialising |
| features/events.py | FeatureInitialisedEvent | Event for feature initialised |
| features/events.py | FeatureShuttingDownEvent | Event for feature shutting down |
| features/events.py | FeatureErrorEvent | Event for feature error |
| features/events.py | publish_feature_event | Publish feature event |
| features/events.py | subscribe_to_feature_events | Subscribe to feature events |

## Feature Configuration

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/config.py | FeatureConfiguration | Base class for feature configuration |
| features/config.py | FeatureConfiguration.is_enabled | Check if feature is enabled |
| features/config.py | FeatureConfiguration.get_settings | Get feature settings |
| features/config.py | FeatureConfiguration.load | Load feature configuration |
| features/config.py | FeatureConfiguration.save | Save feature configuration |
| features/config.py | FeatureConfiguration.get_schema | Get configuration schema |
| features/config.py | FeatureConfiguration.validate | Validate configuration |
| features/config.py | get_feature_config | Get configuration for feature |
| features/config.py | register_feature_config | Register feature configuration |
| features/config.py | load_feature_configs | Load all feature configurations |
| features/config.py | save_feature_configs | Save all feature configurations |

## Feature Services

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/services.py | FeatureService | Base class for feature services |
| features/services.py | FeatureService.initialise | Initialise service |
| features/services.py | FeatureService.shutdown | Shutdown service |
| features/services.py | FeatureService.is_running | Check if service is running |
| features/services.py | FeatureService.start | Start service |
| features/services.py | FeatureService.stop | Stop service |
| features/services.py | FeatureService.restart | Restart service |
| features/services.py | FeatureServiceRegistry | Registry for feature services |
| features/services.py | FeatureServiceRegistry.register | Register service |
| features/services.py | FeatureServiceRegistry.unregister | Unregister service |
| features/services.py | FeatureServiceRegistry.get_service | Get service by name |
| features/services.py | FeatureServiceRegistry.get_services | Get all services for feature |
| features/services.py | get_registry | Get singleton registry instance |
| features/services.py | register_service | Register service with registry |
| features/services.py | get_service | Get service from registry |

## Feature Hooks

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/hooks.py | FeatureHook | Base class for feature hooks |
| features/hooks.py | FeatureHook.execute | Execute hook |
| features/hooks.py | FeatureHook.should_execute | Check if hook should execute |
| features/hooks.py | LoadHook | Hook for feature loading |
| features/hooks.py | LoadHook.execute | Execute on feature load |
| features/hooks.py | UnloadHook | Hook for feature unloading |
| features/hooks.py | UnloadHook.execute | Execute on feature unload |
| features/hooks.py | InitialiseHook | Hook for feature initialisation |
| features/hooks.py | InitialiseHook.execute | Execute on feature initialisation |
| features/hooks.py | ShutdownHook | Hook for feature shutdown |
| features/hooks.py | ShutdownHook.execute | Execute on feature shutdown |
| features/hooks.py | HookRegistry | Registry for feature hooks |
| features/hooks.py | HookRegistry.register | Register hook |
| features/hooks.py | HookRegistry.get_hooks | Get hooks for feature |
| features/hooks.py | get_registry | Get singleton registry instance |
| features/hooks.py | register_hook | Register hook with registry |

## Feature Providers

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/providers.py | FeatureProvider | Base class for feature providers |
| features/providers.py | FeatureProvider.register_feature | Register feature |
| features/providers.py | FeatureProvider.get_features | Get features from provider |
| features/providers.py | PackageProvider | Provider for package-based features |
| features/providers.py | PackageProvider.discover | Discover features in packages |
| features/providers.py | PackageProvider.load | Load feature from package |
| features/providers.py | DirectoryProvider | Provider for directory-based features |
| features/providers.py | DirectoryProvider.discover | Discover features in directory |
| features/providers.py | DirectoryProvider.load | Load feature from directory |
| features/providers.py | ProviderRegistry | Registry for feature providers |
| features/providers.py | ProviderRegistry.register | Register provider |
| features/providers.py | ProviderRegistry.get_provider | Get provider by name |
| features/providers.py | ProviderRegistry.get_providers | Get all providers |
| features/providers.py | get_registry | Get singleton registry instance |
| features/providers.py | register_provider | Register provider with registry |

## Standardised Feature Implementations

### Points Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/points/feature.py | PointsFeature | Main points feature class |
| features/points/manager.py | PointsManager | Manager for points functionality |
| features/points/commands.py | register_points_commands | Register points commands |
| features/points/commands.py | PointsCommand | Command to check points |
| features/points/commands.py | GiveCommand | Command to give points |
| features/points/commands.py | GambleCommand | Command to gamble points |
| features/points/events.py | register_points_events | Register points event handlers |
| features/points/events.py | handle_message_points | Handle points for messages |
| features/points/events.py | handle_bits_points | Handle points for bits |
| features/points/middleware.py | register_middleware | Register points middleware |
| features/points/middleware.py | EarningMiddleware | Middleware for points earning |
| features/points/middleware.py | SpendingMiddleware | Middleware for points spending |
| features/points/middleware.py | TransferMiddleware | Middleware for points transfers |
| features/points/config.py | PointsConfiguration | Configuration for points feature |
| features/points/repository.py | PointsRepository | Repository for points data |
| features/points/utils.py | format_points | Format points for display |
| features/points/utils.py | calculate_points_reward | Calculate points reward |
| features/points/initialisation.py | initialise_points | Initialise points feature |

### Shop Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/shop/feature.py | ShopFeature | Main shop feature class |
| features/shop/manager.py | ShopManager | Manager for shop functionality |
| features/shop/items/base.py | ShopItem | Base class for shop items |
| features/shop/items/weapon.py | Weapon | Weapon item implementation |
| features/shop/items/armour.py | Armour | Armour item implementation |
| features/shop/items/modification.py | Modification | Modification item implementation |
| features/shop/items/toy.py | Toy | Toy item implementation |
| features/shop/commands.py | register_shop_commands | Register shop commands |
| features/shop/commands.py | ShopCommand | Command to display shop |
| features/shop/commands.py | BuyCommand | Command to buy items |
| features/shop/commands.py | UpgradeCommand | Command to upgrade items |
| features/shop/commands.py | ModifyCommand | Command to modify items |
| features/shop/events.py | register_shop_events | Register shop event handlers |
| features/shop/middleware.py | register_middleware | Register shop middleware |
| features/shop/middleware.py | PurchaseMiddleware | Middleware for purchases |
| features/shop/middleware.py | UpgradeMiddleware | Middleware for upgrades |
| features/shop/config.py | ShopConfiguration | Configuration for shop feature |
| features/shop/repository.py | ShopRepository | Repository for shop data |
| features/shop/utils.py | format_item | Format item for display |
| features/shop/initialisation.py | initialise_shop | Initialise shop feature |

### Duel Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/duel/feature.py | DuelFeature | Main duel feature class |
| features/duel/manager.py | DuelManager | Manager for duel functionality |
| features/duel/calculator.py | DuelCalculator | Calculator for duel outcomes |
| features/duel/environment.py | EnvironmentManager | Manager for environments |
| features/duel/commands.py | register_duel_commands | Register duel commands |
| features/duel/commands.py | DuelCommand | Command to challenge to duel |
| features/duel/commands.py | AcceptCommand | Command to accept duel |
| features/duel/commands.py | RejectCommand | Command to reject duel |
| features/duel/events.py | register_duel_events | Register duel event handlers |
| features/duel/middleware.py | register_middleware | Register duel middleware |
| features/duel/middleware.py | ChallengeMiddleware | Middleware for challenges |
| features/duel/middleware.py | ResolutionMiddleware | Middleware for resolutions |
| features/duel/config.py | DuelConfiguration | Configuration for duel feature |
| features/duel/repository.py | DuelRepository | Repository for duel data |
| features/duel/utils.py | format_duel_result | Format duel result |
| features/duel/initialisation.py | initialise_duel | Initialise duel feature |

### Inventory Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/inventory/feature.py | InventoryFeature | Main inventory feature class |
| features/inventory/manager.py | InventoryManager | Manager for inventory functionality |
| features/inventory/equipment.py | EquipmentManager | Manager for equipment |
| features/inventory/toys.py | ToysManager | Manager for toys |
| features/inventory/cards.py | CardsManager | Manager for cards |
| features/inventory/commands.py | register_inventory_commands | Register inventory commands |
| features/inventory/commands.py | InventoryCommand | Command to display inventory |
| features/inventory/commands.py | GearCommand | Command to display gear |
| features/inventory/commands.py | ToysCommand | Command to display toys |
| features/inventory/commands.py | CardsCommand | Command to display cards |
| features/inventory/events.py | register_inventory_events | Register inventory event handlers |
| features/inventory/middleware.py | register_middleware | Register inventory middleware |
| features/inventory/middleware.py | AddItemMiddleware | Middleware for adding items |
| features/inventory/middleware.py | RemoveItemMiddleware | Middleware for removing items |
| features/inventory/middleware.py | UseItemMiddleware | Middleware for using items |
| features/inventory/config.py | InventoryConfiguration | Configuration for inventory feature |
| features/inventory/repository.py | InventoryRepository | Repository for inventory data |
| features/inventory/utils.py | format_inventory | Format inventory for display |
| features/inventory/initialisation.py | initialise_inventory | Initialise inventory feature |

### DOMT Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/domt/feature.py | DOMTFeature | Main DOMT feature class |
| features/domt/manager.py | DOMTManager | Manager for DOMT functionality |
| features/domt/cards.py | Card | Card implementation |
| features/domt/effects.py | CardEffect | Card effect implementation |
| features/domt/commands.py | register_domt_commands | Register DOMT commands |
| features/domt/commands.py | CardCommand | Command to use card |
| features/domt/commands.py | CardsCommand | Command to view cards |
| features/domt/events.py | register_domt_events | Register DOMT event handlers |
| features/domt/events.py | handle_bits_event | Handle bits for DOMT |
| features/domt/middleware.py | register_middleware | Register DOMT middleware |
| features/domt/config.py | DOMTConfiguration | Configuration for DOMT feature |
| features/domt/repository.py | DOMTRepository | Repository for DOMT data |
| features/domt/utils.py | format_card | Format card for display |
| features/domt/initialisation.py | initialise_domt | Initialise DOMT feature |

### OBS Actions Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/obs_actions/feature.py | OBSActionsFeature | Main OBS actions feature class |
| features/obs_actions/manager.py | OBSActionManager | Manager for OBS actions functionality |
| features/obs_actions/actions/base.py | OBSAction | Base action implementation |
| features/obs_actions/actions/scene.py | SceneAction | Scene action implementation |
| features/obs_actions/actions/source.py | SourceAction | Source action implementation |
| features/obs_actions/actions/audio.py | AudioAction | Audio action implementation |
| features/obs_actions/sequence.py | ActionSequence | Action sequence implementation |
| features/obs_actions/triggers/base.py | Trigger | Base trigger implementation |
| features/obs_actions/triggers/command.py | CommandTrigger | Command trigger implementation |
| features/obs_actions/triggers/bits.py | BitsTrigger | Bits trigger implementation |
| features/obs_actions/triggers/reward.py | RewardTrigger | Reward trigger implementation |
| features/obs_actions/commands.py | register_obs_actions_commands | Register OBS actions commands |
| features/obs_actions/events.py | register_obs_actions_events | Register OBS actions event handlers |
| features/obs_actions/middleware.py | register_middleware | Register OBS actions middleware |
| features/obs_actions/config.py | OBSActionsConfiguration | Configuration for OBS actions feature |
| features/obs_actions/repository.py | OBSActionsRepository | Repository for OBS actions data |
| features/obs_actions/utils.py | format_action | Format action for display |
| features/obs_actions/initialisation.py | initialise_obs_actions | Initialise OBS actions feature |

### Easter Eggs Feature

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/easter_eggs/feature.py | EasterEggsFeature | Main easter eggs feature class |
| features/easter_eggs/manager.py | EasterEggManager | Manager for easter eggs functionality |
| features/easter_eggs/eggs/emote_combo.py | EmoteComboEgg | Emote combo easter egg |
| features/easter_eggs/eggs/self_targeting.py | SelfTargetingEgg | Self-targeting easter egg |
| features/easter_eggs/eggs/message_timing.py | MessageTimingEgg | Message timing easter egg |
| features/easter_eggs/triggers/base.py | EggTrigger | Base trigger implementation |
| features/easter_eggs/triggers/message.py | MessagePatternTrigger | Message pattern trigger |
| features/easter_eggs/triggers/command.py | CommandTrigger | Command trigger |
| features/easter_eggs/triggers/event.py | EventTrigger | Event trigger |
| features/easter_eggs/conditions/base.py | EggCondition | Base condition implementation |
| features/easter_eggs/rewards/base.py | EggReward | Base reward implementation |
| features/easter_eggs/commands.py | register_easter_egg_commands | Register easter egg commands |
| features/easter_eggs/events.py | register_easter_egg_events | Register easter egg event handlers |
| features/easter_eggs/middleware.py | register_middleware | Register easter egg middleware |
| features/easter_eggs/config.py | EasterEggsConfiguration | Configuration for easter eggs feature |
| features/easter_eggs/repository.py | EasterEggRepository | Repository for easter eggs data |
| features/easter_eggs/emotes.py | EmoteDetector | Detector for emotes |
| features/easter_eggs/timing.py | MessageTimingTracker | Tracker for message timing |
| features/easter_eggs/initialisation.py | initialise_easter_eggs | Initialise easter eggs feature |

## Feature Initialisation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| features/initialisation.py | initialise_features | Initialise feature system |
| features/initialisation.py | register_core_features | Register core features |
| features/initialisation.py | discover_features | Discover available features |
| features/initialisation.py | load_enabled_features | Load enabled features |
| features/initialisation.py | initialise_features | Initialise loaded features |
| features/initialisation.py | register_feature_commands | Register feature commands |
| features/initialisation.py | register_feature_events | Register feature events |
| features/initialisation.py | register_feature_middleware | Register feature middleware |
| features/initialisation.py | shutdown_features | Shutdown feature system |