# Database Package Structure and Components

The `db` package serves as the data persistence layer for the Twitch bot, handling all database operations, schema management, and data access patterns. This document outlines the structure and purpose of each module within the `db` package.

## Connection Management
| Module | Function | Description |
|--------|----------|-------------|
| connection.py | DatabaseConnection | Class for managing database connections |
| connection.py | get_connection | Get a database connection from the pool |
| connection.py | create_connection_pool | Create a connection pool |
| connection.py | close_connection_pool | Close the connection pool |
| connection.py | with_connection | Context manager for database connections |
| connection.py | with_transaction | Context manager for database transactions |
| connection.py | execute_query | Execute SQL query with parameters |
| connection.py | execute_script | Execute SQL script file |
| connection.py | fetch_one | Fetch single row from query result |
| connection.py | fetch_all | Fetch all rows from query result |
| connection.py | fetch_value | Fetch single value from query result |
| connection.py | initialise_database | Initialise database connection |
| connection.py | test_connection | Test database connection |

## Schema Management
| Module | Function | Description |
|--------|----------|-------------|
| schema.py | create_schema | Create database schema |
| schema.py | drop_schema | Drop database schema |
| schema.py | check_schema_exists | Check if schema exists |
| schema.py | get_schema_version | Get current schema version |
| schema.py | set_schema_version | Update schema version |
| schema.py | validate_schema | Validate schema integrity |
| schema.py | read_schema_file | Read schema from SQL file |
| schema.py | create_table | Create table from definition |
| schema.py | add_column | Add column to existing table |
| schema.py | create_index | Create index on table |
| schema.py | load_schema_from_file | Load schema from file |

## Migrations
| Module | Function | Description |
|--------|----------|-------------|
| migrations/manager.py | MigrationManager | Class for managing migrations |
| migrations/manager.py | apply_migrations | Apply pending migrations |
| migrations/manager.py | rollback_migration | Rollback specific migration |
| migrations/manager.py | get_applied_migrations | Get list of applied migrations |
| migrations/manager.py | get_pending_migrations | Get list of pending migrations |
| migrations/manager.py | register_migration | Register migration script |
| migrations/manager.py | create_migration | Create new migration file |
| migrations/base.py | Migration | Base class for migrations |
| migrations/base.py | Migration.apply | Apply migration |
| migrations/base.py | Migration.rollback | Rollback migration |
| migrations/base.py | Migration.get_version | Get migration version |
| migrations/loader.py | load_migrations | Load migrations from directory |
| migrations/loader.py | sort_migrations | Sort migrations by version |

## Models
| Module | Function | Description |
|--------|----------|-------------|
| models/base.py | Model | Base class for all models |
| models/base.py | Model.from_row | Create model from database row |
| models/base.py | Model.to_dict | Convert model to dictionary |
| models/base.py | Field | Class for model field definition |
| models/base.py | PrimaryKeyField | Field for primary keys |
| models/base.py | ForeignKeyField | Field for foreign keys |
| models/base.py | IntegerField | Field for integer values |
| models/base.py | TextField | Field for text values |
| models/base.py | BooleanField | Field for boolean values |
| models/base.py | DateTimeField | Field for datetime values |
| models/base.py | EnumField | Field for enum values |
| models/base.py | JSONField | Field for JSON values |

## User Model
| Module | Function | Description |
|--------|----------|-------------|
| models/user.py | User | User model class |
| models/user.py | User.get_roles | Get user roles |
| models/user.py | User.has_role | Check if user has role |
| models/user.py | User.has_permission | Check if user has permission |
| models/user.py | User.get_points | Get user points |
| models/user.py | User.add_points | Add points to user |
| models/user.py | User.subtract_points | Subtract points from user |
| models/user.py | User.get_inventory | Get user inventory |
| models/user.py | User.get_current_weapon | Get user's current weapon |
| models/user.py | User.get_current_armour | Get user's current armour |
| models/user.py | User.update_last_seen | Update last seen timestamp |

## Item Models
| Module | Function | Description |
|--------|----------|-------------|
| models/item.py | Item | Base class for all items |
| models/item.py | Item.get_cost | Get item cost |
| models/item.py | Item.get_level | Get item level |
| models/item.py | Item.get_type | Get item type |
| models/item.py | Weapon | Weapon item class |
| models/item.py | Weapon.get_durability | Get weapon durability |
| models/item.py | Weapon.reduce_durability | Reduce weapon durability |
| models/item.py | Weapon.repair | Repair weapon durability |
| models/item.py | Armour | Armour item class |
| models/item.py | Armour.get_durability | Get armour durability |
| models/item.py | Armour.reduce_durability | Reduce armour durability |
| models/item.py | Armour.repair | Repair armour durability |
| models/item.py | Toy | Toy item class |
| models/item.py | Modification | Modification item class |
| models/item.py | Card | Card item class |

