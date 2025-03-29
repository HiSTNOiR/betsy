# Easter Eggs Package Structure and Components

The `features/easter_eggs` package implements hidden features and rewards for the Twitch bot, providing special interactions for users who discover specific triggers or meet certain conditions. This document outlines the structure and purpose of each module within the easter eggs feature package.

## Easter Egg Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | EasterEggManager | Main manager class for easter egg functionality |
| manager.py | EasterEggManager.initialise | Initialise easter eggs system |
| manager.py | EasterEggManager.shutdown | Shut down easter eggs system |
| manager.py | EasterEggManager.register_egg | Register new easter egg |
| manager.py | EasterEggManager.unregister_egg | Unregister easter egg |
| manager.py | EasterEggManager.get_egg | Get easter egg by identifier |
| manager.py | EasterEggManager.get_all_eggs | Get all registered easter eggs |
| manager.py | EasterEggManager.process_message | Process chat message for easter eggs |
| manager.py | EasterEggManager.process_command | Process command for easter eggs |
| manager.py | EasterEggManager.process_event | Process event for easter eggs |
| manager.py | EasterEggManager.trigger_egg | Trigger specific easter egg |
| manager.py | EasterEggManager.check_conditions | Check if conditions are met for egg |
| manager.py | EasterEggManager.register_trigger | Register trigger for easter egg |
| manager.py | EasterEggManager.register_condition | Register condition for easter eggs |
| manager.py | EasterEggManager.register_reward | Register reward for easter eggs |
| manager.py | get_egg_manager | Get singleton manager instance |
| manager.py | initialise | Initialise easter eggs system with global manager |
| manager.py | shutdown | Shutdown easter eggs system with global manager |

## Easter Egg Definition
| Module | Function | Description |
|--------|----------|-------------|
| eggs/base.py | EasterEgg | Base class for all easter eggs |
| eggs/base.py | EasterEgg.get_id | Get egg identifier |
| eggs/base.py | EasterEgg.get_name | Get egg name |
| eggs/base.py | EasterEgg.get_description | Get egg description |
| eggs/base.py | EasterEgg.get_trigger | Get egg trigger |
| eggs/base.py | EasterEgg.get_conditions | Get egg conditions |
| eggs/base.py | EasterEgg.get_reward | Get egg reward |
| eggs/base.py | EasterEgg.is_enabled | Check if egg is enabled |
| eggs/base.py | EasterEgg.is_triggered_by | Check if egg is triggered by input |
| eggs/base.py | EasterEgg.check_conditions | Check if conditions are met |
| eggs/base.py | EasterEgg.apply_reward | Apply reward for egg |
| eggs/base.py | EasterEgg.has_triggered_for_user | Check if egg has triggered for user |
| eggs/base.py | EasterEgg.reset_for_user | Reset egg trigger status for user |
| eggs/base.py | EasterEgg.to_dict | Convert egg to dictionary |
| eggs/base.py | EasterEgg.from_dict | Create egg from dictionary |
| eggs/base.py | EggRegistry | Registry for easter egg types |
| eggs/base.py | register_egg | Register easter egg with registry |
| eggs/base.py | get_egg_registry | Get singleton egg registry |

