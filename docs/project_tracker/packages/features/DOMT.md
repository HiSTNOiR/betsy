# Deck of Many Things Package Structure and Components

The `features/domt` package implements the Deck of Many Things system for the Twitch bot, allowing users to draw random cards with various effects during streams. This document outlines the structure and purpose of each module within the DOMT feature package.

## DOMT Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | DOMTManager | Main manager class for DOMT functionality |
| manager.py | DOMTManager.initialise | Initialise DOMT system |
| manager.py | DOMTManager.shutdown | Shut down DOMT system |
| manager.py | DOMTManager.draw_card | Draw a card from the deck |
| manager.py | DOMTManager.process_card_effect | Process the effect of drawn card |
| manager.py | DOMTManager.reset_deck | Reset the deck when all cards drawn |
| manager.py | DOMTManager.get_remaining_cards | Get count of remaining cards |
| manager.py | DOMTManager.get_all_cards | Get all cards in the deck |
| manager.py | DOMTManager.get_drawn_cards | Get list of already drawn cards |
| manager.py | DOMTManager.get_card_by_name | Get card by its name |
| manager.py | DOMTManager.is_card_drawn | Check if specific card has been drawn |
| manager.py | DOMTManager.add_card_to_inventory | Add card to user's inventory |
| manager.py | DOMTManager.use_card_from_inventory | Use card from user's inventory |
| manager.py | DOMTManager.validate_bits_amount | Validate bits amount for drawing |
| manager.py | get_domt_manager | Get singleton manager instance |
| manager.py | initialise | Initialise DOMT system with global manager |
| manager.py | shutdown | Shutdown DOMT system with global manager |

## Card Definitions
| Module | Function | Description |
|--------|----------|-------------|
| cards.py | Card | Base class for DOMT cards |
| cards.py | Card.get_name | Get card name |
| cards.py | Card.get_description | Get card description |
| cards.py | Card.get_source | Get card image source |
| cards.py | Card.is_drawn | Check if card has been drawn |
| cards.py | Card.mark_drawn | Mark card as drawn |
| cards.py | Card.is_retainable | Check if card can be retained |
| cards.py | Card.get_action_sequence | Get associated action sequence |
| cards.py | Card.execute_effect | Execute card effect |
| cards.py | Card.can_use | Check if card can be used |
| cards.py | Card.use | Use card effect |
| cards.py | Card.get_times_drawn | Get number of times card has been drawn |
| cards.py | Card.increment_drawn_count | Increment card drawn counter |
| cards.py | Card.to_dict | Convert card to dictionary representation |
| cards.py | Card.from_dict | Create card from dictionary representation |
| cards.py | CardRegistry | Registry for card definitions |
| cards.py | register_card | Register card with registry |
| cards.py | get_card_registry | Get singleton card registry |
| cards.py | initialise_cards | Initialise card definitions |

## Card Effects
| Module | Function | Description |
|--------|----------|-------------|
| effects.py | CardEffect | Base class for card effects |
| effects.py | CardEffect.get_description | Get effect description |
| effects.py | CardEffect.execute | Execute effect |
| effects.py | CardEffect.can_execute | Check if effect can be executed |
| effects.py | CardEffect.validate_parameters | Validate effect parameters |
| effects.py | PointsEffect | Effect for modifying points |
| effects.py | PointsEffect.execute | Execute points modification |
| effects.py | TimeoutEffect | Effect for timing out user |
| effects.py | TimeoutEffect.execute | Execute timeout effect |
| effects.py | StreamEffect | Effect for modifying stream |
| effects.py | StreamEffect.execute | Execute stream modification |
| effects.py | OBSEffect | Effect for OBS actions |
| effects.py | OBSEffect.execute | Execute OBS action |
| effects.py | ChatEffect | Effect for chat actions |
| effects.py | ChatEffect.execute | Execute chat action |
| effects.py | InventoryEffect | Effect for inventory changes |
| effects.py | InventoryEffect.execute | Execute inventory change |
| effects.py | CompositeEffect | Composite of multiple effects |
| effects.py | CompositeEffect.execute | Execute multiple effects in sequence |
| effects.py | create_effect | Create effect from parameters |
| effects.py | register_effect | Register effect handler |