## Command Models
| Module | Function | Description |
|--------|----------|-------------|
| models/command.py | Command | Command model class |
| models/command.py | Command.get_aliases | Get command aliases |
| models/command.py | Command.get_permission | Get required permission level |
| models/command.py | Command.get_cooldown | Get command cooldown |
| models/command.py | Command.get_usage_count | Get command usage count |
| models/command.py | Command.increment_usage | Increment usage count |
| models/command.py | Command.get_response | Get command response text |
| models/command.py | Command.update_response | Update command response text |
| models/command.py | Command.get_action_sequence | Get associated action sequence |

## Duel Models
| Module | Function | Description |
|--------|----------|-------------|
| models/duel.py | Duel | Duel model class |
| models/duel.py | Duel.get_challenger | Get duel challenger |
| models/duel.py | Duel.get_opponent | Get duel opponent |
| models/duel.py | Duel.get_pot_size | Get duel pot size |
| models/duel.py | Duel.get_winner | Get duel winner |
| models/duel.py | Duel.set_winner | Set duel winner |
| models/duel.py | Duel.is_draw | Check if duel was a draw |
| models/duel.py | Duel.set_draw | Set duel as draw |
| models/duel.py | Duel.get_environment | Get duel environment |
| models/duel.py | DuelEnvironment | Duel environment model class |
| models/duel.py | EnvironmentEffect | Environment effect model class |

## OBS Models
| Module | Function | Description |
|--------|----------|-------------|
| models/obs.py | OBSAction | OBS action model class |
| models/obs.py | OBSAction.get_scene | Get associated scene |
| models/obs.py | OBSAction.get_sources | Get associated sources |
| models/obs.py | OBSAction.get_filters | Get associated filters |
| models/obs.py | OBSAction.get_duration | Get action duration |
| models/obs.py | OBSSequence | OBS action sequence model class |
| models/obs.py | OBSSequence.get_actions | Get sequence actions |
| models/obs.py | OBSSequence.get_trigger | Get sequence trigger |
| models/obs.py | OBSSequence.get_ordered_actions | Get actions in order |

## DOMT Models
| Module | Function | Description |
|--------|----------|-------------|
| models/domt.py | DOMTCard | DOMT card model class |
| models/domt.py | DOMTCard.is_drawn | Check if card is drawn |
| models/domt.py | DOMTCard.mark_drawn | Mark card as drawn |
| models/domt.py | DOMTCard.is_retainable | Check if card is retainable |
| models/domt.py | DOMTCard.get_description | Get card description |
| models/domt.py | DOMTCard.get_action_sequence | Get associated action sequence |
| models/domt.py | DOMTCard.increment_drawn_count | Increment times drawn counter |
| models/domt.py | DOMTDeck | DOMT deck model class |
| models/domt.py | DOMTDeck.draw_card | Draw card from deck |
| models/domt.py | DOMTDeck.reset | Reset deck |
| models/domt.py | DOMTDeck.get_remaining_cards | Get remaining cards |

## Repositories
| Module | Function | Description |
|--------|----------|-------------|
| repositories/base.py | Repository | Base class for all repositories |
| repositories/base.py | Repository.find | Find entity by ID |
| repositories/base.py | Repository.find_all | Find all entities |
| repositories/base.py | Repository.save | Save entity |
| repositories/base.py | Repository.update | Update entity |
| repositories/base.py | Repository.delete | Delete entity |
| repositories/base.py | Repository.count | Count entities |
| repositories/base.py | Repository.exists | Check if entity exists |
| repositories/base.py | Repository.transaction | Execute in transaction |

## User Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/user_repository.py | UserRepository | Repository for user data |
| repositories/user_repository.py | UserRepository.find_by_username | Find user by username |
| repositories/user_repository.py | UserRepository.find_by_twitch_id | Find user by Twitch ID |
| repositories/user_repository.py | UserRepository.create_user | Create new user |
| repositories/user_repository.py | UserRepository.update_points | Update user points |
| repositories/user_repository.py | UserRepository.update_last_seen | Update last seen timestamp |
| repositories/user_repository.py | UserRepository.transfer_points | Transfer points between users |
| repositories/user_repository.py | UserRepository.get_top_users | Get users with most points |
| repositories/user_repository.py | UserRepository.get_recent_users | Get recently active users |
| repositories/user_repository.py | UserRepository.update_rank | Update user rank |
| repositories/user_repository.py | UserRepository.get_inventory | Get user inventory |
| repositories/user_repository.py | UserRepository.add_to_inventory | Add item to user inventory |
| repositories/user_repository.py | UserRepository.remove_from_inventory | Remove item from inventory |

