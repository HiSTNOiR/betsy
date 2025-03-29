# Event System Package Structure and Components

The `events` package provides a comprehensive event handling framework for the Twitch bot, allowing different components to communicate through a consistent event-driven architecture. This document outlines the structure and purpose of each module within the `events` package.

## Event Base Framework
| Module | Function | Description |
|--------|----------|-------------|
| base.py | Event | Base class for all events |
| base.py | Event.get_name | Get event name |
| base.py | Event.get_data | Get event data |
| base.py | Event.get_source | Get event source |
| base.py | Event.get_timestamp | Get event creation timestamp |
| base.py | Event.is_cancellable | Check if event can be cancelled |
| base.py | Event.is_cancelled | Check if event has been cancelled |
| base.py | Event.cancel | Cancel event if cancellable |
| base.py | Event.propagate | Allow event to continue propagation |
| base.py | Event.stop_propagation | Stop event propagation |
| base.py | Event.is_propagating | Check if event is still propagating |
| base.py | EventContext | Context object for event handling |
| base.py | EventContext.get_event | Get event being handled |
| base.py | EventContext.get_bot | Get bot instance |
| base.py | EventContext.get_user | Get user associated with event |
| base.py | EventContext.get_platform | Get platform where event originated |

## Event Registry
| Module | Function | Description |
|--------|----------|-------------|
| registry.py | EventRegistry | Registry for event listeners |
| registry.py | EventRegistry.register | Register event listener |
| registry.py | EventRegistry.unregister | Unregister event listener |
| registry.py | EventRegistry.get_listeners | Get listeners for event type |
| registry.py | EventRegistry.get_all_listeners | Get all registered listeners |
| registry.py | EventRegistry.clear | Clear all registered listeners |
| registry.py | EventRegistry.register_wildcard | Register listener for all events |
| registry.py | EventRegistry.get_wildcard_listeners | Get all wildcard listeners |
| registry.py | get_registry | Get singleton registry instance |
| registry.py | register_listener | Register listener with global registry |
| registry.py | unregister_listener | Unregister listener from global registry |
| registry.py | get_listeners | Get listeners from global registry |

## Event Dispatcher
| Module | Function | Description |
|--------|----------|-------------|
| dispatcher.py | EventDispatcher | Dispatches events to registered listeners |
| dispatcher.py | EventDispatcher.dispatch | Dispatch event to listeners |
| dispatcher.py | EventDispatcher.dispatch_async | Dispatch event asynchronously |
| dispatcher.py | EventDispatcher.get_registry | Get event registry |
| dispatcher.py | EventDispatcher.set_registry | Set event registry |
| dispatcher.py | EventDispatcher.is_dispatching | Check if currently dispatching |
| dispatcher.py | EventDispatcher.set_error_handler | Set handler for dispatch errors |
| dispatcher.py | EventDispatcher.register_middleware | Register dispatch middleware |
| dispatcher.py | get_dispatcher | Get singleton dispatcher instance |
| dispatcher.py | dispatch | Dispatch event with global dispatcher |
| dispatcher.py | dispatch_async | Dispatch event asynchronously with global dispatcher |
| dispatcher.py | register_error_handler | Register error handler with global dispatcher |

## Event Listener
| Module | Function | Description |
|--------|----------|-------------|
| listener.py | EventListener | Base class for event listeners |
| listener.py | EventListener.handle_event | Handle event |
| listener.py | EventListener.get_priority | Get listener priority |
| listener.py | EventListener.get_supported_events | Get supported event types |
| listener.py | EventListener.should_handle | Check if listener should handle event |
| listener.py | FunctionListener | Listener wrapping function handler |
| listener.py | FunctionListener.handle_event | Handle event with function |
| listener.py | ClassMethodListener | Listener wrapping class method |
| listener.py | ClassMethodListener.handle_event | Handle event with class method |
| listener.py | create_listener | Create appropriate listener from callable |
| listener.py | listener | Decorator to create event listener |
| listener.py | priority | Decorator to set listener priority |

