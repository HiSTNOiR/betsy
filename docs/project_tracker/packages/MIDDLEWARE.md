# Standardised Middleware Pipeline

The middleware pipeline provides a consistent approach to processing requests, events, and operations throughout the application. This document outlines the standardised middleware structure that all feature-specific middleware should follow.

## Core Middleware Framework

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/base.py | Middleware | Abstract base class for all middleware |
| middleware/base.py | Middleware.process | Process request and call next middleware |
| middleware/base.py | Middleware.handle_error | Handle error in middleware chain |
| middleware/base.py | Middleware.get_priority | Get middleware priority |
| middleware/base.py | MiddlewarePipeline | Pipeline for executing middleware |
| middleware/base.py | MiddlewarePipeline.add | Add middleware to pipeline |
| middleware/base.py | MiddlewarePipeline.remove | Remove middleware from pipeline |
| middleware/base.py | MiddlewarePipeline.process | Process request through pipeline |
| middleware/base.py | MiddlewarePipeline.build | Build middleware chain |
| middleware/base.py | MiddlewareContext | Context for middleware execution |
| middleware/base.py | MiddlewareContext.get_request | Get request being processed |
| middleware/base.py | MiddlewareContext.get_response | Get response from processing |
| middleware/base.py | MiddlewareContext.get_pipeline | Get pipeline being executed |
| middleware/base.py | MiddlewareContext.set_value | Set context value |
| middleware/base.py | MiddlewareContext.get_value | Get context value |
| middleware/base.py | NextMiddleware | Function for calling next middleware |

## Middleware Manager

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/manager.py | MiddlewareManager | Manager for middleware |
| middleware/manager.py | MiddlewareManager.register | Register middleware |
| middleware/manager.py | MiddlewareManager.unregister | Unregister middleware |
| middleware/manager.py | MiddlewareManager.get_middleware | Get middleware by name |
| middleware/manager.py | MiddlewareManager.get_pipeline | Get pipeline for type |
| middleware/manager.py | MiddlewareManager.create_middleware | Create middleware instance |
| middleware/manager.py | get_manager | Get singleton manager instance |
| middleware/manager.py | register_middleware | Register middleware with manager |
| middleware/manager.py | get_pipeline | Get pipeline for specific type |

## Command Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/command/base.py | CommandMiddleware | Base class for command middleware |
| middleware/command/base.py | CommandMiddleware.process | Process command |
| middleware/command/base.py | CommandRequest | Command request object |
| middleware/command/base.py | CommandRequest.get_command | Get command being executed |
| middleware/command/base.py | CommandRequest.get_context | Get command context |
| middleware/command/base.py | CommandRequest.get_arguments | Get command arguments |
| middleware/command/base.py | CommandResponse | Command response object |
| middleware/command/base.py | CommandResponse.get_result | Get command execution result |
| middleware/command/base.py | CommandResponse.set_result | Set command execution result |
| middleware/command/base.py | CommandResponse.is_success | Check if command succeeded |
| middleware/command/base.py | CommandResponse.set_error | Set command error |
| middleware/command/base.py | CommandResponse.get_error | Get command error |
| middleware/command/pipeline.py | CommandPipeline | Pipeline for command middleware |
| middleware/command/pipeline.py | CommandPipeline.execute | Execute command through pipeline |
| middleware/command/pipeline.py | get_command_pipeline | Get pipeline for commands |

## Command Middleware Implementations

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/command/logging.py | LoggingMiddleware | Log command execution |
| middleware/command/logging.py | LoggingMiddleware.process | Log command and results |
| middleware/command/permission.py | PermissionMiddleware | Check command permissions |
| middleware/command/permission.py | PermissionMiddleware.process | Verify user has permission |
| middleware/command/permission.py | PermissionMiddleware.check_permission | Check specific permission |
| middleware/command/cooldown.py | CooldownMiddleware | Handle command cooldowns |
| middleware/command/cooldown.py | CooldownMiddleware.process | Check and apply cooldowns |
| middleware/command/cooldown.py | CooldownMiddleware.is_on_cooldown | Check if command is on cooldown |
| middleware/command/cooldown.py | CooldownMiddleware.apply_cooldown | Apply cooldown to command |
| middleware/command/validation.py | ValidationMiddleware | Validate command input |
| middleware/command/validation.py | ValidationMiddleware.process | Validate command arguments |
| middleware/command/error.py | ErrorHandlingMiddleware | Handle command errors |
| middleware/command/error.py | ErrorHandlingMiddleware.process | Process and handle errors |
| middleware/command/error.py | ErrorHandlingMiddleware.format_error | Format error message |
| middleware/command/throttling.py | ThrottlingMiddleware | Throttle command execution |
| middleware/command/throttling.py | ThrottlingMiddleware.process | Apply throttling |
| middleware/command/throttling.py | ThrottlingMiddleware.should_throttle | Check if should throttle |

