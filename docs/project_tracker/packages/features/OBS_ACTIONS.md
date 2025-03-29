# OBS Actions Package Structure and Components

The `features/obs_actions` package provides a comprehensive system for defining, managing, and executing sequences of OBS actions triggered by various events in the Twitch bot. This document outlines the structure and purpose of each module within the OBS actions feature package.

## Action Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | OBSActionManager | Main manager class for OBS actions functionality |
| manager.py | OBSActionManager.initialise | Initialise OBS actions system |
| manager.py | OBSActionManager.shutdown | Shut down OBS actions system |
| manager.py | OBSActionManager.create_action | Create a new OBS action |
| manager.py | OBSActionManager.get_action | Get action by identifier |
| manager.py | OBSActionManager.update_action | Update existing action |
| manager.py | OBSActionManager.delete_action | Delete existing action |
| manager.py | OBSActionManager.execute_action | Execute single action |
| manager.py | OBSActionManager.create_sequence | Create a new action sequence |
| manager.py | OBSActionManager.get_sequence | Get sequence by identifier |
| manager.py | OBSActionManager.update_sequence | Update existing sequence |
| manager.py | OBSActionManager.delete_sequence | Delete existing sequence |
| manager.py | OBSActionManager.execute_sequence | Execute action sequence |
| manager.py | OBSActionManager.get_actions_by_type | Get actions by type |
| manager.py | OBSActionManager.get_sequences_by_trigger | Get sequences by trigger type |
| manager.py | OBSActionManager.register_action_type | Register new action type |
| manager.py | OBSActionManager.register_trigger_type | Register new trigger type |
| manager.py | get_action_manager | Get singleton manager instance |
| manager.py | initialise | Initialise OBS actions system with global manager |
| manager.py | shutdown | Shutdown OBS actions system with global manager |

## Action Definition
| Module | Function | Description |
|--------|----------|-------------|
| actions/base.py | OBSAction | Base class for all OBS actions |
| actions/base.py | OBSAction.get_id | Get action identifier |
| actions/base.py | OBSAction.get_name | Get action name |
| actions/base.py | OBSAction.get_description | Get action description |
| actions/base.py | OBSAction.get_parameters | Get action parameters |
| actions/base.py | OBSAction.get_type | Get action type |
| actions/base.py | OBSAction.validate_parameters | Validate action parameters |
| actions/base.py | OBSAction.execute | Execute action with OBS connection |
| actions/base.py | OBSAction.to_dict | Convert action to dictionary |
| actions/base.py | OBSAction.from_dict | Create action from dictionary |
| actions/base.py | ActionRegistry | Registry for action types |
| actions/base.py | register_action | Register action type with registry |
| actions/base.py | get_action_registry | Get singleton action registry |

## Scene Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/scene.py | SceneAction | Base class for scene-related actions |
| actions/scene.py | SceneAction.validate_parameters | Validate scene parameters |
| actions/scene.py | SceneChangeAction | Action to change active scene |
| actions/scene.py | SceneChangeAction.execute | Execute scene change |
| actions/scene.py | SceneChangeAction.validate_parameters | Validate scene change parameters |
| actions/scene.py | SceneListAction | Action to get list of scenes |
| actions/scene.py | SceneListAction.execute | Execute scene list retrieval |
| actions/scene.py | SceneItemAction | Base class for scene item actions |
| actions/scene.py | SceneItemAction.validate_parameters | Validate scene item parameters |
| actions/scene.py | SceneItemShowAction | Action to show scene item |
| actions/scene.py | SceneItemShowAction.execute | Execute scene item show |
| actions/scene.py | SceneItemHideAction | Action to hide scene item |
| actions/scene.py | SceneItemHideAction.execute | Execute scene item hide |
| actions/scene.py | SceneItemToggleAction | Action to toggle scene item visibility |
| actions/scene.py | SceneItemToggleAction.execute | Execute scene item visibility toggle |
| actions/scene.py | register_scene_actions | Register all scene actions |

