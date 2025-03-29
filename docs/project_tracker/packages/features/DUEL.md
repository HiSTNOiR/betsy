# Duel System Package Structure and Components

The `features/duel` package implements the duelling system for the Twitch bot, allowing users to challenge each other to duels with XP stakes and equipment-based outcomes. This document outlines the structure and purpose of each module within the duel feature package.

## Duel Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | DuelManager | Main manager class for duel functionality |
| manager.py | DuelManager.initialise | Initialise duel system |
| manager.py | DuelManager.shutdown | Shut down duel system |
| manager.py | DuelManager.create_challenge | Create new duel challenge |
| manager.py | DuelManager.accept_challenge | Accept duel challenge |
| manager.py | DuelManager.reject_challenge | Reject duel challenge |
| manager.py | DuelManager.cancel_challenge | Cancel pending duel challenge |
| manager.py | DuelManager.timeout_challenge | Process timeout for challenge |
| manager.py | DuelManager.execute_duel | Execute duel and determine winner |
| manager.py | DuelManager.is_challenge_active | Check if user has active challenge |
| manager.py | DuelManager.get_active_challenges | Get all active duel challenges |
| manager.py | DuelManager.get_challenge_by_id | Get challenge by identifier |
| manager.py | DuelManager.get_challenges_for_user | Get challenges for specific user |
| manager.py | DuelManager.validate_challenge | Validate duel challenge parameters |
| manager.py | get_duel_manager | Get singleton manager instance |
| manager.py | initialise | Initialise duel system with global manager |
| manager.py | shutdown | Shutdown duel system with global manager |

## Duel Calculator
| Module | Function | Description |
|--------|----------|-------------|
| calculator.py | DuelCalculator | Calculator for duel outcomes |
| calculator.py | DuelCalculator.calculate_winner | Calculate winner of duel |
| calculator.py | DuelCalculator.calculate_user_score | Calculate duel score for user |
| calculator.py | DuelCalculator.apply_environment_effects | Apply environmental effects to scores |
| calculator.py | DuelCalculator.calculate_equipment_bonus | Calculate equipment bonus for user |
| calculator.py | DuelCalculator.calculate_durability_factor | Calculate durability factor for equipment |
| calculator.py | DuelCalculator.calculate_level_factor | Calculate level factor for equipment |
| calculator.py | DuelCalculator.calculate_modification_bonus | Calculate modifications bonus |
| calculator.py | DuelCalculator.apply_random_factor | Apply random factor to score |
| calculator.py | DuelCalculator.check_underdog_win | Check if underdog win should occur |
| calculator.py | DuelCalculator.calculate_underdog_chance | Calculate chance of underdog victory |
| calculator.py | DuelCalculator.process_durability_loss | Process durability loss after duel |
| calculator.py | DuelCalculator.generate_duel_message | Generate duel result message |
| calculator.py | get_calculator | Get singleton calculator instance |
| calculator.py | calculate_winner | Calculate winner with global instance |

## Environment System
| Module | Function | Description |
|--------|----------|-------------|
| environment.py | EnvironmentManager | Manager for duel environments |
| environment.py | EnvironmentManager.get_environments | Get all available environments |
| environment.py | EnvironmentManager.get_environment | Get environment by name |
| environment.py | EnvironmentManager.get_random_environment | Get random environment for duel |
| environment.py | EnvironmentManager.get_environment_effects | Get effects for environment |
| environment.py | EnvironmentManager.get_item_effect | Get effect of item in environment |
| environment.py | EnvironmentManager.register_environment | Register new environment |
| environment.py | EnvironmentManager.register_environment_effect | Register environment effect |
| environment.py | EnvironmentManager.get_environment_description | Get description of environment |
| environment.py | EnvironmentManager.get_environment_boons | Get boons for environment |
| environment.py | EnvironmentManager.get_environment_busts | Get busts for environment |
| environment.py | EnvironmentManager.format_environment_effects | Format environment effects for display |
| environment.py | get_environment_manager | Get singleton manager instance |
| environment.py | get_random_environment | Get random environment with global instance |

