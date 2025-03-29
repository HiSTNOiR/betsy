# Package middleware

## Commands Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | Middleware | Base class for command middleware |
| middleware.py | Middleware.process_command | Process command before execution |
| middleware.py | Middleware.process_context | Process context before execution |
| middleware.py | Middleware.handle_error | Handle error during execution |
| middleware.py | Middleware.after_command | Process after command execution |
| middleware.py | MiddlewareManager | Manager for middleware chain |
| middleware.py | MiddlewareManager.add | Add middleware to chain |
| middleware.py | MiddlewareManager.remove | Remove middleware from chain |
| middleware.py | MiddlewareManager.process | Process command through middleware chain |
| middleware.py | LoggingMiddleware | Middleware for command logging |
| middleware.py | PermissionMiddleware | Middleware for permission checks |
| middleware.py | CooldownMiddleware | Middleware for cooldown handling |
| middleware.py | ThrottlingMiddleware | Middleware for command throttling |

## Events Middleware
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

## Shop Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | ShopMiddleware | Middleware for shop transactions |
| middleware.py | ShopMiddleware.process_transaction | Process through middleware |
| middleware.py | ShopMiddleware.register_middleware | Register transaction middleware |
| middleware.py | ShopMiddleware.validate_transaction | Validate transaction |
| middleware.py | ShopMiddleware.modify_transaction | Modify transaction |
| middleware.py | ShopMiddleware.log_transaction | Log transaction details |
| middleware.py | ShopMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_transaction_middleware | Register middleware |

## Inventory Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | InventoryMiddleware | Middleware for inventory operations |
| middleware.py | InventoryMiddleware.process_operation | Process operation through middleware |
| middleware.py | InventoryMiddleware.register_middleware | Register operation middleware |
| middleware.py | InventoryMiddleware.validate_operation | Validate inventory operation |
| middleware.py | InventoryMiddleware.modify_operation | Modify inventory operation |
| middleware.py | InventoryMiddleware.log_operation | Log operation details |
| middleware.py | InventoryMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |

## DOMT Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | DOMTMiddleware | Middleware for DOMT operations |
| middleware.py | DOMTMiddleware.process_operation | Process operation through middleware |
| middleware.py | DOMTMiddleware.register_middleware | Register operation middleware |
| middleware.py | DOMTMiddleware.validate_operation | Validate DOMT operation |
| middleware.py | DOMTMiddleware.modify_operation | Modify DOMT operation |
| middleware.py | DOMTMiddleware.log_operation | Log operation details |
| middleware.py | DOMTMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |

## Duel Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | DuelMiddleware | Middleware for duel operations |
| middleware.py | DuelMiddleware.process_operation | Process operation through middleware |
| middleware.py | DuelMiddleware.register_middleware | Register operation middleware |
| middleware.py | DuelMiddleware.validate_operation | Validate duel operation |
| middleware.py | DuelMiddleware.modify_operation | Modify duel operation |
| middleware.py | DuelMiddleware.log_operation | Log operation details |
| middleware.py | DuelMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |

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

## OBS Actions Middleware
| Module | Function | Description |
|--------|----------|-------------|
| middleware.py | OBSActionsMiddleware | Middleware for OBS actions operations |
| middleware.py | OBSActionsMiddleware.process_operation | Process operation through middleware |
| middleware.py | OBSActionsMiddleware.register_middleware | Register operation middleware |
| middleware.py | OBSActionsMiddleware.validate_operation | Validate OBS actions operation |
| middleware.py | OBSActionsMiddleware.modify_operation | Modify OBS actions operation |
| middleware.py | OBSActionsMiddleware.log_operation | Log operation details |
| middleware.py | OBSActionsMiddleware.get_chain | Get middleware chain |
| middleware.py | get_middleware | Get singleton middleware instance |
| middleware.py | register_middleware | Register middleware with global instance |