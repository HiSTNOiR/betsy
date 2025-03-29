# Points System Package Structure and Components

The `features/points` package implements the XP/points system for the Twitch bot, providing mechanisms for users to earn, spend, and transfer points within the platform. This document outlines the structure and purpose of each module within the points feature package.

## Points Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | PointsManager | Main manager class for points functionality |
| manager.py | PointsManager.initialise | Initialise points system |
| manager.py | PointsManager.shutdown | Shut down points system |
| manager.py | PointsManager.get_user_points | Get points for a user |
| manager.py | PointsManager.add_points | Add points to a user |
| manager.py | PointsManager.remove_points | Remove points from a user |
| manager.py | PointsManager.transfer_points | Transfer points between users |
| manager.py | PointsManager.register_points_source | Register new source of points |
| manager.py | PointsManager.register_points_sink | Register new sink for points |
| manager.py | PointsManager.get_transaction_history | Get history of point transactions |
| manager.py | PointsManager.get_leaderboard | Get points leaderboard |
| manager.py | get_points_manager | Get singleton manager instance |
| manager.py | initialise | Initialise points system with global manager |
| manager.py | shutdown | Shutdown points system with global manager |

## Points Tracker
| Module | Function | Description |
|--------|----------|-------------|
| tracker.py | PointsTracker | Tracks point earnings and expenditures |
| tracker.py | PointsTracker.start_tracking | Start tracking points for session |
| tracker.py | PointsTracker.stop_tracking | Stop tracking points for session |
| tracker.py | PointsTracker.track_transaction | Track points transaction |
| tracker.py | PointsTracker.get_earnings_summary | Get summary of point earnings |
| tracker.py | PointsTracker.get_spending_summary | Get summary of point spending |
| tracker.py | PointsTracker.get_session_summary | Get summary of points for session |
| tracker.py | PointsTracker.get_total_tracked | Get total points tracked |
| tracker.py | PointsTracker.reset_tracking | Reset tracking data |
| tracker.py | get_tracker | Get singleton tracker instance |
| tracker.py | start_tracking | Start tracking with global tracker |
| tracker.py | stop_tracking | Stop tracking with global tracker |

## Points Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_points_commands | Register all points-related commands |
| commands.py | PointsCommand | Command to check user points |
| commands.py | PointsCommand.execute | Display user's current points |
| commands.py | GiveCommand | Command to give points to another user |
| commands.py | GiveCommand.execute | Transfer points to another user |
| commands.py | GambleCommand | Command to gamble points |
| commands.py | GambleCommand.execute | Process gambling of points |
| commands.py | LeaderboardCommand | Command to show points leaderboard |
| commands.py | LeaderboardCommand.execute | Display points leaderboard |
| commands.py | AdministrativePointsCommand | Administrative command group for points |
| commands.py | AddPointsCommand | Admin command to add points to user |
| commands.py | RemovePointsCommand | Admin command to remove points from user |
| commands.py | SetPointsCommand | Admin command to set user's points |

## Points Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_points_events | Register all points-related event handlers |
| events.py | handle_message_points | Handle points for chat messages |
| events.py | handle_bits_points | Handle points for Twitch bits |
| events.py | handle_subscription_points | Handle points for subscriptions |
| events.py | handle_reward_points | Handle points for channel point redemptions |
| events.py | handle_raid_points | Handle points for raids |
| events.py | handle_follow_points | Handle points for follows |
| events.py | handle_watch_time_points | Handle points for watch time |
| events.py | handle_transaction | Create and dispatch points transaction event |
| events.py | on_stream_start | Handle stream start event for points |
| events.py | on_stream_end | Handle stream end event for points |

