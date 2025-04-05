# PROJECT STRUCTURE

> ✅ finalised  
> 🧪 needs testing  
> 🛑 needs fixing  
> 👉 i am here  
> 📄 created

```md
betsy_bot/
│
├── 📄 core/
│   ├── 📄 __init__.py
│   ├── ✅ config.py
│   ├── ✅ errors.py
│   └── ✅ logging.py
│
├── 📄 data/
│   ├── 📄 __init__.py
│   ├── ✅ bot.db
│   ├── ✅ database.py
│   ├── ✅ database_manager.py
│   └── 📄 backups/
│       └── 📄 __init__.py
│
├── 📄 subscribers/           # Components that listen for events
│   └── 📄 __init__.py
│
├── 📄 publishers/            # Components that create events
│   └── 📄 __init__.py
│
├── 📄 processors/            # Components that transform events
│   └── 📄 __init__.py
│
├── 📄 logs/
│
├── 📄 models/                # Data models used by events
│   └── 📄 __init__.py
│
├── 📄 utils/                 # Stateless utility functions
│   ├── 📄 __init__.py
│   └── ✅ platform_connections.py  # Thread-safe singleton handling
│
├── 📄 web/                   # Web application components
│   ├── 📄 __init__.py
│   ├── 📄 routes/            # Route handlers
│   │   └── 📄 __init__.py
│   └── 📄 static/            # Frontend assets
│       ├── 📄 js/            # JavaScript files
│       ├── 📄 css/           # CSS files
│       └── 📄 templates/     # HTML templates
│
├── 📄 kivy_app/              # Kivy application components
│   ├── 📄 __init__.py
│   ├── 📄 screens/           # Screen components
│   │   └── 📄 __init__.py
│   ├── 📄 widgets/           # Reusable widgets
│   │   └── 📄 __init__.py
│   └── 📄 utils/             # Kivy-specific utilities
│       └── 📄 __init__.py
│
├── 📄 migrations/            # Database management
│   ├── ✅ schema.sql         # Database schema
│   └── ✅ seed.sql           # Initial data
│
├── 📄 tests/
│   ├── 📄 __init____.py
│   ├── ✅ test_config.py
│   ├── ✅ test_database.py
│   ├── ✅ test_errors.py
│   └── ✅ test_logging.py
│
├── ✅ .env                   # Example environment variables
├── ✅ requirements.txt       # Dependencies
└── 📄 main.py                # Entry point
```
