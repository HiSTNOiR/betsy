# Utility Functions for Twitch Bot (Up to Version 1.0)

## Text Processing and Formatting
| Module | Function | Description |
|--------|----------|-------------|
| format.py | format_chat_message | Format messages for Twitch chat output |
| format.py | normalise_username | Normalise Twitch usernames to consistent format |
| format.py | format_points | Format XP/points with commas and appropriate styling |
| format.py | format_command | Format command syntax for help text and documentation |
| format.py | format_duration | Format time durations for cooldowns and timers |
| format.py | format_item_name | Format item names consistently for display |
| format.py | pluralise | Handle plural forms of words based on count |
| format.py | truncate | Truncate text to specified length with ellipsis |
| format.py | format_list | Format lists of items for display in chat |

## Input Parsing and Validation
| Module | Function | Description |
|--------|----------|-------------|
| parsing.py | parse_command | Parse raw command input from chat |
| parsing.py | parse_args | Parse arguments from command string |
| parsing.py | extract_user_and_amount | Extract target user and amount from commands |
| parsing.py | parse_item_name | Parse and normalise item names from user input |
| parsing.py | parse_bits_amount | Parse bits donation amounts |
| parsing.py | parse_duration | Parse time duration from string input |
| parsing.py | extract_targets | Extract multiple targets from a command |
| parsing.py | safe_int_conversion | Safely convert string to integer with fallback |
| parsing.py | parse_key_value_pairs | Parse key-value pairs from string input |
| parsing.py | fuzzy_match_item | Find closest matching item from input |

## Security and Sanitisation
| Module | Function | Description |
|--------|----------|-------------|
| sanitisation.py | sanitise_input | General input sanitisation |
| sanitisation.py | sanitise_username | Sanitise usernames for safety |
| sanitisation.py | sanitise_command_args | Sanitise command arguments |
| sanitisation.py | sanitise_for_db | Sanitise inputs for database operations |
| sanitisation.py | strip_twitch_emotes | Remove Twitch emotes from text |
| sanitisation.py | sanitise_html | Sanitise HTML content for any web components |
| sanitisation.py | remove_non_alphanumeric | Strip all non-alphanumeric characters |
| sanitisation.py | clean_numeric_string | Clean and validate numeric string input |

## Security Utilities
| Module | Function | Description |
|--------|----------|-------------|
| security.py | generate_secure_token | Generate secure tokens for authentication |
| security.py | hash_password | Securely hash passwords |
| security.py | verify_password | Verify password against stored hash |
| security.py | sanitise_path | Sanitise file paths to prevent directory traversal |
| security.py | is_valid_oauth_token | Validate OAuth token format |
| security.py | mask_sensitive_data | Mask sensitive data in logs |
| security.py | is_safe_string | Check if string contains potentially unsafe content |
| security.py | rate_limit_key | Generate keys for rate limiting |

## Permissions and Rate Limiting
| Module | Function | Description |
|--------|----------|-------------|
| permission.py | check_permission | Check if user has permission for action |
| permission.py | get_user_role | Get role level of user |
| permission.py | is_broadcaster | Check if user is the broadcaster |
| permission.py | is_moderator | Check if user is a moderator |
| permission.py | is_vip | Check if user is a VIP |
| permission.py | is_subscriber | Check if user is a subscriber |
| permission.py | is_elevated | Check if user has elevated permissions |

## Throttling Utilities
| Module | Function | Description |
|--------|----------|-------------|
| throttling.py | token_bucket | Token bucket algorithm implementation |
| throttling.py | rate_limit | Rate limit function execution |
| throttling.py | throttle_message | Throttle outgoing chat messages |
| throttling.py | per_user_rate_limit | Apply rate limits per user |
| throttling.py | command_throttle | Throttle command execution |

## Time-Related Utilities
| Module | Function | Description |
|--------|----------|-------------|
| time.py | get_current_timestamp | Get current timestamp |
| time.py | get_current_datetime | Get current datetime object |
| time.py | format_datetime | Format datetime for display |
| time.py | parse_datetime | Parse datetime from string |
| time.py | get_time_difference | Calculate time difference between two times |
| time.py | is_expired | Check if timestamp is expired |
| time.py | get_random_delay | Generate random time delay |
| time.py | format_cooldown | Format cooldown time remaining |
| time.py | sleep | Asynchronous sleep function |
| time.py | with_timeout | Execute function with timeout |

