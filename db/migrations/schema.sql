-- Stream statistics
CREATE TABLE IF NOT EXISTS stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count INTEGER NOT NULL DEFAULT 0,
    total_duration_minutes INTEGER NOT NULL DEFAULT 0,
    avg_duration_minutes INTEGER NOT NULL DEFAULT 0,
    last_stream_date TEXT,
    most_streamed_category TEXT,
    most_streamed_category_minutes INTEGER NOT NULL DEFAULT 0
);

-- Users
-- TODO remove 'untouchable' rank
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    twitch_user_id TEXT UNIQUE,
    twitch_username TEXT,
    discord_username TEXT,
    youtube_username TEXT,
    rank TEXT CHECK (rank IN ('viewer', 'vip', 'subscriber', 'moderator', 'broadcaster', 'bot_admin', 'untouchable')) DEFAULT 'viewer',
    points INTEGER NOT NULL DEFAULT 0,
    points_gifted INTEGER NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL,
    last_seen TEXT,
    weapon_id INTEGER REFERENCES weapons(id) ON DELETE SET NULL,
    weapon_durability INTEGER DEFAULT 10 CHECK (weapon_durability >= 0 AND weapon_durability <= 10),
    weapon_mod_id INTEGER REFERENCES weapon_mods(id) ON DELETE SET NULL,
    armour_id INTEGER REFERENCES armour(id) ON DELETE SET NULL,
    armour_durability INTEGER DEFAULT 10 CHECK (armour_durability >= 0 AND armour_durability <= 10),
    armour_mod_id INTEGER REFERENCES armour_mods(id) ON DELETE SET NULL,
    duel_wins INTEGER NOT NULL DEFAULT 0,
    duel_loses INTEGER NOT NULL DEFAULT 0
);

-- User viewing habits
CREATE TABLE IF NOT EXISTS user_viewing_habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    avg_session_minutes INTEGER NOT NULL DEFAULT 0,
    most_active_day TEXT,
    most_active_hour INTEGER,
    avg_messages_per_stream INTEGER NOT NULL DEFAULT 0,
    lurker_ratio REAL NOT NULL DEFAULT 0, -- 0 = always chatting, 1 = pure lurker
    favorite_category TEXT,
    bits_spent INTEGER NOT NULL DEFAULT 0,
    rewards_redeemed INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- User inventory: toys
CREATE TABLE IF NOT EXISTS user_toys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    toy_id INTEGER NOT NULL,
    date_acquired TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (toy_id) REFERENCES toys(id) ON DELETE CASCADE,
    UNIQUE (user_id, toy_id)
);

-- User inventory: cards
CREATE TABLE IF NOT EXISTS user_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    card_name TEXT NOT NULL,
    date_acquired TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- User weapon mods
CREATE TABLE IF NOT EXISTS user_weapon_mods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    mod_id INTEGER NOT NULL,
    date_applied TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mod_id) REFERENCES weapon_mods(id) ON DELETE CASCADE,
    UNIQUE (user_id, mod_id)
);

-- User armour mods
CREATE TABLE IF NOT EXISTS user_armour_mods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    mod_id INTEGER NOT NULL,
    date_applied TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mod_id) REFERENCES armour_mods(id) ON DELETE CASCADE,
    UNIQUE (user_id, mod_id)
);

-- OBS actions
CREATE TABLE IF NOT EXISTS obs_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    scene_name TEXT,
    source_name TEXT,
    source_id TEXT,
    input_name TEXT,
    filter_name TEXT,
    state TEXT CHECK (state IN ('enabled', 'disabled')),
    position_x INTEGER,
    position_y INTEGER,
    size_width INTEGER,
    size_height INTEGER,
    text TEXT,
    animate_params TEXT, -- JSON string with animation parameters
    transform_params TEXT, -- JSON string with transform parameters
    duration_ms INTEGER DEFAULT 0, -- Duration of action in milliseconds
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Action sequences
CREATE TABLE IF NOT EXISTS action_sequences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    trigger_type TEXT NOT NULL CHECK (trigger_type IN ('bits', 'reward', 'command', 'discord', 'emote_combo', 'shield_mode')),
    trigger_value TEXT, -- Bits amount, reward ID, command name, etc.
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Sequence actions (junction table)
CREATE TABLE IF NOT EXISTS sequence_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER NOT NULL,
    action_id INTEGER NOT NULL,
    order_index INTEGER NOT NULL, -- Order of execution in sequence
    delay_ms INTEGER DEFAULT 0, -- Delay before executing this action
    FOREIGN KEY (sequence_id) REFERENCES action_sequences(id) ON DELETE CASCADE,
    FOREIGN KEY (action_id) REFERENCES obs_actions(id) ON DELETE CASCADE,
    UNIQUE (sequence_id, order_index)
);

