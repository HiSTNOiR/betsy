# PROJECT STRUCTURE

> 🤖 created by the bot
> ✅ finalised  
> 🧪 needs testing  
> 🛑 needs fixing  
> 👉 i am here  
> 📄 created
> 🧠 contemplating if this is needed

```md
betsy_bot/
│
├── 📄 core/
│   ├── 📄 __init__.py
│   ├── ✅ config.py
│   ├── ✅ errors.py
│   └── ✅ logging.py
│
├── 📄 db/
│   ├── 📄 __init__.py
│   ├── 🤖 bot.db
│   ├── ✅ database.py
│   │── 📄 backups/
│   │   └── 📄 __init__.py
│   └── 📄 migrations/
│       ├── ✅ schema.sql
│       └── ✅ seed.sql
│
├── 📄 docs/
│
├── 📄 event_bus/           # Event distribution 👉 THE CORE OF THE BOT
│   ├── 📄 __init__.py
│   ├── 📄 bus.py           # Main bus
│   └── 📄 registry.py      # Subscription registry
│
├── 📄 events/              # Event definitions
│   ├── 📄 __init__.py
│   ├── 📄 base.py
│   ├── 📄 obs.py           # e.g. a source is disabled either manually by the streamer, or through an obs_action sequence
│   ├── 📄 twitch.py        # i.e. channel reward redemption, cheers/bits, subscriptions, raids, hosts, gifted subs, !commands
│   └── 📄 user.py          # Tracks user stuff that isn't platform-specific
│
├── 📄 kivy/
│   ├── 📄 __init__.py
│   ├── 📄 screens/
│   │   └── 📄 __init__.py
│   ├── 📄 widgets/
│   │   └── 📄 __init__.py
│   └── 📄 utils/
│       └── 📄 __init__.py
│
├── 📄 logs/
│
├── 📄 models/              # Db models used by events
│   ├── 📄 __init__.py
│   ├── 📄 user.py
│   ├── 📄 command.py
│   └── 📄 message.py
│
├── 📄 plugins/              # Extends the base functionality
│   ├── 📄 __init__.py
│   ├── 🧠 base.py
│   └── 🧠 registry.py      # e.g. DOMT, duel system, shop system
│
├── 📄 processors/            # Transform events
│   ├── 📄 __init__.py
│   ├── 📄 base.py
│   ├── 📄 command_parser.py
│   └── 📄 sanitiser.py
│
├── 📄 publishers/            # Generate events
│   ├── 📄 __init__.py
│   ├── 📄 base.py
│   ├── 📄 obs_reader.py
│   └── 📄 twitch_reader.py
│
├── 📄 subscribers/         # React to events
│   ├── 📄 __init__.py
│   ├── 📄 base.py
│   ├── 📄 obs_handler.py
│   └── 📄 twitch_handler.py     # Sends messages to Twitch
│
├── 📄 tests/
│   ├── 📄 __init____.py
│   ├── ✅ test_config.py
│   ├── ✅ test_database.py
│   ├── ✅ test_errors.py
│   └── ✅ test_logging.py
│
├── 📄 utils/ 
│   ├── 📄 __init__.py
│   ├── 📄 threadpool.py
│   ├── 📄 locks.py
│   └── ✅ platform_connections.py  # Thread-safe singleton handling
│
├── 📄 venv/
│
├── 📄 web/                   # Web application components
│   ├── 📄 __init__.py
│   ├── 📄 routes/ 
│   │   └── 📄 __init__.py
│   └── 📄 static/
│       ├── 📄 js/ 
│       ├── 📄 css/
│       └── 📄 templates/
│
├── ✅ .env
├── ✅ .gitignore
├── ✅ .prettierrc
├── ✅ CHANGELOG.md           # TODO update once app is released
├── ✅ LICENSE                # MIT Licence
├── 📄 main.py                # Entry point
├── ✅ README.md
└── ✅ requirements.txt
```