## Queue Management
| Module | Function | Description |
|--------|----------|-------------|
| queue.py | priority_message_queue | Queue for prioritised chat messages |
| queue.py | command_queue | Queue for command execution |
| queue.py | duel_queue | Queue for duel challenges |
| queue.py | task_queue | Queue for asynchronous tasks |
| queue.py | add_to_queue | Add item to appropriate queue |
| queue.py | process_queue | Process items from queue |

## Random Utilities
| Module | Function | Description |
|--------|----------|-------------|
| random.py | random_choice | Select random item from list |
| random.py | random_choices | Select multiple random items from list |
| random.py | random_sample | Sample random items without replacement |
| random.py | random_int | Generate random integer in range |
| random.py | random_float | Generate random float in range |
| random.py | random_string | Generate random string |
| random.py | shuffle_list | Shuffle list in place |
| random.py | weighted_choice | Select item based on weights |
| random.py | random_bool | Generate random boolean with probability |
| random.py | calculate_random_odds | Calculate if random event occurs |

## Cooldown Management
| Module | Function | Description |
|--------|----------|-------------|
| cooldown.py | add_cooldown | Add cooldown for command/user |
| cooldown.py | check_cooldown | Check if command/user is on cooldown |
| cooldown.py | get_remaining_cooldown | Get remaining cooldown time |
| cooldown.py | reset_cooldown | Reset cooldown for command/user |
| cooldown.py | get_bucket_key | Get bucket key for cooldown |
| cooldown.py | register_cooldown | Register new cooldown type |

## Database Utilities
| Module | Function | Description |
|--------|----------|-------------|
| db.py | connect_db | Connect to database |
| db.py | close_db | Close database connection |
| db.py | execute_query | Execute SQL query |
| db.py | execute_transaction | Execute transaction with multiple queries |
| db.py | get_user | Get user from database |
| db.py | update_user_points | Update user's points/XP |
| db.py | get_item | Get item details from database |
| db.py | backup_db | Create database backup |
| db.py | check_db_integrity | Check database integrity |

## OBS Integration Utilities
| Module | Function | Description |
|--------|----------|-------------|
| obs.py | connect_obs | Connect to OBS WebSocket |
| obs.py | disconnect_obs | Disconnect from OBS WebSocket |
| obs.py | switch_scene | Switch to different scene |
| obs.py | toggle_source | Toggle source visibility |
| obs.py | set_source_position | Set position of source |
| obs.py | animate_source | Animate source movement |
| obs.py | toggle_filter | Toggle filter on/off |
| obs.py | set_text_content | Set content of text source |
| obs.py | toggle_audio | Toggle audio source mute state |
| obs.py | start_stop_stream | Start or stop stream |
| obs.py | start_stop_recording | Start or stop recording |

## Twitch Integration Utilities
| Module | Function | Description |
|--------|----------|-------------|
| twitch.py | send_chat_message | Send message to Twitch chat |
| twitch.py | timeout_user | Timeout user in chat |
| twitch.py | get_channel_rewards | Get channel point rewards |
| twitch.py | update_stream_title | Update stream title |
| twitch.py | get_user_info | Get information about Twitch user |
| twitch.py | handle_bits_event | Handle bits donation event |
| twitch.py | handle_reward_redemption | Handle channel point reward redemption |
| twitch.py | toggle_emote_only_mode | Toggle emote-only mode in chat |
| twitch.py | toggle_sub_only_mode | Toggle subscriber-only mode in chat |
| twitch.py | toggle_follower_only_mode | Toggle follower-only mode in chat |