## DOMT Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_domt_commands | Register all DOMT-related commands |
| commands.py | CardCommand | Command to use card from inventory |
| commands.py | CardCommand.execute | Process card usage |
| commands.py | CardsCommand | Command to view owned cards |
| commands.py | CardsCommand.execute | Display owned cards |
| commands.py | CardInfoCommand | Command to view card information |
| commands.py | CardInfoCommand.execute | Display card information |
| commands.py | DOMTStatusCommand | Command to view DOMT status |
| commands.py | DOMTStatusCommand.execute | Display DOMT status |
| commands.py | AdminDOMTCommand | Administrative command group for DOMT |
| commands.py | ResetDeckCommand | Admin command to reset deck |
| commands.py | ResetDeckCommand.execute | Process deck reset |
| commands.py | GiveCardCommand | Admin command to give card to user |
| commands.py | GiveCardCommand.execute | Process giving card to user |
| commands.py | DrawCardCommand | Admin command to force card draw |
| commands.py | DrawCardCommand.execute | Process forced card draw |

## Bits Integration
| Module | Function | Description |
|--------|----------|-------------|
| bits.py | BitsHandler | Handler for Twitch bits integration |
| bits.py | BitsHandler.register | Register bits handler with Twitch |
| bits.py | BitsHandler.handle_bits | Handle bits donation for DOMT |
| bits.py | BitsHandler.validate_amount | Validate bits amount |
| bits.py | BitsHandler.process_card_draw | Process card draw from bits |
| bits.py | BitsHandler.notify_card_draw | Send card draw notification |
| bits.py | BitsHandler.log_bits_transaction | Log bits transaction |
| bits.py | get_bits_handler | Get singleton handler instance |
| bits.py | register_bits_handler | Register bits handler with global instance |
| bits.py | handle_bits | Handle bits with global instance |

## Deck Implementation
| Module | Function | Description |
|--------|----------|-------------|
| deck.py | Deck | Implementation of card deck |
| deck.py | Deck.initialise | Initialise deck with cards |
| deck.py | Deck.reset | Reset deck to initial state |
| deck.py | Deck.draw | Draw card from deck |
| deck.py | Deck.get_remaining | Get count of remaining cards |
| deck.py | Deck.get_drawn | Get list of drawn cards |
| deck.py | Deck.is_empty | Check if deck is empty |
| deck.py | Deck.get_all_cards | Get all cards in deck |
| deck.py | Deck.mark_card_drawn | Mark specific card as drawn |
| deck.py | Deck.is_card_drawn | Check if specific card is drawn |
| deck.py | Deck.get_draw_history | Get history of card draws |
| deck.py | Deck.get_reset_count | Get number of times deck has been reset |
| deck.py | Deck.increment_reset_count | Increment deck reset counter |
| deck.py | Deck.save_state | Save deck state |
| deck.py | Deck.load_state | Load deck state |
| deck.py | get_deck | Get singleton deck instance |
| deck.py | reset_deck | Reset deck with global instance |

## Card Display Formatter
| Module | Function | Description |
|--------|----------|-------------|
| display.py | CardDisplay | Formatter for card displays |
| display.py | CardDisplay.format_card | Format card information |
| display.py | CardDisplay.format_card_draw | Format card draw result |
| display.py | CardDisplay.format_card_list | Format list of cards |
| display.py | CardDisplay.format_user_cards | Format user's owned cards |
| display.py | CardDisplay.format_deck_status | Format deck status information |
| display.py | CardDisplay.format_card_effect | Format card effect description |
| display.py | CardDisplay.format_points_effect | Format points effect description |
| display.py | CardDisplay.format_timeout_effect | Format timeout effect description |
| display.py | CardDisplay.format_stream_effect | Format stream effect description |
| display.py | CardDisplay.format_obs_effect | Format OBS effect description |
| display.py | CardDisplay.format_chat_effect | Format chat effect description |
| display.py | CardDisplay.format_inventory_effect | Format inventory effect description |
| display.py | get_card_display | Get singleton display instance |
| display.py | format_card | Format card with global instance |