-- Commands
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    alias_1 TEXT,
    alias_2 TEXT, 
    description TEXT,
    response TEXT, -- Response text to send to chat
    action_sequence_id INTEGER, -- OBS action sequence
    permission_level TEXT CHECK (permission_level IN ('viewer', 'vip', 'subscriber', 'moderator', 'broadcaster', 'bot_admin')) DEFAULT 'viewer',
    restricted_to_user_id INTEGER DEFAULT NULL,
    cooldown_seconds INTEGER DEFAULT 3,
    total_uses INTEGER NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL,
    FOREIGN KEY (action_sequence_id) REFERENCES action_sequences(id) ON DELETE SET NULL,
    FOREIGN KEY (restricted_to_user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (name),
    UNIQUE (alias_1),
    UNIQUE (alias_2)
);

-- Twitch bits
CREATE TABLE IF NOT EXISTS twitch_bits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bits INTEGER, -- The number of bits
    description TEXT,
    action_sequence_id INTEGER,
    uses INTEGER NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL,
    FOREIGN KEY (action_sequence_id) REFERENCES action_sequences(id) ON DELETE SET NULL
);

-- Twitch rewards
CREATE TABLE IF NOT EXISTS twitch_rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reward_id TEXT UNIQUE NOT NULL, -- Twitch ID for the reward
    name TEXT NOT NULL,
    description TEXT,
    cost INTEGER DEFAULT 0,
    is_enabled BOOLEAN DEFAULT 1,
    background_color TEXT,
    is_user_input_required BOOLEAN DEFAULT 0,
    user_input_prompt TEXT,
    max_per_stream INTEGER DEFAULT NULL,
    max_per_user_per_stream INTEGER DEFAULT NULL,
    global_cooldown_seconds INTEGER DEFAULT NULL,
    action_sequence_id INTEGER,
    handler_type TEXT DEFAULT 'default', -- 'default', 'custom', 'command', etc.
    handler_config TEXT, -- JSON string with handler configuration
    auto_fulfill BOOLEAN DEFAULT 1,
    total_uses INTEGER NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL,
    last_updated TEXT,
    FOREIGN KEY (action_sequence_id) REFERENCES action_sequences(id) ON DELETE SET NULL
);

-- Reward redemption history
CREATE TABLE IF NOT EXISTS reward_redemptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reward_id TEXT NOT NULL,
    user_id TEXT NOT NULL, 
    redeemed_at TEXT NOT NULL,
    status TEXT DEFAULT 'fulfilled', -- 'fulfilled', 'cancelled', 'pending'
    user_input TEXT,
    FOREIGN KEY (reward_id) REFERENCES twitch_rewards(reward_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(twitch_user_id) ON DELETE CASCADE
);

-- Reward handler configurations
CREATE TABLE IF NOT EXISTS reward_handlers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handler_name TEXT UNIQUE NOT NULL,
    handler_description TEXT,
    enabled BOOLEAN DEFAULT 1,
    config_schema TEXT, -- JSON schema for the handler configuration
    date_added TEXT NOT NULL
);

-- Armour
CREATE TABLE IF NOT EXISTS armour (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    cost INTEGER NOT NULL,
    date_added TEXT NOT NULL
);

-- Weapons
CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    cost INTEGER NOT NULL,
    date_added TEXT NOT NULL
);

-- Armour mods
CREATE TABLE IF NOT EXISTS armour_mods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    adjective TEXT NOT NULL,
    cost INTEGER NOT NULL,
    date_added TEXT NOT NULL
);

-- Weapon mods
CREATE TABLE IF NOT EXISTS weapon_mods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    adjective TEXT NOT NULL,
    cost INTEGER NOT NULL,
    date_added TEXT NOT NULL
);

-- Toys
CREATE TABLE IF NOT EXISTS toys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    cost INTEGER NOT NULL,
    command TEXT, -- Associated command to use the toy
    date_added TEXT NOT NULL
);