## Duel System Utilities
| Module | Function | Description |
|--------|----------|-------------|
| duel.py | create_duel | Create new duel challenge |
| duel.py | accept_duel | Accept duel challenge |
| duel.py | reject_duel | Reject duel challenge |
| duel.py | calculate_winner | Calculate duel winner |
| duel.py | get_environmental_bonus | Calculate environmental bonuses/penalties |
| duel.py | reduce_durability | Reduce durability of equipment |
| duel.py | check_underdog_win | Check if underdog win occurs |
| duel.py | distribute_pot | Distribute duel pot to winner |
| duel.py | format_duel_result | Format duel result for chat |
| duel.py | calculate_equipment_score | Calculate base score from equipment stats |
| duel.py | calculate_environment_effect | Calculate effect of environment on equipment |
| duel.py | format_duel_challenge | Format duel challenge notification for chat |
| duel.py | format_duel_timeout | Format duel timeout notification for chat |
| duel.py | format_durability_change | Format durability change notification |
| duel.py | format_duel_stats | Format duel statistics for display |
| duel.py | format_duel_history | Format user's duel history for display |
| duel.py | format_duel_leaderboard | Format duel leaderboard for display |
| duel.py | format_environment_description | Format environment description with effects |
| duel.py | generate_duel_id | Generate unique ID for duel challenge |
| duel.py | is_valid_duel_amount | Validate duel amount is within allowed range |
| duel.py | calculate_underdog_factor | Calculate underdog factor based on score difference |
| duel.py | get_duel_timeout_time | Calculate when duel challenge should time out |
| duel.py | is_equipment_compatible | Check if equipment is compatible with environment |
| duel.py | determine_equipment_advantage | Determine equipment advantage in environment |
| duel.py | track_duel_metrics | Track metrics for duel system analytics |
| duel.py | get_user_duel_rank | Get user's rank based on duel statistics |
| duel.py | calculate_win_probability | Calculate win probability for duel participants |
| duel.py | format_win_loss_record | Format user's win/loss record for display |
| duel.py | categorise_duel_participants | Categorise participants by experience level |

## Shop System Utilities
| Module | Function | Description |
|--------|----------|-------------|
| shop.py | get_shop_items | Get available shop items |
| shop.py | get_item_cost | Get cost of specific item |
| shop.py | purchase_item | Process item purchase |
| shop.py | upgrade_equipment | Upgrade weapon or armour |
| shop.py | add_modification | Add modification to equipment |
| shop.py | check_ownership | Check if user owns specific item |
| shop.py | format_shop_display | Format shop display for chat |
| shop.py | get_next_upgrade | Get next available upgrade for user |
| shop.py | check_affordability | Check if user can afford item |

## Deck of Many Things Utilities

| Module | Function | Description |
|--------|----------|-------------|
| domt.py | draw_card | Draw card from deck |
| domt.py | process_card_effect | Process effect of drawn card |
| domt.py | reset_deck | Reset deck when all cards drawn |
| domt.py | get_remaining_cards | Get count of remaining cards |
| domt.py | add_card_to_inventory | Add card to user's inventory |
| domt.py | use_card_from_inventory | Use card from user's inventory |
| domt.py | format_card_result | Format card draw result for chat |
| domt.py | format_card_description | Format description of card |
| domt.py | format_card_effect | Format description of card effect |
| domt.py | validate_bits_for_draw | Validate bits amount for card draw |
| domt.py | calculate_effect_chance | Calculate chance of effect happening |
| domt.py | check_retainable_card | Check if card can be retained |
| domt.py | generate_card_display | Generate formatted card display |
| domt.py | parse_card_parameters | Parse parameters for card effect |
| domt.py | get_card_stats | Get statistics for specific card |
| domt.py | format_deck_status | Format deck status for display |
| domt.py | format_cards_inventory | Format user's owned cards for display |
| domt.py | check_card_compatibility | Check if card is compatible with user |
| domt.py | get_card_history | Get history of card draws |
| domt.py | calculate_card_probability | Calculate probability of drawing card |

## OBS Card Animation Utilities

| Module | Function | Description |
|--------|----------|-------------|
| obs_cards.py | show_card_in_obs | Show card in OBS |
| obs_cards.py | hide_card_in_obs | Hide card in OBS |
| obs_cards.py | animate_card_reveal | Animate card reveal in OBS |
| obs_cards.py | animate_card_flip | Animate card flip in OBS |
| obs_cards.py | create_card_sequence | Create OBS action sequence for card |
| obs_cards.py | apply_card_filter | Apply filter for card effect |
| obs_cards.py | remove_card_filter | Remove filter for card effect |
| obs_cards.py | set_card_position | Set position of card in OBS |
| obs_cards.py | play_card_sound | Play sound for card draw |
| obs_cards.py | create_card_animation | Create animation for card |

## Bits Integration Utilities

