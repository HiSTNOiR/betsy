# .ENV

```bash
# Twitch Bot Configuration
# Bot settings
BOT_NICK=username_here
BOT_PREFIX=!
CHANNEL=channel_here

# Twitch API credentials
# Get token from https://dev.twitch.tv/console/apps
TMI_TOKEN=oauth:oauth_here
# Get id from https://twitchtokengenerator.com
CLIENT_ID=id_here

# Feature flags (true/false)
DB_ENABLED=false
TWITCH_ENABLED=false
OBS_ENABLED=false
DISCORD_ENABLED=false
YOUTUBE_ENABLED=false

# SQLite database path (relative or absolute)
DB_PATH=data/bot.db

# OBS WebSocket settings (if OBS_ENABLED=true)
OBS_HOST=ip_here
OBS_PORT=port_here
OBS_PASSWORD=password_here

# Discord settings (if DISCORD_ENABLED=true)
DISCORD_TOKEN=my_discord_bot_token
DISCORD_CHANNEL_ID=my_channel_id
```
