# DECK OF MANY THINGS

Triggered through Twitch bits.

## Version 0.9

{
name: "Balance",
source: "i_card_01",
description:
"All subjects of the realm shall be rendered equal, their experience set to 10,000.", // TODO in English = set XP for all users to 10000
},
{
name: "Comet",
source: "i_card_02",
description:
"Bestowed the eternal right to proclaim messages across the kingdom's scrying glass at will.", // TODO in English = !comet some long-arse message goes here and then is displayed in the t_Msg text source in OBS
},
{
name: "Donjon",
source: "i_card_03",
description:
"Confined to the high tower for one hour's time, for thy protection and reflection.", // TODO in English = /timeout user for 1 hour
},
{
name: "Euryale",
source: "i_card_04",
description:
"Granted the mystical power to remould one of the realm's champions to thy heart's desire.", // TODO in English: customise one of my ingame toons
},
{
name: "Fates",
source: "i_card_05",
description: "A divine ward against a single future transgression.", // TODO in English = retain card and automatically 'burn' it when next receiving a punishment card
},
{
name: "Flames",
source: "i_card_06",
description:
"Thy words shall be cleansed by fire, silencing thee briefly with each utterance.", // TODO in English = purge user after 3 seconds whenever they speak (for remainder of stream)
},
{
name: "Fool",
source: "i_card_07",
description:
"For five minutes hence, the scrying glass is transformed into a whimsical carnival. Merry melodies shall enchant the air, while peculiar illusions dance across the vision. Behold as the realm descends into delightful madness!", // TODO in English = domt filter on STREAM scene
},
{
name: "Idiot",
source: "i_card_08",
description:
"A plague of idiocy sweeps the realm, rendering all subjects incapable of coherent speech. For five minutes hence, only mystical symbols and arcane gestures may convey meaning.", // TODO in English = /emoteonly chat
},
{
name: "Jester",
source: "i_card_09",
description: "Gifted a shitty picture drawn by Hist, using an idea generated by AI.", // TODO in English = posts a prompt for chatgpt that tells me what to draw
},
{
name: "Key",
source: "i_card_10",
description:
"Behold, the master key to the Coffer of Curiosities! With this mystical key, you shall unlock a chest of wonders beyond mortal comprehension. From within its depths, you'll draw forth a prize so peculiar, it defies the very laws of reality ...", // TODO in English = bizarre virtual prizes like an invisible trophy that silently judges your life choices, or an unsigned certificate of quantum indecision
},
{
name: "Knight",
source: "i_card_11",
description:
"Blessed by the Knight's Favour. While this card graces your hand, your prowess grows twofold, doubling all XP gained. But heed this warning: should you falter in honour or face righteous punishment, you shall suffer the Severance of Fealty, and the Knight's boon shall be lost.", // TODO in English = add card to inv, while held double XP, if punished lose card only
},
{
name: "Moon",
source: "i_card_12",
description:
"By invoking this arcane sigil, you shall shroud the realm's scrying glass in a cloak of impenetrable darkness. For five minutes hence, the visions within shall be obscured, as if viewed through the murky depths of a moonless night. Squint and strain, brave viewers, for in this twilight realm, only the keenest eyes may discern the whispers of movement and form. Let those who seek enlightenment first endure the challenge of shadow!", // TODO in English = DarkMode filter on STREAM scene for 5 mins
},
{
name: "Rogue",
source: "i_card_13",
description: "A grand larceny befalls the kingdom, emptying all coffers and pouches.", // TODO in English = delete XP, weapons, armour, toys and cards for ALL users in db
},
{
name: "Ruin",
source: "i_card_14",
description: "Released by Thanos.", // TODO in English = delete half the users in the db (randomly selected)
},
{
name: "Skull",
source: "i_card_15",
description: "Banished from the realm for a full day and night.", // TODO in English = /timeout user for 24 hours
},
{
name: "Star",
source: "i_card_16",
description: "Empowered to rewrite the kingdom's banner at will, until the night falls.", // TODO in English = change the stream title for rest of broadcast: !star New title goes here
},
{
name: "Sun",
source: "i_card_17",
description:
"The searing light of a thousand suns shall be summoned to the scrying glass. For five minutes hence, the realm shall be bathed in blinding radiance, challenging all to witness the visions through squinted eyes. May the bravest endure this brilliant ordeal!", // TODO in English = BrightLight filter on STREAM scene
},
{
name: "Talons",
source: "i_card_18",
description: "The realm's leader is struck mute for five minutes by an ethereal force.",
},
{
name: "Throne",
source: "i_card_19",
description:
"Elevated to the nobility as a guardian of the realm. If already noble, a coup d'état occurs.", // TODO in English = toggles mod status
},
{
name: "Vizier",
source: "i_card_20",
description: "Granted the arcane ability to command the realm's leader until nightfall.", // TODO in English = command me for rest of cast: !vizier Dance like a chicken
},
{
name: "Void",
source: "i_card_21",
description: "The cosmic tapestry unravels, ending this world's saga.", // TODO in English = end stream
},

## Version 1.0

-   add toys, armour, weapons interactions