## Event Decorators
| Module | Function | Description |
|--------|----------|-------------|
| decorators.py | event_listener | Decorator to create event listener |
| decorators.py | event_filter | Decorator to create event filter |
| decorators.py | event_handler | Decorator to create event handler |
| decorators.py | once | Decorator for one-time event handling |
| decorators.py | priority | Decorator to set listener priority |
| decorators.py | filter | Decorator to add filter to listener |
| decorators.py | async_event | Decorator to mark event handler as async |
| decorators.py | threaded_event | Decorator to run event handler in thread |
| decorators.py | timed_event | Decorator to time event handler execution |
| decorators.py | retry | Decorator to retry event handler on failure |
| decorators.py | timeout | Decorator to set event handler timeout |
| decorators.py | throttle | Decorator to throttle event handler |
| decorators.py | error_handler | Decorator for event error handler |

## Twitch Event Types
| Module | Function | Description |
|--------|----------|-------------|
| types/twitch.py | TwitchEvent | Base class for Twitch events |
| types/twitch.py | TwitchMessageEvent | Event for Twitch chat messages |
| types/twitch.py | TwitchMessageEvent.get_message | Get message content |
| types/twitch.py | TwitchMessageEvent.get_sender | Get message sender |
| types/twitch.py | TwitchMessageEvent.get_channel | Get channel message was sent in |
| types/twitch.py | TwitchMessageEvent.is_command | Check if message is command |
| types/twitch.py | TwitchBitsEvent | Event for Twitch bits donations |
| types/twitch.py | TwitchBitsEvent.get_amount | Get bits amount |
| types/twitch.py | TwitchBitsEvent.get_message | Get donation message |
| types/twitch.py | TwitchBitsEvent.get_donor | Get donation sender |
| types/twitch.py | TwitchRewardEvent | Event for channel point redemptions |
| types/twitch.py | TwitchRewardEvent.get_reward | Get reward details |
| types/twitch.py | TwitchRewardEvent.get_user | Get redeeming user |
| types/twitch.py | TwitchRewardEvent.get_message | Get redemption message |
| types/twitch.py | TwitchSubscriptionEvent | Event for channel subscriptions |
| types/twitch.py | TwitchSubscriptionEvent.get_subscriber | Get subscriber |
| types/twitch.py | TwitchSubscriptionEvent.get_tier | Get subscription tier |
| types/twitch.py | TwitchSubscriptionEvent.get_is_gift | Check if subscription is gift |
| types/twitch.py | TwitchSubscriptionEvent.get_gifter | Get subscription gifter |
| types/twitch.py | TwitchSubscriptionEvent.get_message | Get subscription message |
| types/twitch.py | TwitchFollowEvent | Event for new followers |
| types/twitch.py | TwitchFollowEvent.get_follower | Get follower |
| types/twitch.py | TwitchModEvent | Event for moderator actions |
| types/twitch.py | TwitchModEvent.get_moderator | Get moderator |
| types/twitch.py | TwitchModEvent.get_target | Get action target |
| types/twitch.py | TwitchModEvent.get_action | Get action details |
| types/twitch.py | TwitchStreamEvent | Event for stream state changes |
| types/twitch.py | TwitchStreamEvent.get_stream_state | Get stream state |

## OBS Event Types
| Module | Function | Description |
|--------|----------|-------------|
| types/obs.py | OBSEvent | Base class for OBS events |
| types/obs.py | OBSSceneChangeEvent | Event for scene changes |
| types/obs.py | OBSSceneChangeEvent.get_scene_name | Get new scene name |
| types/obs.py | OBSSceneChangeEvent.get_previous_scene | Get previous scene name |
| types/obs.py | OBSSourceVisibilityEvent | Event for source visibility changes |
| types/obs.py | OBSSourceVisibilityEvent.get_source_name | Get source name |
| types/obs.py | OBSSourceVisibilityEvent.get_is_visible | Check if source is visible |
| types/obs.py | OBSStreamStatusEvent | Event for stream status changes |
| types/obs.py | OBSStreamStatusEvent.get_is_streaming | Check if streaming |
| types/obs.py | OBSStreamStatusEvent.get_stream_time | Get streaming time |
| types/obs.py | OBSRecordingStatusEvent | Event for recording status changes |
| types/obs.py | OBSRecordingStatusEvent.get_is_recording | Check if recording |
| types/obs.py | OBSRecordingStatusEvent.get_recording_time | Get recording time |
| types/obs.py | OBSFilterEvent | Event for filter changes |
| types/obs.py | OBSFilterEvent.get_source_name | Get source name |
| types/obs.py | OBSFilterEvent.get_filter_name | Get filter name |
| types/obs.py | OBSFilterEvent.get_is_enabled | Check if filter is enabled |