## Item Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/item_repository.py | ItemRepository | Repository for item data |
| repositories/item_repository.py | ItemRepository.find_by_name | Find item by name |
| repositories/item_repository.py | ItemRepository.find_by_type | Find items by type |
| repositories/item_repository.py | ItemRepository.find_by_level | Find items by level |
| repositories/item_repository.py | ItemRepository.find_weapon | Find weapon by name |
| repositories/item_repository.py | ItemRepository.find_armour | Find armour by name |
| repositories/item_repository.py | ItemRepository.find_toy | Find toy by name |
| repositories/item_repository.py | ItemRepository.find_modification | Find modification by name |
| repositories/item_repository.py | ItemRepository.find_next_level | Find next level item |
| repositories/item_repository.py | ItemRepository.fuzzy_find | Find item by fuzzy name match |
| repositories/item_repository.py | ItemRepository.get_all_weapons | Get all weapons |
| repositories/item_repository.py | ItemRepository.get_all_armour | Get all armour |
| repositories/item_repository.py | ItemRepository.get_all_toys | Get all toys |
| repositories/item_repository.py | ItemRepository.get_all_modifications | Get all modifications |

## Command Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/command_repository.py | CommandRepository | Repository for command data |
| repositories/command_repository.py | CommandRepository.find_by_name | Find command by name |
| repositories/command_repository.py | CommandRepository.find_by_alias | Find command by alias |
| repositories/command_repository.py | CommandRepository.create_command | Create new command |
| repositories/command_repository.py | CommandRepository.update_command | Update command |
| repositories/command_repository.py | CommandRepository.delete_command | Delete command |
| repositories/command_repository.py | CommandRepository.increment_usage | Increment usage count |
| repositories/command_repository.py | CommandRepository.get_all_commands | Get all commands |
| repositories/command_repository.py | CommandRepository.find_by_permission | Find commands by permission level |
| repositories/command_repository.py | CommandRepository.get_most_used | Get most used commands |

## Duel Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/duel_repository.py | DuelRepository | Repository for duel data |
| repositories/duel_repository.py | DuelRepository.create_duel | Create new duel |
| repositories/duel_repository.py | DuelRepository.complete_duel | Complete duel with result |
| repositories/duel_repository.py | DuelRepository.get_active_duels | Get active duels |
| repositories/duel_repository.py | DuelRepository.get_user_duels | Get duels for user |
| repositories/duel_repository.py | DuelRepository.get_user_wins | Get wins for user |
| repositories/duel_repository.py | DuelRepository.get_user_losses | Get losses for user |
| repositories/duel_repository.py | DuelRepository.get_environment | Get duel environment |
| repositories/duel_repository.py | DuelRepository.get_all_environments | Get all environments |
| repositories/duel_repository.py | DuelRepository.get_environment_effects | Get environment effects |
| repositories/duel_repository.py | DuelRepository.get_random_environment | Get random environment |

## OBS Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/obs_repository.py | OBSRepository | Repository for OBS data |
| repositories/obs_repository.py | OBSRepository.find_action | Find OBS action |
| repositories/obs_repository.py | OBSRepository.create_action | Create OBS action |
| repositories/obs_repository.py | OBSRepository.update_action | Update OBS action |
| repositories/obs_repository.py | OBSRepository.delete_action | Delete OBS action |
| repositories/obs_repository.py | OBSRepository.find_sequence | Find action sequence |
| repositories/obs_repository.py | OBSRepository.create_sequence | Create action sequence |
| repositories/obs_repository.py | OBSRepository.update_sequence | Update action sequence |
| repositories/obs_repository.py | OBSRepository.delete_sequence | Delete action sequence |
| repositories/obs_repository.py | OBSRepository.get_sequence_actions | Get actions for sequence |
| repositories/obs_repository.py | OBSRepository.add_action_to_sequence | Add action to sequence |
| repositories/obs_repository.py | OBSRepository.remove_action_from_sequence | Remove action from sequence |
| repositories/obs_repository.py | OBSRepository.find_by_trigger | Find sequences by trigger |

## DOMT Repository
| Module | Function | Description |
|--------|----------|-------------|
| repositories/domt_repository.py | DOMTRepository | Repository for DOMT data |
| repositories/domt_repository.py | DOMTRepository.find_card | Find DOMT card |
| repositories/domt_repository.py | DOMTRepository.get_all_cards | Get all cards |
| repositories/domt_repository.py | DOMTRepository.get_undrawn_cards | Get undrawn cards |
| repositories/domt_repository.py | DOMTRepository.draw_card | Draw card from deck |
| repositories/domt_repository.py | DOMTRepository.reset_deck | Reset deck |
| repositories/domt_repository.py | DOMTRepository.add_to_inventory | Add card to user inventory |
| repositories/domt_repository.py | DOMTRepository.get_user_cards | Get cards for user |
| repositories/domt_repository.py | DOMTRepository.remove_from_inventory | Remove card from inventory |
| repositories/domt_repository.py | DOMTRepository.get_card_stats | Get card draw statistics |

