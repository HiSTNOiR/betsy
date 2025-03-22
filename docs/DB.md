# DATABASE

## users

-   user_id (PK)
-   twitch_user_id (we need this and the username, because users can change their username and we want their XP to follow them when they do)
-   twitch_username
-   discord_username
-   youtube_username
-   rank (i.e. viewer, vip, subscriber, moderator, broadcaster, bot_admin)
-   points
-   points_gifted (for tracking generosity and giving silent bonuses to a user)
-   date_added
-   last_seen
-   weapon
-   weapon_durability (i.e. 1-10 ... this goes down when duelling, and up when using mods)
-   armour
-   armour_durability (i.e. 1-10)
-   toys
-   cards
-   duel_wins
-   duel_loses

## twitch_bits

-   bits (PK)
-   description
-   trigger (i.e. an OBS action, a Discord thing, a thing on YouTube etc.)
-   uses (to track how popular each bits event is)

## twitch_rewards

-   id (PK)
-   description
-   trigger (i.e. an OBS action, a Discord thing, a thing on YouTube etc.)
-   uses (to track how popular each channel reward is)

## armour/weapon

-   id (PK)
-   level
-   name
-   cost (i.e. how much XP it costs to upgrade to this item)

## armour_mods/weapon_mods

-   id (PK)
-   name (e.g. Polish, Repair kit)
-   adjective (e.g. polished, repaired - this is for modifing the weapon/armour name: 'Wooden Dagger' becomes 'polished Wooden Dagger')
-   cost (i.e. the XP a user needs to spend to apply this mod)