## Source Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/source.py | SourceAction | Base class for source-related actions |
| actions/source.py | SourceAction.validate_parameters | Validate source parameters |
| actions/source.py | SourcePositionAction | Action to set source position |
| actions/source.py | SourcePositionAction.execute | Execute source position change |
| actions/source.py | SourcePositionAction.validate_parameters | Validate position parameters |
| actions/source.py | SourceSizeAction | Action to set source size |
| actions/source.py | SourceSizeAction.execute | Execute source size change |
| actions/source.py | SourceSizeAction.validate_parameters | Validate size parameters |
| actions/source.py | SourceRotationAction | Action to set source rotation |
| actions/source.py | SourceRotationAction.execute | Execute source rotation change |
| actions/source.py | SourceRotationAction.validate_parameters | Validate rotation parameters |
| actions/source.py | SourceCropAction | Action to set source crop |
| actions/source.py | SourceCropAction.execute | Execute source crop change |
| actions/source.py | SourceCropAction.validate_parameters | Validate crop parameters |
| actions/source.py | SourceTransformAction | Action to set multiple transform properties |
| actions/source.py | SourceTransformAction.execute | Execute source transform change |
| actions/source.py | SourceTransformAction.validate_parameters | Validate transform parameters |
| actions/source.py | register_source_actions | Register all source actions |

## Text Source Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/text.py | TextSourceAction | Base class for text source actions |
| actions/text.py | TextSourceAction.validate_parameters | Validate text source parameters |
| actions/text.py | TextContentAction | Action to set text content |
| actions/text.py | TextContentAction.execute | Execute text content change |
| actions/text.py | TextContentAction.validate_parameters | Validate text content parameters |
| actions/text.py | TextFontAction | Action to set text font properties |
| actions/text.py | TextFontAction.execute | Execute text font change |
| actions/text.py | TextFontAction.validate_parameters | Validate text font parameters |
| actions/text.py | TextColourAction | Action to set text colour |
| actions/text.py | TextColourAction.execute | Execute text colour change |
| actions/text.py | TextColourAction.validate_parameters | Validate text colour parameters |
| actions/text.py | TextFromFileAction | Action to set text from file content |
| actions/text.py | TextFromFileAction.execute | Execute text from file update |
| actions/text.py | TextFromFileAction.validate_parameters | Validate file parameters |
| actions/text.py | register_text_actions | Register all text source actions |

## Filter Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/filter.py | FilterAction | Base class for filter-related actions |
| actions/filter.py | FilterAction.validate_parameters | Validate filter parameters |
| actions/filter.py | FilterEnableAction | Action to enable filter |
| actions/filter.py | FilterEnableAction.execute | Execute filter enable |
| actions/filter.py | FilterDisableAction | Action to disable filter |
| actions/filter.py | FilterDisableAction.execute | Execute filter disable |
| actions/filter.py | FilterToggleAction | Action to toggle filter state |
| actions/filter.py | FilterToggleAction.execute | Execute filter state toggle |
| actions/filter.py | FilterPropertyAction | Action to set filter property |
| actions/filter.py | FilterPropertyAction.execute | Execute filter property change |
| actions/filter.py | FilterPropertyAction.validate_parameters | Validate property parameters |
| actions/filter.py | register_filter_actions | Register all filter actions |

