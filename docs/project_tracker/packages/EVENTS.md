# Normalised Event System

The event system provides a unified approach to handling events from different sources, with a standardised event structure and consistent dispatch mechanism. This document outlines the structure and components of the normalised event system.

## Core Event Framework

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/base.py | Event | Base class for all events |
| events/base.py | Event.get_type | Get event type |
| events/base.py | Event.get_source | Get event source |
| events/base.py | Event.get_timestamp | Get event timestamp |
| events/base.py | Event.get_data | Get event data |
| events/base.py | Event.get_metadata | Get event metadata |
| events/base.py | Event.is_cancellable | Check if event can be cancelled |
| events/base.py | Event.is_cancelled | Check if event is cancelled |
| events/base.py | Event.cancel | Cancel event if possible |
| events/base.py | Event.is_handled | Check if event is handled |
| events/base.py | Event.mark_handled | Mark event as handled |
| events/base.py | Event.to_dict | Convert event to dictionary |
| events/base.py | Event.from_dict | Create event from dictionary |
| events/base.py | EventMetadata | Container for event metadata |
| events/base.py | EventMetadata.get | Get metadata value |
| events/base.py | EventMetadata.set | Set metadata value |
| events/base.py | EventMetadata.has | Check if metadata exists |
| events/base.py | EventMetadata.remove | Remove metadata value |
| events/base.py | EventMetadata.to_dict | Convert metadata to dictionary |

## Event Manager

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/manager.py | EventManager | Manager for event system |
| events/manager.py | EventManager.initialise | Initialise event system |
| events/manager.py | EventManager.shutdown | Shutdown event system |
| events/manager.py | EventManager.subscribe | Subscribe to events |
| events/manager.py | EventManager.unsubscribe | Unsubscribe from events |
| events/manager.py | EventManager.publish | Publish event |
| events/manager.py | EventManager.publish_async | Publish event asynchronously |
| events/manager.py | EventManager.get_subscribers | Get subscribers for event type |
| events/manager.py | EventManager.clear_subscribers | Clear all subscribers |
| events/manager.py | EventManager.register_filter | Register event filter |
| events/manager.py | EventManager.get_queue | Get event queue |
| events/manager.py | EventManager.process_queue | Process event queue |
| events/manager.py | get_manager | Get singleton manager instance |
| events/manager.py | subscribe | Subscribe to events using global manager |
| events/manager.py | unsubscribe | Unsubscribe from events using global manager |
| events/manager.py | publish | Publish event using global manager |
| events/manager.py | publish_async | Publish event asynchronously using global manager |

## Event Types

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/types.py | EventType | Enum of standard event types |
| events/types.py | EventType.PLATFORM | Platform-related events |
| events/types.py | EventType.COMMAND | Command-related events |
| events/types.py | EventType.USER | User-related events |
| events/types.py | EventType.SYSTEM | System-related events |
| events/types.py | EventType.FEATURE | Feature-related events |
| events/types.py | EventType.TRANSACTION | Transaction-related events |
| events/types.py | EventCategory | Enum of event categories |
| events/types.py | EventCategory.TWITCH | Twitch-related events |
| events/types.py | EventCategory.OBS | OBS-related events |
| events/types.py | EventCategory.POINTS | Points-related events |
| events/types.py | EventCategory.SHOP | Shop-related events |
| events/types.py | EventCategory.DUEL | Duel-related events |
| events/types.py | EventCategory.INVENTORY | Inventory-related events |
| events/types.py | EventCategory.DOMT | DOMT-related events |
| events/types.py | EventCategory.EASTER_EGG | Easter egg-related events |
| events/types.py | EventSource | Enum of event sources |
| events/types.py | EventSource.USER | User-initiated events |
| events/types.py | EventSource.SYSTEM | System-initiated events |
| events/types.py | EventSource.FEATURE | Feature-initiated events |
| events/types.py | EventSource.SCHEDULED | Scheduled events |
| events/types.py | EventSource.EXTERNAL | External events |

## Standardised Events

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/standard.py | PlatformEvent | Base class for platform events |
| events/standard.py | PlatformEvent.get_platform | Get platform name |
| events/standard.py | CommandEvent | Base class for command events |
| events/standard.py | CommandEvent.get_command | Get command name |
| events/standard.py | CommandEvent.get_arguments | Get command arguments |
| events/standard.py | CommandEvent.get_user | Get user who executed command |
| events/standard.py | UserEvent | Base class for user events |
| events/standard.py | UserEvent.get_user | Get user associated with event |
| events/standard.py | SystemEvent | Base class for system events |
| events/standard.py | SystemEvent.get_component | Get system component |
| events/standard.py | FeatureEvent | Base class for feature events |
| events/standard.py | FeatureEvent.get_feature | Get feature name |
| events/standard.py | TransactionEvent | Base class for transaction events |
| events/standard.py | TransactionEvent.get_transaction_type | Get transaction type |
| events/standard.py | TransactionEvent.get_amount | Get transaction amount |
| events/standard.py | TransactionEvent.get_user | Get user involved in transaction |