## DOMT Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_domt_events | Register all DOMT-related event handlers |
| events.py | handle_bits_donation | Handle bits donation for DOMT |
| events.py | handle_card_drawn | Handle card drawn event |
| events.py | handle_card_effect_executed | Handle card effect execution |
| events.py | handle_deck_reset | Handle deck reset event |
| events.py | handle_card_added_to_inventory | Handle card added to inventory |
| events.py | handle_card_used_from_inventory | Handle card used from inventory |
| events.py | notify_card_drawn | Send card drawn notification |
| events.py | notify_effect_executed | Send effect execution notification |
| events.py | notify_deck_reset | Send deck reset notification |
| events.py | notify_card_added | Send card added notification |
| events.py | notify_card_used | Send card used notification |
| events.py | log_card_draw | Log card draw event |
| events.py | log_effect_execution | Log effect execution event |
| events.py | log_deck_reset | Log deck reset event |

## OBS Actions Integration
| Module | Function | Description |
|--------|----------|-------------|
| obs_actions.py | OBSActionHandler | Handler for OBS actions integration |
| obs_actions.py | OBSActionHandler.register_actions | Register DOMT OBS actions |
| obs_actions.py | OBSActionHandler.card_draw_sequence | Execute card draw sequence |
| obs_actions.py | OBSActionHandler.card_effect_sequence | Execute card effect sequence |
| obs_actions.py | OBSActionHandler.deck_reset_sequence | Execute deck reset sequence |
| obs_actions.py | OBSActionHandler.show_card | Show card in OBS |
| obs_actions.py | OBSActionHandler.hide_card | Hide card in OBS |
| obs_actions.py | OBSActionHandler.animate_card | Animate card in OBS |
| obs_actions.py | OBSActionHandler.apply_filter | Apply filter for card effect |
| obs_actions.py | OBSActionHandler.remove_filter | Remove filter for card effect |
| obs_actions.py | OBSActionHandler.play_card_sound | Play sound for card draw |
| obs_actions.py | get_obs_handler | Get singleton handler instance |
| obs_actions.py | execute_card_draw_sequence | Execute sequence with global instance |

## DOMT Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | DOMTConfig | Configuration for DOMT system |
| config.py | DOMTConfig.get_bits_cost | Get bits cost for drawing card |
| config.py | DOMTConfig.get_card_count | Get total number of cards in deck |
| config.py | DOMTConfig.get_obs_scene | Get OBS scene for DOMT |
| config.py | DOMTConfig.get_obs_sources | Get OBS sources for DOMT |
| config.py | DOMTConfig.get_card_duration | Get duration to show card |
| config.py | DOMTConfig.get_effect_probability | Get probability of effect execution |
| config.py | DOMTConfig.get_retainable_cards | Get list of retainable cards |
| config.py | DOMTConfig.get_animation_settings | Get animation settings for cards |
| config.py | DOMTConfig.load | Load configuration from settings |
| config.py | DOMTConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## DOMT Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | DOMTRepository | Repository for DOMT data |
| repository.py | DOMTRepository.get_card | Get card from database |
| repository.py | DOMTRepository.get_all_cards | Get all cards from database |
| repository.py | DOMTRepository.update_card | Update card in database |
| repository.py | DOMTRepository.mark_card_drawn | Mark card as drawn in database |
| repository.py | DOMTRepository.reset_deck | Reset deck in database |
| repository.py | DOMTRepository.get_user_cards | Get user's cards from database |
| repository.py | DOMTRepository.add_card_to_user | Add card to user in database |
| repository.py | DOMTRepository.remove_card_from_user | Remove card from user in database |
| repository.py | DOMTRepository.log_card_draw | Log card draw in database |
| repository.py | DOMTRepository.get_draw_history | Get card draw history from database |
| repository.py | DOMTRepository.get_deck_stats | Get deck statistics from database |
| repository.py | DOMTRepository.increase_draw_count | Increase card draw count in database |
| repository.py | DOMTRepository.increase_reset_count | Increase deck reset count in database |
| repository.py | get_repository | Get singleton repository instance |

## DOMT Analytics
| Module | Function | Description |
|--------|----------|-------------|
| analytics.py | DOMTAnalytics | Analytics for DOMT system |
| analytics.py | DOMTAnalytics.get_popular_cards | Get most frequently drawn cards |
| analytics.py | DOMTAnalytics.get_rare_cards | Get least frequently drawn cards |
| analytics.py | DOMTAnalytics.get_bits_spent | Get total bits spent on DOMT |
| analytics.py | DOMTAnalytics.get_card_distribution | Get distribution of card draws |
| analytics.py | DOMTAnalytics.get_effect_statistics | Get statistics on effect execution |
| analytics.py | DOMTAnalytics.get_user_statistics | Get statistics for user card draws |
| analytics.py | DOMTAnalytics.get_reset_statistics | Get statistics on deck resets |
| analytics.py | DOMTAnalytics.get_retained_card_statistics | Get statistics on retained cards |
| analytics.py | DOMTAnalytics.get_card_usage_statistics | Get statistics on card usage |
| analytics.py | DOMTAnalytics.generate_report | Generate analytics report |
| analytics.py | get_analytics | Get singleton analytics instance |
| analytics.py | generate_report | Generate report with global instance |