## Emote Combo System
| Module | Function | Description |
|--------|----------|-------------|
| eggs/emote_combo.py | EmoteComboEgg | Easter egg for emote combinations |
| eggs/emote_combo.py | EmoteComboEgg.get_emote_sequence | Get required emote sequence |
| eggs/emote_combo.py | EmoteComboEgg.get_users_required | Get number of users required |
| eggs/emote_combo.py | EmoteComboEgg.get_reward_xp | Get XP reward amount |
| eggs/emote_combo.py | EmoteComboEgg.is_triggered_by | Check if message contributes to combo |
| eggs/emote_combo.py | EmoteComboEgg.add_emote_to_sequence | Add emote to current sequence |
| eggs/emote_combo.py | EmoteComboEgg.check_sequence_completion | Check if sequence is complete |
| eggs/emote_combo.py | EmoteComboEgg.reset_sequence | Reset current sequence |
| eggs/emote_combo.py | EmoteComboEgg.get_current_sequence | Get current sequence progress |
| eggs/emote_combo.py | EmoteComboEgg.apply_reward | Apply reward to participants |
| eggs/emote_combo.py | EmoteComboEgg.get_sequence_progress | Get progress percentage for sequence |
| eggs/emote_combo.py | EmoteComboEgg.get_participating_users | Get users participating in current sequence |
| eggs/emote_combo.py | EmoteComboEgg.format_combo_notification | Format notification for completed combo |
| eggs/emote_combo.py | EmoteComboTracker | Tracker for emote combo progress |
| eggs/emote_combo.py | EmoteComboTracker.add_emote | Add emote to sequence |
| eggs/emote_combo.py | EmoteComboTracker.is_sequence_complete | Check if sequence is complete |
| eggs/emote_combo.py | EmoteComboTracker.reset | Reset tracker state |
| eggs/emote_combo.py | EmoteComboTracker.get_progress | Get progress status |
| eggs/emote_combo.py | register_emote_combo_egg | Register emote combo easter egg |
| eggs/emote_combo.py | create_emote_combo | Create new emote combo egg |

## Self-Targeting Egg
| Module | Function | Description |
|--------|----------|-------------|
| eggs/self_targeting.py | SelfTargetingEgg | Easter egg for self-targeting prevention |
| eggs/self_targeting.py | SelfTargetingEgg.is_triggered_by | Check if command targets self |
| eggs/self_targeting.py | SelfTargetingEgg.apply_reward | Apply "reward" (points deduction) |
| eggs/self_targeting.py | SelfTargetingEgg.get_target_commands | Get commands affected by egg |
| eggs/self_targeting.py | SelfTargetingEgg.get_points_penalty | Get points penalty amount |
| eggs/self_targeting.py | SelfTargetingEgg.get_recipient | Get recipient of deducted points |
| eggs/self_targeting.py | SelfTargetingEgg.format_penalty_notification | Format notification for penalty |
| eggs/self_targeting.py | SelfTargetingEgg.check_conditions | Check if conditions are met for egg |
| eggs/self_targeting.py | SelfTargetingEgg.detect_self_targeting | Detect self-targeting in command |
| eggs/self_targeting.py | register_self_targeting_egg | Register self-targeting easter egg |
| eggs/self_targeting.py | create_self_targeting_egg | Create new self-targeting egg |

## Message Timing Egg
| Module | Function | Description |
|--------|----------|-------------|
| eggs/message_timing.py | MessageTimingEgg | Easter egg for precise message timing |
| eggs/message_timing.py | MessageTimingEgg.is_triggered_by | Check if message matches timing pattern |
| eggs/message_timing.py | MessageTimingEgg.apply_reward | Apply reward for consistent timing |
| eggs/message_timing.py | MessageTimingEgg.get_target_interval | Get target interval between messages |
| eggs/message_timing.py | MessageTimingEgg.get_tolerance | Get allowed tolerance from exact timing |
| eggs/message_timing.py | MessageTimingEgg.get_streak_requirement | Get required streak for reward |
| eggs/message_timing.py | MessageTimingEgg.get_bonus_multiplier | Get XP bonus multiplier |
| eggs/message_timing.py | MessageTimingEgg.update_user_timing | Update timing data for user |
| eggs/message_timing.py | MessageTimingEgg.check_user_streak | Check if user has achieved streak |
| eggs/message_timing.py | MessageTimingEgg.get_user_streak | Get current streak count for user |
| eggs/message_timing.py | MessageTimingEgg.reset_user_streak | Reset streak count for user |
| eggs/message_timing.py | MessageTimingEgg.format_streak_notification | Format notification for achieved streak |
| eggs/message_timing.py | MessageTimingTracker | Tracker for user message timing |
| eggs/message_timing.py | MessageTimingTracker.add_message | Add message timestamp |
| eggs/message_timing.py | MessageTimingTracker.check_interval | Check if message matches interval |
| eggs/message_timing.py | MessageTimingTracker.get_streak | Get current streak count |
| eggs/message_timing.py | MessageTimingTracker.reset | Reset tracker state |
| eggs/message_timing.py | register_message_timing_egg | Register message timing easter egg |
| eggs/message_timing.py | create_message_timing_egg | Create new message timing egg |

