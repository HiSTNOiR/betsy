-- ARMOUR
INSERT INTO armour (level, name, cost, date_added) VALUES
(1, 'Tattered Cloth', 100, datetime('now')),
(2, 'Worn Leather', 500, datetime('now')),
(3, 'Cracked Hide', 1000, datetime('now')),
(4, 'Dented Chainmail', 2000, datetime('now')),
(5, 'Pitted Brigandine', 5000, datetime('now')),
(6, 'Chipped Scale Mail', 10000, datetime('now')),
(7, 'Rusty Plate', 20000, datetime('now')),
(8, 'Old Breastplate', 40000, datetime('now')),
(9, 'Battleworn Cuirass', 70000, datetime('now')),
(10, 'Ironclad Hauberk', 100000, datetime('now')),
(11, 'Silvered Mail', 150000, datetime('now')),
(12, 'Dragonhide Vest', 200000, datetime('now')),
(13, 'Phoenix Guard', 300000, datetime('now')),
(14, 'Valkyrie Aegis', 400000, datetime('now')),
(15, 'Shadow Plate', 500000, datetime('now')),
(16, 'Obsidian Armour', 600000, datetime('now')),
(17, 'Titanium Bastion', 700000, datetime('now')),
(18, 'Eternal Bulwark', 800000, datetime('now')),
(19, 'Celestial Plate', 900000, datetime('now')),
(20, 'Armour of The Gods', 1000000, datetime('now'));

-- ARMOUR MODS
INSERT INTO armour_mods (name, adjective, cost, date_added) VALUES
('Polish', 'polished', 100, datetime('now')),
('Repair Kit', 'repaired', 100, datetime('now')),
('Padding', 'padded', 100, datetime('now')),
('Helmet Plume', 'plumed', 100, datetime('now')),
('Heraldic Tabard', 'decorated', 100, datetime('now')),
('Leather Belt', 'belted', 100, datetime('now')),
('Red Dye', 'red', 100, datetime('now')),
('Orange Dye', 'orange', 100, datetime('now')),
('Yellow Dye', 'yellow', 100, datetime('now')),
('Green Dye', 'green', 100, datetime('now')),
('Blue Dye', 'blue', 100, datetime('now')),
('Indigo Dye', 'indigo', 100, datetime('now')),
('Violet Dye', 'violet', 100, datetime('now')),
('White Dye', 'white', 100, datetime('now')),
('Black Dye', 'black', 100, datetime('now'));

-- WEAPONS
INSERT INTO weapons (level, name, cost, date_added) VALUES
(1, 'Rusty Dagger', 100, datetime('now')),
(2, 'Wooden Club', 500, datetime('now')),
(3, 'Bent Short Sword', 1000, datetime('now')),
(4, 'Cracked Buckler', 2000, datetime('now')),
(5, 'Worn Hatchet', 5000, datetime('now')),
(6, 'Dented Spear', 10000, datetime('now')),
(7, 'Chipped Scimitar', 20000, datetime('now')),
(8, 'Old Warhammer', 40000, datetime('now')),
(9, 'Tarnished Longsword', 70000, datetime('now')),
(10, 'Battleworn Axe', 100000, datetime('now')),
(11, 'Ironclad Mace', 150000, datetime('now')),
(12, 'Serpent''s Fang', 200000, datetime('now')),
(13, 'Flamebrand', 300000, datetime('now')),
(14, 'Direblade', 400000, datetime('now')),
(15, 'Valkyrie''s Wrath', 500000, datetime('now')),
(16, 'Obsidian Edge', 600000, datetime('now')),
(17, 'Warbringer', 700000, datetime('now')),
(18, 'Eclipse Blade', 800000, datetime('now')),
(19, 'Armageddon', 900000, datetime('now')),
(20, 'World Ender', 1000000, datetime('now'));

-- WEAPON MODS
INSERT INTO weapon_mods (name, adjective, cost, date_added) VALUES
('Weapon Oil', 'oiled', 100, datetime('now')),
('Scabbard', 'sheathed', 100, datetime('now')),
('Cleaning Kit', 'cleaned', 100, datetime('now')),
('Leather Grip', 'wrapped', 100, datetime('now')),
('Talisman', 'intimidating', 100, datetime('now')),
('Poison Vial', 'poisoned', 100, datetime('now')),
('Balancing Weight', 'weighted', 100, datetime('now')),
('Whet Stone', 'sharpened', 100, datetime('now'));

