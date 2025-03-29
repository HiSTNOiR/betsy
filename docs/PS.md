# PROJECT STRUCTURE

> ✅ good to go  
> 👉 working on now  
> 🧪 needs testing  
> 🛑 borked

```
betsy/
├── .env                 # Environment variables (from ENV.md template)
├── .gitignore
├── README.md
├── requirements.txt
├── main.py              # Entry point for the application
│
├── bot/
│   ├── __init__.py
│   │
│   ├── core/                 # Core modules
│   │   ├── __init__.py
│   │   ├── state.py          # Real-time state management and persistence
│   │   ├── bot.py            # Main bot class
│   │   ├── connections.py    # Initialises connections to OBS, Twitch etc
│   │   ├── constants.py      # Common constants and enums
│   │   ├── errors.py         # Custom exception classes
│   │   ├── logging.py        # Logging configuration
│   │   │
│   │   ├── config/            # Configuration modules
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # Configuration loader (reads from .env)
│   │   │   ├── dev.py         # Development config values
│   │   │   ├── prod.py        # Production config values
│   │   │   └── default.py     # Default config values
│   │   │
│   │   └── cache/
│   │       ├── __init__.py
│   │       ├── manager.py           # Core cache management logic (incl periodic db sync)
│   │       ├── command_cache.py
│   │       ├── item_cache.py        # Item and shop cache
│   │       ├── strategies.py        # Memory, file caching etc
│   │       └── user_cache.py
│   │
│   ├── middleware/                  
│   │   ├── __init__.py
│   │   ├── base.py          # Base middleware classes and infrastructure
│   │   ├── registry.py      # Middleware registration
│   │   ├── manager.py       # Middleware chain management
│   │   ├── points.py        # Points-specific middleware
│   │   ├── shop.py          # Shop-specific middleware
│   │   ├── validation.py    # Input validation middleware
│   │   ├── logging.py       # Logging middleware
│   │   ├── security.py      # Security middleware
│   │   └── throttling.py    # Rate limiting middleware
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── cooldown.py        # Command CD handling
│   │   ├── formatting.py      # Consistent formatting of user inputs
│   │   ├── parsing.py         # Type conversion, argument parsing, sanitisation etc
│   │   ├── permissions.py     # User access permissions
│   │   ├── queue.py           # Priority-based queue
│   │   ├── random_utils.py    # Random selection for duels, DOMT card drawing etc
│   │   ├── sanitisation.py    # Sanitising all inputs/outputs
│   │   ├── security.py        # Security utils, token handling etc
│   │   ├── throttling.py      # Bot throttling
│   │   ├── time_utils.py      # Timers, scheduling, duration calculations
│   │   └── validation.py      # Validating all inputs/outputs
│   │
│   ├── health/            # Bot health monitoring
│   │   ├── __init__.py
│   │   └── status.py
│   │
│   ├── metrics/            # Monitoring and analytics modules
│   │   ├── __init__.py
│   │   ├── analytics.py    # Analytics collection
│   │   └── reporters.py    # Visualisation or reporting tools
│   │
│   ├── db/                  # Database modules
│   │   ├── __init__.py
│   │   ├── ✅schema.sql     # DB schema
│   │   ├── connection.py    # DB connection manager
│   │   ├── users.py         # All CRUD operation for users
│   │   ├── items.py         # All CRUD operation for items
│   │   ├── commands.py      # All CRUD operation for commands
│   │   ├── duels.py         # All CRUD operation for duels
│   │   └── domt.py          # All CRUD operation for domt
│   │
│   ├── services/          # Service layers for external systems
│   │   ├── __init__.py
│   │   │
│   │   ├── twitch/            # Twitch integration
│   │   │   ├── __init__.py
│   │   │   ├── api.py         # Twitch API wrapper
│   │   │   ├── chat.py        # Chat message handling
│   │   │   ├── events.py      # Event subscription handling
│   │   │   ├── bits.py        # Bits and cheers handling
│   │   │   └── rewards.py     # Channel points handling
│   │   │
│   │   ├── obs/                 # OBS integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py        # OBS WebSocket client
│   │   │   ├── scenes.py        # Scene management
│   │   │   ├── sources.py       # Source management
│   │   │   ├── audio.py         # Audio management
│   │   │   ├── sequences.py     # Complex sequences of actions
│   │   │   ├── animations.py    # Source animation helpers
│   │   │   └── filters.py       # Filter management
│   │   │
│   │   └── discord/          # Future Discord integration
│   │       ├── __init__.py
│   │       └── client.py     # Discord client
│   │
│   ├── features/         # Feature modules
│   │   ├── __init__.py
│   │   ├── points.py     # XP/Points system
│   │   │
│   │   ├── shop/                   # Shop system
│   │   │   ├── __init__.py
│   │   │   ├── buy.py              # Handlers for buying items
│   │   │   ├── armour.py
│   │   │   ├── armour_mods.py
│   │   │   ├── toys.py
│   │   │   ├── weapons.py
│   │   │   └── weapons_mods.py
│   │   │
│   │   ├── duel_system/           # Duels system
│   │   │   ├── __init__.py
│   │   │   ├── environments.py    # Handling of duel environments
│   │   │   ├── seasonal.py        # Handling of seasonal affixes
│   │   │   ├── duel.py            # Core duel system modules
│   │   │   └── winner.py          # Calculating the winner
│   │   │
│   │   ├── inventory/           # Inventory management
│   │   │   ├── __init__.py
│   │   │   └── user_items.py    # Handling users' items
│   │   │
│   │   ├── domt/                  # Deck of Many Things
│   │   │   ├── __init__.py
│   │   │   ├── domt.py            # Core modules
│   │   │   └── cards/             # Handling of each card
│   │   │       ├── balance.py
│   │   │       ├── comet.py
│   │   │       ├── donjon.py
│   │   │       ├── euryale.py
│   │   │       ├── fates.py
│   │   │       ├── flames.py
│   │   │       ├── fool.py
│   │   │       ├── idiot.py
│   │   │       ├── jester.py
│   │   │       ├── key.py
│   │   │       ├── knight.py
│   │   │       ├── moon.py
│   │   │       ├── rogue.py
│   │   │       ├── ruin.py
│   │   │       ├── skull.py
│   │   │       ├── star.py
│   │   │       ├── sun.py
│   │   │       ├── talons.py
│   │   │       ├── throne.py
│   │   │       ├── vizier.py
│   │   │       └── void.py
│   │   │
│   │   └── easter_eggs/       # Easter eggs
│   │       ├── __init__.py
│   │       ├── one.py
│   │       ├── two.py
│   │       └── three.py
│   │
│   ├── commands/          # Handlers for default/core commands
│   │   ├── __init__.py
│   │   ├── general.py     # General commands (help, hello, addcmd etc.)
│   │   ├── points.py      # XP/Points commands
│   │   └── admin.py       # Bot admin commands (Hist only)
│   │
│   └── handlers/          # Event handlers
│       ├── __init__.py
│       ├── chat.py        # Chat message handlers
│       ├── bits.py        # Bits handlers
│       ├── rewards.py     # Channel point reward handlers
│       └── shields.py     # Shield mode handlers
│
├── scripts/           # Utility scripts
│   ├── setup_db.py    # Database setup script
│   ├── backup.py      # Backup utility
│   └── migrate.py     # Version migration script
│
├── tests/                 # Test modules
│   ├── __init__.py
│   ├── ✅ run_tests.py    # Runs all tests with 'test_' prefix
│   └── test_thing.py
│
├── migrations/        # Database migrations
│   ├── __init__.py
│   └── versions/      # Migration versions
│
└── gui/               # GUI implementation (Version 2.0)
    ├── __init__.py
    ├── kivy_app.py    # Kivy application
    ├── web_app.py     # Web application
    └── templates/     # Web templates
```