## Bot Event Types
| Module | Function | Description |
|--------|----------|-------------|
| types/bot.py | BotEvent | Base class for bot events |
| types/bot.py | BotStartEvent | Event for bot startup |
| types/bot.py | BotStartEvent.get_startup_time | Get startup time |
| types/bot.py | BotShutdownEvent | Event for bot shutdown |
| types/bot.py | BotShutdownEvent.get_shutdown_reason | Get shutdown reason |
| types/bot.py | BotShutdownEvent.get_uptime | Get total uptime |
| types/bot.py | CommandEvent | Event for command execution |
| types/bot.py | CommandEvent.get_command | Get command being executed |
| types/bot.py | CommandEvent.get_arguments | Get command arguments |
| types/bot.py | CommandEvent.get_sender | Get command sender |
| types/bot.py | CommandEvent.get_result | Get command execution result |
| types/bot.py | CommandErrorEvent | Event for command errors |
| types/bot.py | CommandErrorEvent.get_command | Get command that errored |
| types/bot.py | CommandErrorEvent.get_error | Get error that occurred |
| types/bot.py | PointsEvent | Event for points transactions |
| types/bot.py | PointsEvent.get_user | Get user involved in transaction |
| types/bot.py | PointsEvent.get_amount | Get transaction amount |
| types/bot.py | PointsEvent.get_reason | Get transaction reason |
| types/bot.py | PointsEvent.get_balance | Get new points balance |

## Feature Event Types
| Module | Function | Description |
|--------|----------|-------------|
| types/features.py | FeatureEvent | Base class for feature-specific events |
| types/features.py | DuelEvent | Event for duel actions |
| types/features.py | DuelEvent.get_challenger | Get duel challenger |
| types/features.py | DuelEvent.get_opponent | Get duel opponent |
| types/features.py | DuelEvent.get_amount | Get duel amount |
| types/features.py | DuelEvent.get_winner | Get duel winner |
| types/features.py | DuelEvent.get_environment | Get duel environment |
| types/features.py | ShopEvent | Event for shop transactions |
| types/features.py | ShopEvent.get_user | Get user making purchase |
| types/features.py | ShopEvent.get_item | Get item being purchased |
| types/features.py | ShopEvent.get_cost | Get purchase cost |
| types/features.py | DOMTEvent | Event for Deck of Many Things |
| types/features.py | DOMTEvent.get_user | Get user drawing card |
| types/features.py | DOMTEvent.get_card | Get card drawn |
| types/features.py | DOMTEvent.get_effect | Get card effect |
| types/features.py | InventoryEvent | Event for inventory changes |
| types/features.py | InventoryEvent.get_user | Get user whose inventory changed |
| types/features.py | InventoryEvent.get_item | Get item added/removed |
| types/features.py | InventoryEvent.get_is_added | Check if item was added |

## Event Filters
| Module | Function | Description |
|--------|----------|-------------|
| filters.py | EventFilter | Base class for event filters |
| filters.py | EventFilter.filter | Filter events based on criteria |
| filters.py | EventFilter.should_handle | Check if event should be handled |
| filters.py | EventFilterChain | Chain multiple filters together |
| filters.py | EventFilterChain.add_filter | Add filter to chain |
| filters.py | EventFilterChain.filter | Apply all filters in chain |
| filters.py | UserFilter | Filter events by user |
| filters.py | UserFilter.filter | Filter based on user criteria |
| filters.py | PlatformFilter | Filter events by platform |
| filters.py | PlatformFilter.filter | Filter based on platform |
| filters.py | TypeFilter | Filter events by type |
| filters.py | TypeFilter.filter | Filter based on event type |
| filters.py | PropertyFilter | Filter events by property value |
| filters.py | PropertyFilter.filter | Filter based on property criteria |
| filters.py | RegexFilter | Filter events using regex patterns |
| filters.py | RegexFilter.filter | Filter based on regex matching |
| filters.py | CompositeFilter | Create complex filters with logic operators |
| filters.py | CompositeFilter.filter | Apply composite filter logic |