-- TOYS
INSERT INTO toys (name, cost, command, date_added) VALUES
('Leather Ball', 100, '!ball', datetime('now')),
('Matrix Wand', 1000, '!matrix', datetime('now')),
('Noir Wand', 1000, '!noir', datetime('now')),
('Sepia Wand', 1000, '!sepia', datetime('now')),
('Pepto Wand', 1000, '!pepto', datetime('now'));

-- DUEL ENVIRONMENTS
INSERT INTO duel_environments (name, description) VALUES
('Desert', 'A hot, dry landscape with limited cover and heat mirages.'),
('Jungle', 'Dense foliage providing cover but limited mobility.'),
('Snow/Arctic', 'Cold temperatures with reduced visibility and slippery surfaces.'),
('Urban', 'City streets with many hiding places and obstacles.'),
('Aquatic/Coastal', 'Partially submerged terrain with water affecting movement and visibility.'),
('Underground/Cave', 'Dark environment with limited visibility and echoing sounds.'),
('Volcanic/Fiery', 'Extreme heat with hazardous terrain and limited visibility due to smoke.');

-- ENVIRONMENT EFFECTS - DESERT
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Tattered Cloth', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Worn Leather', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Cracked Hide', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Yellow Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Orange Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'White Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Padding', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon', 'Chipped Scimitar', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon', 'Bent Short Sword', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon_mod', 'Leather Grip', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon_mod', 'Scabbard', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon_mod', 'Weapon Oil', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Dented Chainmail', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Rusty Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour', 'Ironclad Hauberk', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Black Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Blue Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'armour_mod', 'Indigo Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon', 'Old Warhammer', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon', 'Battleworn Axe', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Desert'), 'weapon_mod', 'Poison Vial', 'bust');

-- ENVIRONMENT EFFECTS - JUNGLE
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Worn Leather', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Cracked Hide', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Dragonhide Vest', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'Green Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'Brown Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'Repair Kit', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon', 'Rusty Dagger', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon', 'Worn Hatchet', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon', 'Bent Short Sword', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon_mod', 'Leather Grip', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon_mod', 'Poison Vial', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon_mod', 'Cleaning Kit', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Rusty Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Old Breastplate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour', 'Pitted Brigandine', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'White Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'Violet Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'armour_mod', 'Heraldic Tabard', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon', 'Dented Spear', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon', 'Tarnished Longsword', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon_mod', 'Balancing Weight', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Jungle'), 'weapon_mod', 'Scabbard', 'bust');

-- ENVIRONMENT EFFECTS - SNOW/ARCTIC
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour', 'Silvered Mail', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour', 'Phoenix Guard', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'White Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'Blue Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'Padding', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon', 'Old Warhammer', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon', 'Ironclad Mace', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon', 'Battleworn Axe', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon_mod', 'Leather Grip', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon_mod', 'Weapon Oil', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon_mod', 'Cleaning Kit', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour', 'Tattered Cloth', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour', 'Shadow Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'Red Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'Yellow Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'armour_mod', 'Polish', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon', 'Serpent''s Fang', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon', 'Chipped Scimitar', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Snow/Arctic'), 'weapon_mod', 'Poison Vial', 'bust');

-- ENVIRONMENT EFFECTS - URBAN
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour', 'Shadow Plate', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour', 'Tattered Cloth', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour', 'Dragonhide Vest', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour_mod', 'Black Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour_mod', 'Indigo Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour_mod', 'Polish', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'Rusty Dagger', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'Serpent''s Fang', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'Bent Short Sword', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon_mod', 'Poison Vial', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon_mod', 'Scabbard', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon_mod', 'Cleaning Kit', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour', 'Celestial Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour', 'Rusty Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour_mod', 'Helmet Plume', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'armour_mod', 'Heraldic Tabard', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'Dented Spear', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'Armageddon', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon', 'World Ender', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Urban'), 'weapon_mod', 'Talisman', 'bust');

-- ENVIRONMENT EFFECTS - AQUATIC/COASTAL
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Worn Leather', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Dragonhide Vest', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Titanium Bastion', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Blue Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Green Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Repair Kit', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon', 'Dented Spear', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon', 'Flamebrand', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon_mod', 'Weapon Oil', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon_mod', 'Cleaning Kit', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Rusty Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Dented Chainmail', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour', 'Ironclad Hauberk', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Red Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Orange Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'armour_mod', 'Polish', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon', 'Rusty Dagger', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon', 'Ironclad Mace', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Aquatic/Coastal'), 'weapon_mod', 'Poison Vial', 'bust');