## Platform Event Adapters

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/platforms/twitch.py | TwitchEventAdapter | Adapter for Twitch events |
| events/platforms/twitch.py | TwitchEventAdapter.convert | Convert Twitch event to standard event |
| events/platforms/twitch.py | convert_message | Convert Twitch message event |
| events/platforms/twitch.py | convert_bits | Convert Twitch bits event |
| events/platforms/twitch.py | convert_subscription | Convert Twitch subscription event |
| events/platforms/twitch.py | convert_reward | Convert Twitch reward event |
| events/platforms/twitch.py | convert_follow | Convert Twitch follow event |
| events/platforms/twitch.py | convert_raid | Convert Twitch raid event |
| events/platforms/twitch.py | convert_ban | Convert Twitch ban event |
| events/platforms/obs.py | OBSEventAdapter | Adapter for OBS events |
| events/platforms/obs.py | OBSEventAdapter.convert | Convert OBS event to standard event |
| events/platforms/obs.py | convert_scene_change | Convert OBS scene change event |
| events/platforms/obs.py | convert_source_visibility | Convert OBS source visibility event |
| events/platforms/obs.py | convert_stream_status | Convert OBS stream status event |
| events/platforms/obs.py | convert_recording_status | Convert OBS recording status event |

## Event Subscribers

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/subscriber.py | EventSubscriber | Base class for event subscribers |
| events/subscriber.py | EventSubscriber.handle_event | Handle event |
| events/subscriber.py | EventSubscriber.get_subscription_id | Get subscriber ID |
| events/subscriber.py | EventSubscriber.get_event_types | Get event types to subscribe to |
| events/subscriber.py | EventSubscriber.can_handle | Check if subscriber can handle event |
| events/subscriber.py | FunctionSubscriber | Subscriber wrapping function |
| events/subscriber.py | FunctionSubscriber.handle_event | Call function with event |
| events/subscriber.py | MethodSubscriber | Subscriber wrapping class method |
| events/subscriber.py | MethodSubscriber.handle_event | Call method with event |
| events/subscriber.py | SubscriberRegistry | Registry for subscribers |
| events/subscriber.py | SubscriberRegistry.register | Register subscriber |
| events/subscriber.py | SubscriberRegistry.unregister | Unregister subscriber |
| events/subscriber.py | SubscriberRegistry.get_subscriber | Get subscriber by ID |
| events/subscriber.py | SubscriberRegistry.get_subscribers | Get subscribers for event type |
| events/subscriber.py | get_registry | Get singleton registry instance |

## Event Queue

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/queue.py | EventQueue | Queue for events |
| events/queue.py | EventQueue.add | Add event to queue |
| events/queue.py | EventQueue.get | Get next event from queue |
| events/queue.py | EventQueue.get_all | Get all events from queue |
| events/queue.py | EventQueue.process | Process next event in queue |
| events/queue.py | EventQueue.process_all | Process all events in queue |
| events/queue.py | EventQueue.is_empty | Check if queue is empty |
| events/queue.py | EventQueue.clear | Clear all events from queue |
| events/queue.py | EventQueue.size | Get number of events in queue |
| events/queue.py | PriorityEventQueue | Queue with priority for events |
| events/queue.py | PriorityEventQueue.add | Add event with priority |
| events/queue.py | PriorityEventQueue.get_priority | Calculate priority for event |
| events/queue.py | get_queue | Get singleton queue instance |
| events/queue.py | add_to_queue | Add event to global queue |
| events/queue.py | process_queue | Process events in global queue |

## Event Filters

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/filters.py | EventFilter | Base class for event filters |
| events/filters.py | EventFilter.filter | Filter event |
| events/filters.py | EventFilter.should_filter | Check if event should be filtered |
| events/filters.py | TypeFilter | Filter by event type |
| events/filters.py | TypeFilter.filter | Filter based on event type |
| events/filters.py | SourceFilter | Filter by event source |
| events/filters.py | SourceFilter.filter | Filter based on event source |
| events/filters.py | CategoryFilter | Filter by event category |
| events/filters.py | CategoryFilter.filter | Filter based on event category |
| events/filters.py | UserFilter | Filter by user |
| events/filters.py | UserFilter.filter | Filter based on user |
| events/filters.py | PropertyFilter | Filter by event property |
| events/filters.py | PropertyFilter.filter | Filter based on property value |
| events/filters.py | CompositeFilter | Composite filter combining multiple filters |
| events/filters.py | CompositeFilter.filter | Apply multiple filters |
| events/filters.py | FilterChain | Chain of filters |
| events/filters.py | FilterChain.add | Add filter to chain |
| events/filters.py | FilterChain.filter | Apply chain of filters |
| events/filters.py | FilterRegistry | Registry for filters |
| events/filters.py | FilterRegistry.register | Register filter |
| events/filters.py | FilterRegistry.get_filter | Get filter by name |
| events/filters.py | get_registry | Get singleton registry instance |