## Audio Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/audio.py | AudioAction | Base class for audio-related actions |
| actions/audio.py | AudioAction.validate_parameters | Validate audio parameters |
| actions/audio.py | AudioMuteAction | Action to mute audio source |
| actions/audio.py | AudioMuteAction.execute | Execute audio mute |
| actions/audio.py | AudioUnmuteAction | Action to unmute audio source |
| actions/audio.py | AudioUnmuteAction.execute | Execute audio unmute |
| actions/audio.py | AudioToggleMuteAction | Action to toggle audio mute state |
| actions/audio.py | AudioToggleMuteAction.execute | Execute audio mute toggle |
| actions/audio.py | AudioVolumeAction | Action to set audio volume |
| actions/audio.py | AudioVolumeAction.execute | Execute audio volume change |
| actions/audio.py | AudioVolumeAction.validate_parameters | Validate volume parameters |
| actions/audio.py | AudioFadeAction | Action to fade audio volume |
| actions/audio.py | AudioFadeAction.execute | Execute audio volume fade |
| actions/audio.py | AudioFadeAction.validate_parameters | Validate fade parameters |
| actions/audio.py | register_audio_actions | Register all audio actions |

## Stream Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/stream.py | StreamAction | Base class for stream-related actions |
| actions/stream.py | StreamAction.validate_parameters | Validate stream parameters |
| actions/stream.py | StreamStartAction | Action to start streaming |
| actions/stream.py | StreamStartAction.execute | Execute stream start |
| actions/stream.py | StreamStopAction | Action to stop streaming |
| actions/stream.py | StreamStopAction.execute | Execute stream stop |
| actions/stream.py | RecordingStartAction | Action to start recording |
| actions/stream.py | RecordingStartAction.execute | Execute recording start |
| actions/stream.py | RecordingStopAction | Action to stop recording |
| actions/stream.py | RecordingStopAction.execute | Execute recording stop |
| actions/stream.py | RecordingPauseAction | Action to pause recording |
| actions/stream.py | RecordingPauseAction.execute | Execute recording pause |
| actions/stream.py | RecordingResumeAction | Action to resume recording |
| actions/stream.py | RecordingResumeAction.execute | Execute recording resume |
| actions/stream.py | register_stream_actions | Register all stream actions |

## Animation Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/animation.py | AnimationAction | Base class for animation actions |
| actions/animation.py | AnimationAction.validate_parameters | Validate animation parameters |
| actions/animation.py | MoveAnimationAction | Action to animate source movement |
| actions/animation.py | MoveAnimationAction.execute | Execute movement animation |
| actions/animation.py | MoveAnimationAction.validate_parameters | Validate movement parameters |
| actions/animation.py | SizeAnimationAction | Action to animate source size change |
| actions/animation.py | SizeAnimationAction.execute | Execute size animation |
| actions/animation.py | SizeAnimationAction.validate_parameters | Validate size parameters |
| actions/animation.py | RotateAnimationAction | Action to animate source rotation |
| actions/animation.py | RotateAnimationAction.execute | Execute rotation animation |
| actions/animation.py | RotateAnimationAction.validate_parameters | Validate rotation parameters |
| actions/animation.py | FadeAnimationAction | Action to animate source opacity |
| actions/animation.py | FadeAnimationAction.execute | Execute opacity animation |
| actions/animation.py | FadeAnimationAction.validate_parameters | Validate opacity parameters |
| actions/animation.py | register_animation_actions | Register all animation actions |

## Delay Actions
| Module | Function | Description |
|--------|----------|-------------|
| actions/delay.py | DelayAction | Action to introduce delay in sequence |
| actions/delay.py | DelayAction.execute | Execute delay |
| actions/delay.py | DelayAction.validate_parameters | Validate delay parameters |
| actions/delay.py | RandomDelayAction | Action to introduce random delay in sequence |
| actions/delay.py | RandomDelayAction.execute | Execute random delay |
| actions/delay.py | RandomDelayAction.validate_parameters | Validate random delay parameters |
| actions/delay.py | WaitForSourceAction | Action to wait for source to exist |
| actions/delay.py | WaitForSourceAction.execute | Execute wait for source |
| actions/delay.py | WaitForSourceAction.validate_parameters | Validate source parameters |
| actions/delay.py | register_delay_actions | Register all delay actions |

