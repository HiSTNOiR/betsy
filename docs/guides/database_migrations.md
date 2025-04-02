# Database Migration Guide

This guide explains how to use the database migration system to manage your database schema changes effectively.

## Overview

The migration system provides a way to evolve your database schema over time while preserving existing data. It tracks which changes have been applied, allowing you to:

- Apply new migrations to update the schema
- Roll back migrations to revert changes
- Track the current version of the database
- Create new migrations for schema changes

## Using Migrations in the Application

### Initialising the Database

When the application starts, we need to apply any pending migrations to ensure the database schema is up to date. This should be done during the application initialisation phase.

```python
from bot.db import initialise_db_connection, migrate_database

def initialise_database():
    # Connect to the database
    initialise_db_connection()
    
    # Apply pending migrations
    migrate_database()
```

This can be registered as a lifecycle hook to ensure it's called at the right time:

```python
from bot.core.lifecycle import get_lifecycle_manager, HookType

def register_database_hooks(manager=None):
    if manager is None:
        manager = get_lifecycle_manager()
    
    manager.register_initialise_hook(
        "initialise_database",
        initialise_database,
        priority=40  # After configuration, logging, and error handling
    )
```

### Creating New Migrations

When you need to make changes to the database schema, create a new migration using the command-line tool:

```bash
python scripts/migrate.py --create add_user_settings
```

This will create two new files in the `migrations` directory:

- `NNNN_add_user_settings.sql` - For the schema changes
- `NNNN_add_user_settings.down.sql` - For rolling back the changes

Edit these files to implement your schema changes.

### Testing Migrations

Before deploying migrations, test them locally to ensure they work correctly:

1. Apply the migration:
   ```bash
   python scripts/migrate.py --up
   ```

2. Verify that the changes work as expected with your application.

3. Roll back the migration to ensure it can be reverted:
   ```bash
   python scripts/migrate.py --down
   ```

4. Verify that the rollback works correctly.

5. Re-apply the migration:
   ```bash
   python scripts/migrate.py --up
   ```

### Deploying Migrations

When deploying new versions of the application, migrations should be applied automatically as part of the initialisation process. No manual steps should be needed.

If you need to manually apply migrations during deployment, you can run:

```bash
python scripts/migrate.py --up
```

## Migration Best Practices

### 1. Keep Migrations Focused

Each migration should make a focused, logical change to the schema. Avoid mixing multiple unrelated changes in a single migration, as this makes it harder to roll back specific changes if needed.

### 2. Make Migrations Reversible

Always provide a down script that properly reverts the changes made in the up script. This allows you to roll back changes if issues arise.

### 3. Consider Data Preservation

When modifying existing schemas, consider how to preserve existing data. For example, if renaming a column:

```sql
-- In the up script
ALTER TABLE users ADD COLUMN username TEXT;
UPDATE users SET username = name;
ALTER TABLE users DROP COLUMN name;

-- In the down script
ALTER TABLE users ADD COLUMN name TEXT;
UPDATE users SET name = username;
ALTER TABLE users DROP COLUMN username;
```

### 4. Use Transactions

The migration system automatically wraps each migration in a transaction, ensuring that migrations are either fully applied or not applied at all. This prevents partial migrations that could leave the database in an inconsistent state.

### 5. Be Cautious with Large Data Changes

For migrations that involve large data changes, consider breaking them down into smaller migrations or implementing them in a way that doesn't lock the database for extended periods.

### 6. Document Your Migrations

Add comments to your migration scripts explaining what they do and why. This makes it easier for other developers to understand the purpose of each migration.

## API Reference

### Migration Manager

The `MigrationManager` class is responsible for managing migrations. It provides methods for:

- Getting available migrations
- Getting applied migrations
- Applying migrations
- Rolling back migrations
- Creating new migrations

### Helper Functions

The migration module provides several helper functions:

- `initialise_migration_manager()`: Initialise the migration manager
- `migrate_database()`: Apply pending migrations
- `rollback_database()`: Roll back applied migrations
- `get_database_version()`: Get the current database version
- `create_migration()`: Create a new migration

These functions simplify common migration tasks and are suitable for most use cases.

## Troubleshooting

### Migration Fails to Apply

If a migration fails to apply, check:

1. SQL syntax errors in the migration script
2. Missing dependencies (e.g., referenced tables don't exist)
3. Conflicts with existing schema elements

The migration system will automatically roll back failed migrations to maintain database consistency.

### Cannot Roll Back Migration

If a migration cannot be rolled back, check:

1. SQL syntax errors in the down script
2. Dependencies that prevent rollback (e.g., data integrity constraints)
3. Missing down script

In some cases, you may need to manually fix the database state before rolling back.

### Invalid Migration State

If the migration state becomes inconsistent (e.g., due to manual database changes), you may need to manually update the `migrations` table to reflect the actual state of the database.