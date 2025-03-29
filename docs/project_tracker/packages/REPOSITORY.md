# Repository Pattern Implementation

The repository pattern provides a consistent approach to data access throughout the application. This document outlines the standardised repository structure that all feature-specific repositories should follow.

## Base Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/base.py | Repository | Abstract base repository class |
| repository/base.py | Repository.initialise | Initialise repository |
| repository/base.py | Repository.shutdown | Shut down repository |
| repository/base.py | Repository.find | Find entity by ID |
| repository/base.py | Repository.find_all | Find all entities |
| repository/base.py | Repository.find_where | Find entities matching criteria |
| repository/base.py | Repository.find_one | Find single entity matching criteria |
| repository/base.py | Repository.exists | Check if entity exists |
| repository/base.py | Repository.count | Count entities matching criteria |
| repository/base.py | Repository.create | Create new entity |
| repository/base.py | Repository.update | Update existing entity |
| repository/base.py | Repository.delete | Delete entity |
| repository/base.py | Repository.transaction | Execute operations in transaction |
| repository/base.py | Repository.with_transaction | Context manager for transactions |
| repository/base.py | Repository.execute_query | Execute raw query |
| repository/base.py | Repository.paginate | Paginate query results |
| repository/base.py | Repository.get_connection | Get database connection |
| repository/base.py | Repository.clear_cache | Clear repository cache |
| repository/base.py | get_repository | Get repository instance for entity type |
| repository/base.py | register_repository | Register repository for entity type |

## Repository Factory

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/factory.py | RepositoryFactory | Factory for creating repository instances |
| repository/factory.py | RepositoryFactory.register | Register repository type |
| repository/factory.py | RepositoryFactory.create | Create repository instance |
| repository/factory.py | get_factory | Get singleton factory instance |

## SQLite Implementation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/sqlite/repository.py | SQLiteRepository | SQLite implementation of Repository |
| repository/sqlite/repository.py | SQLiteRepository.initialise | Initialise SQLite repository |
| repository/sqlite/repository.py | SQLiteRepository.shutdown | Shut down SQLite repository |
| repository/sqlite/repository.py | SQLiteRepository.get_connection | Get SQLite connection |
| repository/sqlite/repository.py | SQLiteRepository.execute_query | Execute SQLite query |
| repository/sqlite/repository.py | SQLiteRepository.execute_script | Execute SQLite script |
| repository/sqlite/repository.py | SQLiteRepository.last_insert_id | Get last inserted ID |
| repository/sqlite/connection.py | SQLiteConnection | SQLite connection manager |
| repository/sqlite/connection.py | SQLiteConnectionPool | SQLite connection pool |
| repository/sqlite/transaction.py | SQLiteTransaction | SQLite transaction manager |
| repository/sqlite/query_builder.py | SQLiteQueryBuilder | SQLite query builder |

## Feature Repositories

### User Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/user_repository.py | UserRepository | Repository for user data |
| repository/user_repository.py | UserRepository.find_by_username | Find user by username |
| repository/user_repository.py | UserRepository.find_by_twitch_id | Find user by Twitch ID |
| repository/user_repository.py | UserRepository.update_points | Update user points |
| repository/user_repository.py | UserRepository.transfer_points | Transfer points between users |
| repository/user_repository.py | UserRepository.get_top_users | Get users with most points |
| repository/user_repository.py | UserRepository.get_recent_users | Get recently active users |
| repository/user_repository.py | UserRepository.update_last_seen | Update last seen timestamp |

### Item Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/item_repository.py | ItemRepository | Repository for item data |
| repository/item_repository.py | ItemRepository.find_by_name | Find item by name |
| repository/item_repository.py | ItemRepository.find_by_type | Find items by type |
| repository/item_repository.py | ItemRepository.find_by_level | Find items by level |
| repository/item_repository.py | ItemRepository.find_next_level | Find next level item |
| repository/item_repository.py | ItemRepository.fuzzy_find | Find item by fuzzy name match |

### Inventory Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/inventory_repository.py | InventoryRepository | Repository for inventory data |
| repository/inventory_repository.py | InventoryRepository.get_user_inventory | Get user's inventory |
| repository/inventory_repository.py | InventoryRepository.get_user_gear | Get user's equipment |
| repository/inventory_repository.py | InventoryRepository.add_item | Add item to inventory |
| repository/inventory_repository.py | InventoryRepository.remove_item | Remove item from inventory |
| repository/inventory_repository.py | InventoryRepository.update_durability | Update item durability |
| repository/inventory_repository.py | InventoryRepository.has_item | Check if user has item |

### Command Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/command_repository.py | CommandRepository | Repository for command data |
| repository/command_repository.py | CommandRepository.find_by_name | Find command by name |
| repository/command_repository.py | CommandRepository.find_by_alias | Find command by alias |
| repository/command_repository.py | CommandRepository.update_usage | Update command usage count |
| repository/command_repository.py | CommandRepository.get_most_used | Get most used commands |
| repository/command_repository.py | CommandRepository.find_by_permission | Find commands by permission |