## Duel Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_duel_commands | Register all duel-related commands |
| commands.py | DuelCommand | Command to challenge user to duel |
| commands.py | DuelCommand.execute | Process duel challenge creation |
| commands.py | AcceptCommand | Command to accept duel challenge |
| commands.py | AcceptCommand.execute | Process duel challenge acceptance |
| commands.py | RejectCommand | Command to reject duel challenge |
| commands.py | RejectCommand.execute | Process duel challenge rejection |
| commands.py | CancelDuelCommand | Command to cancel duel challenge |
| commands.py | CancelDuelCommand.execute | Process duel challenge cancellation |
| commands.py | DuelHistoryCommand | Command to show duel history |
| commands.py | DuelHistoryCommand.execute | Display user's duel history |
| commands.py | DuelLeaderboardCommand | Command to show duel leaderboard |
| commands.py | DuelLeaderboardCommand.execute | Display duel leaderboard |
| commands.py | DuelInfoCommand | Command to show duel system information |
| commands.py | DuelInfoCommand.execute | Display duel system information |

## Duel Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_duel_events | Register all duel-related event handlers |
| events.py | handle_challenge_created | Handle duel challenge creation |
| events.py | handle_challenge_accepted | Handle duel challenge acceptance |
| events.py | handle_challenge_rejected | Handle duel challenge rejection |
| events.py | handle_challenge_cancelled | Handle duel challenge cancellation |
| events.py | handle_challenge_timeout | Handle duel challenge timeout |
| events.py | handle_duel_completed | Handle completed duel |
| events.py | handle_duel_draw | Handle duel ending in draw |
| events.py | handle_durability_change | Handle equipment durability changes |
| events.py | handle_equipment_break | Handle equipment breaking from durability loss |
| events.py | notify_challenge | Send duel challenge notification |
| events.py | notify_acceptance | Send duel acceptance notification |
| events.py | notify_rejection | Send duel rejection notification |
| events.py | notify_cancellation | Send duel cancellation notification |
| events.py | notify_timeout | Send duel timeout notification |
| events.py | notify_duel_result | Send duel result notification |
| events.py | notify_durability_loss | Send durability loss notification |

## Duel Models
| Module | Function | Description |
|--------|----------|-------------|
| models.py | DuelChallenge | Model for duel challenge |
| models.py | DuelChallenge.get_id | Get challenge identifier |
| models.py | DuelChallenge.get_challenger | Get challenging user |
| models.py | DuelChallenge.get_opponent | Get challenged opponent |
| models.py | DuelChallenge.get_amount | Get staked amount |
| models.py | DuelChallenge.get_creation_time | Get challenge creation time |
| models.py | DuelChallenge.get_expiry_time | Get challenge expiry time |
| models.py | DuelChallenge.is_expired | Check if challenge is expired |
| models.py | DuelChallenge.accept | Accept the challenge |
| models.py | DuelChallenge.reject | Reject the challenge |
| models.py | DuelChallenge.cancel | Cancel the challenge |
| models.py | DuelChallenge.execute | Execute the duel |
| models.py | DuelChallenge.get_state | Get challenge state |
| models.py | DuelChallenge.to_dict | Convert challenge to dictionary |

## Duel Result
| Module | Function | Description |
|--------|----------|-------------|
| result.py | DuelResult | Class representing duel results |
| result.py | DuelResult.get_winner | Get duel winner |
| result.py | DuelResult.get_loser | Get duel loser |
| result.py | DuelResult.is_draw | Check if duel was a draw |
| result.py | DuelResult.is_underdog_win | Check if underdog won the duel |
| result.py | DuelResult.get_challenger_score | Get challenger's score |
| result.py | DuelResult.get_opponent_score | Get opponent's score |
| result.py | DuelResult.get_pot_amount | Get total pot amount |
| result.py | DuelResult.get_environment | Get duel environment |
| result.py | DuelResult.get_durability_changes | Get equipment durability changes |
| result.py | DuelResult.format_message | Format duel result message |
| result.py | DuelResult.format_stats | Format detailed duel statistics |
| result.py | DuelResult.to_dict | Convert result to dictionary |
| result.py | create_result | Create duel result from parameters |

