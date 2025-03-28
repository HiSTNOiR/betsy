# FEATURES

## Version 0.x

-   SQLite database for storing user data, OBS scenes and sources, commands, Twitch channel rewards, Twitch bits
-   secure database transactions, so records are not duplicated
-   robust error handling, with user-friendly error messages to help with debugging
-   idiot proofing, as random Twitch chatters will be interacting with the bot (e.g. if they misuse a command, the bot shouldn't crash)
-   data parsing and consistent formatting, so Twitch chat messages are properly handled when math functions need to be utilised (e.g. ensuring Twitch bits are converted to integers before being handled by other functions) - this includes capitalisation, so "amour of the old gods" and "ArmOUr of THe Old gods" both work

## Version 0.8

### Users

**Users can:**

1. use `!commands` to see what commands they have access to (based on user permissions)
2. interact with OBS through bot commands, Twitch channel rewards, and Twitch bits
3. earn loyalty points (XP), which they can keep, `!give` to another user, or spend on chat-based games
    - they earn a minimal number of XP passively by just being in the channel while it's live (a year's worth of passive XP is equal to the cost of the most expensive weapon or armour item in the `!shop`)
    - they earn a small number of XP whenever they send a chat message
    - they earn XP when redeeming Twitch channel rewards (the cost of the reward / 2 = the number of XP)
    - they earn XP when spending Twitch bits (the number of bits = the number of XP)
4. spend XP on a `!gamble` command that either rewards or punishes them
5. `!give` XP to another user, because they're nice (and in doing so, they get hidden perks)
6. check their available XP with `!points` or `!xp`
7. use command aliases (e.g. `!xp` or `!points`)

**Users can't:**

1. see commands they don't have permission to use when using `!commands`
2. break the bot with unusual chat commands
3. cause the bot to spam chat (i.e. messages the bot sends are throttled and queued based on priority [i.e. responding to `!points` is more important than `!hello`])

**The Broadcaster can:**

1. `print()` the currently active Twitch Channel Reward rewards, so their IDs can be retrieved
2. trigger any Twitch bits event through a manual broadcaster-only command (e.g. I want to trigger the event tied to a user spending 200 bits, so I use `!bits200`)
    - this ensures that bits events can be tested by the channel owner, who cannot spend bits in their own channel

### Software and Platform Integrations

**OBS:**

1. a single source can be made visible for a specific duration, then switched off
    - e.g. source "ball" in scene "STREAM" becomes visible for 5 seconds, then disappears.
2. multiple sources can be made visible at the same time, then switched off at the same time
    - e.g. sources "sub", "username" and "thanks" in scene "ALERTS" become visible for 5 seconds, then disappear together.
3. multiple sources can be made visible in a timed sequence, then switched off either together or in sequence
    - e.g. source "domt_video" in scene "DOMT" becomes visible for 40 seconds; "domt_video" disappears, and "pouch_top" and "pouch_bottom" become visible; 2 second later "card_01" becomes visible; 3 seconds later "pouch_top", "pouch_bottom" and "card_01" disappear together.
4. sources (e.g. text sources) can have their settings changed (e.g. text content is replaced by what the user provides)
5. sources can be transformed (i.e. their position or size)
6. sources can be animated by repeatedly changing their x,y values (e.g. a bird image source quickly swoops across the screen from top left to bottom right)
    - the speed and start/stop coordinates can be changed as needed
7. filters can be enabled/disabled on scenes and sources
8. a single audio input/output can be manipulated (e.g. the mic input can be muted, the music output can be muted/unmuted)
9. multiple audio inputs and outputs can be manipulated for a specific duration
    - e.g. the mic input and music output are muted for 30 seconds while a video source plays, when the video is finished, the mic and music are unmuted
10. scenes can be switched to
11. the stream can be started and stopped
12. a local recording can be started for a set duration, then stopped
13. (a single Twitch event can trigger any or all of the above actions in a specific sequence)

**Twitch:**

1. users can use !commands in chat to trigger the bot
    - e.g. `!hug Sammy` 👉 the bot posts `Timmy gives Sammy a warm hug` to chat
    - e.g. `!point` 👉 the bot checks the user's current points in the db, then posts `@Timmy, you have 12,345 XP` to chat
    - e.g. `!ball Sammy` 👉 the "ball" OBS source in scene "DOLLARYDOOS" is shown and animated to fly across the screen in a slow upward arc; the "Leather Ball" toy is removed from Timmy's inventory and added to Sammy's inventory; the bot posts `@Sammy, you now have the Leather Ball toy. Kick it to someone with 👉 !ball <user's name>` to chat