### Duel Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/duel_repository.py | DuelRepository | Repository for duel data |
| repository/duel_repository.py | DuelRepository.create_duel | Create new duel |
| repository/duel_repository.py | DuelRepository.complete_duel | Complete duel with result |
| repository/duel_repository.py | DuelRepository.get_active_duels | Get active duels |
| repository/duel_repository.py | DuelRepository.get_user_stats | Get duel statistics for user |
| repository/duel_repository.py | DuelRepository.get_leaderboard | Get duel leaderboard |
| repository/duel_repository.py | DuelRepository.get_environment | Get duel environment |

### DOMT Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/domt_repository.py | DOMTRepository | Repository for DOMT data |
| repository/domt_repository.py | DOMTRepository.get_card | Get card by name |
| repository/domt_repository.py | DOMTRepository.get_undrawn_cards | Get undrawn cards |
| repository/domt_repository.py | DOMTRepository.mark_card_drawn | Mark card as drawn |
| repository/domt_repository.py | DOMTRepository.reset_deck | Reset deck |
| repository/domt_repository.py | DOMTRepository.add_card_to_user | Add card to user |
| repository/domt_repository.py | DOMTRepository.get_user_cards | Get user's cards |

### OBS Actions Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/obs_actions_repository.py | OBSActionsRepository | Repository for OBS actions data |
| repository/obs_actions_repository.py | OBSActionsRepository.get_action | Get action by ID |
| repository/obs_actions_repository.py | OBSActionsRepository.get_sequence | Get sequence by ID |
| repository/obs_actions_repository.py | OBSActionsRepository.get_actions_by_type | Get actions by type |
| repository/obs_actions_repository.py | OBSActionsRepository.get_sequences_by_trigger | Get sequences by trigger |
| repository/obs_actions_repository.py | OBSActionsRepository.add_action_to_sequence | Add action to sequence |
| repository/obs_actions_repository.py | OBSActionsRepository.update_action_order | Update action order |

### Easter Egg Repository

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/easter_egg_repository.py | EasterEggRepository | Repository for easter egg data |
| repository/easter_egg_repository.py | EasterEggRepository.get_egg | Get easter egg by ID |
| repository/easter_egg_repository.py | EasterEggRepository.get_emote_combo | Get emote combo |
| repository/easter_egg_repository.py | EasterEggRepository.update_combo_progress | Update combo progress |
| repository/easter_egg_repository.py | EasterEggRepository.get_timing_stats | Get message timing stats |
| repository/easter_egg_repository.py | EasterEggRepository.log_trigger | Log easter egg trigger |

## Repository Cache

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/cache.py | RepositoryCache | Cache for repository results |
| repository/cache.py | RepositoryCache.get | Get item from cache |
| repository/cache.py | RepositoryCache.set | Set item in cache |
| repository/cache.py | RepositoryCache.delete | Delete item from cache |
| repository/cache.py | RepositoryCache.clear | Clear cache |
| repository/cache.py | RepositoryCache.size | Get cache size |
| repository/cache.py | cached_query | Decorator for caching query results |
| repository/cache.py | invalidate_cache | Invalidate specific cache entries |

## Repository Migrations

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/migrations/manager.py | MigrationManager | Manager for database migrations |
| repository/migrations/manager.py | MigrationManager.get_applied | Get applied migrations |
| repository/migrations/manager.py | MigrationManager.get_pending | Get pending migrations |
| repository/migrations/manager.py | MigrationManager.apply | Apply pending migrations |
| repository/migrations/manager.py | MigrationManager.rollback | Rollback migration |
| repository/migrations/base.py | Migration | Base class for migrations |
| repository/migrations/base.py | Migration.up | Apply migration |
| repository/migrations/base.py | Migration.down | Revert migration |
| repository/migrations/loader.py | MigrationLoader | Loader for migration files |
| repository/migrations/loader.py | MigrationLoader.load | Load migrations from directory |
| repository/migrations/loader.py | MigrationLoader.sort | Sort migrations by version |

## Repository Maintenance

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/maintenance.py | backup_database | Create database backup |
| repository/maintenance.py | restore_database | Restore from backup |
| repository/maintenance.py | optimise_database | Optimise database |
| repository/maintenance.py | check_integrity | Check database integrity |
| repository/maintenance.py | repair_database | Attempt database repair |
| repository/maintenance.py | get_database_size | Get database file size |
| repository/maintenance.py | get_table_stats | Get statistics for tables |
| repository/maintenance.py | vacuum_database | Run VACUUM command |

## Repository Events

| Module | Class/Function | Description |
|--------|----------------|-------------|
| repository/events.py | RepositoryEvent | Base class for repository events |
| repository/events.py | EntityCreatedEvent | Event for entity creation |
| repository/events.py | EntityUpdatedEvent | Event for entity update |
| repository/events.py | EntityDeletedEvent | Event for entity deletion |
| repository/events.py | QueryExecutedEvent | Event for query execution |
| repository/events.py | TransactionBeginEvent | Event for transaction begin |
| repository/events.py | TransactionCommitEvent | Event for transaction commit |
| repository/events.py | TransactionRollbackEvent | Event for transaction rollback |
| repository/events.py | publish_repository_event | Publish repository event |
| repository/events.py | subscribe_to_repository_events | Subscribe to repository events |