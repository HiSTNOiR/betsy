# Inventory System Package Structure and Components

The `features/inventory` package provides a comprehensive inventory management system for the Twitch bot, allowing users to track and manage their owned items, equipment, and collectibles. This document outlines the structure and purpose of each module within the inventory feature package.

## Inventory Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | InventoryManager | Core manager for inventory functionality |
| manager.py | InventoryManager.initialise | Initialise inventory system |
| manager.py | InventoryManager.shutdown | Shut down inventory system |
| manager.py | InventoryManager.get_user_inventory | Get user's complete inventory |
| manager.py | InventoryManager.get_user_gear | Get user's equipped weapons and armour |
| manager.py | InventoryManager.get_user_toys | Get user's owned toys |
| manager.py | InventoryManager.get_user_cards | Get user's DOMT cards |
| manager.py | InventoryManager.add_item | Add item to user's inventory |
| manager.py | InventoryManager.remove_item | Remove item from user's inventory |
| manager.py | InventoryManager.has_item | Check if user has specific item |
| manager.py | InventoryManager.count_items | Count number of specific items user has |
| manager.py | InventoryManager.use_item | Use item from inventory |
| manager.py | InventoryManager.get_item_details | Get details about inventory item |
| manager.py | InventoryManager.transfer_item | Transfer item between users |
| manager.py | get_inventory_manager | Get singleton manager instance |
| manager.py | initialise | Initialise inventory system with global manager |
| manager.py | shutdown | Shutdown inventory system with global manager |

## Inventory Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_inventory_commands | Register all inventory-related commands |
| commands.py | InventoryCommand | Command to display user's inventory |
| commands.py | InventoryCommand.execute | Display user's complete inventory |
| commands.py | GearCommand | Command to display user's equipped gear |
| commands.py | GearCommand.execute | Display user's weapons and armour |
| commands.py | ToysCommand | Command to display user's toys |
| commands.py | ToysCommand.execute | Display user's collection of toys |
| commands.py | CardsCommand | Command to display user's DOMT cards |
| commands.py | CardsCommand.execute | Display user's collection of cards |
| commands.py | UseCommand | Command to use an item from inventory |
| commands.py | UseCommand.execute | Process item usage from inventory |
| commands.py | GiveItemCommand | Command to give item to another user |
| commands.py | GiveItemCommand.execute | Process item transfer between users |
| commands.py | AdminInventoryCommand | Administrative command group for inventory |
| commands.py | AddItemCommand | Admin command to add item to user's inventory |
| commands.py | RemoveItemCommand | Admin command to remove item from inventory |
| commands.py | ClearInventoryCommand | Admin command to clear user's inventory |

## Item Usage Handler
| Module | Function | Description |
|--------|----------|-------------|
| usage.py | ItemUsageHandler | Handles usage of inventory items |
| usage.py | ItemUsageHandler.can_use | Check if item can be used |
| usage.py | ItemUsageHandler.process_usage | Process item usage |
| usage.py | ItemUsageHandler.get_usage_effect | Get effect of using item |
| usage.py | ItemUsageHandler.apply_usage_effect | Apply effect of item usage |
| usage.py | ItemUsageHandler.consume_item | Consume item if single-use |
| usage.py | ItemUsageHandler.put_on_cooldown | Put item on cooldown if applicable |
| usage.py | ItemUsageHandler.notify_usage | Send item usage notification |
| usage.py | ItemUsageHandler.log_usage | Log item usage details |
| usage.py | ItemUsageHandler.register_usage_handler | Register custom usage handler |
| usage.py | get_usage_handler | Get singleton handler instance |
| usage.py | process_usage | Process usage with global handler |
| usage.py | register_usage_handler | Register handler with global instance |

## Equipment Manager
| Module | Function | Description |
|--------|----------|-------------|
| equipment.py | EquipmentManager | Manager for equipment-specific functionality |
| equipment.py | EquipmentManager.get_weapon | Get user's current weapon |
| equipment.py | EquipmentManager.get_armour | Get user's current armour |
| equipment.py | EquipmentManager.update_weapon | Update user's weapon |
| equipment.py | EquipmentManager.update_armour | Update user's armour |
| equipment.py | EquipmentManager.get_weapon_durability | Get weapon durability |
| equipment.py | EquipmentManager.get_armour_durability | Get armour durability |
| equipment.py | EquipmentManager.update_weapon_durability | Update weapon durability |
| equipment.py | EquipmentManager.update_armour_durability | Update armour durability |
| equipment.py | EquipmentManager.get_weapon_mods | Get weapon modifications |
| equipment.py | EquipmentManager.get_armour_mods | Get armour modifications |
| equipment.py | EquipmentManager.get_equipment_stats | Get combined equipment statistics |
| equipment.py | EquipmentManager.calculate_combat_rating | Calculate user's combat rating |
| equipment.py | EquipmentManager.repair_equipment | Repair equipment durability |
| equipment.py | get_equipment_manager | Get singleton manager instance |
| equipment.py | calculate_combat_rating | Calculate rating with global instance |

