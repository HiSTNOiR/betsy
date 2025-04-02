# Database Migrations

This directory contains database migrations for the bot. Each migration represents a change to the database schema or data, and migrations are applied in order based on their version number.

## Migration Files

Each migration consists of two files:

- `NNNN_name.sql` - The SQL script to apply the migration (upgrade)
- `NNNN_name.down.sql` - The SQL script to roll back the migration (downgrade)

Where `NNNN` is a four-digit version number, and `name` is a descriptive name for the migration.

## Managing Migrations

You can manage migrations using the `migrate.py` script:

```bash
# Apply all pending migrations
python scripts/migrate.py --up

# Roll back the last migration
python scripts/migrate.py --down

# Roll back multiple migrations
python scripts/migrate.py --down 3

# Migrate to a specific version
python scripts/migrate.py --to 5

# Create a new migration
python scripts/migrate.py --create add_users_table

# Show migration status
python scripts/migrate.py --status
```

## Writing Migrations

When creating a new migration, follow these guidelines:

1. **Keep it focused**: Each migration should do one logical change.
2. **Make it reversible**: Always provide a down script to roll back changes.
3. **Test both directions**: Verify both the up and down scripts work correctly.
4. **Consider dependencies**: Make sure table references and foreign keys are created in the correct order.
5. **Use IF EXISTS / IF NOT EXISTS**: Make scripts resilient to different states.

### Example Migration

Here's an example of a simple migration:

```sql
-- 0002_add_user_settings.sql
CREATE TABLE IF NOT EXISTS user_settings (
    user_id TEXT NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    PRIMARY KEY (user_id, setting_key),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_settings_key ON user_settings(setting_key);
```

And the corresponding down script:

```sql
-- 0002_add_user_settings.down.sql
DROP INDEX IF EXISTS idx_user_settings_key;
DROP TABLE IF EXISTS user_settings;
```

## Migration Tracking

The migration system keeps track of which migrations have been applied in a table called `migrations` in the database. This table stores:

- `version`: The migration version number
- `name`: The migration name
- `applied_at`: The timestamp when the migration was applied

This allows the system to apply only pending migrations and roll back migrations in the correct order.