## Secret Command Egg
| Module | Function | Description |
|--------|----------|-------------|
| eggs/secret_command.py | SecretCommandEgg | Easter egg for hidden commands |
| eggs/secret_command.py | SecretCommandEgg.is_triggered_by | Check if message matches secret command |
| eggs/secret_command.py | SecretCommandEgg.apply_reward | Apply reward for finding secret command |
| eggs/secret_command.py | SecretCommandEgg.get_command | Get secret command trigger |
| eggs/secret_command.py | SecretCommandEgg.get_reward_description | Get description of reward |
| eggs/secret_command.py | SecretCommandEgg.get_usage_limit | Get usage limit per user |
| eggs/secret_command.py | SecretCommandEgg.increment_usage_count | Increment usage count for user |
| eggs/secret_command.py | SecretCommandEgg.get_usage_count | Get usage count for user |
| eggs/secret_command.py | SecretCommandEgg.format_reward_notification | Format notification for reward |
| eggs/secret_command.py | SecretCommandEgg.hide_from_logs | Check if command should be hidden from logs |
| eggs/secret_command.py | register_secret_command_egg | Register secret command easter egg |
| eggs/secret_command.py | create_secret_command_egg | Create new secret command egg |

## Random Event Egg
| Module | Function | Description |
|--------|----------|-------------|
| eggs/random_event.py | RandomEventEgg | Easter egg for random events |
| eggs/random_event.py | RandomEventEgg.is_triggered_by | Check if random event triggers |
| eggs/random_event.py | RandomEventEgg.apply_reward | Apply reward for random event |
| eggs/random_event.py | RandomEventEgg.get_trigger_chance | Get chance of triggering |
| eggs/random_event.py | RandomEventEgg.get_cooldown | Get cooldown between triggers |
| eggs/random_event.py | RandomEventEgg.check_cooldown | Check if egg is on cooldown |
| eggs/random_event.py | RandomEventEgg.put_on_cooldown | Put egg on cooldown after triggering |
| eggs/random_event.py | RandomEventEgg.get_event_description | Get description of random event |
| eggs/random_event.py | RandomEventEgg.format_event_notification | Format notification for event |
| eggs/random_event.py | RandomEventEgg.get_eligible_users | Get users eligible for random event |
| eggs/random_event.py | register_random_event_egg | Register random event easter egg |
| eggs/random_event.py | create_random_event_egg | Create new random event egg |

## Easter Egg Trigger System
| Module | Function | Description |
|--------|----------|-------------|
| triggers/base.py | EggTrigger | Base class for easter egg triggers |
| triggers/base.py | EggTrigger.get_type | Get trigger type |
| triggers/base.py | EggTrigger.matches | Check if input matches trigger |
| triggers/base.py | EggTrigger.reset | Reset trigger state |
| triggers/base.py | EggTrigger.to_dict | Convert trigger to dictionary |
| triggers/base.py | EggTrigger.from_dict | Create trigger from dictionary |
| triggers/base.py | TriggerRegistry | Registry for trigger types |
| triggers/base.py | register_trigger_type | Register trigger type with registry |
| triggers/base.py | get_trigger_registry | Get singleton trigger registry |
| triggers/base.py | create_trigger | Create trigger from parameters |

## Message Pattern Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/message.py | MessagePatternTrigger | Trigger for message pattern matching |
| triggers/message.py | MessagePatternTrigger.matches | Check if message matches pattern |
| triggers/message.py | MessagePatternTrigger.get_pattern | Get trigger pattern |
| triggers/message.py | MessagePatternTrigger.is_regex | Check if pattern is regex |
| triggers/message.py | register_message_trigger | Register message pattern trigger |
| triggers/message.py | create_message_trigger | Create new message pattern trigger |