## Points Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | PointsConfig | Configuration for points system |
| config.py | PointsConfig.get_message_points | Get points for chat messages |
| config.py | PointsConfig.get_lurker_points | Get points for lurking |
| config.py | PointsConfig.get_bits_ratio | Get bits to points ratio |
| config.py | PointsConfig.get_subscription_points | Get points for subscriptions |
| config.py | PointsConfig.get_gift_multiplier | Get multiplier for gifting points |
| config.py | PointsConfig.get_gamble_settings | Get settings for gambling |
| config.py | PointsConfig.get_min_give_amount | Get minimum amount for gifting |
| config.py | PointsConfig.get_max_give_amount | Get maximum amount for gifting |
| config.py | PointsConfig.load | Load configuration from settings |
| config.py | PointsConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## Points Schedule
| Module | Function | Description |
|--------|----------|-------------|
| schedule.py | PointsSchedule | Scheduler for periodic points awards |
| schedule.py | PointsSchedule.start | Start points schedule |
| schedule.py | PointsSchedule.stop | Stop points schedule |
| schedule.py | PointsSchedule.add_periodic_award | Add periodic points award |
| schedule.py | PointsSchedule.remove_periodic_award | Remove periodic points award |
| schedule.py | PointsSchedule.process_awards | Process all due awards |
| schedule.py | PointsSchedule.award_active_viewers | Award points to active viewers |
| schedule.py | PointsSchedule.award_all_viewers | Award points to all viewers |
| schedule.py | get_schedule | Get singleton schedule instance |
| schedule.py | start_schedule | Start schedule with global instance |
| schedule.py | stop_schedule | Stop schedule with global instance |

## Points Transaction
| Module | Function | Description |
|--------|----------|-------------|
| transaction.py | PointsTransaction | Class representing a points transaction |
| transaction.py | PointsTransaction.get_user | Get user involved in transaction |
| transaction.py | PointsTransaction.get_amount | Get transaction amount |
| transaction.py | PointsTransaction.get_type | Get transaction type |
| transaction.py | PointsTransaction.get_reason | Get transaction reason |
| transaction.py | PointsTransaction.get_timestamp | Get transaction timestamp |
| transaction.py | PointsTransaction.get_source | Get source of transaction |
| transaction.py | PointsTransaction.is_earning | Check if transaction is earning |
| transaction.py | PointsTransaction.is_spending | Check if transaction is spending |
| transaction.py | PointsTransaction.get_balance_after | Get balance after transaction |
| transaction.py | TransactionType | Enum for transaction types |
| transaction.py | create_transaction | Create transaction object |
| transaction.py | validate_transaction | Validate transaction is possible |

## Points Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | PointsRepository | Repository for points data |
| repository.py | PointsRepository.get_points | Get points for user |
| repository.py | PointsRepository.update_points | Update user's points |
| repository.py | PointsRepository.add_transaction | Add transaction to history |
| repository.py | PointsRepository.get_transactions | Get transaction history for user |
| repository.py | PointsRepository.get_top_users | Get users with most points |
| repository.py | PointsRepository.get_transaction_count | Get count of transactions |
| repository.py | PointsRepository.get_total_points | Get total points in circulation |
| repository.py | PointsRepository.get_total_earned | Get total points earned by all users |
| repository.py | PointsRepository.get_total_spent | Get total points spent by all users |
| repository.py | get_repository | Get singleton repository instance |

## Gambling System
| Module | Function | Description |
|--------|----------|-------------|
| gambling.py | GamblingSystem | System for points gambling |
| gambling.py | GamblingSystem.process_gamble | Process gambling request |
| gambling.py | GamblingSystem.calculate_outcome | Calculate gambling outcome |
| gambling.py | GamblingSystem.get_win_multiplier | Get winning multiplier |
| gambling.py | GamblingSystem.get_lose_chance | Get chance of losing |
| gambling.py | GamblingSystem.validate_amount | Validate gambling amount |
| gambling.py | GamblingSystem.get_min_amount | Get minimum gambling amount |
| gambling.py | GamblingSystem.get_max_amount | Get maximum gambling amount |
| gambling.py | GamblingSystem.get_limits | Get gambling limits for user |
| gambling.py | GamblingSystem.adjust_limits | Adjust gambling limits for user |
| gambling.py | get_gambling_system | Get singleton gambling system |
| gambling.py | process_gamble | Process gamble with global system |