## Event Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | EventMiddleware | Base class for event middleware |
| middleware.py | EventMiddleware.process | Process event before dispatching |
| middleware.py | EventMiddleware.get_priority | Get middleware priority |
| middleware.py | MiddlewareManager | Manager for middleware chain |
| middleware.py | MiddlewareManager.add | Add middleware to chain |
| middleware.py | MiddlewareManager.remove | Remove middleware from chain |
| middleware.py | MiddlewareManager.process | Process event through middleware chain |
| middleware.py | LoggingMiddleware | Middleware for event logging |
| middleware.py | LoggingMiddleware.process | Log event details |
| middleware.py | ValidationMiddleware | Middleware for event validation |
| middleware.py | ValidationMiddleware.process | Validate event data |
| middleware.py | ThrottlingMiddleware | Middleware for event throttling |
| middleware.py | ThrottlingMiddleware.process | Throttle frequent events |
| middleware.py | SecurityMiddleware | Middleware for security checks |
| middleware.py | SecurityMiddleware.process | Perform security checks on events |
| middleware.py | TransformationMiddleware | Middleware for event transformation |
| middleware.py | TransformationMiddleware.process | Transform event data |

## Event Errors
| Module | Function | Description |
|--------|----------|-------------|
| errors.py | EventError | Base exception for event errors |
| errors.py | InvalidEventError | Error for invalid event data |
| errors.py | EventHandlingError | Error during event handling |
| errors.py | EventFilterError | Error in event filter |
| errors.py | EventMiddlewareError | Error in event middleware |
| errors.py | EventCancellationError | Error when cancelling non-cancellable event |
| errors.py | EventDispatchError | Error during event dispatch |
| errors.py | EventTimeoutError | Error when event handler times out |
| errors.py | handle_event_error | Handle event error appropriately |
| errors.py | format_error_message | Format error message for logging |

## Scheduled Events
| Module | Function | Description |
|--------|----------|-------------|
| scheduled.py | ScheduledEvent | Event scheduled for future execution |
| scheduled.py | ScheduledEvent.get_execution_time | Get scheduled execution time |
| scheduled.py | ScheduledEvent.is_due | Check if event is due for execution |
| scheduled.py | ScheduledEvent.get_recurring | Check if event is recurring |
| scheduled.py | ScheduledEvent.get_interval | Get interval for recurring events |
| scheduled.py | EventScheduler | Scheduler for future events |
| scheduled.py | EventScheduler.schedule | Schedule event for future execution |
| scheduled.py | EventScheduler.schedule_recurring | Schedule recurring event |
| scheduled.py | EventScheduler.cancel | Cancel scheduled event |
| scheduled.py | EventScheduler.get_scheduled | Get all scheduled events |
| scheduled.py | EventScheduler.process_due | Process all due events |
| scheduled.py | get_scheduler | Get singleton scheduler instance |
| scheduled.py | schedule | Schedule event with global scheduler |
| scheduled.py | schedule_recurring | Schedule recurring event with global scheduler |
| scheduled.py | cancel_scheduled | Cancel scheduled event with global scheduler |

## Event Converters
| Module | Function | Description |
|--------|----------|-------------|
| converters.py | convert_twitch_message | Convert Twitch message to event |
| converters.py | convert_twitch_bits | Convert Twitch bits to event |
| converters.py | convert_twitch_subscription | Convert Twitch subscription to event |
| converters.py | convert_twitch_reward | Convert Twitch reward to event |
| converters.py | convert_twitch_follow | Convert Twitch follow to event |
| converters.py | convert_twitch_mod_action | Convert Twitch moderation action to event |
| converters.py | convert_obs_scene_change | Convert OBS scene change to event |
| converters.py | convert_obs_source_visibility | Convert OBS source visibility to event |
| converters.py | convert_obs_stream_status | Convert OBS stream status to event |
| converters.py | convert_external_event | Convert external event to internal format |
| converters.py | convert_to_json | Convert event to JSON representation |
| converters.py | convert_from_json | Convert JSON to event object |

## Event Queue
| Module | Function | Description |
|--------|----------|-------------|
| queue.py | EventQueue | Queue for event processing |
| queue.py | EventQueue.add | Add event to queue |
| queue.py | EventQueue.process | Process next event in queue |
| queue.py | EventQueue.process_all | Process all events in queue |
| queue.py | EventQueue.clear | Clear all events from queue |
| queue.py | EventQueue.get_size | Get number of events in queue |
| queue.py | EventQueue.is_empty | Check if queue is empty |
| queue.py | PriorityEventQueue | Queue with priority ordering |
| queue.py | PriorityEventQueue.add | Add event with priority |
| queue.py | PriorityEventQueue.get_priority | Get priority for event |
| queue.py | get_queue | Get singleton queue instance |
| queue.py | add_to_queue | Add event to global queue |
| queue.py | process_queue | Process events in global queue |
| queue.py | clear_queue | Clear global event queue |