## Command Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/command.py | CommandTrigger | Trigger for command execution |
| triggers/command.py | CommandTrigger.matches | Check if command matches trigger |
| triggers/command.py | CommandTrigger.get_command | Get trigger command |
| triggers/command.py | CommandTrigger.requires_arguments | Check if trigger requires arguments |
| triggers/command.py | register_command_trigger | Register command trigger |
| triggers/command.py | create_command_trigger | Create new command trigger |

## Event Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/event.py | EventTrigger | Trigger for system events |
| triggers/event.py | EventTrigger.matches | Check if event matches trigger |
| triggers/event.py | EventTrigger.get_event_type | Get trigger event type |
| triggers/event.py | EventTrigger.get_event_filter | Get event filter criteria |
| triggers/event.py | register_event_trigger | Register event trigger |
| triggers/event.py | create_event_trigger | Create new event trigger |

## User State Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/user_state.py | UserStateTrigger | Trigger for specific user states |
| triggers/user_state.py | UserStateTrigger.matches | Check if user state matches trigger |
| triggers/user_state.py | UserStateTrigger.get_state_criteria | Get state criteria |
| triggers/user_state.py | UserStateTrigger.compare_user_state | Compare user state to criteria |
| triggers/user_state.py | register_user_state_trigger | Register user state trigger |
| triggers/user_state.py | create_user_state_trigger | Create new user state trigger |

## Random Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/random.py | RandomTrigger | Trigger with random chance |
| triggers/random.py | RandomTrigger.matches | Check if trigger activates randomly |
| triggers/random.py | RandomTrigger.get_chance | Get activation chance |
| triggers/random.py | RandomTrigger.get_seed | Get random seed if used |
| triggers/random.py | register_random_trigger | Register random trigger |
| triggers/random.py | create_random_trigger | Create new random trigger |

## Easter Egg Conditions
| Module | Function | Description |
|--------|----------|-------------|
| conditions/base.py | EggCondition | Base class for easter egg conditions |
| conditions/base.py | EggCondition.is_met | Check if condition is met |
| conditions/base.py | EggCondition.get_description | Get condition description |
| conditions/base.py | EggCondition.to_dict | Convert condition to dictionary |
| conditions/base.py | EggCondition.from_dict | Create condition from dictionary |
| conditions/base.py | ConditionRegistry | Registry for condition types |
| conditions/base.py | register_condition_type | Register condition type with registry |
| conditions/base.py | get_condition_registry | Get singleton condition registry |
| conditions/base.py | create_condition | Create condition from parameters |

## User Role Condition
| Module | Function | Description |
|--------|----------|-------------|
| conditions/user_role.py | UserRoleCondition | Condition for user role requirements |
| conditions/user_role.py | UserRoleCondition.is_met | Check if user has required role |
| conditions/user_role.py | UserRoleCondition.get_roles | Get allowed roles |
| conditions/user_role.py | register_user_role_condition | Register user role condition |
| conditions/user_role.py | create_user_role_condition | Create new user role condition |

## Points Condition
| Module | Function | Description |
|--------|----------|-------------|
| conditions/points.py | PointsCondition | Condition for points requirements |
| conditions/points.py | PointsCondition.is_met | Check if user has required points |
| conditions/points.py | PointsCondition.get_min_points | Get minimum points required |
| conditions/points.py | PointsCondition.get_max_points | Get maximum points allowed |
| conditions/points.py | register_points_condition | Register points condition |
| conditions/points.py | create_points_condition | Create new points condition |

## Stream State Condition
| Module | Function | Description |
|--------|----------|-------------|
| conditions/stream.py | StreamStateCondition | Condition for stream state requirements |
| conditions/stream.py | StreamStateCondition.is_met | Check if stream state matches requirement |
| conditions/stream.py | StreamStateCondition.get_required_state | Get required stream state |
| conditions/stream.py | register_stream_state_condition | Register stream state condition |
| conditions/stream.py | create_stream_state_condition | Create new stream state condition |