## Points Analysis
| Module | Function | Description |
|--------|----------|-------------|
| analysis.py | PointsAnalysis | Analysis tools for points economy |
| analysis.py | PointsAnalysis.get_inflation_rate | Get inflation rate of points |
| analysis.py | PointsAnalysis.get_distribution | Get points distribution statistics |
| analysis.py | PointsAnalysis.get_earning_sources | Get breakdown of earning sources |
| analysis.py | PointsAnalysis.get_spending_sinks | Get breakdown of spending sinks |
| analysis.py | PointsAnalysis.get_activity_correlation | Get correlation with activity |
| analysis.py | PointsAnalysis.get_user_stats | Get statistics for specific user |
| analysis.py | PointsAnalysis.get_top_earners | Get top points earners |
| analysis.py | PointsAnalysis.get_top_spenders | Get top points spenders |
| analysis.py | PointsAnalysis.generate_report | Generate analysis report |
| analysis.py | get_analysis | Get singleton analysis instance |
| analysis.py | generate_report | Generate report with global instance |

## Points Economy Management
| Module | Function | Description |
|--------|----------|-------------|
| economy.py | PointsEconomy | Management of points economy |
| economy.py | PointsEconomy.get_circulation | Get total points in circulation |
| economy.py | PointsEconomy.adjust_rates | Adjust earning/spending rates |
| economy.py | PointsEconomy.simulate_changes | Simulate rate changes |
| economy.py | PointsEconomy.get_health | Get economy health metrics |
| economy.py | PointsEconomy.analyse_inflation | Analyse inflation trends |
| economy.py | PointsEconomy.adjust_for_inflation | Adjust rates for inflation |
| economy.py | PointsEconomy.get_recommendations | Get economic recommendations |
| economy.py | PointsEconomy.balance_economy | Apply automatic balancing |
| economy.py | get_economy | Get singleton economy instance |
| economy.py | balance_economy | Balance economy with global instance |

## Points Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | PointsFeature | Main points feature class |
| feature.py | PointsFeature.initialise | Initialise points feature |
| feature.py | PointsFeature.shutdown | Shutdown points feature |
| feature.py | PointsFeature.get_commands | Get commands provided by feature |
| feature.py | PointsFeature.get_event_handlers | Get event handlers for feature |
| feature.py | PointsFeature.is_enabled | Check if feature is enabled |
| feature.py | PointsFeature.get_dependencies | Get feature dependencies |
| feature.py | PointsFeature.get_manager | Get points manager |
| feature.py | PointsFeature.get_config | Get points configuration |
| feature.py | register_feature | Register points feature with system |
| feature.py | get_feature | Get points feature instance |

## Points Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | PointsHooks | Hooks for points system integration |
| hooks.py | PointsHooks.register_earning_hook | Register hook for points earning |
| hooks.py | PointsHooks.register_spending_hook | Register hook for points spending |
| hooks.py | PointsHooks.register_transfer_hook | Register hook for points transfer |
| hooks.py | PointsHooks.register_balance_hook | Register hook for balance changes |
| hooks.py | PointsHooks.trigger_earning_hooks | Trigger hooks for points earning |
| hooks.py | PointsHooks.trigger_spending_hooks | Trigger hooks for points spending |
| hooks.py | PointsHooks.trigger_transfer_hooks | Trigger hooks for points transfer |
| hooks.py | PointsHooks.trigger_balance_hooks | Trigger hooks for balance changes |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

## Points Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | PointsMiddleware | Middleware for points transactions |
| middleware.py | PointsMiddleware.process_transaction | Process transaction through middleware |
| middleware.py | PointsMiddleware.register_middleware | Register transaction middleware |
| middleware.py | PointsMiddleware.validate_transaction | Validate transaction is allowed |
| middleware.py | PointsMiddleware.modify_transaction | Modify transaction amount |
| middleware.py | PointsMiddleware.log_transaction | Log transaction details |
| middleware.py | PointsMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_transaction_middleware | Register middleware with global instance |

## Points Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_points | Initialise points system |
| initialisation.py | register_points_commands | Register points commands |
| initialisation.py | register_points_events | Register points event handlers |
| initialisation.py | setup_points_schedule | Set up points scheduler |
| initialisation.py | load_points_config | Load points configuration |
| initialisation.py | register_default_hooks | Register default points hooks |
| initialisation.py | setup_points_repository | Set up points data repository |
| initialisation.py | verify_points_economy | Verify points economy health |
| initialisation.py | shutdown_points | Shutdown points system |
| initialisation.py | get_points_settings | Get points settings from config |