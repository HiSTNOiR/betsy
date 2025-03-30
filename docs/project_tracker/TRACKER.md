# PROJECT STRUCTURE

> ✅ finalised  
> 🧪 needs testing  
> 🛑 borked  
> 👉 i am here  
> 📄 created

```md
betsy/
│
├── 📄 bot/
│   ├── 📄 __init__.py
│   │
│   ├── 📄 core/
│   │   ├── 🧪 __init__.py
│   │   ├── 🧪 app.py                      # Main application entry point
│   │   ├── 🧪 constants.py                # Global constants
│   │   ├── 🧪 errors.py                   # Error hierarchy
│   │   ├── 🧪 logging.py                  # Logging configuration
│   │   │
│   │   ├── 📄 config/                     # Configuration management
│   │   │   ├── 🧪 __init__.py
│   │   │   ├── ✅ config.py               # Configuration manager
│   │   │   └── 🧪 validators.py           # Configuration validators
│   │   │
│   │   ├── 📄 events/                     # Event system
│   │   │   ├── 🧪 __init__.py
│   │   │   ├── ✅ base.py                 # Base event classes
│   │   │   ├── ✅ dispatcher.py           # Event dispatcher
│   │   │   ├── ✅ registry.py             # Event registry
│   │   │   └── ✅ handlers.py             # Global event handlers
│   │   │
│   │   └── 📄 lifecycle/                  # Application lifecycle
│   │       ├── 🧪 __init__.py
│   │       ├── ✅ manager.py              # Lifecycle manager
│   │       └── ✅ hooks.py                # Lifecycle hooks
│   │
│   ├── 📄 commands/                       # Command system
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base command classes
│   │   ├── context.py                  # Command context
│   │   ├── handler.py                  # Command handler
│   │   ├── parser.py                   # Command parser
│   │   ├── registry.py                 # Command registry
│   │   ├── cooldown.py                 # Command cooldowns
│   │   ├── permissions.py              # Command permissions
│   │   └── decorators.py               # Command decorators
│   │
│   ├── 📄 db/                             # Database layer
│   │   ├── 📄 __init__.py
│   │   ├── connection.py               # Database connection management
│   │   ├── migrations.py               # Database migrations
│   │   ├── 📄 schema.sql                  # Database schema
│   │   │
│   │   ├── 📄 models/                     # Data models
│   │   │   ├── 📄 __init__.py
│   │   │   ├── base.py                 # Base model
│   │   │   ├── user.py                 # User model
│   │   │   ├── command.py              # Command model
│   │   │   ├── item.py                 # Item model
│   │   │   ├── inventory.py            # Inventory model
│   │   │   └── stream.py               # Stream model
│   │   │
│   │   └── 📄 repositories/               # Data access layer
│   │       ├── 📄 __init__.py
│   │       ├── base.py                 # Base repository
│   │       ├── user_repository.py      # User repository
│   │       ├── command_repository.py   # Command repository
│   │       ├── item_repository.py      # Item repository
│   │       └── stream_repository.py    # Stream repository
│   │
│   ├── 📄 middleware/                     # Middleware system
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base middleware
│   │   ├── pipeline.py                 # Middleware pipeline
│   │   │
│   │   ├── 📄 commands/                   # Command middleware
│   │   │   ├── 📄 __init__.py
│   │   │   ├── permission.py           # Permission middleware
│   │   │   ├── cooldown.py             # Cooldown middleware
│   │   │   ├── logging.py              # Logging middleware
│   │   │   ├── validation.py           # Validation middleware
│   │   │   └── error.py                # Error handling middleware
│   │   │
│   │   ├── 📄 events/                     # Event middleware
│   │   │   ├── 📄 __init__.py
│   │   │   ├── logging.py              # Logging middleware
│   │   │   ├── validation.py           # Validation middleware
│   │   │   ├── filtering.py            # Filtering middleware
│   │   │   └── error.py                # Error handling middleware
│   │   │
│   │   └── 📄 features/                   # Feature middleware
│   │       ├── 📄 __init__.py
│   │       ├── points.py               # Points middleware
│   │       ├── shop.py                 # Shop middleware
│   │       ├── inventory.py            # Inventory middleware
│   │       └── duel.py                 # Duel middleware
│   │
│   ├── 📄 platforms/                      # Platform integrations
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base platform
│   │   │
│   │   ├── 📄 twitch/                     # Twitch integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── client.py               # Twitch client
│   │   │   ├── auth.py                 # Twitch auth
│   │   │   ├── chat.py                 # Twitch chat
│   │   │   ├── events.py               # Twitch events
│   │   │   ├── api.py                  # Twitch API
│   │   │   └── handlers.py             # Twitch event handlers
│   │   │
│   │   ├──📄  obs/                        # OBS integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── client.py               # OBS client
│   │   │   ├── scenes.py               # Scene management
│   │   │   ├── sources.py              # Source management
│   │   │   ├── filters.py              # Filter management
│   │   │   ├── audio.py                # Audio management
│   │   │   └── events.py               # OBS events
│   │   │
│   │   ├── 📄 discord/                    # Discord integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── client.py               # Discord client
│   │   │   ├── commands.py             # Discord commands
│   │   │   ├── events.py               # Discord events
│   │   │   └── sync.py                 # Discord synchronisation
│   │   │
│   │   ├── 📄 youtube/                    # YouTube integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── client.py               # YouTube client
│   │   │   ├── chat.py                 # YouTube chat
│   │   │   ├── events.py               # YouTube events
│   │   │   └── api.py                  # YouTube API
│   │   │
│   │   └── 📄 bitfocus/                   # BitFocus Companion integration
│   │       ├── 📄 __init__.py
│   │       ├── client.py               # BitFocus client
│   │       ├── actions.py              # BitFocus actions
│   │       └── events.py               # BitFocus events
│   │
│   ├── 📄 features/                       # Feature modules
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base feature
│   │   ├── manager.py                  # Feature manager
│   │   │
│   │   ├── 📄 points/                     # Points system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Points feature
│   │   │   ├── manager.py              # Points manager
│   │   │   ├── commands.py             # Points commands
│   │   │   ├── events.py               # Points events
│   │   │   ├── repository.py           # Points repository
│   │   │   └── middleware.py           # Points middleware
│   │   │
│   │   ├── 📄 shop/                       # Shop system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Shop feature
│   │   │   ├── manager.py              # Shop manager
│   │   │   ├── commands.py             # Shop commands
│   │   │   ├── events.py               # Shop events
│   │   │   ├── repository.py           # Shop repository
│   │   │   ├── middleware.py           # Shop middleware
│   │   │   │
│   │   │   └── 📄 items/                  # Shop items
│   │   │       ├── 📄 __init__.py
│   │   │       ├── base.py             # Base item
│   │   │       ├── weapon.py           # Weapon items
│   │   │       ├── armour.py           # Armour items
│   │   │       ├── toy.py              # Toy items
│   │   │       └── mod.py              # Modification items
│   │   │
│   │   ├── 📄 inventory/                  # Inventory system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Inventory feature
│   │   │   ├── manager.py              # Inventory manager
│   │   │   ├── commands.py             # Inventory commands
│   │   │   ├── events.py               # Inventory events
│   │   │   ├── repository.py           # Inventory repository
│   │   │   └── middleware.py           # Inventory middleware
│   │   │
│   │   ├── 📄 duel/                       # Duel system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Duel feature
│   │   │   ├── manager.py              # Duel manager
│   │   │   ├── commands.py             # Duel commands
│   │   │   ├── events.py               # Duel events
│   │   │   ├── repository.py           # Duel repository
│   │   │   ├── middleware.py           # Duel middleware
│   │   │   ├── calculator.py           # Duel calculator
│   │   │   └── environment.py          # Duel environments
│   │   │
│   │   ├── 📄 domt/                       # Deck of Many Things
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # DOMT feature
│   │   │   ├── manager.py              # DOMT manager
│   │   │   ├── commands.py             # DOMT commands
│   │   │   ├── events.py               # DOMT events
│   │   │   ├── repository.py           # DOMT repository
│   │   │   ├── middleware.py           # DOMT middleware
│   │   │   ├── cards.py                # Card definitions
│   │   │   └── effects.py              # Card effects
│   │   │
│   │   ├── 📄 obs_actions/                # OBS action system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # OBS Actions feature
│   │   │   ├── manager.py              # Action manager
│   │   │   ├── commands.py             # Action commands
│   │   │   ├── events.py               # Action events
│   │   │   ├── repository.py           # Action repository
│   │   │   ├── middleware.py           # Action middleware
│   │   │   ├── triggers.py             # Action triggers
│   │   │   ├── sequences.py            # Action sequences
│   │   │   │
│   │   │   └── 📄 actions/                # Action implementations
│   │   │       ├── 📄 __init__.py
│   │   │       ├── base.py             # Base action
│   │   │       ├── scene.py            # Scene actions
│   │   │       ├── source.py           # Source actions
│   │   │       ├── filter.py           # Filter actions
│   │   │       ├── audio.py            # Audio actions
│   │   │       ├── text.py             # Text actions
│   │   │       └── animation.py        # Animation actions
│   │   │
│   │   ├── 📄 easter_eggs/                # Easter eggs
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Easter Eggs feature
│   │   │   ├── manager.py              # Easter Eggs manager
│   │   │   ├── commands.py             # Easter Eggs commands
│   │   │   ├── events.py               # Easter Eggs events
│   │   │   ├── repository.py           # Easter Eggs repository
│   │   │   ├── middleware.py           # Easter Eggs middleware
│   │   │   ├── emote_combos.py         # Emote combos
│   │   │   └── special_commands.py     # Special commands
│   │   │
│   │   ├── 📄 dungeon/                    # Dungeon/raid system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Dungeon feature
│   │   │   ├── manager.py              # Dungeon manager
│   │   │   ├── commands.py             # Dungeon commands
│   │   │   ├── events.py               # Dungeon events
│   │   │   ├── repository.py           # Dungeon repository
│   │   │   ├── middleware.py           # Dungeon middleware
│   │   │   ├── boss.py                 # Boss definitions
│   │   │   └── rewards.py              # Dungeon rewards
│   │   │
│   │   ├── 📄 betsy_vault/                # Betsy Vault feature
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Betsy Vault feature
│   │   │   ├── manager.py              # Vault manager
│   │   │   ├── commands.py             # Vault commands
│   │   │   ├── events.py               # Vault events
│   │   │   ├── repository.py           # Vault repository
│   │   │   └── middleware.py           # Vault middleware
│   │   │
│   │   ├── 📄 shield_mode/                # Shield Mode feature
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Shield Mode feature
│   │   │   ├── manager.py              # Shield Mode manager
│   │   │   ├── commands.py             # Shield Mode commands
│   │   │   ├── events.py               # Shield Mode events
│   │   │   └── actions.py              # Shield Mode actions
│   │   │
│   │   ├── 📄 todo/                       # To-Do system
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Todo feature
│   │   │   ├── manager.py              # Todo manager
│   │   │   ├── commands.py             # Todo commands
│   │   │   ├── events.py               # Todo events
│   │   │   └── repository.py           # Todo repository
│   │   │
│   │   ├── 📄 chat_log/                   # Chat logging
│   │   │   ├── 📄 __init__.py
│   │   │   ├── feature.py              # Chat Log feature
│   │   │   ├── manager.py              # Log manager
│   │   │   ├── commands.py             # Log commands
│   │   │   ├── events.py               # Log events
│   │   │   └── repository.py           # Log repository
│   │   │
│   │   └── 📄 ai/                         # AI integration
│   │       ├── 📄 __init__.py
│   │       ├── feature.py              # AI feature
│   │       ├── manager.py              # AI manager
│   │       ├── commands.py             # AI commands
│   │       ├── events.py               # AI events
│   │       ├── repository.py           # AI repository
│   │       ├── llm.py                  # Language model integration
│   │       └── chat.py                 # AI chat functionality
│   │
│   ├── 📄 ui/                             # User interface systems
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base UI
│   │   │
│   │   ├── 📄 cli/                        # Command-line interface
│   │   │   ├── 📄 __init__.py
│   │   │   ├── app.py                  # CLI application
│   │   │   ├── commands.py             # CLI commands
│   │   │   └── formatter.py            # CLI output formatter
│   │   │
│   │   ├── 📄 kivy/                       # Kivy GUI application
│   │   │   ├── 📄 __init__.py
│   │   │   ├── app.py                  # Kivy application
│   │   │   ├── main.py                 # Main Kivy entry point
│   │   │   │
│   │   │   ├── 📄 screens/                # Kivy screens
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── base.py             # Base screen
│   │   │   │   ├── dashboard.py        # Dashboard screen
│   │   │   │   ├── commands.py         # Commands screen
│   │   │   │   ├── shop.py             # Shop screen
│   │   │   │   ├── users.py            # Users screen
│   │   │   │   ├── settings.py         # Settings screen
│   │   │   │   └── logs.py             # Logs screen
│   │   │   │
│   │   │   ├── 📄 widgets/                # Kivy widgets
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── base.py             # Base widgets
│   │   │   │   ├── cards.py            # Card widgets
│   │   │   │   ├── charts.py           # Chart widgets
│   │   │   │   ├── lists.py            # List widgets
│   │   │   │   └── modals.py           # Modal widgets
│   │   │   │
│   │   │   └── 📄 styles/                 # Kivy styles
│   │   │       ├── 📄 __init__.py
│   │   │       ├── theme.py            # Theme definition
│   │   │       └── colours.py          # Colour definitions
│   │   │
│   │   ├── 📄 web/                        # Web application
│   │   │   ├── 📄 __init__.py
│   │   │   ├── app.py                  # Web app
│   │   │   ├── routes.py               # Web routes
│   │   │   ├── auth.py                 # Web auth
│   │   │   │
│   │   │   ├── 📄 api/                    # Web API
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── routes.py           # API routes
│   │   │   │   ├── users.py            # User endpoints
│   │   │   │   ├── commands.py         # Command endpoints
│   │   │   │   ├── stats.py            # Stats endpoints
│   │   │   │   └── settings.py         # Settings endpoints
│   │   │   │
│   │   │   ├── 📄 templates/              # Web templates
│   │   │   │   ├── base.html           # Base template
│   │   │   │   ├── dashboard.html      # Dashboard template
│   │   │   │   ├── login.html          # Login template
│   │   │   │   └── settings.html       # Settings template
│   │   │   │
│   │   │   └── 📄 static/                 # Web static files
│   │   │       ├── css/                # CSS files
│   │   │       ├── js/                 # JavaScript files
│   │   │       └── img/                # Image files
│   │   │
│   │   └── 📄 mobile/                     # Mobile app integration
│   │       ├── 📄 __init__.py
│   │       ├── app.py                  # Mobile app
│   │       └── api.py                  # Mobile API client
│   │
│   ├── 📄 visualisation/                  # Data visualisation
│   │   ├── 📄 __init__.py
│   │   ├── base.py                     # Base visualisation
│   │   ├── charts.py                   # Chart generation
│   │   ├── reports.py                  # Report generation
│   │   ├── metrics.py                  # Metrics calculation
│   │   └── dashboard.py                # Dashboard components
│   │
│   └── 📄 utils/                          # Utility modules
│       ├── ✅ __init__.py
│       ├── cooldown.py                 # Cooldown utilities
│       ├── ✅ formatting.py               # Text formatting
│       ├── parsing.py                  # Text parsing
│       ├── permissions.py              # Permission utilities
│       ├── queue.py                    # Queue implementations
│       ├── random.py                   # Random utilities
│       ├── sanitisation.py             # Input sanitisation
│       ├── ✅ security.py                 # Security utilities
│       ├── throttling.py               # Rate limiting
│       ├── ✅ time.py                     # Time utilities
│       └── validation.py               # Input validation
│
├── 📄 docs/                               # Documentation
│   ├── index.md                        # Documentation index
│   │
│   ├── api/                            # API documentation
│   │   └── index.md                    # API documentation index
│   │
│   ├── 📄 features/                       # Feature documentation
│   │   ├── points.md                   # Points system docs
│   │   ├── shop.md                     # Shop system docs
│   │   ├── duel.md                     # Duel system docs
│   │   ├── domt.md                     # DOMT docs
│   │   └── obs_actions.md              # OBS Actions docs
│   │
│   ├── guides/                         # User guides
│   │   ├── installation.md             # Installation guide
│   │   ├── configuration.md            # Configuration guide
│   │   └── commands.md                 # Commands reference
│   │
│   ├── dev/                            # Developer documentation
│   │   ├── architecture.md             # Architecture overview
│   │   ├── contributing.md             # Contributing guide
│   │   └── testing.md                  # Testing guide
│   │
│   └── 📄 refs/                           # Reference documentation
│       ├── twitch/                     # Twitch API references
│       ├── obs/                        # OBS API references
│       └── database/                   # Database schema reference
│
├── 📄 scripts/                            # Utility scripts
│   ├── setup.py                        # Setup script
│   ├── backup.py                       # Database backup script
│   ├── migrate.py                      # Database migration script
│   └── bootstrap.py                    # Environment bootstrap script
│
├── 📄 tests/
│   ├── 📄 __init__.py
│   ├── ✅ run_tests.py
│   │
│   ├── 📄 unit/
│   │   ├── 📄 __init__.py
│   │   ├── test_commands.py
│   │   ├── test_features.py
│   │   ├── test_utils.py
│   │   │
│   │   ├── 📄 core/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── test_app_constants.py
│   │   │   ├── test_config_validators.py
│   │   │   ├── test_config.py
│   │   │   ├── test_errors.py
│   │   │   ├── test_logging.py
│   │   │   ├── test_lifecycle.py
│   │   │   ├── test_lifecycle_hooks.py
│   │   │   │
│   │   │   ├── 📄 config/
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── ✅ test_config.py
│   │   │   │   └── 📄 test_validators.py
│   │   │   │
│   │   │   ├── 📄 events/
│   │   │   │   ├── 📄 __init__.py
│   │   │   │   ├── ✅ test_base.py
│   │   │   │   ├── ✅ test_dispatcher.py
│   │   │   │   ├── ✅ test_handlers.py
│   │   │   │   └── ✅ test_registry.py
│   │   │   │
│   │   │   └── 📄 lifecycle/
│   │   │       ├── 📄 __init__.py
│   │   │       ├── ✅ test_hooks.py
│   │   │       └── ✅ test_manager.py
│   │   │
│   │   └── 📄 utils/
│   │       ├── 📄 __init__.py
│   │       ├── ✅ test_formatting.py
│   │       ├── ✅ test_security.py
│   │       └── ✅ test_time.py
│   │
│   ├── 📄 integration/                    # Integration tests
│   │   ├── 📄 __init__.py
│   │   ├── test_database.py            # Database integration tests
│   │   ├── test_twitch.py              # Twitch integration tests
│   │   └── test_obs.py                 # OBS integration tests
│   │
│   ├── 📄 e2e/                            # End-to-end tests
│   │   ├── 📄 __init__.py
│   │   ├── test_commands.py            # Command E2E tests
│   │   ├── test_shop.py                # Shop E2E tests
│   │   └── test_duel.py                # Duel E2E tests
│   │
│   └── 📄 mocks/                          # Test mocks
│       ├── 📄 __init__.py
│       ├── twitch.py                   # Twitch API mocks
│       ├── obs.py                      # OBS API mocks
│       └── db.py                       # Database mocks
│
├── 📄 data/                               # Data directory
│   ├── .gitignore                      # Gitignore for data files
│   └── README.md                       # Data directory README
│
├── 📄 logs/                               # Log directory
│   ├── .gitignore                      # Gitignore for log files
│   └── README.md                       # Log directory README
│
├── 📄 README.md                           # Project README
├── 📄 CHANGELOG.md                        # Project changelog
├── 📄 LICENSE                             # Project license
├── 📄 .env                                # Environment variables
├── 📄 .gitignore                          # Git ignore file
├── pyproject.toml                      # Poetry/PEP 518 config
├── setup.py                            # Package setup script
├── 📄 requirements.txt                    # Package requirements
└── tox.ini                             # Tox configuration (testing)
```