## Time Condition
| Module | Function | Description |
|--------|----------|-------------|
| conditions/time.py | TimeCondition | Condition for time requirements |
| conditions/time.py | TimeCondition.is_met | Check if current time meets condition |
| conditions/time.py | TimeCondition.get_time_range | Get allowed time range |
| conditions/time.py | TimeCondition.get_days | Get allowed days |
| conditions/time.py | register_time_condition | Register time condition |
| conditions/time.py | create_time_condition | Create new time condition |

## Usage Limit Condition
| Module | Function | Description |
|--------|----------|-------------|
| conditions/usage.py | UsageLimitCondition | Condition for usage limit requirements |
| conditions/usage.py | UsageLimitCondition.is_met | Check if usage is within limits |
| conditions/usage.py | UsageLimitCondition.get_limit | Get usage limit |
| conditions/usage.py | UsageLimitCondition.get_period | Get period for limit |
| conditions/usage.py | UsageLimitCondition.increment_usage | Increment usage count |
| conditions/usage.py | UsageLimitCondition.get_usage | Get current usage count |
| conditions/usage.py | UsageLimitCondition.reset_usage | Reset usage count |
| conditions/usage.py | register_usage_limit_condition | Register usage limit condition |
| conditions/usage.py | create_usage_limit_condition | Create new usage limit condition |

## Easter Egg Rewards
| Module | Function | Description |
|--------|----------|-------------|
| rewards/base.py | EggReward | Base class for easter egg rewards |
| rewards/base.py | EggReward.apply | Apply reward to recipient(s) |
| rewards/base.py | EggReward.get_description | Get reward description |
| rewards/base.py | EggReward.to_dict | Convert reward to dictionary |
| rewards/base.py | EggReward.from_dict | Create reward from dictionary |
| rewards/base.py | RewardRegistry | Registry for reward types |
| rewards/base.py | register_reward_type | Register reward type with registry |
| rewards/base.py | get_reward_registry | Get singleton reward registry |
| rewards/base.py | create_reward | Create reward from parameters |

## Points Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/points.py | PointsReward | Reward for awarding points |
| rewards/points.py | PointsReward.apply | Apply points to recipient(s) |
| rewards/points.py | PointsReward.get_amount | Get points amount |
| rewards/points.py | PointsReward.is_percentage | Check if amount is percentage of user's points |
| rewards/points.py | PointsReward.calculate_amount | Calculate actual points amount |
| rewards/points.py | register_points_reward | Register points reward |
| rewards/points.py | create_points_reward | Create new points reward |

## Points Multiplier Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/multiplier.py | MultiplierReward | Reward for applying points multiplier |
| rewards/multiplier.py | MultiplierReward.apply | Apply multiplier to recipient(s) |
| rewards/multiplier.py | MultiplierReward.get_multiplier | Get multiplier value |
| rewards/multiplier.py | MultiplierReward.get_duration | Get multiplier duration |
| rewards/multiplier.py | MultiplierReward.calculate_end_time | Calculate when multiplier ends |
| rewards/multiplier.py | register_multiplier_reward | Register multiplier reward |
| rewards/multiplier.py | create_multiplier_reward | Create new multiplier reward |

## Item Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/item.py | ItemReward | Reward for awarding items |
| rewards/item.py | ItemReward.apply | Apply item to recipient(s) |
| rewards/item.py | ItemReward.get_item | Get item to award |
| rewards/item.py | ItemReward.add_to_inventory | Add item to user's inventory |
| rewards/item.py | register_item_reward | Register item reward |
| rewards/item.py | create_item_reward | Create new item reward |

## OBS Action Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/obs_action.py | OBSActionReward | Reward for triggering OBS actions |
| rewards/obs_action.py | OBSActionReward.apply | Apply OBS action sequence |
| rewards/obs_action.py | OBSActionReward.get_action_sequence | Get action sequence to execute |
| rewards/obs_action.py | register_obs_action_reward | Register OBS action reward |
| rewards/obs_action.py | create_obs_action_reward | Create new OBS action reward |