-- ENVIRONMENT EFFECTS - UNDERGROUND/CAVE
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour', 'Shadow Plate', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour', 'Obsidian Armour', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour', 'Cracked Hide', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'Black Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'Indigo Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'Padding', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon', 'Rusty Dagger', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon', 'Worn Hatchet', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon', 'Wooden Club', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon_mod', 'Leather Grip', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon_mod', 'Cleaning Kit', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour', 'Valkyrie Aegis', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour', 'Celestial Plate', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'White Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'Yellow Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'armour_mod', 'Heraldic Tabard', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon', 'Dented Spear', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon', 'World Ender', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Underground/Cave'), 'weapon_mod', 'Talisman', 'bust');

-- ENVIRONMENT EFFECTS - VOLCANIC/FIERY
-- Boons
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour', 'Phoenix Guard', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour', 'Dragonhide Vest', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour', 'Obsidian Armour', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour_mod', 'Red Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour_mod', 'Orange Dye', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour_mod', 'Repair Kit', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon', 'Flamebrand', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon', 'Direblade', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon', 'Obsidian Edge', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon_mod', 'Weapon Oil', 'boon'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon_mod', 'Whet Stone', 'boon');

-- Busts
INSERT INTO environment_effects (environment_id, item_type, item_name, effect_type) VALUES
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour', 'Tattered Cloth', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour', 'Worn Leather', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour_mod', 'Green Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'armour_mod', 'Blue Dye', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon', 'Wooden Club', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon', 'Serpent''s Fang', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon_mod', 'Leather Grip', 'bust'),
((SELECT id FROM duel_environments WHERE name = 'Volcanic/Fiery'), 'weapon_mod', 'Poison Vial', 'bust');

