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

## obs actions

-   id (PK)
-   scene_name
-   source_name
-   source_id (from OBS itself)
-   input_name (for mic and desktop audio devices)
-   filter_name (for turning on a filter on a source or scene)
-   state (enabled/disabled)
-   position (x, y)
-   size (width, height)
-   text (string that replaces whatever is currently in the OBS Text source)
-   animate_params (start here, stop there, do this animation)
-   transform_params (change to these dimensions, relocate to these coordinates without an animation)
-   (other stuff that might be needed in the future???)

## action sequences

_(For complex actions like DOMT, sub alerts, bits triggers)_

-   id (PK)
-   name (animate_arc_up, animate_a_to_b, show_delayed, multi_sources)
-   trigger_type (i.e. bits, twitch reward redemption, !command, Discord action, emote combo (easter eggs) etc)

## commands

_(These are custom commands, base commands are all hard-coded to reduce load on the db)_

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
-   command (i.e. for the user to actually use the toy e.g. `!ball Sammy` will kick the Leather Ball to Sammy)
-   date_added (e.g. for notifying users about newly added toys)

## duels

-   if (PK)
-   challenger (who initiated the duel)
-   opponent (who accepted the duel)
-   pot_size
-   winner
-   was_draw
-   was_underdog_win
-   duel_date

## duel environments

-   id (PK)
-   name
-   description
-   boons_armour (all of the armour types that benefit from this environment)
-   boons_armour_mods (all of the armour mod types that benefit from this environment)
-   busts_armour (all of the armour types that are disadvantaged from this environment)
-   busts_armour_mods (all of the armour mod types that are disadvantaged from this environment)
-   boons_weapon (all of the weapon types that benefit from this environment)
-   boons_weapon_mods (all of the weapon mod types that benefit from this environment)
-   busts_weapon (all of the weapon types that are disadvantaged from this environment)
-   busts_weapon_mods (all of the weapon mod types that are disadvantaged from this environment)

---

## Version 3.0

-   tables for Discord, YouTube, StreamElements, Spotify etc