| Module | Function | Description |
|--------|----------|-------------|
| bits_domt.py | validate_domt_bits | Validate bits for DOMT draw |
| bits_domt.py | process_domt_bits | Process bits for DOMT draw |
| bits_domt.py | calculate_bits_cost | Calculate cost in bits for card draw |
| bits_domt.py | format_bits_notification | Format bits donation notification for DOMT |
| bits_domt.py | track_bits_spending | Track bits spent on DOMT |

## Inventory System Utilities
| Module | Function | Description |
|--------|----------|-------------|
| inventory.py | get_user_inventory | Get user's complete inventory |
| inventory.py | get_user_gear | Get user's equipped gear |
| inventory.py | get_user_toys | Get user's toys |
| inventory.py | get_user_cards | Get user's DOMT cards |
| inventory.py | add_to_inventory | Add item to user's inventory |
| inventory.py | remove_from_inventory | Remove item from user's inventory |
| inventory.py | format_inventory_display | Format inventory display for chat |
| inventory.py | check_inventory_space | Check if user has inventory space |
| inventory.py | get_item_details | Get detailed information about item |
| inventory.py | use_inventory_item | Use item from inventory |
| inventory.py | transfer_inventory_item | Transfer item between users |
| inventory.py | count_inventory_items | Count specific items in inventory |
| inventory.py | search_inventory | Search inventory for matching items |
| inventory.py | categorise_inventory | Group inventory items by category |
| inventory.py | sort_inventory | Sort inventory by various criteria |
| inventory.py | validate_item_transfer | Validate if item transfer is allowed |
| inventory.py | format_durability_bar | Format visual durability bar for display |
| inventory.py | calculate_equipment_stats | Calculate combined stats from equipment |
| inventory.py | check_cooldown_status | Check if item is on cooldown for usage |
| inventory.py | format_cooldown_remaining | Format remaining cooldown time |
| inventory.py | generate_item_history | Generate history of item acquisitions and usage |

## Command Parsing and Validation

| Module | Function | Description |
|--------|----------|-------------|
| command.py | is_hidden_command | Check if command is hidden based on metadata |
| command.py | is_admin_command | Check if command has admin-only permission level |
| command.py | should_execute_command | Determine if command should be executed based on context |
| command.py | normalise_command_name | Normalise command name for internal processing |
| command.py | validate_command_name | Validate that a command name meets requirements |
| command.py | collect_command_metadata | Collect metadata from command decorators |
| command.py | format_argument_help | Format argument help text for command help display |
| command.py | get_command_categories | Get all command categories from registered commands |
| command.py | filter_commands_for_user | Filter commands based on user's permissions |
| command.py | format_command_group_help | Format help text for command groups |
| command.py | generate_command_signature | Generate command signature from argument definitions |
| command.py | format_cooldown_info | Format cooldown information for display |
| command.py | format_permission_info | Format permission requirements for display |

## Event Utilities

| Module | Function | Description |
|--------|----------|-------------|
| event.py | event_to_dict | Convert event object to dictionary representation |
| event.py | dict_to_event | Convert dictionary to event object |
| event.py | merge_event_data | Merge data from multiple events |
| event.py | filter_event_data | Filter sensitive data from event |
| event.py | get_event_type | Get standardised event type from event object |
| event.py | is_same_event_type | Compare if two events are of same type |
| event.py | extract_event_metadata | Extract metadata from event |
| event.py | create_event_id | Create unique ID for event |
| event.py | categorise_event | Categorise event into standard categories |
| event.py | format_event_for_display | Format event for user-friendly display |
| event.py | generate_event_timestamp | Generate consistent timestamp for event |
| event.py | copy_event | Create deep copy of event |
| event.py | prioritise_event | Determine priority level for event |
| event.py | match_event_pattern | Match event against pattern specification |

## EventBus Utilities

| Module | Function | Description |
|--------|----------|-------------|
| eventbus.py | create_event_subscription | Create standardised event subscription |
| eventbus.py | parse_event_pattern | Parse event pattern for subscription |
| eventbus.py | match_subscription | Check if event matches subscription pattern |
| eventbus.py | get_subscription_key | Generate key for subscription |
| eventbus.py | filter_event_subscriptions | Filter subscriptions by criteria |
| eventbus.py | sort_subscribers | Sort subscribers by priority |
| eventbus.py | validate_event_handler | Validate handler function or method |
| eventbus.py | wrap_sync_handler | Wrap synchronous handler for async execution |
| eventbus.py | wrap_async_handler | Wrap async handler for sync execution |