## Sequence Definition
| Module | Function | Description |
|--------|----------|-------------|
| sequence.py | ActionSequence | Class for action sequences |
| sequence.py | ActionSequence.get_id | Get sequence identifier |
| sequence.py | ActionSequence.get_name | Get sequence name |
| sequence.py | ActionSequence.get_description | Get sequence description |
| sequence.py | ActionSequence.get_trigger_type | Get sequence trigger type |
| sequence.py | ActionSequence.get_trigger_value | Get sequence trigger value |
| sequence.py | ActionSequence.get_actions | Get ordered actions in sequence |
| sequence.py | ActionSequence.add_action | Add action to sequence |
| sequence.py | ActionSequence.remove_action | Remove action from sequence |
| sequence.py | ActionSequence.update_action_order | Update action order in sequence |
| sequence.py | ActionSequence.execute | Execute entire sequence |
| sequence.py | ActionSequence.validate | Validate sequence definition |
| sequence.py | ActionSequence.to_dict | Convert sequence to dictionary |
| sequence.py | ActionSequence.from_dict | Create sequence from dictionary |
| sequence.py | create_sequence | Create sequence from parameters |
| sequence.py | validate_sequence | Validate sequence definition |

## Trigger System
| Module | Function | Description |
|--------|----------|-------------|
| triggers/base.py | Trigger | Base class for action triggers |
| triggers/base.py | Trigger.get_type | Get trigger type |
| triggers/base.py | Trigger.get_value | Get trigger value |
| triggers/base.py | Trigger.matches | Check if event matches trigger |
| triggers/base.py | Trigger.validate_value | Validate trigger value |
| triggers/base.py | TriggerRegistry | Registry for trigger types |
| triggers/base.py | register_trigger | Register trigger type with registry |
| triggers/base.py | get_trigger_registry | Get singleton trigger registry |
| triggers/base.py | create_trigger | Create trigger from parameters |

## Command Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/command.py | CommandTrigger | Trigger for command execution |
| triggers/command.py | CommandTrigger.matches | Check if command matches trigger |
| triggers/command.py | CommandTrigger.validate_value | Validate command name |
| triggers/command.py | register_command_trigger | Register command trigger |

## Bits Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/bits.py | BitsTrigger | Trigger for bits donations |
| triggers/bits.py | BitsTrigger.matches | Check if bits donation matches trigger |
| triggers/bits.py | BitsTrigger.validate_value | Validate bits amount |
| triggers/bits.py | register_bits_trigger | Register bits trigger |

## Reward Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/reward.py | RewardTrigger | Trigger for channel point redemptions |
| triggers/reward.py | RewardTrigger.matches | Check if redemption matches trigger |
| triggers/reward.py | RewardTrigger.validate_value | Validate reward ID |
| triggers/reward.py | register_reward_trigger | Register reward trigger |

## Subscription Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/subscription.py | SubscriptionTrigger | Trigger for channel subscriptions |
| triggers/subscription.py | SubscriptionTrigger.matches | Check if subscription matches trigger |
| triggers/subscription.py | SubscriptionTrigger.validate_value | Validate subscription parameters |
| triggers/subscription.py | register_subscription_trigger | Register subscription trigger |

## Follow Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/follow.py | FollowTrigger | Trigger for channel follows |
| triggers/follow.py | FollowTrigger.matches | Check if follow matches trigger |
| triggers/follow.py | FollowTrigger.validate_value | Validate follow parameters |
| triggers/follow.py | register_follow_trigger | Register follow trigger |

## Raid Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/raid.py | RaidTrigger | Trigger for channel raids |
| triggers/raid.py | RaidTrigger.matches | Check if raid matches trigger |
| triggers/raid.py | RaidTrigger.validate_value | Validate raid parameters |
| triggers/raid.py | register_raid_trigger | Register raid trigger |