## Environment Effects
| Module | Function | Description |
|--------|----------|-------------|
| effects.py | EnvironmentEffect | Class representing environment effect |
| effects.py | EnvironmentEffect.get_type | Get effect type (boon or bust) |
| effects.py | EnvironmentEffect.get_item_type | Get affected item type |
| effects.py | EnvironmentEffect.get_item_name | Get affected item name |
| effects.py | EnvironmentEffect.get_multiplier | Get effect multiplier |
| effects.py | EnvironmentEffect.applies_to | Check if effect applies to item |
| effects.py | EnvironmentEffect.apply | Apply effect to score |
| effects.py | EnvironmentEffect.format_description | Format effect description |
| effects.py | BoonEffect | Class for positive environment effects |
| effects.py | BoonEffect.apply | Apply boon effect to score |
| effects.py | BustEffect | Class for negative environment effects |
| effects.py | BustEffect.apply | Apply bust effect to score |
| effects.py | create_effect | Create environment effect from parameters |
| effects.py | register_effect | Register effect with environment system |

## Duel Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | DuelConfig | Configuration for duel system |
| config.py | DuelConfig.get_min_amount | Get minimum stake amount |
| config.py | DuelConfig.get_max_amount | Get maximum stake amount |
| config.py | DuelConfig.get_timeout_seconds | Get challenge timeout in seconds |
| config.py | DuelConfig.get_underdog_win_chance | Get base underdog win chance |
| config.py | DuelConfig.get_durability_loss | Get durability loss per duel |
| config.py | DuelConfig.get_random_factor_range | Get random factor range |
| config.py | DuelConfig.get_environment_boost_multiplier | Get environment boost multiplier |
| config.py | DuelConfig.get_environment_penalty_multiplier | Get environment penalty multiplier |
| config.py | DuelConfig.get_cooldown_seconds | Get duel command cooldown |
| config.py | DuelConfig.load | Load configuration from settings |
| config.py | DuelConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## Duel Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | DuelRepository | Repository for duel data |
| repository.py | DuelRepository.get_user_duels | Get duels for specific user |
| repository.py | DuelRepository.get_user_stats | Get duel statistics for user |
| repository.py | DuelRepository.add_duel | Add duel to history |
| repository.py | DuelRepository.get_active_duels | Get active duel challenges |
| repository.py | DuelRepository.update_duel_state | Update duel challenge state |
| repository.py | DuelRepository.remove_duel | Remove duel challenge |
| repository.py | DuelRepository.get_duel_by_id | Get duel by identifier |
| repository.py | DuelRepository.get_duels_for_user | Get duels involving user |
| repository.py | DuelRepository.get_leaderboard | Get duel leaderboard |
| repository.py | DuelRepository.update_user_stats | Update user duel statistics |
| repository.py | DuelRepository.get_total_duels | Get total number of duels |
| repository.py | DuelRepository.get_total_xp_wagered | Get total XP wagered in duels |
| repository.py | DuelRepository.get_environment_stats | Get environment usage statistics |
| repository.py | get_repository | Get singleton repository instance |

## Duel Challenge Queue
| Module | Function | Description |
|--------|----------|-------------|
| queue.py | DuelQueue | Queue for duel challenges |
| queue.py | DuelQueue.add_challenge | Add challenge to queue |
| queue.py | DuelQueue.remove_challenge | Remove challenge from queue |
| queue.py | DuelQueue.get_challenge | Get challenge by identifier |
| queue.py | DuelQueue.get_challenges_for_user | Get challenges for user |
| queue.py | DuelQueue.has_active_challenge | Check if user has active challenge |
| queue.py | DuelQueue.process_timeouts | Process expired challenges |
| queue.py | DuelQueue.get_all_challenges | Get all active challenges |
| queue.py | DuelQueue.clear | Clear all challenges from queue |
| queue.py | get_duel_queue | Get singleton queue instance |
| queue.py | add_challenge | Add challenge with global instance |
| queue.py | remove_challenge | Remove challenge with global instance |

## Duel Analytics
| Module | Function | Description |
|--------|----------|-------------|
| analytics.py | DuelAnalytics | Analytics for duel system |
| analytics.py | DuelAnalytics.get_top_duelists | Get users with most duels |
| analytics.py | DuelAnalytics.get_win_loss_ratios | Get win/loss ratios for users |
| analytics.py | DuelAnalytics.get_environment_stats | Get environment usage statistics |
| analytics.py | DuelAnalytics.get_equipment_effectiveness | Get effectiveness of different equipment |
| analytics.py | DuelAnalytics.get_underdog_win_statistics | Get underdog win statistics |
| analytics.py | DuelAnalytics.get_average_pot_size | Get average duel pot size |
| analytics.py | DuelAnalytics.get_duel_frequency | Get duel frequency over time |
| analytics.py | DuelAnalytics.get_equipment_usage | Get equipment usage statistics |
| analytics.py | DuelAnalytics.get_durability_statistics | Get durability loss statistics |
| analytics.py | DuelAnalytics.generate_report | Generate analytics report |
| analytics.py | get_analytics | Get singleton analytics instance |
| analytics.py | generate_report | Generate report with global instance |

