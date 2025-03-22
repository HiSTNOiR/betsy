# EXAMPLE BEHAVIOUR

## Twitch

### Scenario

User, Timmy, wants to buy a 'Pepto Wand' from the shop.

**Sequence (success):**

1. (in Twitch chat) Timmy: !buy pepto wand
2. (db) check if 'pepto wand' exists in the toys table (result: it does)
3. (db) check if Timmy has enough XP to afford that wand (result: he does)
4. (db) remove XP from Timmy
5. (db) add `Pepto Wand` to the Timmy's inventory
6. (in Twitch chat) Bot: @Timmy, you now own a Pepto Wand.
7. (bot internals) trigger a 3 second CD on Bot Twitch chat messages

**Sequence (failure):**

1. (in Twitch chat) Timmy: !buy pepto wand
2. (db) check if 'pepto wand' exists in the toys table (result: it does)
3. (db) check if Timmy has enough XP to afford that wand (result: he doesn't)
4. (in Twitch chat) Bot: @Timmy, you're too povo to buy that.
5. (bot internals) trigger a 3 second CD on Bot Twitch chat messages

**Sequence (failure):**

1. (in Twitch chat) Timmy: !buy papto wand (error: typo)
2. (db) check if 'papto wand' exists in the toys table (result: it doesn't)
3. Do nothing further.

**Sequence (failure):**

1. (in Twitch chat) Timmy: !buy wand (error: missing full item name)
2. (db) check if 'wand' exists in the toys table (result: it doesn't)
3. Do nothing further.

---

### Scenario

User, Timmy, is playing silly buggers and trying to break the bot.

**Sequence:**

1. (in Twitch chat) Timmy: !buy 😇 (error: using emojis in any !command)
2. (bot internals) Disregard the message as junk.
3. Do nothing further.

**Sequence:**

1. (in Twitch chat) Timmy: !buy 123435567 (error: using numbers in the `!buy` command)
2. (bot internals) Disregard the message as junk.
3. Do nothing further.

**Sequence:**

1. (in Twitch chat) Timmy: !give Timmy 100 (error: trying to give XP to themself)
2. (bot internals) check if the user is also the 'target' (result: he is)
3. (in Twitch chat) Bot: @Timmy, since you insist on playing silly buggers, I'll take that XP off ya hands ... yoink!
4. (bot internals) trigger a 3 second CD on Bot Twitch chat messages
5. (db) remove 100 points from Timmy
6. (db) add 100 points to the streamer