## Card Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/card.py | CardReward | Reward for awarding DOMT cards |
| rewards/card.py | CardReward.apply | Apply card to recipient(s) |
| rewards/card.py | CardReward.get_card | Get card to award |
| rewards/card.py | CardReward.add_to_inventory | Add card to user's inventory |
| rewards/card.py | register_card_reward | Register card reward |
| rewards/card.py | create_card_reward | Create new card reward |

## Message Reward
| Module | Function | Description |
|--------|----------|-------------|
| rewards/message.py | MessageReward | Reward for sending special messages |
| rewards/message.py | MessageReward.apply | Apply message to chat |
| rewards/message.py | MessageReward.get_message | Get message to send |
| rewards/message.py | MessageReward.format_message | Format message with variables |
| rewards/message.py | register_message_reward | Register message reward |
| rewards/message.py | create_message_reward | Create new message reward |

## Easter Egg Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_easter_egg_commands | Register all easter egg-related commands |
| commands.py | ComboCommand | Command to view active emote combos |
| commands.py | ComboCommand.execute | Display active emote combinations |
| commands.py | StreakCommand | Command to view timing streaks |
| commands.py | StreakCommand.execute | Display current timing streak status |
| commands.py | AdminEggCommand | Administrative command group for easter eggs |
| commands.py | CreateEggCommand | Admin command to create easter egg |
| commands.py | CreateEggCommand.execute | Process easter egg creation |
| commands.py | RemoveEggCommand | Admin command to remove easter egg |
| commands.py | RemoveEggCommand.execute | Process easter egg removal |
| commands.py | EnableEggCommand | Admin command to enable easter egg |
| commands.py | EnableEggCommand.execute | Process easter egg enabling |
| commands.py | DisableEggCommand | Admin command to disable easter egg |
| commands.py | DisableEggCommand.execute | Process easter egg disabling |
| commands.py | ListEggsCommand | Admin command to list easter eggs |
| commands.py | ListEggsCommand.execute | Display registered easter eggs |

## Easter Egg Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_easter_egg_events | Register all easter egg-related event handlers |
| events.py | handle_message | Handle chat message for easter eggs |
| events.py | handle_command | Handle command for easter eggs |
| events.py | handle_system_event | Handle system event for easter eggs |
| events.py | handle_emote_message | Handle message with emotes |
| events.py | handle_user_timing | Handle user message timing |
| events.py | handle_self_targeting | Handle self-targeting in commands |
| events.py | handle_secret_command | Handle secret command discovery |
| events.py | handle_random_event | Handle random event triggers |
| events.py | notify_egg_triggered | Send notification for triggered easter egg |
| events.py | notify_emote_combo | Send notification for emote combo progress |
| events.py | notify_streak_progress | Send notification for timing streak progress |
| events.py | log_egg_trigger | Log easter egg trigger |
| events.py | log_reward_application | Log reward application |

## Easter Egg Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | EasterEggRepository | Repository for easter egg data |
| repository.py | EasterEggRepository.get_egg | Get easter egg from database |
| repository.py | EasterEggRepository.get_all_eggs | Get all easter eggs from database |
| repository.py | EasterEggRepository.add_egg | Add easter egg to database |
| repository.py | EasterEggRepository.update_egg | Update easter egg in database |
| repository.py | EasterEggRepository.remove_egg | Remove easter egg from database |
| repository.py | EasterEggRepository.get_user_progress | Get user progress for egg |
| repository.py | EasterEggRepository.update_user_progress | Update user progress for egg |
| repository.py | EasterEggRepository.get_combo_progress | Get emote combo progress |
| repository.py | EasterEggRepository.update_combo_progress | Update emote combo progress |
| repository.py | EasterEggRepository.get_timing_stats | Get message timing statistics |
| repository.py | EasterEggRepository.update_timing_stats | Update message timing statistics |
| repository.py | EasterEggRepository.log_trigger | Log easter egg trigger in database |
| repository.py | EasterEggRepository.get_trigger_history | Get history of egg triggers |
| repository.py | EasterEggRepository.get_reward_history | Get history of rewards granted |
| repository.py | get_repository | Get singleton repository instance |