## Toys Manager
| Module | Function | Description |
|--------|----------|-------------|
| toys.py | ToysManager | Manager for toy-specific functionality |
| toys.py | ToysManager.get_toys | Get user's owned toys |
| toys.py | ToysManager.has_toy | Check if user has specific toy |
| toys.py | ToysManager.add_toy | Add toy to user's inventory |
| toys.py | ToysManager.remove_toy | Remove toy from user's inventory |
| toys.py | ToysManager.use_toy | Use toy with target |
| toys.py | ToysManager.get_toy_cooldown | Get toy usage cooldown |
| toys.py | ToysManager.is_toy_on_cooldown | Check if toy is on cooldown |
| toys.py | ToysManager.reset_toy_cooldown | Reset toy cooldown |
| toys.py | ToysManager.transfer_toy | Transfer toy between users |
| toys.py | ToysManager.get_toy_command | Get command associated with toy |
| toys.py | ToysManager.register_toy_handler | Register custom toy handler |
| toys.py | get_toys_manager | Get singleton manager instance |
| toys.py | use_toy | Use toy with global instance |
| toys.py | register_toy_handler | Register handler with global instance |

## Cards Manager
| Module | Function | Description |
|--------|----------|-------------|
| cards.py | CardsManager | Manager for card-specific functionality |
| cards.py | CardsManager.get_cards | Get user's owned cards |
| cards.py | CardsManager.has_card | Check if user has specific card |
| cards.py | CardsManager.add_card | Add card to user's inventory |
| cards.py | CardsManager.remove_card | Remove card from user's inventory |
| cards.py | CardsManager.use_card | Use card from inventory |
| cards.py | CardsManager.get_card_effect | Get card effect |
| cards.py | CardsManager.is_card_retainable | Check if card is retainable |
| cards.py | CardsManager.get_card_description | Get card description |
| cards.py | CardsManager.transfer_card | Transfer card between users |
| cards.py | CardsManager.can_use_card | Check if card can be used |
| cards.py | CardsManager.register_card_handler | Register custom card handler |
| cards.py | get_cards_manager | Get singleton manager instance |
| cards.py | use_card | Use card with global instance |
| cards.py | register_card_handler | Register handler with global instance |

## Inventory Display Formatter
| Module | Function | Description |
|--------|----------|-------------|
| display.py | InventoryDisplay | Formatter for inventory displays |
| display.py | InventoryDisplay.format_inventory | Format complete inventory display |
| display.py | InventoryDisplay.format_gear | Format gear display |
| display.py | InventoryDisplay.format_toys | Format toys display |
| display.py | InventoryDisplay.format_cards | Format cards display |
| display.py | InventoryDisplay.format_item_details | Format detailed item information |
| display.py | InventoryDisplay.format_weapon | Format weapon details |
| display.py | InventoryDisplay.format_armour | Format armour details |
| display.py | InventoryDisplay.format_toy | Format toy details |
| display.py | InventoryDisplay.format_card | Format card details |
| display.py | InventoryDisplay.format_durability | Format durability display |
| display.py | InventoryDisplay.format_modification | Format modification details |
| display.py | InventoryDisplay.format_empty_inventory | Format empty inventory message |
| display.py | get_inventory_display | Get singleton display instance |
| display.py | format_inventory | Format inventory with global instance |

## Inventory Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_inventory_events | Register all inventory-related event handlers |
| events.py | handle_item_added | Handle item added to inventory events |
| events.py | handle_item_removed | Handle item removed from inventory events |
| events.py | handle_item_used | Handle item usage events |
| events.py | handle_item_transferred | Handle item transfer events |
| events.py | handle_durability_changed | Handle durability change events |
| events.py | handle_equipment_updated | Handle equipment update events |
| events.py | notify_inventory_change | Send inventory change notification |
| events.py | log_inventory_transaction | Log inventory transaction |
| events.py | update_equipment_stats | Update user's equipment statistics |