## Event Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/event/base.py | EventMiddleware | Base class for event middleware |
| middleware/event/base.py | EventMiddleware.process | Process event |
| middleware/event/base.py | EventRequest | Event request object |
| middleware/event/base.py | EventRequest.get_event | Get event being processed |
| middleware/event/base.py | EventRequest.get_context | Get event context |
| middleware/event/base.py | EventResponse | Event response object |
| middleware/event/base.py | EventResponse.is_handled | Check if event was handled |
| middleware/event/base.py | EventResponse.set_handled | Set event as handled |
| middleware/event/base.py | EventResponse.get_result | Get event processing result |
| middleware/event/base.py | EventResponse.set_result | Set event processing result |
| middleware/event/pipeline.py | EventPipeline | Pipeline for event middleware |
| middleware/event/pipeline.py | EventPipeline.process | Process event through pipeline |
| middleware/event/pipeline.py | get_event_pipeline | Get pipeline for events |

## Event Middleware Implementations

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/event/logging.py | LoggingMiddleware | Log event processing |
| middleware/event/logging.py | LoggingMiddleware.process | Log event details |
| middleware/event/validation.py | ValidationMiddleware | Validate event data |
| middleware/event/validation.py | ValidationMiddleware.process | Validate event properties |
| middleware/event/filtering.py | FilteringMiddleware | Filter events |
| middleware/event/filtering.py | FilteringMiddleware.process | Apply event filters |
| middleware/event/filtering.py | FilteringMiddleware.should_filter | Check if event should be filtered |
| middleware/event/transformation.py | TransformationMiddleware | Transform event data |
| middleware/event/transformation.py | TransformationMiddleware.process | Apply transformations |
| middleware/event/security.py | SecurityMiddleware | Security checks for events |
| middleware/event/security.py | SecurityMiddleware.process | Apply security validations |
| middleware/event/throttling.py | ThrottlingMiddleware | Throttle event processing |
| middleware/event/throttling.py | ThrottlingMiddleware.process | Apply throttling to events |
| middleware/event/error.py | ErrorHandlingMiddleware | Handle event errors |
| middleware/event/error.py | ErrorHandlingMiddleware.process | Process and handle errors |

## Transaction Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/transaction/base.py | TransactionMiddleware | Base class for transaction middleware |
| middleware/transaction/base.py | TransactionMiddleware.process | Process transaction |
| middleware/transaction/base.py | TransactionRequest | Transaction request object |
| middleware/transaction/base.py | TransactionRequest.get_transaction | Get transaction being processed |
| middleware/transaction/base.py | TransactionRequest.get_context | Get transaction context |
| middleware/transaction/base.py | TransactionResponse | Transaction response object |
| middleware/transaction/base.py | TransactionResponse.is_success | Check if transaction succeeded |
| middleware/transaction/base.py | TransactionResponse.set_success | Set transaction success status |
| middleware/transaction/base.py | TransactionResponse.get_result | Get transaction result |
| middleware/transaction/base.py | TransactionResponse.set_result | Set transaction result |
| middleware/transaction/pipeline.py | TransactionPipeline | Pipeline for transaction middleware |
| middleware/transaction/pipeline.py | TransactionPipeline.process | Process transaction through pipeline |
| middleware/transaction/pipeline.py | get_transaction_pipeline | Get pipeline for transactions |