-- DOMT CARDS
INSERT INTO domt_cards (name, source, description, description_english, is_retainable, date_added) VALUES
('Balance', 'i_card_01', 'All subjects of the realm shall be rendered equal, their experience set to 10,000.', 'Set XP for all users to 10000', 0, datetime('now')),
('Comet', 'i_card_02', 'Bestowed the eternal right to proclaim messages across the kingdom''s scrying glass at will.', 'Use !comet [message] to display a message in the t_Msg text source in OBS', 0, datetime('now')),
('Donjon', 'i_card_03', 'Confined to the high tower for one hour''s time, for thy protection and reflection.', 'Timeout user for 1 hour', 0, datetime('now')),
('Euryale', 'i_card_04', 'Granted the mystical power to remould one of the realm''s champions to thy heart''s desire.', 'Customise one of the streamer''s in-game characters', 0, datetime('now')),
('Fates', 'i_card_05', 'A divine ward against a single future transgression.', 'Retain card and automatically burn it when next receiving a punishment card', 1, datetime('now')),
('Flames', 'i_card_06', 'Thy words shall be cleansed by fire, silencing thee briefly with each utterance.', 'Purge user after 3 seconds whenever they speak (for remainder of stream)', 0, datetime('now')),
('Fool', 'i_card_07', 'For five minutes hence, the scrying glass is transformed into a whimsical carnival. Merry melodies shall enchant the air, while peculiar illusions dance across the vision. Behold as the realm descends into delightful madness!', 'Apply DOMT filter on STREAM scene for 5 minutes', 0, datetime('now')),
('Idiot', 'i_card_08', 'A plague of idiocy sweeps the realm, rendering all subjects incapable of coherent speech. For five minutes hence, only mystical symbols and arcane gestures may convey meaning.', 'Enable emote-only mode in chat for 5 minutes', 0, datetime('now')),
('Jester', 'i_card_09', 'Gifted a shitty picture drawn by Hist, using an idea generated by AI.', 'Generate an AI prompt for the streamer to draw', 0, datetime('now')),
('Key', 'i_card_10', 'Behold, the master key to the Coffer of Curiosities! With this mystical key, you shall unlock a chest of wonders beyond mortal comprehension. From within its depths, you''ll draw forth a prize so peculiar, it defies the very laws of reality ...', 'Award a bizarre virtual prize to the user', 0, datetime('now')),
('Knight', 'i_card_11', 'Blessed by the Knight''s Favour. While this card graces your hand, your prowess grows twofold, doubling all XP gained. But heed this warning: should you falter in honour or face righteous punishment, you shall suffer the Severance of Fealty, and the Knight''s boon shall be lost.', 'Add card to inventory, while held double XP, if punished lose card only', 1, datetime('now')),
('Moon', 'i_card_12', 'By invoking this arcane sigil, you shall shroud the realm''s scrying glass in a cloak of impenetrable darkness. For five minutes hence, the visions within shall be obscured, as if viewed through the murky depths of a moonless night. Squint and strain, brave viewers, for in this twilight realm, only the keenest eyes may discern the whispers of movement and form. Let those who seek enlightenment first endure the challenge of shadow!', 'Apply DarkMode filter on STREAM scene for 5 minutes', 0, datetime('now')),
('Rogue', 'i_card_13', 'A grand larceny befalls the kingdom, emptying all coffers and pouches.', 'Delete XP, weapons, armour, toys and cards for ALL users in database', 0, datetime('now')),
('Ruin', 'i_card_14', 'Released by Thanos.', 'Delete half the users in the database (randomly selected)', 0, datetime('now')),
('Skull', 'i_card_15', 'Banished from the realm for a full day and night.', 'Timeout user for 24 hours', 0, datetime('now')),
('Star', 'i_card_16', 'Empowered to rewrite the kingdom''s banner at will, until the night falls.', 'Change the stream title for rest of broadcast using !star [New title]', 0, datetime('now')),
('Sun', 'i_card_17', 'The searing light of a thousand suns shall be summoned to the scrying glass. For five minutes hence, the realm shall be bathed in blinding radiance, challenging all to witness the visions through squinted eyes. May the bravest endure this brilliant ordeal!', 'Apply BrightLight filter on STREAM scene for 5 minutes', 0, datetime('now')),
('Talons', 'i_card_18', 'The realm''s leader is struck mute for five minutes by an ethereal force.', 'Streamer must be silent for 5 minutes', 0, datetime('now')),
('Throne', 'i_card_19', 'Elevated to the nobility as a guardian of the realm. If already noble, a coup d''état occurs.', 'Toggle moderator status for the user', 0, datetime('now')),
('Vizier', 'i_card_20', 'Granted the arcane ability to command the realm''s leader until nightfall.', 'Command the streamer for rest of broadcast using !vizier [command]', 0, datetime('now')),
('Void', 'i_card_21', 'The cosmic tapestry unravels, ending this world''s saga.', 'End the stream', 0, datetime('now'));

-- Initial stream data
INSERT INTO stream (count, total_duration_minutes, avg_duration_minutes, last_stream_date)
VALUES (0, 0, 0, NULL);

-- Create an admin user
INSERT INTO users (twitch_user_id, twitch_username, rank, points, date_added, last_seen, weapon_id, weapon_durability, weapon_mod_id, armour_id, armour_durability, armour_mod_id)
VALUES ('72001547', 'histnoir', 'bot_admin', 100000, datetime('now'), datetime('now'), 10, 10, NULL, 10, 10, NULL);

-- ! TESTING ONLY - delete meh ======================================================================================================================================================
-- TODO delete
INSERT INTO users (twitch_user_id, twitch_username, rank, points, date_added, last_seen, weapon_id, weapon_durability, weapon_mod_id, armour_id, armour_durability, armour_mod_id)
VALUES ('11111111', 'bob', 'untouchable', 1000000000000000000, datetime('now'), datetime('now'), 10, 10, NULL, 10, 10, NULL);

-- Create custom commands (after users table so user-commands can be linked)
-- TODO hook into OBS: show-then-hide source
INSERT INTO commands (name, description, response, permission_level, restricted_to_user_id, cooldown_seconds, total_uses, date_added)
VALUES 
('pinky', "madmann225's command", null, null, (SELECT id FROM users WHERE twitch_username = 'histnoir'), 5, 0, datetime('now'));

INSERT INTO commands (name, description, response, permission_level, cooldown_seconds, total_uses, date_added)
VALUES 
('hug', 'Give someone a hug', '@{user} gives @{args} a warm hug', 'viewer', 5, 0, datetime('now'));