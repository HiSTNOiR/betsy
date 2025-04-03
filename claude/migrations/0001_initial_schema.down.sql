-- Migration rollback: initial_schema
-- Created: 2025-04-03 12:00:00
-- Drops all tables created in the initial schema

-- Drop indexes first
DROP INDEX IF EXISTS idx_env_effects;
DROP INDEX IF EXISTS idx_user_cards;
DROP INDEX IF EXISTS idx_user_toys;
DROP INDEX IF EXISTS idx_user_armour_mods;
DROP INDEX IF EXISTS idx_user_mods;
DROP INDEX IF EXISTS idx_duels_date;
DROP INDEX IF EXISTS idx_duels_users;
DROP INDEX IF EXISTS idx_commands_aliases;
DROP INDEX IF EXISTS idx_commands_name;
DROP INDEX IF EXISTS idx_users_twitch_username;

-- Drop tables in reverse order to handle dependencies
DROP TABLE IF EXISTS bot_stats;
DROP TABLE IF EXISTS emote_combos;
DROP TABLE IF EXISTS domt_cards;
DROP TABLE IF EXISTS environment_effects;
DROP TABLE IF EXISTS duel_environments;
DROP TABLE IF EXISTS duels;
DROP TABLE IF EXISTS toys;
DROP TABLE IF EXISTS weapon_mods;
DROP TABLE IF EXISTS armour_mods;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS armour;
DROP TABLE IF EXISTS twitch_rewards;
DROP TABLE IF EXISTS twitch_bits;
DROP TABLE IF EXISTS commands;
DROP TABLE IF EXISTS sequence_actions;
DROP TABLE IF EXISTS action_sequences;
DROP TABLE IF EXISTS obs_actions;
DROP TABLE IF EXISTS user_armour_mods;
DROP TABLE IF EXISTS user_weapon_mods;
DROP TABLE IF EXISTS user_cards;
DROP TABLE IF EXISTS user_toys;
DROP TABLE IF EXISTS user_viewing_habits;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS stream;