## Feature-Specific Transaction Middleware 

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/transaction/points.py | PointsTransactionMiddleware | Base class for points transactions |
| middleware/transaction/points.py | PointsTransactionMiddleware.process | Process points transaction |
| middleware/transaction/points.py | EarningMiddleware | Handle points earning |
| middleware/transaction/points.py | EarningMiddleware.process | Process earning transaction |
| middleware/transaction/points.py | EarningMiddleware.validate | Validate earning transaction |
| middleware/transaction/points.py | SpendingMiddleware | Handle points spending |
| middleware/transaction/points.py | SpendingMiddleware.process | Process spending transaction |
| middleware/transaction/points.py | SpendingMiddleware.validate | Validate spending transaction |
| middleware/transaction/points.py | TransferMiddleware | Handle points transfers |
| middleware/transaction/points.py | TransferMiddleware.process | Process transfer transaction |
| middleware/transaction/points.py | TransferMiddleware.validate | Validate transfer transaction |
| middleware/transaction/shop.py | ShopTransactionMiddleware | Base class for shop transactions |
| middleware/transaction/shop.py | ShopTransactionMiddleware.process | Process shop transaction |
| middleware/transaction/shop.py | PurchaseMiddleware | Handle item purchases |
| middleware/transaction/shop.py | PurchaseMiddleware.process | Process purchase transaction |
| middleware/transaction/shop.py | PurchaseMiddleware.validate | Validate purchase transaction |
| middleware/transaction/shop.py | UpgradeMiddleware | Handle equipment upgrades |
| middleware/transaction/shop.py | UpgradeMiddleware.process | Process upgrade transaction |
| middleware/transaction/shop.py | UpgradeMiddleware.validate | Validate upgrade transaction |
| middleware/transaction/shop.py | ModificationMiddleware | Handle equipment modifications |
| middleware/transaction/shop.py | ModificationMiddleware.process | Process modification transaction |
| middleware/transaction/shop.py | ModificationMiddleware.validate | Validate modification transaction |
| middleware/transaction/inventory.py | InventoryMiddleware | Base class for inventory operations |
| middleware/transaction/inventory.py | InventoryMiddleware.process | Process inventory operation |
| middleware/transaction/inventory.py | AddItemMiddleware | Handle adding items to inventory |
| middleware/transaction/inventory.py | AddItemMiddleware.process | Process add item operation |
| middleware/transaction/inventory.py | AddItemMiddleware.validate | Validate add item operation |
| middleware/transaction/inventory.py | RemoveItemMiddleware | Handle removing items from inventory |
| middleware/transaction/inventory.py | RemoveItemMiddleware.process | Process remove item operation |
| middleware/transaction/inventory.py | RemoveItemMiddleware.validate | Validate remove item operation |
| middleware/transaction/inventory.py | UseItemMiddleware | Handle using items from inventory |
| middleware/transaction/inventory.py | UseItemMiddleware.process | Process use item operation |
| middleware/transaction/inventory.py | UseItemMiddleware.validate | Validate use item operation |
| middleware/transaction/duel.py | DuelMiddleware | Base class for duel operations |
| middleware/transaction/duel.py | DuelMiddleware.process | Process duel operation |
| middleware/transaction/duel.py | ChallengeMiddleware | Handle duel challenges |
| middleware/transaction/duel.py | ChallengeMiddleware.process | Process challenge operation |
| middleware/transaction/duel.py | ChallengeMiddleware.validate | Validate challenge operation |
| middleware/transaction/duel.py | ResolutionMiddleware | Handle duel resolutions |
| middleware/transaction/duel.py | ResolutionMiddleware.process | Process resolution operation |
| middleware/transaction/duel.py | ResolutionMiddleware.validate | Validate resolution operation |

## Platform Integration Middleware

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/platform/twitch.py | TwitchMiddleware | Base class for Twitch middleware |
| middleware/platform/twitch.py | TwitchMiddleware.process | Process Twitch message/event |
| middleware/platform/twitch.py | MessageMiddleware | Handle Twitch chat messages |
| middleware/platform/twitch.py | MessageMiddleware.process | Process chat message |
| middleware/platform/twitch.py | BitsMiddleware | Handle Twitch bits donations |
| middleware/platform/twitch.py | BitsMiddleware.process | Process bits donation |
| middleware/platform/twitch.py | RewardMiddleware | Handle Twitch channel point redemptions |
| middleware/platform/twitch.py | RewardMiddleware.process | Process reward redemption |
| middleware/platform/obs.py | OBSMiddleware | Base class for OBS middleware |
| middleware/platform/obs.py | OBSMiddleware.process | Process OBS operation |
| middleware/platform/obs.py | ActionMiddleware | Handle OBS actions |
| middleware/platform/obs.py | ActionMiddleware.process | Process OBS action |
| middleware/platform/obs.py | SequenceMiddleware | Handle OBS action sequences |
| middleware/platform/obs.py | SequenceMiddleware.process | Process action sequence |

## Middleware Factory

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/factory.py | MiddlewareFactory | Factory for creating middleware |
| middleware/factory.py | MiddlewareFactory.register | Register middleware type |
| middleware/factory.py | MiddlewareFactory.create | Create middleware instance |
| middleware/factory.py | get_factory | Get singleton factory instance |
| middleware/factory.py | create_middleware | Create middleware with factory |
| middleware/factory.py | register_middleware_type | Register type with factory |

## Middleware Decorators

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/decorators.py | middleware | Decorator to create middleware class |
| middleware/decorators.py | pipeline | Decorator to apply middleware pipeline |
| middleware/decorators.py | transaction | Decorator for transaction middleware |
| middleware/decorators.py | priority | Decorator to set middleware priority |
| middleware/decorators.py | error_handler | Decorator for error handling middleware |
| middleware/decorators.py | before_process | Decorator for pre-processing hooks |
| middleware/decorators.py | after_process | Decorator for post-processing hooks |

## Middleware Initialisation

| Module | Class/Function | Description |
|--------|----------------|-------------|
| middleware/initialisation.py | initialise_middleware | Initialise middleware system |
| middleware/initialisation.py | register_middleware | Register all middleware |
| middleware/initialisation.py | build_pipelines | Build middleware pipelines |
| middleware/initialisation.py | shutdown_middleware | Shutdown middleware system |