## Easter Egg Analytics
| Module | Function | Description |
|--------|----------|-------------|
| analytics.py | EasterEggAnalytics | Analytics for easter egg system |
| analytics.py | EasterEggAnalytics.get_trigger_statistics | Get statistics on egg triggers |
| analytics.py | EasterEggAnalytics.get_reward_statistics | Get statistics on rewards granted |
| analytics.py | EasterEggAnalytics.get_most_triggered | Get most frequently triggered eggs |
| analytics.py | EasterEggAnalytics.get_least_triggered | Get least frequently triggered eggs |
| analytics.py | EasterEggAnalytics.get_user_discovery | Get statistics on user discoveries |
| analytics.py | EasterEggAnalytics.get_emote_combo_stats | Get statistics on emote combos |
| analytics.py | EasterEggAnalytics.get_timing_streak_stats | Get statistics on timing streaks |
| analytics.py | EasterEggAnalytics.get_eggs_by_trigger_type | Get eggs categorised by trigger type |
| analytics.py | EasterEggAnalytics.get_eggs_by_reward_type | Get eggs categorised by reward type |
| analytics.py | EasterEggAnalytics.generate_report | Generate analytics report |
| analytics.py | get_analytics | Get singleton analytics instance |
| analytics.py | generate_report | Generate report with global instance |

## Easter Egg Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | EasterEggConfig | Configuration for easter egg system |
| config.py | EasterEggConfig.get_emote_combo_settings | Get emote combo settings |
| config.py | EasterEggConfig.get_timing_streak_settings | Get timing streak settings |
| config.py | EasterEggConfig.get_self_targeting_settings | Get self-targeting settings |
| config.py | EasterEggConfig.get_random_event_settings | Get random event settings |
| config.py | EasterEggConfig.get_notification_settings | Get notification settings |
| config.py | EasterEggConfig.get_default_rewards | Get default reward settings |
| config.py | EasterEggConfig.get_max_rewards | Get maximum reward limits |
| config.py | EasterEggConfig.load | Load configuration from settings |
| config.py | EasterEggConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## Emote Detection
| Module | Function | Description |
|--------|----------|-------------|
| emotes.py | EmoteDetector | Detector for Twitch emotes in messages |
| emotes.py | EmoteDetector.initialise | Initialise emote detection |
| emotes.py | EmoteDetector.detect_emotes | Detect emotes in message |
| emotes.py | EmoteDetector.is_emote_only | Check if message contains only emotes |
| emotes.py | EmoteDetector.count_emotes | Count emotes in message |
| emotes.py | EmoteDetector.get_emote_sequence | Get sequence of emotes in message |
| emotes.py | EmoteDetector.get_unique_emotes | Get unique emotes in message |
| emotes.py | EmoteDetector.match_sequence | Check if message matches emote sequence |
| emotes.py | EmoteDetector.register_emote | Register custom emote for detection |
| emotes.py | EmoteDetector.load_twitch_emotes | Load Twitch emotes for detection |
| emotes.py | EmoteDetector.load_bttv_emotes | Load BetterTTV emotes for detection |
| emotes.py | EmoteDetector.load_ffz_emotes | Load FrankerFaceZ emotes for detection |
| emotes.py | EmoteDetector.update_emote_cache | Update cached emote data |
| emotes.py | EmoteDetector.clear_cache | Clear emote cache |
| emotes.py | get_emote_detector | Get singleton detector instance |
| emotes.py | detect_emotes | Detect emotes with global instance |
| emotes.py | is_emote_only | Check if message is emote-only with global instance |