## Event Decorators

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/decorators.py | event_handler | Decorator for event handlers |
| events/decorators.py | event_filter | Decorator for event filters |
| events/decorators.py | async_event | Decorator for async event handlers |
| events/decorators.py | subscribe | Decorator to subscribe function to events |
| events/decorators.py | priority | Decorator to set handler priority |
| events/decorators.py | once | Decorator for one-time event handling |
| events/decorators.py | delay | Decorator to delay event handling |
| events/decorators.py | throttle | Decorator to throttle event handling |
| events/decorators.py | debounce | Decorator to debounce event handling |
| events/decorators.py | with_metadata | Decorator to add metadata to event |
| events/decorators.py | filter_events | Decorator to filter events for handler |

## Feature-Specific Event Types

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/features/points.py | PointsEvent | Base class for points events |
| events/features/points.py | PointsEvent.get_points | Get points amount |
| events/features/points.py | PointsEvent.get_user | Get user involved |
| events/features/points.py | PointsAddedEvent | Event for points added |
| events/features/points.py | PointsRemovedEvent | Event for points removed |
| events/features/points.py | PointsTransferredEvent | Event for points transferred |
| events/features/shop.py | ShopEvent | Base class for shop events |
| events/features/shop.py | ShopEvent.get_item | Get item involved |
| events/features/shop.py | ShopEvent.get_user | Get user involved |
| events/features/shop.py | ItemPurchasedEvent | Event for item purchased |
| events/features/shop.py | ItemUpgradedEvent | Event for item upgraded |
| events/features/shop.py | ItemModifiedEvent | Event for item modified |
| events/features/duel.py | DuelEvent | Base class for duel events |
| events/features/duel.py | DuelEvent.get_challenger | Get duel challenger |
| events/features/duel.py | DuelEvent.get_opponent | Get duel opponent |
| events/features/duel.py | DuelChallengeEvent | Event for duel challenge |
| events/features/duel.py | DuelAcceptEvent | Event for duel acceptance |
| events/features/duel.py | DuelRejectEvent | Event for duel rejection |
| events/features/duel.py | DuelCompleteEvent | Event for duel completion |
| events/features/duel.py | DuelDrawEvent | Event for duel draw |
| events/features/inventory.py | InventoryEvent | Base class for inventory events |
| events/features/inventory.py | InventoryEvent.get_user | Get inventory owner |
| events/features/inventory.py | InventoryEvent.get_item | Get item involved |
| events/features/inventory.py | ItemAddedEvent | Event for item added |
| events/features/inventory.py | ItemRemovedEvent | Event for item removed |
| events/features/inventory.py | ItemUsedEvent | Event for item used |
| events/features/inventory.py | DurabilityChangedEvent | Event for durability changed |
| events/features/domt.py | DOMTEvent | Base class for DOMT events |
| events/features/domt.py | DOMTEvent.get_user | Get user involved |
| events/features/domt.py | DOMTEvent.get_card | Get card involved |
| events/features/domt.py | CardDrawnEvent | Event for card drawn |
| events/features/domt.py | CardEffectEvent | Event for card effect |
| events/features/domt.py | DeckResetEvent | Event for deck reset |
| events/features/easter_eggs.py | EasterEggEvent | Base class for easter egg events |
| events/features/easter_eggs.py | EasterEggEvent.get_egg | Get easter egg involved |
| events/features/easter_eggs.py | EasterEggEvent.get_user | Get user involved |
| events/features/easter_eggs.py | EggTriggeredEvent | Event for easter egg triggered |
| events/features/easter_eggs.py | ComboProgressEvent | Event for combo progress |
| events/features/easter_eggs.py | TimingStreakEvent | Event for timing streak |

## Event Factory

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/factory.py | EventFactory | Factory for creating events |
| events/factory.py | EventFactory.create_event | Create event instance |
| events/factory.py | EventFactory.register_event_type | Register event type |
| events/factory.py | EventFactory.get_event_type | Get event type class |
| events/factory.py | get_factory | Get singleton factory instance |
| events/factory.py | create_event | Create event with factory |
| events/factory.py | register_event_type | Register event type with factory |