## Inventory Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | InventoryConfig | Configuration for inventory system |
| config.py | InventoryConfig.get_max_inventory_size | Get maximum inventory size |
| config.py | InventoryConfig.get_max_toys | Get maximum toys allowed |
| config.py | InventoryConfig.get_max_cards | Get maximum cards allowed |
| config.py | InventoryConfig.get_durability_settings | Get durability settings |
| config.py | InventoryConfig.get_repair_cost | Get equipment repair cost |
| config.py | InventoryConfig.get_cooldown_settings | Get cooldown settings |
| config.py | InventoryConfig.get_toy_cooldowns | Get toy-specific cooldowns |
| config.py | InventoryConfig.get_display_settings | Get display settings |
| config.py | InventoryConfig.load | Load configuration from settings |
| config.py | InventoryConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## Inventory Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | InventoryRepository | Repository for inventory data |
| repository.py | InventoryRepository.get_user_inventory | Get user's inventory from database |
| repository.py | InventoryRepository.get_user_gear | Get user's gear from database |
| repository.py | InventoryRepository.get_user_toys | Get user's toys from database |
| repository.py | InventoryRepository.get_user_cards | Get user's cards from database |
| repository.py | InventoryRepository.add_item | Add item to inventory in database |
| repository.py | InventoryRepository.remove_item | Remove item from inventory in database |
| repository.py | InventoryRepository.update_durability | Update durability in database |
| repository.py | InventoryRepository.update_equipment | Update equipment in database |
| repository.py | InventoryRepository.log_transaction | Log inventory transaction in database |
| repository.py | InventoryRepository.get_transactions | Get inventory transactions from database |
| repository.py | InventoryRepository.check_item_exists | Check if item exists in inventory |
| repository.py | get_repository | Get singleton repository instance |

## Inventory Analytics
| Module | Function | Description |
|--------|----------|-------------|
| analytics.py | InventoryAnalytics | Analytics for inventory system |
| analytics.py | InventoryAnalytics.get_popular_items | Get most popular items in inventories |
| analytics.py | InventoryAnalytics.get_item_distribution | Get distribution of items across users |
| analytics.py | InventoryAnalytics.get_usage_patterns | Get item usage patterns |
| analytics.py | InventoryAnalytics.get_durability_statistics | Get durability statistics |
| analytics.py | InventoryAnalytics.get_equipment_trends | Get equipment trends |
| analytics.py | InventoryAnalytics.get_toy_popularity | Get toy popularity |
| analytics.py | InventoryAnalytics.get_card_rarity | Get card rarity statistics |
| analytics.py | InventoryAnalytics.get_inventory_size_distribution | Get inventory size distribution |
| analytics.py | InventoryAnalytics.generate_report | Generate analytics report |
| analytics.py | get_analytics | Get singleton analytics instance |
| analytics.py | generate_report | Generate report with global instance |

## Item Transfer Handler
| Module | Function | Description |
|--------|----------|-------------|
| transfer.py | ItemTransferHandler | Handler for item transfers |
| transfer.py | ItemTransferHandler.can_transfer | Check if transfer is allowed |
| transfer.py | ItemTransferHandler.validate_transfer | Validate transfer parameters |
| transfer.py | ItemTransferHandler.process_transfer | Process item transfer |
| transfer.py | ItemTransferHandler.remove_from_sender | Remove item from sender |
| transfer.py | ItemTransferHandler.add_to_receiver | Add item to receiver |
| transfer.py | ItemTransferHandler.notify_transfer | Send transfer notification |
| transfer.py | ItemTransferHandler.log_transfer | Log transfer details |
| transfer.py | ItemTransferHandler.register_validator | Register transfer validator |
| transfer.py | get_transfer_handler | Get singleton handler instance |
| transfer.py | process_transfer | Process transfer with global handler |
| transfer.py | register_validator | Register validator with global instance |

## Durability Manager
| Module | Function | Description |
|--------|----------|-------------|
| durability.py | DurabilityManager | Manager for equipment durability |
| durability.py | DurabilityManager.get_durability | Get item durability |
| durability.py | DurabilityManager.reduce_durability | Reduce item durability |
| durability.py | DurabilityManager.repair_durability | Repair item durability |
| durability.py | DurabilityManager.calculate_repair_cost | Calculate cost to repair |
| durability.py | DurabilityManager.is_broken | Check if item is broken |
| durability.py | DurabilityManager.get_effectiveness | Get item effectiveness based on durability |
| durability.py | DurabilityManager.format_durability | Format durability for display |
| durability.py | DurabilityManager.notify_durability_change | Notify durability change |
| durability.py | DurabilityManager.notify_broken_item | Notify when item breaks |
| durability.py | get_durability_manager | Get singleton manager instance |
| durability.py | reduce_durability | Reduce durability with global instance |
| durability.py | repair_durability | Repair durability with global instance |

