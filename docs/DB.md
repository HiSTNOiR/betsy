# DATABASE DATA

_This will be changed to a schema document once I've got that ready._

## stream

-   count (i.e. how many times I've streamed)
-   stream_habits (e.g. the average duration of a stream, what days I'm more likely to stream on, what categories I stream in and how often I'm in those categories)

## users

-   user_id (PK)
-   twitch_user_id (we need this and the username, because users can change their username and we want their XP to follow them when they do)
-   twitch_username
-   discord_username
-   youtube_username
-   rank (i.e. viewer, vip, subscriber, moderator, broadcaster, bot_admin)
-   points
-   points_gifted (for tracking generosity and giving silent bonuses to a user)
-   date_added (this will be updated if they get Thanos snapped)
-   last_seen
-   viewing_habits (e.g. for tracking the days and times they typically watch, how long they usually remain in the channel, average number of messages they send/if they predominately lurk, if they tend to only join the stream for specific categories/games, if they use bits, if they redeem Twitch channel rewards, if they're on Discord/YouTube, if they donate via StreamElements etc)
-   weapon
-   weapon_durability (i.e. 1-10 ... this goes down when duelling, and up when using mods)
-   armour
-   armour_durability (i.e. 1-10)
-   toys
-   cards
-   duel_wins
-   duel_loses

## obs scenes

-   name (PK, maybe a composite key with id to future-proof from OBS changes?)
-   id (the id in OBS)
-   state (enabled/disabled)

## obs sources

-   name (PK, maybe a composite key with id to future-proof from OBS changes?)
-   id (the id in OBS, which is needed for targetting the source)
-   state (enabled/disabled)
-   position (x, y coords)
-   transform (width, height)
-   text_content (string, i.e. what an OBS text source needs to be changed to)
-   (other things that might be needed in the future?)

## obs inputs

-   name (PK)
-   id (? dunno if audio inputs/outputs have ids)
-   state (enabled/disabled)

## obs filters

-   name (PK)
-   id (? dunno if filters have ids)
-   source_name
-   state (enabled/disabled)

## commands

-   id (PK)
-   name (this is what the user types in chat, e.g. `!points`)
-   aliases (e.g. aliases for `!hello` are `!hi` and `!gday` - maybe only have a max of 2 aliases, one short and one 'with flavour')
-   actions (e.g. sends a chat message, shows a source in OBS, or a combination of different actions both in Twitch chat and OBS)
-   total_uses (for tracking popularity of commands)
-   date_added (e.g. for notifying users about newly added commands)

## twitch bits

-   bits (PK, the number of bits)
-   description
-   action (i.e. an OBS action, a Discord thing, a YouTube whatever etc.)
-   uses (to track how popular each bits event is)
-   date_added (e.g. for notifying users about newly added bits tiers)

## twitch rewards

-   id (PK, the Twitch id for the reward)
-   name (taken from Twitch's end)
-   action (i.e. an OBS action, a Discord thing, a thing on YouTube etc.)
-   total_uses (to track how popular each channel reward is)
-   date_added (e.g. for notifying users about newly added rewards)

## armour/weapons

-   id (PK)
-   level
-   name
-   cost (i.e. how much XP it costs to upgrade to this item)
-   date_added (e.g. for notifying users about newly added armour/weapons)

## armour mods/weapon mods

-   id (PK)
-   name (e.g. Polish, Repair Kit)
-   adjective (e.g. polished, repaired - this is for modifying the weapon/armour name: 'Wooden Dagger' becomes 'polished Wooden Dagger')
-   cost (i.e. the XP a user needs to spend to apply this mod)
-   date_added (e.g. for notifying users about newly added mods)

## toys

-   id (PK)
-   name
-   cost (i.e. XP needed to buy this item)
-   date_added (e.g. for notifying users about newly added toys)

---

## Version 3.0

-   tables for Discord, YouTube, StreamElements, Spotify etc