## Event Serialisation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/serialisation.py | EventSerialiser | Serialiser for events |
| events/serialisation.py | EventSerialiser.serialise | Serialise event to format |
| events/serialisation.py | EventSerialiser.deserialise | Deserialise event from format |
| events/serialisation.py | JSONSerialiser | JSON serialiser for events |
| events/serialisation.py | JSONSerialiser.serialise | Serialise event to JSON |
| events/serialisation.py | JSONSerialiser.deserialise | Deserialise event from JSON |
| events/serialisation.py | event_to_dict | Convert event to dictionary |
| events/serialisation.py | dict_to_event | Create event from dictionary |
| events/serialisation.py | event_to_json | Convert event to JSON string |
| events/serialisation.py | json_to_event | Create event from JSON string |

## Event Hooks

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/hooks.py | EventHook | Base class for event hooks |
| events/hooks.py | EventHook.execute | Execute hook on event |
| events/hooks.py | EventHook.should_execute | Check if hook should execute |
| events/hooks.py | BeforePublishHook | Hook executed before event publishing |
| events/hooks.py | BeforePublishHook.execute | Execute before publish |
| events/hooks.py | AfterPublishHook | Hook executed after event publishing |
| events/hooks.py | AfterPublishHook.execute | Execute after publish |
| events/hooks.py | BeforeHandleHook | Hook executed before event handling |
| events/hooks.py | BeforeHandleHook.execute | Execute before handling |
| events/hooks.py | AfterHandleHook | Hook executed after event handling |
| events/hooks.py | AfterHandleHook.execute | Execute after handling |
| events/hooks.py | ErrorHook | Hook executed on event error |
| events/hooks.py | ErrorHook.execute | Execute on error |
| events/hooks.py | HookRegistry | Registry for event hooks |
| events/hooks.py | HookRegistry.register | Register hook |
| events/hooks.py | HookRegistry.get_hooks | Get hooks for event type |
| events/hooks.py | get_registry | Get singleton registry instance |
| events/hooks.py | register_hook | Register hook with registry |

## Event Scheduler

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/scheduler.py | EventScheduler | Scheduler for events |
| events/scheduler.py | EventScheduler.schedule | Schedule event for future |
| events/scheduler.py | EventScheduler.schedule_recurring | Schedule recurring event |
| events/scheduler.py | EventScheduler.cancel | Cancel scheduled event |
| events/scheduler.py | EventScheduler.get_scheduled_events | Get all scheduled events |
| events/scheduler.py | EventScheduler.process_due | Process due events |
| events/scheduler.py | ScheduledEvent | Event scheduled for future |
| events/scheduler.py | ScheduledEvent.get_event | Get underlying event |
| events/scheduler.py | ScheduledEvent.get_schedule_time | Get scheduled time |
| events/scheduler.py | ScheduledEvent.is_recurring | Check if event is recurring |
| events/scheduler.py | ScheduledEvent.get_interval | Get recurring interval |
| events/scheduler.py | ScheduledEvent.is_due | Check if event is due |
| events/scheduler.py | get_scheduler | Get singleton scheduler instance |
| events/scheduler.py | schedule_event | Schedule event with global instance |
| events/scheduler.py | schedule_recurring | Schedule recurring with global instance |
| events/scheduler.py | cancel_scheduled | Cancel event with global instance |

## Event Utilities

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/utils.py | event_matches | Check if event matches criteria |
| events/utils.py | get_event_type_name | Get friendly name for event type |
| events/utils.py | get_event_description | Get human-readable description |
| events/utils.py | clone_event | Create clone of event |
| events/utils.py | extract_user_from_event | Extract user from event |
| events/utils.py | extract_data_from_event | Extract data from event |
| events/utils.py | merge_events | Merge data from multiple events |
| events/utils.py | filter_event_data | Filter sensitive data from event |
| events/utils.py | create_event_id | Create unique ID for event |
| events/utils.py | get_event_timestamp | Get formatted timestamp |
| events/utils.py | format_event_for_log | Format event for logging |

## Event Initialisation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| events/initialisation.py | initialise_events | Initialise event system |
| events/initialisation.py | register_standard_events | Register standard events |
| events/initialisation.py | register_platform_adapters | Register platform adapters |
| events/initialisation.py | register_event_hooks | Register event hooks |
| events/initialisation.py | setup_event_queue | Set up event queue |
| events/initialisation.py | setup_event_scheduler | Set up event scheduler |
| events/initialisation.py | shutdown_events | Shutdown event system |