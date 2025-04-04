# DUEL SYSTEM

-   In Twitch chat, user A challenges user B to a duel: `Timmy: !duel Sammy`
-   User B accepts (`!accept`), or duel times out
-   XP is taken from each user and added to the Pot
-   Winner takes all or Pot gets bigger

## Bonuses

-   bonuses come from [Environmental Combat Effects](#environmental-combat-effects) based on what the user is donning/wielding and the mods they've applied

---

## The Pot

-   user A challenges user B to a duel for a fixed number of XP
-   XP from user A and XP from user B gets added to the Pot
-   winner takes the Pot
-   all XP stays in the Pot if it's a draw, adding to the next duel's winnings

---

## Calculating the Winner

### Weighted Stats + Durability + Underdog Bonus

-   Weighted Stats = Base calc + Environment
    -   Base calculation: (Weapon Level + Weapon Mods + amour Level + amour Mods) × Random Factor
    -   Environmental Boons/Busts: as per [Environmental Combat Effects](#environmental-combat-effects)
-   Durability = Weapon durability + Armour durability
-   Underdog Bonus = if the XP gap between the players is very large, there's a greater chance for an underdog victory

```py
# Random factor range
MIN_RANDOM_FACTOR = 0.8
MAX_RANDOM_FACTOR = 1.2

# Underdog win chance (percentage)
UNDERDOG_WIN_CHANCE = 5

# Bonus/penalty multipliers
ENVIRONMENT_BOOST_MULTIPLIER = 1.2
ENVIRONMENT_PENALTY_MULTIPLIER = 0.8
```

---

## Environmental Combat Effects

### Desert Environment

| Effect Type | Boon for...                                | Bust for...                                     |
| ----------- | ------------------------------------------ | ----------------------------------------------- |
| Armour      | Tattered Cloth, Worn Leather, Cracked Hide | Dented Chainmail, Rusty Plate, Ironclad Hauberk |
| Armour Mods | Yellow Dye, Orange Dye, White Dye, Padding | Black Dye, Blue Dye, Indigo Dye                 |
| Weapons     | Chipped Scimitar, Bent Short Sword         | Old Warhammer, Battleworn Axe                   |
| Weapon Mods | Leather Grip, Scabbard, Weapon Oil         | Poison Vial (dries quickly)                     |

### Jungle Environment

| Effect Type | Boon for...                                  | Bust for...                                     |
| ----------- | -------------------------------------------- | ----------------------------------------------- |
| Armour      | Worn Leather, Cracked Hide, Dragonhide Vest  | Rusty Plate, Old Breastplate, Pitted Brigandine |
| Armour Mods | Green Dye, Brown (mix of dyes), Repair Kit   | White Dye, Violet Dye, Heraldic Tabard          |
| Weapons     | Rusty Dagger, Worn Hatchet, Bent Short Sword | Dented Spear, Tarnished Longsword               |
| Weapon Mods | Leather Grip, Poison Vial, Cleaning Kit      | Balancing Weight, Scabbard (gets caught)        |

### Snow/Arctic Environment

| Effect Type | Boon for...                                       | Bust for...                                               |
| ----------- | ------------------------------------------------- | --------------------------------------------------------- |
| Armour      | Silvered Mail, Padding + any amour, Phoenix Guard | Tattered Cloth, Shadow Plate                              |
| Armour Mods | White Dye, Blue Dye, Padding (for insulation)     | Red Dye, Yellow Dye, Polish (reflects & reveals position) |
| Weapons     | Old Warhammer, Ironclad Mace, Battleworn Axe      | Serpent's Fang, Chipped Scimitar                          |
| Weapon Mods | Leather Grip, Oiled, Cleaning Kit                 | Poison Vial (freezes/less effective)                      |

### Urban Environment

| Effect Type | Boon for...                                               | Bust for...                                |
| ----------- | --------------------------------------------------------- | ------------------------------------------ |
| Armour      | Shadow Plate, Tattered Cloth, Dragonhide Vest             | Celestial Plate, Rusty Plate (noisy)       |
| Armour Mods | Black Dye, Indigo Dye, Polish (if matching guard colours) | Helmet Plume, Heraldic Tabard (stands out) |
| Weapons     | Rusty Dagger, Serpent's Fang, Bent Short Sword            | Dented Spear, Armageddon, World Ender      |
| Weapon Mods | Poison Vial, Scabbard (concealment), Cleaning Kit         | Intimidating Talisman (attracts attention) |

### Aquatic/Coastal Environment

| Effect Type | Boon for...                                     | Bust for...                                     |
| ----------- | ----------------------------------------------- | ----------------------------------------------- |
| Armour      | Worn Leather, Dragonhide Vest, Titanium Bastion | Rusty Plate, Dented Chainmail, Ironclad Hauberk |
| Armour Mods | Blue Dye, Green Dye, Repair Kit                 | Red Dye, Orange Dye, Polish (reflects in water) |
| Weapons     | Dented Spear, Flamebrand (if waterproofed)      | Rusty Dagger, Ironclad Mace (heavy in water)    |
| Weapon Mods | Weapon Oil (prevents rust), Cleaning Kit        | Poison Vial (dilutes in water)                  |

### Underground/Cave Environment

| Effect Type | Boon for...                                          | Bust for...                                       |
| ----------- | ---------------------------------------------------- | ------------------------------------------------- |
| Armour      | Shadow Plate, Obsidian Armour, Cracked Hide          | Valkyrie Aegis, Celestial Plate (reflects light)  |
| Armour Mods | Black Dye, Indigo Dye, Padding (for noise reduction) | White Dye, Yellow Dye, Heraldic Tabard            |
| Weapons     | Rusty Dagger, Worn Hatchet, Wooden Club              | Dented Spear, World Ender (too large for tunnels) |
| Weapon Mods | Leather Grip, Cleaning Kit                           | Intimidating Talisman (echoes in caves)           |

### Volcanic/Fiery Environment

| Effect Type | Boon for...                                     | Bust for...                                     |
| ----------- | ----------------------------------------------- | ----------------------------------------------- |
| Armour      | Phoenix Guard, Dragonhide Vest, Obsidian Armour | Tattered Cloth, Worn Leather (flammable)        |
| Armour Mods | Red Dye, Orange Dye, Repair Kit                 | Green Dye, Blue Dye (stand out)                 |
| Weapons     | Flamebrand, Direblade, Obsidian Edge            | Wooden Club, Serpent's Fang (organic materials) |
| Weapon Mods | Weapon Oil, Sharpened (heat treatment bonus)    | Leather Grip, Poison Vial (evaporates)          |