2. Twitch bits trigger bot events
    - e.g. cheering 666 bits causes a jumpscare video source in OBS to play after a random delay; the user is awarded 666 XP
    - e.g. cheering 200 bits causes OBS to mute the mic and music channels, play a video source for 30 seconds, then unmute the audio channels; the user is awarded 200 XP
3. Twitch channel rewards trigger bot events
    - e.g. user redeems "Boo"

### Database

1. _(stored data detailed in full in `DS.md`)_
2. stores OBS scenes and sources, with their respective OBS ids
    - the bot will scrape this data from OBS each time it starts up, as well as have a option to manually update the list should I add a source/scene while streaming

---

## Version 0.9

1. A 'Deck of Many Things' system
    - users spend 1111 bits to trigger this event
    - a random card is pulled from the Deck of Many Things, which either rewards or harms the user/other users/the stream itself
    - each time a card it drawn, it is removed from the deck (for all users) - when all cards are gone, the deck is 'replenished'
    - some cards can be retained by the user and used at a later time, so those get added to their inventory
    - when a user uses one of their held cards, it is removed from their inventory

---

## Version 1.0

1. A `!duel` system
    - users bet XP, which gets added to a Pot for the winner
    - the winner is calculated by adding the weapon level and any addons, with the armour level and any addons, in addition to any environmental bonuses (e.g. +dmg when fighting in a jungle), with a small percentage chance of the underdog winning
    - duels happen in random environments, which grant bonuses to the user with the 'right' weapon or armour (e.g. user has a dagger and therefore gets a bonus in a jungle environment where swinging a long weapon is impossible)
    - duelling causes a durability loss on the user's weapon and armour (i.e. each duel = -1 durability on both weapon and armour)
2. A `!shop` system, aka 'The Corner Store'
    - offers users toys, weapons and armour (toys include a leather ball that can be kicked to another viewer, and wands that change the appearance of the stream)
    - users can view what's available in the shop, in a compact and easy-to-read format (perhaps only showing the toys they don't already own, and the next level weapon/armour)
    - users buy toys with XP, and use those toys through chat commands (i.e. !ball <user_to_catch_ball>)
    - users can upgrade their weapon and armour, so they have a better chance of winning duels (i.e. !upgrade weapon --> "Congrats! You now own the Mithril Shortsword!")
    - users can buy mods for their weapon and armour, such as a whet stone or leather padding etc.
3. An `!inventory` system
    - users can see what `!gear` they have, which shows the stats of their currently equipped weapon and armour
    - users can see what `!toys` they have
    - users can see what `!cards` they have earned through the Deck of Many Things

---

## Version 1.1

1. When 'Shield Mode' is activated in the Twitch channel, a sequence of actions fire
    - a shield wall video source is shown in OBS
    - the chat room settings are changed: can only chat if following for at least 6 months (3 months? 1 year??); TTS is disabled; a shield icon is shown in the corner of the stream (while the settings are active); sub alerts only show the Koala image and not the username or any messages; anything that can be trolled is basically disabled until Shield Mode is deactivated
2. 'To Do' system
    - add something to the list and it gets printed at the end of the stream

---

## Version 2.0

1. Rough GUI using Kivy (just for the bot admin side of things)
    - I need to be able to click&drag components/windows out of the main GUI to "show on stream"
    - customise colours, font sizes, Discord "streamer mode" to redact doxxable shit
2. Web app
3. Mobile app using Kivy
4. Visualisation and reporting tools for metrics (stream stats, viewer trends etc)
5. Chat log
    - Twitch
    - YouTube
    - Discord etc
    - split based on service
    - combine all services into one Mother Chat

---

## Version 3.0+

1. BitFocus Companion integration
2. The Betsy Vault
    - click to store someone's chat message for 'ron
3. A MUD/MOO UI for Betsy
    - terminal based
    - full-on "You find yourself in a darkened room and can't see beyond the nose on your face. What do you do?" (this means Betsy is not running nor connected to OBS/Twitch)
        - > Reach out and grab torch
        - "You grasp the moist shaft of the wooden torch from it's sconce (???)."
        - > Use flint
        - "With an efficient flick of the wrist you light the oily fabric and the torch ignites and ... you can see shit." (this = `npm start`)

---

## Mmmmaybe one day (if time, motivation, dollarydoos permit)

-   Discord integration
-   YouTube integration
-   a `!dungeon` where a group of viewers get together to fight a boss for some extra-special reward (was called `!raid` but that sounds like a Twitch channel raid)
-   AI chatting (contingent upon my getting a self-hosted setup in place, because I can't stream+game+LLM on one machine)
-   order pizza/sushi (sans doxxing info)
