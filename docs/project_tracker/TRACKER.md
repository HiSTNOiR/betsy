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
│   ├── 📄 app.py             # Application bootstrapping
│   ├── 📄 config.py          # Configuration management
│   ├── 📄 event_bus.py       # Central publish-subscribe event system
│   ├── 📄 errors.py          # Error handling
│   └── 📄 logging.py
│
├── 📄 subscribers/           # Components that listen for events
│   ├── 📄 __init__.py
│   ├── 📄 command_handler.py # Processes command events
│   ├── 📄 point_manager.py   # Manages user points
│   ├── 📄 duel_manager.py    # Handles duel events
│   ├── 📄 db_writer.py       # Persists events to the database
│   ├── 📄 twitch_sender.py   # Sends messages to Twitch
│   ├── 📄 obs_controller.py  # Controls OBS based on events
│   └── 📄 notification_manager.py  # Manages notifications to UIs
│
├── 📄 publishers/            # Components that create events
│   ├── 📄 __init__.py
│   ├── 📄 twitch_reader.py   # Reads from Twitch and publishes events
│   ├── 📄 timer.py           # Publishes time-based events
│   ├── 📄 db_reader.py       # Reads from DB and publishes events
│   ├── 📄 api_listener.py    # Listens for API calls and publishes events
│   ├── 📄 web_input.py       # Handles web UI input events
│   └── 📄 kivy_input.py      # Handles Kivy UI input events
│
├── 📄 processors/            # Components that transform events
│   ├── 📄 __init__.py
│   ├── 📄 sanitiser.py       # Sanitises user input
│   ├── 📄 validator.py       # Validates and transforms data
│   ├── 📄 formatter.py       # Formats output messages
│   └── 📄 command_parser.py  # Parses raw messages into command events
│
├── 📄 models/                # Data models used by events
│   ├── 📄 __init__.py
│   ├── 📄 message.py         # Message data structure
│   ├── 📄 command.py         # Command data structure
│   ├── 📄 item.py            # Item data structure
│   ├── 📄 user.py            # User data structure
│   └── 📄 duel.py            # Duel data structure
│
├── 📄 utils/                 # Stateless utility functions
│   ├── 📄 __init__.py
│   ├── 📄 text.py            # Text manipulation functions
│   └── 📄 time.py            # Time-related functions
│
├── 📄 web/                   # Web application components
│   ├── 📄 __init__.py
│   ├── 📄 server.py          # Web server (Flask/FastAPI)
│   ├── 📄 api.py             # REST API endpoints
│   ├── 📄 websocket.py       # WebSocket handler for real-time updates
│   ├── 📄 auth.py            # Authentication
│   ├── 📄 routes/            # Route handlers
│   │   ├── 📄 __init__.py
│   │   ├── 📄 dashboard.py   # Dashboard routes
│   │   ├── 📄 commands.py    # Command management routes
│   │   └── 📄 shop.py        # Shop management routes
│   │   └── 📄 users.py       # User management routes
│   └── 📄 static/            # Frontend assets
│       ├── 📄 js/            # JavaScript files
│       ├── 📄 css/           # CSS files
│       └── 📄 templates/     # HTML templates
│
├── 📄 kivy_app/              # Kivy application components
│   ├── 📄 __init__.py
│   ├── 📄 app.py             # Main Kivy application
│   ├── 📄 screens/           # Screen components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 login.py       # Login screen
│   │   ├── 📄 dashboard.py   # Main dashboard
│   │   ├── 📄 chat.py        # Chat monitor
│   │   ├── 📄 settings.py    # Settings screen
│   │   └── 📄 shop.py        # Shop screen
│   ├── 📄 widgets/           # Reusable widgets
│   │   ├── 📄 __init__.py
│   │   ├── 📄 chat_message.py   # Chat message bubbles
│   │   └── 📄 stats_card.py     # Statistics display cards
│   └── 📄 utils/             # Kivy-specific utilities
│       ├── 📄 __init__.py
│       └── 📄 animations.py  # UI animations
│
├── 📄 migrations/            # Database management
│   ├── ✅ schema.sql         # Database schema
│   └── 📄 seed.sql           # Initial data
│
├── ✅ .env                   # Example environment variables
├── ✅ requirements.txt       # Dependencies
└── 📄 main.py                # Entry point
```