## Event Scheduling Utilities

| Module | Function | Description |
|--------|----------|-------------|
| event_scheduling.py | calculate_next_occurrence | Calculate next occurrence for recurring event |
| event_scheduling.py | parse_cron_expression | Parse cron expression for scheduling |
| event_scheduling.py | create_schedule | Create schedule from specification |
| event_scheduling.py | is_event_due | Check if scheduled event is due |
| event_scheduling.py | get_time_until_event | Get time until scheduled event |
| event_scheduling.py | sort_scheduled_events | Sort events by scheduled time |
| event_scheduling.py | create_recurring_schedule | Create schedule for recurring event |
| event_scheduling.py | validate_schedule | Validate schedule specification |

## Points Utility Functions

| Module | Function | Description |
|--------|----------|-------------|
| points.py | calculate_earning_rate | Calculate points earning rate based on user activity |
| points.py | calculate_points_over_time | Calculate points earned over time period |
| points.py | validate_points_amount | Validate points amount is within allowed range |
| points.py | check_points_transfer | Check if points transfer is valid |
| points.py | calculate_gamble_outcome | Calculate outcome of points gambling |
| points.py | format_points_leaderboard | Format points leaderboard for display |
| points.py | calculate_points_statistics | Calculate statistics for points economy |
| points.py | convert_bits_to_points | Convert Twitch bits to points amount |
| points.py | convert_subscription_to_points | Convert subscription to points amount |
| points.py | estimate_watch_time_points | Estimate points earned from watch time |
| points.py | apply_points_multiplier | Apply multiplier to points amount |
| points.py | calculate_points_inflation | Calculate inflation rate in points economy |
| points.py | format_transaction_history | Format points transaction history for display |
| points.py | generate_earning_summary | Generate summary of points earning sources |
| points.py | generate_spending_summary | Generate summary of points spending sinks |

## Economy Analysis Utilities

| Module | Function | Description |
|--------|----------|-------------|
| economy.py | calculate_gini_coefficient | Calculate Gini coefficient for points distribution |
| economy.py | calculate_points_velocity | Calculate velocity of points in economy |
| economy.py | detect_points_anomalies | Detect anomalies in points transactions |
| economy.py | calculate_points_sink_ratio | Calculate ratio of points sinks to sources |
| economy.py | predict_points_inflation | Predict future inflation rate |
| economy.py | recommend_economy_adjustments | Recommend adjustments to balance economy |
| economy.py | simulate_economy_change | Simulate effect of economy parameter change |
| economy.py | calculate_economy_health | Calculate overall health of points economy |

## Shop System Utilities

| Module | Function | Description |
|--------|----------|-------------|
| shop.py | format_shop_display | Format shop items for display in chat |
| shop.py | format_item_details | Format detailed item information |
| shop.py | categorise_items | Group items by category for display |
| shop.py | get_next_level_item | Get next level item for upgrading |
| shop.py | calculate_upgrade_cost | Calculate cost to upgrade to next level |
| shop.py | calculate_refund_value | Calculate refund value for an item |
| shop.py | calculate_effective_cost | Calculate effective cost after discounts |
| shop.py | validate_modification_compatibility | Check if modification is compatible with item |
| shop.py | format_item_comparison | Format comparison between two items |
| shop.py | format_equipment_stats | Format weapon or armour statistics |
| shop.py | generate_item_description | Generate description for an item |
| shop.py | fuzzy_search_items | Search for items using fuzzy matching |
| shop.py | format_durability_display | Format durability display for items |
| shop.py | calculate_modification_bonus | Calculate bonus from item modifications |
| shop.py | recommend_user_upgrade | Recommend next upgrade for user |
| shop.py | get_affordable_items | Get items user can afford from shop |
| shop.py | check_level_requirement | Check if user meets level requirements |
| shop.py | calculate_bulk_purchase_discount | Calculate discount for bulk purchases |
| shop.py | format_owned_vs_available | Format comparison of owned vs available items |
| shop.py | calculate_total_cost | Calculate total cost for multiple purchases |