-- Duels
CREATE TABLE IF NOT EXISTS duels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenger INTEGER NOT NULL,
    opponent INTEGER NOT NULL,
    pot_size INTEGER NOT NULL,
    winner INTEGER,
    was_draw BOOLEAN NOT NULL DEFAULT 0,
    was_underdog_win BOOLEAN NOT NULL DEFAULT 0,
    environment_id INTEGER NOT NULL,
    duel_date TEXT NOT NULL,
    FOREIGN KEY (challenger) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (opponent) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (winner) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (environment_id) REFERENCES duel_environments(id) ON DELETE CASCADE
);

-- Duel environments
CREATE TABLE IF NOT EXISTS duel_environments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

-- Environment bonuses and penalties
CREATE TABLE IF NOT EXISTS environment_effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    environment_id INTEGER NOT NULL,
    item_type TEXT NOT NULL CHECK (item_type IN ('armour', 'armour_mod', 'weapon', 'weapon_mod')),
    item_name TEXT NOT NULL,
    effect_type TEXT NOT NULL CHECK (effect_type IN ('boon', 'bust')),
    FOREIGN KEY (environment_id) REFERENCES duel_environments(id) ON DELETE CASCADE,
    UNIQUE (environment_id, item_type, item_name)
);

-- DOMT Cards
CREATE TABLE IF NOT EXISTS domt_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL, -- OBS source reference
    description TEXT NOT NULL,
    description_english TEXT, -- Explains what the streamer needs to do
    is_drawn BOOLEAN NOT NULL DEFAULT 0, -- Whether the card has been drawn in the current deck
    is_retainable BOOLEAN NOT NULL DEFAULT 0, -- Whether the card can be kept by a user
    action_sequence_id INTEGER,
    times_drawn INTEGER NOT NULL DEFAULT 0, -- Total times this card has been drawn
    deck_resets INTEGER NOT NULL DEFAULT 0, -- How many times deck has been reset after this card was drawn
    last_drawn_date TEXT, -- When this card was last drawn
    date_added TEXT NOT NULL,
    FOREIGN KEY (action_sequence_id) REFERENCES action_sequences(id) ON DELETE SET NULL
);

-- Emote combo easter eggs
CREATE TABLE IF NOT EXISTS emote_combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    emote_sequence TEXT NOT NULL, -- Comma-separated emote names in order
    users_required INTEGER NOT NULL DEFAULT 3, -- Number of different users needed
    reward_xp INTEGER NOT NULL DEFAULT 100,
    action_sequence_id INTEGER,
    times_triggered INTEGER NOT NULL DEFAULT 0,
    date_added TEXT NOT NULL,
    FOREIGN KEY (action_sequence_id) REFERENCES action_sequences(id) ON DELETE SET NULL
);

-- Bot stats and status
CREATE TABLE IF NOT EXISTS bot_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_date TEXT NOT NULL,
    uptime_seconds INTEGER NOT NULL DEFAULT 0,
    commands_processed INTEGER NOT NULL DEFAULT 0,
    errors_encountered INTEGER NOT NULL DEFAULT 0,
    chat_messages_sent INTEGER NOT NULL DEFAULT 0,
    obs_actions_triggered INTEGER NOT NULL DEFAULT 0,
    xp_given INTEGER NOT NULL DEFAULT 0, -- XP given through lurking, chatting, rewards etc
    xp_spent INTEGER NOT NULL DEFAULT 0 -- XP spent by users on items, duels etc
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_twitch_username ON users(twitch_username);
CREATE INDEX IF NOT EXISTS idx_commands_name ON commands(name);
CREATE INDEX IF NOT EXISTS idx_commands_aliases ON commands(alias_1, alias_2);
CREATE INDEX IF NOT EXISTS idx_duels_users ON duels(challenger, opponent);
CREATE INDEX IF NOT EXISTS idx_duels_date ON duels(duel_date);
CREATE INDEX IF NOT EXISTS idx_user_mods ON user_weapon_mods(user_id);
CREATE INDEX IF NOT EXISTS idx_user_armour_mods ON user_armour_mods(user_id);
CREATE INDEX IF NOT EXISTS idx_user_toys ON user_toys(user_id);
CREATE INDEX IF NOT EXISTS idx_user_cards ON user_cards(user_id);
CREATE INDEX IF NOT EXISTS idx_env_effects ON environment_effects(environment_id, item_type);