## Timing Tracker
| Module | Function | Description |
|--------|----------|-------------|
| timing.py | MessageTimingTracker | Tracker for user message timing patterns |
| timing.py | MessageTimingTracker.add_message | Record new message timestamp |
| timing.py | MessageTimingTracker.get_intervals | Get intervals between messages |
| timing.py | MessageTimingTracker.get_average_interval | Get average interval between messages |
| timing.py | MessageTimingTracker.check_consistency | Check if intervals are consistent |
| timing.py | MessageTimingTracker.detect_pattern | Detect timing pattern in messages |
| timing.py | MessageTimingTracker.get_current_streak | Get current streak of consistent timing |
| timing.py | MessageTimingTracker.reset_streak | Reset streak count |
| timing.py | MessageTimingTracker.calculate_next_expected | Calculate next expected message time |
| timing.py | MessageTimingTracker.is_within_tolerance | Check if message is within timing tolerance |
| timing.py | MessageTimingTracker.get_user_history | Get history of user's timing patterns |
| timing.py | get_timing_tracker | Get singleton tracker instance |
| timing.py | add_message | Add message with global instance |
| timing.py | check_pattern | Check pattern with global instance |

## Easter Egg Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | EasterEggFeature | Main easter egg feature class |
| feature.py | EasterEggFeature.initialise | Initialise easter egg feature |
| feature.py | EasterEggFeature.shutdown | Shutdown easter egg feature |
| feature.py | EasterEggFeature.get_commands | Get commands provided by feature |
| feature.py | EasterEggFeature.get_event_handlers | Get event handlers for feature |
| feature.py | EasterEggFeature.is_enabled | Check if feature is enabled |
| feature.py | EasterEggFeature.get_dependencies | Get feature dependencies |
| feature.py | EasterEggFeature.get_manager | Get easter egg manager |
| feature.py | EasterEggFeature.get_config | Get easter egg configuration |
| feature.py | register_feature | Register easter egg feature with system |
| feature.py | get_feature | Get easter egg feature instance |

## Easter Egg Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | EasterEggHooks | Hooks for easter egg system integration |
| hooks.py | EasterEggHooks.register_egg_discovery_hook | Register hook for egg discovery |
| hooks.py | EasterEggHooks.register_reward_hook | Register hook for reward application |
| hooks.py | EasterEggHooks.register_emote_combo_hook | Register hook for emote combo progress |
| hooks.py | EasterEggHooks.register_timing_streak_hook | Register hook for timing streak progress |
| hooks.py | EasterEggHooks.trigger_egg_discovery_hooks | Trigger hooks for egg discovery |
| hooks.py | EasterEggHooks.trigger_reward_hooks | Trigger hooks for reward application |
| hooks.py | EasterEggHooks.trigger_emote_combo_hooks | Trigger hooks for emote combo progress |
| hooks.py | EasterEggHooks.trigger_timing_streak_hooks | Trigger hooks for timing streak progress |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

## Easter Egg Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | EasterEggMiddleware | Middleware for easter egg operations |
| middleware.py | EasterEggMiddleware.process_operation | Process operation through middleware |
| middleware.py | EasterEggMiddleware.register_middleware | Register operation middleware |
| middleware.py | EasterEggMiddleware.validate_operation | Validate easter egg operation |
| middleware.py | EasterEggMiddleware.modify_operation | Modify easter egg operation |
| middleware.py | EasterEggMiddleware.log_operation | Log operation details |
| middleware.py | EasterEggMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |

## Easter Egg Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_easter_eggs | Initialise easter egg system |
| initialisation.py | register_default_eggs | Register default easter eggs |
| initialisation.py | register_triggers | Register built-in triggers |
| initialisation.py | register_conditions | Register built-in conditions |
| initialisation.py | register_rewards | Register built-in rewards |
| initialisation.py | register_easter_egg_commands | Register easter egg commands |
| initialisation.py | register_easter_egg_events | Register easter egg event handlers |
| initialisation.py | setup_emote_detector | Set up emote detector |
| initialisation.py | setup_timing_tracker | Set up timing tracker |
| initialisation.py | load_easter_egg_config | Load easter egg configuration |
| initialisation.py | setup_easter_egg_repository | Set up easter egg data repository |
| initialisation.py | register_default_hooks | Register default easter egg hooks |
| initialisation.py | shutdown_easter_eggs | Shutdown easter egg system |
| initialisation.py | get_easter_egg_settings | Get easter egg settings from config |