## DOMT Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | DOMTFeature | Main DOMT feature class |
| feature.py | DOMTFeature.initialise | Initialise DOMT feature |
| feature.py | DOMTFeature.shutdown | Shutdown DOMT feature |
| feature.py | DOMTFeature.get_commands | Get commands provided by feature |
| feature.py | DOMTFeature.get_event_handlers | Get event handlers for feature |
| feature.py | DOMTFeature.is_enabled | Check if feature is enabled |
| feature.py | DOMTFeature.get_dependencies | Get feature dependencies |
| feature.py | DOMTFeature.get_manager | Get DOMT manager |
| feature.py | DOMTFeature.get_config | Get DOMT configuration |
| feature.py | register_feature | Register DOMT feature with system |
| feature.py | get_feature | Get DOMT feature instance |

## DOMT Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | DOMTHooks | Hooks for DOMT system integration |
| hooks.py | DOMTHooks.register_card_draw_hook | Register hook for card draws |
| hooks.py | DOMTHooks.register_effect_execution_hook | Register hook for effect execution |
| hooks.py | DOMTHooks.register_deck_reset_hook | Register hook for deck resets |
| hooks.py | DOMTHooks.register_card_add_hook | Register hook for cards added to inventory |
| hooks.py | DOMTHooks.register_card_use_hook | Register hook for cards used from inventory |
| hooks.py | DOMTHooks.trigger_card_draw_hooks | Trigger hooks for card draws |
| hooks.py | DOMTHooks.trigger_effect_execution_hooks | Trigger hooks for effect execution |
| hooks.py | DOMTHooks.trigger_deck_reset_hooks | Trigger hooks for deck resets |
| hooks.py | DOMTHooks.trigger_card_add_hooks | Trigger hooks for cards added to inventory |
| hooks.py | DOMTHooks.trigger_card_use_hooks | Trigger hooks for cards used from inventory |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

## Card Animations
| Module | Function | Description |
|--------|----------|-------------|
| animations.py | CardAnimation | Base class for card animations |
| animations.py | CardAnimation.play | Play card animation |
| animations.py | CardAnimation.stop | Stop card animation |
| animations.py | CardAnimation.get_duration | Get animation duration |
| animations.py | CardAnimation.get_parameters | Get animation parameters |
| animations.py | CardDrawAnimation | Animation for drawing card |
| animations.py | CardDrawAnimation.play | Play card draw animation |
| animations.py | CardEffectAnimation | Animation for card effect |
| animations.py | CardEffectAnimation.play | Play card effect animation |
| animations.py | CardFlipAnimation | Animation for card flip |
| animations.py | CardFlipAnimation.play | Play card flip animation |
| animations.py | CardRevealAnimation | Animation for card reveal |
| animations.py | CardRevealAnimation.play | Play card reveal animation |
| animations.py | create_animation | Create animation from parameters |
| animations.py | register_animation | Register animation type |

## DOMT Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_domt | Initialise DOMT system |
| initialisation.py | register_domt_commands | Register DOMT commands |
| initialisation.py | register_domt_events | Register DOMT event handlers |
| initialisation.py | setup_card_registry | Set up card registry |
| initialisation.py | setup_deck | Set up card deck |
| initialisation.py | setup_bits_handler | Set up bits handler |
| initialisation.py | setup_obs_handler | Set up OBS handler |
| initialisation.py | load_domt_config | Load DOMT configuration |
| initialisation.py | register_default_hooks | Register default DOMT hooks |
| initialisation.py | setup_domt_repository | Set up DOMT data repository |
| initialisation.py | setup_card_display | Set up card display formatter |
| initialisation.py | shutdown_domt | Shutdown DOMT system |
| initialisation.py | get_domt_settings | Get DOMT settings from config |