## Inventory Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | InventoryFeature | Main inventory feature class |
| feature.py | InventoryFeature.initialise | Initialise inventory feature |
| feature.py | InventoryFeature.shutdown | Shutdown inventory feature |
| feature.py | InventoryFeature.get_commands | Get commands provided by feature |
| feature.py | InventoryFeature.get_event_handlers | Get event handlers for feature |
| feature.py | InventoryFeature.is_enabled | Check if feature is enabled |
| feature.py | InventoryFeature.get_dependencies | Get feature dependencies |
| feature.py | InventoryFeature.get_manager | Get inventory manager |
| feature.py | InventoryFeature.get_config | Get inventory configuration |
| feature.py | register_feature | Register inventory feature with system |
| feature.py | get_feature | Get inventory feature instance |

## Inventory Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | InventoryHooks | Hooks for inventory system integration |
| hooks.py | InventoryHooks.register_add_hook | Register hook for item addition |
| hooks.py | InventoryHooks.register_remove_hook | Register hook for item removal |
| hooks.py | InventoryHooks.register_use_hook | Register hook for item usage |
| hooks.py | InventoryHooks.register_transfer_hook | Register hook for item transfer |
| hooks.py | InventoryHooks.register_equipment_hook | Register hook for equipment changes |
| hooks.py | InventoryHooks.trigger_add_hooks | Trigger hooks for item addition |
| hooks.py | InventoryHooks.trigger_remove_hooks | Trigger hooks for item removal |
| hooks.py | InventoryHooks.trigger_use_hooks | Trigger hooks for item usage |
| hooks.py | InventoryHooks.trigger_transfer_hooks | Trigger hooks for item transfer |
| hooks.py | InventoryHooks.trigger_equipment_hooks | Trigger hooks for equipment changes |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

## Inventory Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | InventoryMiddleware | Middleware for inventory operations |
| middleware.py | InventoryMiddleware.process_operation | Process operation through middleware |
| middleware.py | InventoryMiddleware.register_middleware | Register operation middleware |
| middleware.py | InventoryMiddleware.validate_operation | Validate inventory operation |
| middleware.py | InventoryMiddleware.modify_operation | Modify inventory operation |
| middleware.py | InventoryMiddleware.log_operation | Log operation details |
| middleware.py | InventoryMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |

## Cooldown Manager
| Module | Function | Description |
|--------|----------|-------------|
| cooldown.py | CooldownManager | Manager for inventory item cooldowns |
| cooldown.py | CooldownManager.add_cooldown | Add cooldown for item |
| cooldown.py | CooldownManager.check_cooldown | Check if item is on cooldown |
| cooldown.py | CooldownManager.get_remaining | Get remaining cooldown time |
| cooldown.py | CooldownManager.reset_cooldown | Reset cooldown for item |
| cooldown.py | CooldownManager.get_cooldown_key | Get key for cooldown tracking |
| cooldown.py | CooldownManager.format_cooldown | Format cooldown for display |
| cooldown.py | CooldownManager.register_cooldown | Register cooldown settings |
| cooldown.py | get_cooldown_manager | Get singleton manager instance |
| cooldown.py | add_cooldown | Add cooldown with global instance |
| cooldown.py | check_cooldown | Check cooldown with global instance |
| cooldown.py | get_remaining | Get remaining time with global instance |

## Inventory Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_inventory | Initialise inventory system |
| initialisation.py | register_inventory_commands | Register inventory commands |
| initialisation.py | register_inventory_events | Register inventory event handlers |
| initialisation.py | setup_equipment_manager | Set up equipment manager |
| initialisation.py | setup_toys_manager | Set up toys manager |
| initialisation.py | setup_cards_manager | Set up cards manager |
| initialisation.py | setup_durability_manager | Set up durability manager |
| initialisation.py | setup_cooldown_manager | Set up cooldown manager |
| initialisation.py | load_inventory_config | Load inventory configuration |
| initialisation.py | register_default_hooks | Register default inventory hooks |
| initialisation.py | setup_inventory_repository | Set up inventory data repository |
| initialisation.py | setup_inventory_display | Set up inventory display formatter |
| initialisation.py | shutdown_inventory | Shutdown inventory system |
| initialisation.py | get_inventory_settings | Get inventory settings from config |