## Shield Mode Trigger
| Module | Function | Description |
|--------|----------|-------------|
| triggers/shield_mode.py | ShieldModeTrigger | Trigger for shield mode changes |
| triggers/shield_mode.py | ShieldModeTrigger.matches | Check if shield mode change matches trigger |
| triggers/shield_mode.py | ShieldModeTrigger.validate_value | Validate shield mode parameters |
| triggers/shield_mode.py | register_shield_mode_trigger | Register shield mode trigger |

## Sequence Execution
| Module | Function | Description |
|--------|----------|-------------|
| executor.py | SequenceExecutor | Executor for action sequences |
| executor.py | SequenceExecutor.execute_sequence | Execute action sequence |
| executor.py | SequenceExecutor.execute_action | Execute single action |
| executor.py | SequenceExecutor.handle_action_error | Handle action execution error |
| executor.py | SequenceExecutor.get_execution_context | Get context for execution |
| executor.py | SequenceExecutor.log_execution | Log sequence execution |
| executor.py | SequenceExecutor.register_execution_hook | Register hook for execution |
| executor.py | get_executor | Get singleton executor instance |
| executor.py | execute_sequence | Execute sequence with global instance |
| executor.py | execute_action | Execute action with global instance |

## OBS Actions Commands
| Module | Function | Description |
|--------|----------|-------------|
| commands.py | register_obs_actions_commands | Register all OBS actions-related commands |
| commands.py | ActionCommand | Command to trigger action sequence |
| commands.py | ActionCommand.execute | Execute sequence from command |
| commands.py | ActionListCommand | Command to list available actions |
| commands.py | ActionListCommand.execute | Display available actions |
| commands.py | SequenceListCommand | Command to list available sequences |
| commands.py | SequenceListCommand.execute | Display available sequences |
| commands.py | AdminActionCommand | Administrative command group for actions |
| commands.py | CreateSequenceCommand | Admin command to create sequence |
| commands.py | CreateSequenceCommand.execute | Process sequence creation |
| commands.py | DeleteSequenceCommand | Admin command to delete sequence |
| commands.py | DeleteSequenceCommand.execute | Process sequence deletion |
| commands.py | EnableSequenceCommand | Admin command to enable sequence |
| commands.py | EnableSequenceCommand.execute | Process sequence enabling |
| commands.py | DisableSequenceCommand | Admin command to disable sequence |
| commands.py | DisableSequenceCommand.execute | Process sequence disabling |
| commands.py | TestSequenceCommand | Admin command to test sequence |
| commands.py | TestSequenceCommand.execute | Process sequence testing |

## OBS Actions Event Handlers
| Module | Function | Description |
|--------|----------|-------------|
| events.py | register_obs_actions_events | Register all OBS actions-related event handlers |
| events.py | handle_command_event | Handle command events for sequences |
| events.py | handle_bits_event | Handle bits events for sequences |
| events.py | handle_reward_event | Handle reward events for sequences |
| events.py | handle_subscription_event | Handle subscription events for sequences |
| events.py | handle_follow_event | Handle follow events for sequences |
| events.py | handle_raid_event | Handle raid events for sequences |
| events.py | handle_shield_mode_event | Handle shield mode events for sequences |
| events.py | log_sequence_execution | Log sequence execution |
| events.py | log_action_execution | Log action execution |
| events.py | notify_sequence_execution | Send sequence execution notification |
| events.py | notify_action_error | Send action error notification |