## Event Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | EventHook | Base class for event hooks |
| hooks.py | EventHook.execute | Execute hook function |
| hooks.py | BeforeDispatchHook | Hook that runs before dispatch |
| hooks.py | AfterDispatchHook | Hook that runs after dispatch |
| hooks.py | ErrorHook | Hook that runs on dispatch error |
| hooks.py | HookManager | Manager for event hooks |
| hooks.py | HookManager.add_before_hook | Add hook before dispatch |
| hooks.py | HookManager.add_after_hook | Add hook after dispatch |
| hooks.py | HookManager.add_error_hook | Add hook for dispatch error |
| hooks.py | HookManager.run_before_hooks | Run all before hooks |
| hooks.py | HookManager.run_after_hooks | Run all after hooks |
| hooks.py | HookManager.run_error_hooks | Run all error hooks |
| hooks.py | get_hook_manager | Get singleton hook manager |
| hooks.py | register_hook | Register hook with global manager |

## Event Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | EventManager | Manager for event system |
| manager.py | EventManager.initialise | Initialise event system |
| manager.py | EventManager.shutdown | Shutdown event system |
| manager.py | EventManager.register_listener | Register event listener |
| manager.py | EventManager.unregister_listener | Unregister event listener |
| manager.py | EventManager.dispatch | Dispatch event |
| manager.py | EventManager.schedule | Schedule event |
| manager.py | EventManager.process_queue | Process event queue |
| manager.py | EventManager.register_middleware | Register event middleware |
| manager.py | EventManager.register_hook | Register event hook |
| manager.py | EventManager.register_filter | Register event filter |
| manager.py | get_manager | Get singleton manager instance |
| manager.py | initialise | Initialise event system with global manager |
| manager.py | shutdown | Shutdown event system with global manager |
| manager.py | register_listener | Register listener with global manager |

## Event Bus
| Module | Function | Description |
|--------|----------|-------------|
| bus.py | EventBus | Central event bus for application |
| bus.py | EventBus.publish | Publish event to bus |
| bus.py | EventBus.subscribe | Subscribe to events on bus |
| bus.py | EventBus.unsubscribe | Unsubscribe from events on bus |
| bus.py | EventBus.get_subscribers | Get subscribers for event type |
| bus.py | EventBus.clear_subscribers | Clear all subscribers |
| bus.py | EventBus.publish_async | Publish event asynchronously |
| bus.py | EventBus.has_subscribers | Check if event type has subscribers |
| bus.py | get_bus | Get singleton bus instance |
| bus.py | publish | Publish event with global bus |
| bus.py | subscribe | Subscribe to events with global bus |
| bus.py | unsubscribe | Unsubscribe from events with global bus |

## Event Logging
| Module | Function | Description |
|--------|----------|-------------|
| logging.py | EventLogger | Logger for event system |
| logging.py | EventLogger.log_event | Log event details |
| logging.py | EventLogger.log_dispatch | Log event dispatch |
| logging.py | EventLogger.log_error | Log event error |
| logging.py | EventLogger.set_level | Set logging level |
| logging.py | EventLogger.get_level | Get current logging level |
| logging.py | EventLogger.enable | Enable event logging |
| logging.py | EventLogger.disable | Disable event logging |
| logging.py | EventLogger.is_enabled | Check if logging is enabled |
| logging.py | get_logger | Get singleton logger instance |
| logging.py | log_event | Log event with global logger |
| logging.py | set_log_level | Set log level for global logger |
| logging.py | format_event_log | Format event for logging |

## Event Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_events | Initialise event system |
| initialisation.py | register_platform_converters | Register platform event converters |
| initialisation.py | register_default_listeners | Register default event listeners |
| initialisation.py | register_core_middleware | Register core event middleware |
| initialisation.py | setup_event_hooks | Set up event hooks |
| initialisation.py | configure_events | Configure event settings |
| initialisation.py | shutdown_events | Shutdown event system |
| initialisation.py | get_event_settings | Get event settings from config |
| initialisation.py | setup_event_bus | Set up central event bus |
| initialisation.py | setup_event_scheduler | Set up event scheduler |