## Duel Message Formatter
| Module | Function | Description |
|--------|----------|-------------|
| messages.py | DuelMessages | Formatter for duel-related messages |
| messages.py | DuelMessages.format_challenge | Format duel challenge message |
| messages.py | DuelMessages.format_acceptance | Format duel acceptance message |
| messages.py | DuelMessages.format_rejection | Format duel rejection message |
| messages.py | DuelMessages.format_cancellation | Format duel cancellation message |
| messages.py | DuelMessages.format_timeout | Format duel timeout message |
| messages.py | DuelMessages.format_victory | Format duel victory message |
| messages.py | DuelMessages.format_defeat | Format duel defeat message |
| messages.py | DuelMessages.format_draw | Format duel draw message |
| messages.py | DuelMessages.format_underdog_win | Format underdog win message |
| messages.py | DuelMessages.format_environment | Format environment description |
| messages.py | DuelMessages.format_durability_loss | Format durability loss message |
| messages.py | DuelMessages.format_equipment_break | Format equipment break message |
| messages.py | get_messages | Get singleton messages instance |
| messages.py | format_challenge | Format challenge with global instance |

## Duel Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | DuelFeature | Main duel feature class |
| feature.py | DuelFeature.initialise | Initialise duel feature |
| feature.py | DuelFeature.shutdown | Shutdown duel feature |
| feature.py | DuelFeature.get_commands | Get commands provided by feature |
| feature.py | DuelFeature.get_event_handlers | Get event handlers for feature |
| feature.py | DuelFeature.is_enabled | Check if feature is enabled |
| feature.py | DuelFeature.get_dependencies | Get feature dependencies |
| feature.py | DuelFeature.get_manager | Get duel manager |
| feature.py | DuelFeature.get_config | Get duel configuration |
| feature.py | register_feature | Register duel feature with system |
| feature.py | get_feature | Get duel feature instance |

## Duel Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | DuelHooks | Hooks for duel system integration |
| hooks.py | DuelHooks.register_challenge_hook | Register hook for challenge creation |
| hooks.py | DuelHooks.register_acceptance_hook | Register hook for challenge acceptance |
| hooks.py | DuelHooks.register_rejection_hook | Register hook for challenge rejection |
| hooks.py | DuelHooks.register_cancellation_hook | Register hook for challenge cancellation |
| hooks.py | DuelHooks.register_completion_hook | Register hook for duel completion |
| hooks.py | DuelHooks.register_draw_hook | Register hook for duel draw |
| hooks.py | DuelHooks.register_timeout_hook | Register hook for challenge timeout |
| hooks.py | DuelHooks.trigger_challenge_hooks | Trigger hooks for challenge creation |
| hooks.py | DuelHooks.trigger_acceptance_hooks | Trigger hooks for challenge acceptance |
| hooks.py | DuelHooks.trigger_rejection_hooks | Trigger hooks for challenge rejection |
| hooks.py | DuelHooks.trigger_cancellation_hooks | Trigger hooks for challenge cancellation |
| hooks.py | DuelHooks.trigger_completion_hooks | Trigger hooks for duel completion |
| hooks.py | DuelHooks.trigger_draw_hooks | Trigger hooks for duel draw |
| hooks.py | DuelHooks.trigger_timeout_hooks | Trigger hooks for challenge timeout |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

## Duel Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_duel | Initialise duel system |
| initialisation.py | register_duel_commands | Register duel commands |
| initialisation.py | register_duel_events | Register duel event handlers |
| initialisation.py | setup_environments | Set up duel environments |
| initialisation.py | setup_calculator | Set up duel calculator |
| initialisation.py | setup_challenge_queue | Set up challenge queue |
| initialisation.py | load_duel_config | Load duel configuration |
| initialisation.py | register_default_hooks | Register default duel hooks |
| initialisation.py | setup_duel_repository | Set up duel data repository |
| initialisation.py | setup_duel_messages | Set up duel message formatter |
| initialisation.py | shutdown_duel | Shutdown duel system |
| initialisation.py | get_duel_settings | Get duel settings from config |