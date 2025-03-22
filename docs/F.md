# FEATURES

## Version 0.x

-   SQLite database for storing user data, OBS scenes and sources, commands, Twitch channel rewards, Twitch bits
-   secure database transactions, so records are not duplicated
-   robust error handling, with user-friendly error messages to help with debugging
-   idiot proofing, as random Twitch chatters will be interacting with the bot (e.g. if they misuse a command, the bot shouldn't crash)
-   data parsing and consistent formatting, so Twitch chat messages are properly handled when math functions need to be utilised (e.g. ensuring Twitch bits are converted to integers before being handled by other functions) - this includes capitalisation, so "amour of the old gods" and "ArmOUr of THe Old gods" both work

## Version 0.8

Users can:

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

Users can't:

1. see commands they don't have permission to use when using `!commands`
2. break the bot with unusual chat commands

The Broadcaster can:

1. `print()` the currently active Twitch Channel Reward rewards, so their IDs can be retrieved
2. trigger any Twitch bits event through a manual broadcaster-only command (e.g. I want to trigger the event tied to a user spending 200 bits, so I use `!bits200`)
    - this ensures that bits events can be tested by the channel owner, who cannot spend bits in their own channel

## Version 0.9

1. A 'Deck of Many Things' system
    - users spend 1111 bits to trigger this event
    - a random card is pulled from the Deck of Many Things, which either rewards or harms the user/other users/the stream itself
    - each time a card it drawn, it is removed from the deck (for all users) - when all cards are gone, the deck is 'replenished'
    - some cards can be retained by the user, so those get added to their inventory
    - when a user uses one of their held cards, it is removed from their inventory

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

## Version 2.0

1. Rough GUI using Kivy (just for the bot admin)
2. Web app
3. Mobile app using Kivy

---

## Mmmmaybe one day (if time, motivation, dollarydoos permit)

-   Discord integration
-   YouTube integration
-   a `!raid` where a group of viewers get together to fight a boss for some extra-special reward
-   AI chatting (contingent upon my getting a selfhosted setup in place, because I can't stream+game+LLM on one machine)