## Database Maintenance
| Module | Function | Description |
|--------|----------|-------------|
| maintenance.py | backup_database | Create database backup |
| maintenance.py | restore_database | Restore from backup |
| maintenance.py | optimise_database | Optimise database (VACUUM) |
| maintenance.py | check_integrity | Check database integrity |
| maintenance.py | repair_database | Attempt to repair database |
| maintenance.py | compress_database | Compress database file |
| maintenance.py | get_database_size | Get size of database file |
| maintenance.py | get_table_sizes | Get sizes of tables |
| maintenance.py | get_row_counts | Get row counts for tables |
| maintenance.py | clean_orphaned_records | Clean orphaned records |
| maintenance.py | truncate_logs | Truncate log tables |
| maintenance.py | create_backup_filename | Create backup filename |

## Query Builder
| Module | Function | Description |
|--------|----------|-------------|
| query_builder.py | QueryBuilder | SQL query builder |
| query_builder.py | QueryBuilder.select | Build SELECT query |
| query_builder.py | QueryBuilder.insert | Build INSERT query |
| query_builder.py | QueryBuilder.update | Build UPDATE query |
| query_builder.py | QueryBuilder.delete | Build DELETE query |
| query_builder.py | QueryBuilder.where | Add WHERE clause |
| query_builder.py | QueryBuilder.order_by | Add ORDER BY clause |
| query_builder.py | QueryBuilder.group_by | Add GROUP BY clause |
| query_builder.py | QueryBuilder.limit | Add LIMIT clause |
| query_builder.py | QueryBuilder.offset | Add OFFSET clause |
| query_builder.py | QueryBuilder.join | Add JOIN clause |
| query_builder.py | QueryBuilder.left_join | Add LEFT JOIN clause |

## Cache Layer
| Module | Function | Description |
|--------|----------|-------------|
| cache.py | Cache | Cache interface |
| cache.py | MemoryCache | In-memory cache implementation |
| cache.py | DatabaseCache | Database-backed cache implementation |
| cache.py | get_cache | Get cache instance |
| cache.py | cache_key | Generate cache key |
| cache.py | cached | Decorator for caching function results |
| cache.py | cache_clear | Clear cache |
| cache.py | cache_get | Get value from cache |
| cache.py | cache_set | Set value in cache |
| cache.py | cache_delete | Delete value from cache |
| cache.py | cache_has | Check if key exists in cache |
| cache.py | cache_ttl | Get TTL for cached item |

## Database Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_database | Initialise database |
| initialisation.py | create_tables | Create database tables |
| initialisation.py | create_indexes | Create database indexes |
| initialisation.py | create_constraints | Create database constraints |
| initialisation.py | seed_database | Seed database with initial data |
| initialisation.py | seed_items | Seed item data |
| initialisation.py | seed_commands | Seed command data |
| initialisation.py | seed_environments | Seed environment data |
| initialisation.py | seed_domt_cards | Seed DOMT card data |
| initialisation.py | check_database_exists | Check if database exists |
| initialisation.py | create_database | Create database |

## Database Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | get_db_path | Get database file path |
| config.py | get_db_timeout | Get database timeout |
| config.py | get_connection_pool_size | Get connection pool size |
| config.py | get_pragma_settings | Get SQLite PRAGMA settings |
| config.py | configure_database | Configure database connection |
| config.py | get_backup_directory | Get backup directory path |
| config.py | get_max_backups | Get maximum number of backups to keep |
| config.py | get_cache_ttl | Get cache time-to-live |
| config.py | should_use_wal_mode | Check if WAL mode should be used |
| config.py | should_optimize_on_close | Check if optimize on close |

## Database Statistics
| Module | Function | Description |
|--------|----------|-------------|
| statistics.py | get_table_stats | Get statistics for tables |
| statistics.py | get_index_stats | Get statistics for indexes |
| statistics.py | get_query_count | Get number of queries executed |
| statistics.py | get_slow_queries | Get slow queries |
| statistics.py | get_query_timing | Get query execution timing |
| statistics.py | get_connection_stats | Get connection pool statistics |
| statistics.py | get_transaction_stats | Get transaction statistics |
| statistics.py | reset_statistics | Reset statistics counters |
| statistics.py | get_top_users_by_points | Get users with most points |
| statistics.py | get_most_used_commands | Get most used commands |
| statistics.py | get_most_active_users | Get most active users |