## Action Repository Integration
| Module | Function | Description |
|--------|----------|-------------|
| repository.py | ActionRepository | Repository for action data |
| repository.py | ActionRepository.get_action | Get action from database |
| repository.py | ActionRepository.get_actions_by_type | Get actions by type from database |
| repository.py | ActionRepository.create_action | Create action in database |
| repository.py | ActionRepository.update_action | Update action in database |
| repository.py | ActionRepository.delete_action | Delete action from database |
| repository.py | ActionRepository.get_sequence | Get sequence from database |
| repository.py | ActionRepository.get_sequences_by_trigger | Get sequences by trigger from database |
| repository.py | ActionRepository.create_sequence | Create sequence in database |
| repository.py | ActionRepository.update_sequence | Update sequence in database |
| repository.py | ActionRepository.delete_sequence | Delete sequence from database |
| repository.py | ActionRepository.get_sequence_actions | Get actions for sequence from database |
| repository.py | ActionRepository.add_action_to_sequence | Add action to sequence in database |
| repository.py | ActionRepository.remove_action_from_sequence | Remove action from sequence in database |
| repository.py | ActionRepository.update_action_order | Update action order in database |
| repository.py | ActionRepository.get_execution_history | Get execution history from database |
| repository.py | ActionRepository.log_execution | Log execution in database |
| repository.py | get_repository | Get singleton repository instance |

## OBS Actions Configuration
| Module | Function | Description |
|--------|----------|-------------|
| config.py | OBSActionsConfig | Configuration for OBS actions system |
| config.py | OBSActionsConfig.get_default_scene | Get default scene for actions |
| config.py | OBSActionsConfig.get_default_duration | Get default duration for temporary actions |
| config.py | OBSActionsConfig.get_animation_fps | Get frames per second for animations |
| config.py | OBSActionsConfig.get_animation_defaults | Get default animation settings |
| config.py | OBSActionsConfig.get_admin_commands | Get admin-only command settings |
| config.py | OBSActionsConfig.get_execution_timeout | Get timeout for sequence execution |
| config.py | OBSActionsConfig.load | Load configuration from settings |
| config.py | OBSActionsConfig.save | Save configuration to settings |
| config.py | get_config | Get singleton configuration instance |

## Animation Engine
| Module | Function | Description |
|--------|----------|-------------|
| animation.py | AnimationEngine | Engine for source animations |
| animation.py | AnimationEngine.animate | Start animation process |
| animation.py | AnimationEngine.stop_animation | Stop animation process |
| animation.py | AnimationEngine.is_animating | Check if source is animating |
| animation.py | AnimationEngine.get_animations | Get active animations |
| animation.py | AnimationEngine.calculate_frame | Calculate animation frame |
| animation.py | AnimationEngine.calculate_linear | Calculate linear interpolation |
| animation.py | AnimationEngine.calculate_ease_in | Calculate ease-in interpolation |
| animation.py | AnimationEngine.calculate_ease_out | Calculate ease-out interpolation |
| animation.py | AnimationEngine.calculate_ease_in_out | Calculate ease-in-out interpolation |
| animation.py | AnimationEngine.calculate_bounce | Calculate bounce interpolation |
| animation.py | AnimationEngine.register_easing | Register custom easing function |
| animation.py | get_animation_engine | Get singleton engine instance |
| animation.py | animate_source | Animate source with global instance |
| animation.py | stop_animation | Stop animation with global instance |

## Template System
| Module | Function | Description |
|--------|----------|-------------|
| templates.py | TemplateManager | Manager for action sequence templates |
| templates.py | TemplateManager.get_templates | Get available templates |
| templates.py | TemplateManager.get_template | Get template by name |
| templates.py | TemplateManager.register_template | Register new template |
| templates.py | TemplateManager.create_from_template | Create sequence from template |
| templates.py | TemplateManager.validate_template | Validate template definition |
| templates.py | TemplateManager.load_templates | Load templates from storage |
| templates.py | TemplateManager.save_template | Save template to storage |
| templates.py | Template | Class representing action sequence template |
| templates.py | Template.get_name | Get template name |
| templates.py | Template.get_description | Get template description |
| templates.py | Template.get_parameters | Get template parameters |
| templates.py | Template.create_sequence | Create sequence from template |
| templates.py | get_template_manager | Get singleton manager instance |
| templates.py | create_from_template | Create from template with global instance |

## OBS Actions Feature Integration
| Module | Function | Description |
|--------|----------|-------------|
| feature.py | OBSActionsFeature | Main OBS actions feature class |
| feature.py | OBSActionsFeature.initialise | Initialise OBS actions feature |
| feature.py | OBSActionsFeature.shutdown | Shutdown OBS actions feature |
| feature.py | OBSActionsFeature.get_commands | Get commands provided by feature |
| feature.py | OBSActionsFeature.get_event_handlers | Get event handlers for feature |
| feature.py | OBSActionsFeature.is_enabled | Check if feature is enabled |
| feature.py | OBSActionsFeature.get_dependencies | Get feature dependencies |
| feature.py | OBSActionsFeature.get_manager | Get OBS actions manager |
| feature.py | OBSActionsFeature.get_config | Get OBS actions configuration |
| feature.py | register_feature | Register OBS actions feature with system |
| feature.py | get_feature | Get OBS actions feature instance |

## OBS Actions Hooks
| Module | Function | Description |
|--------|----------|-------------|
| hooks.py | OBSActionsHooks | Hooks for OBS actions system integration |
| hooks.py | OBSActionsHooks.register_action_creation_hook | Register hook for action creation |
| hooks.py | OBSActionsHooks.register_action_update_hook | Register hook for action update |
| hooks.py | OBSActionsHooks.register_action_deletion_hook | Register hook for action deletion |
| hooks.py | OBSActionsHooks.register_sequence_creation_hook | Register hook for sequence creation |
| hooks.py | OBSActionsHooks.register_sequence_update_hook | Register hook for sequence update |
| hooks.py | OBSActionsHooks.register_sequence_deletion_hook | Register hook for sequence deletion |
| hooks.py | OBSActionsHooks.register_execution_hook | Register hook for sequence execution |
| hooks.py | OBSActionsHooks.register_action_error_hook | Register hook for action error |
| hooks.py | OBSActionsHooks.trigger_action_creation_hooks | Trigger hooks for action creation |
| hooks.py | OBSActionsHooks.trigger_action_update_hooks | Trigger hooks for action update |
| hooks.py | OBSActionsHooks.trigger_action_deletion_hooks | Trigger hooks for action deletion |
| hooks.py | OBSActionsHooks.trigger_sequence_creation_hooks | Trigger hooks for sequence creation |
| hooks.py | OBSActionsHooks.trigger_sequence_update_hooks | Trigger hooks for sequence update |
| hooks.py | OBSActionsHooks.trigger_sequence_deletion_hooks | Trigger hooks for sequence deletion |
| hooks.py | OBSActionsHooks.trigger_execution_hooks | Trigger hooks for sequence execution |
| hooks.py | OBSActionsHooks.trigger_action_error_hooks | Trigger hooks for action error |
| hooks.py | get_hooks | Get singleton hooks instance |
| hooks.py | register_hook | Register hook with global instance |

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

## OBS Initialisation
| Module | Function | Description |
|--------|----------|-------------|
| initialisation.py | initialise_obs_actions | Initialise OBS actions system |
| initialisation.py | register_actions | Register built-in actions |
| initialisation.py | register_triggers | Register built-in triggers |
| initialisation.py | register_obs_actions_commands | Register OBS actions commands |
| initialisation.py | register_obs_actions_events | Register OBS actions event handlers |
| initialisation.py | load_sequences | Load saved sequences |
| initialisation.py | setup_animation_engine | Set up animation engine |
| initialisation.py | setup_template_manager | Set up template manager |
| initialisation.py | load_obs_actions_config | Load OBS actions configuration |
| initialisation.py | register_default_hooks | Register default OBS actions hooks |
| initialisation.py | setup_obs_actions_repository | Set up OBS actions data repository |
| initialisation.py | shutdown_obs_actions | Shutdown OBS actions system |
| initialisation.py | get_obs_actions_settings | Get OBS actions settings from config |