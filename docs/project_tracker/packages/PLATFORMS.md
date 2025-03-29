# Platforms Package Structure and Components

The `platforms` package provides a streamlined interface for interacting with external services like Twitch and OBS using existing libraries (`twitchio` and `obs-websocket-py`). This document outlines the simplified structure that leverages these libraries.

## Platform Base
| Module | Function | Description |
|--------|----------|-------------|
| base.py | BasePlatform | Abstract base class for all platform integrations |
| base.py | BasePlatform.connect | Connect to platform service |
| base.py | BasePlatform.disconnect | Disconnect from platform service |
| base.py | BasePlatform.is_connected | Check if platform is currently connected |
| base.py | BasePlatform.reconnect | Attempt to reconnect to platform |

## Platform Manager
| Module | Function | Description |
|--------|----------|-------------|
| manager.py | PlatformManager | Manager for platform integrations |
| manager.py | PlatformManager.initialise | Initialise platform manager |
| manager.py | PlatformManager.shutdown | Shutdown all platforms |
| manager.py | PlatformManager.register_platform | Register platform instance |
| manager.py | PlatformManager.get_platform | Get platform by type |
| manager.py | PlatformManager.connect_all | Connect all registered platforms |
| manager.py | PlatformManager.disconnect_all | Disconnect all platforms |
| manager.py | PlatformManager.reconnect_platform | Reconnect specific platform |

## Twitch Platform (using twitchio)
| Module | Function | Description |
|--------|----------|-------------|
| twitch.py | TwitchPlatform | Wrapper for twitchio functionality |
| twitch.py | TwitchPlatform.connect | Connect to Twitch services using twitchio |
| twitch.py | TwitchPlatform.disconnect | Disconnect from Twitch services |
| twitch.py | TwitchPlatform.is_connected | Check Twitch connection status |
| twitch.py | TwitchPlatform.register_event_handlers | Register event handlers with twitchio |
| twitch.py | TwitchPlatform.send_message | Send message to Twitch chat |
| twitch.py | TwitchPlatform.timeout_user | Timeout user in chat |
| twitch.py | TwitchPlatform.ban_user | Ban user from chat |
| twitch.py | TwitchPlatform.unban_user | Unban user from chat |
| twitch.py | TwitchPlatform.set_chat_mode | Set chat mode (emote-only, followers-only, etc.) |
| twitch.py | TwitchPlatform.get_user_info | Get information about Twitch user |
| twitch.py | TwitchPlatform.activate_shield_mode | Activate Twitch Shield Mode |
| twitch.py | TwitchPlatform.deactivate_shield_mode | Deactivate Twitch Shield Mode |
| twitch.py | TwitchPlatform.get_shield_mode_status | Get Shield Mode status |

## OBS Platform (using obs-websocket-py)
| Module | Function | Description |
|--------|----------|-------------|
| obs.py | OBSPlatform | Wrapper for obs-websocket-py functionality |
| obs.py | OBSPlatform.connect | Connect to OBS WebSocket |
| obs.py | OBSPlatform.disconnect | Disconnect from OBS WebSocket |
| obs.py | OBSPlatform.is_connected | Check OBS connection status |
| obs.py | OBSPlatform.reconnect | Reconnect to OBS WebSocket |
| obs.py | OBSPlatform.register_event_handlers | Register event handlers with OBS WebSocket |
| obs.py | OBSPlatform.get_scenes | Get list of available scenes |
| obs.py | OBSPlatform.get_current_scene | Get currently active scene |
| obs.py | OBSPlatform.set_current_scene | Switch to specified scene |
| obs.py | OBSPlatform.get_sources | Get sources in specified scene |
| obs.py | OBSPlatform.set_source_visibility | Set source visibility |
| obs.py | OBSPlatform.set_source_filter_visibility | Set filter visibility |
| obs.py | OBSPlatform.set_source_text | Set text for text source |
| obs.py | OBSPlatform.set_source_position | Set position of source |
| obs.py | OBSPlatform.set_audio_muted | Mute/unmute audio source |
| obs.py | OBSPlatform.set_audio_volume | Set volume of audio source |
| obs.py | OBSPlatform.start_streaming | Start OBS streaming |
| obs.py | OBSPlatform.stop_streaming | Stop OBS streaming |
| obs.py | OBSPlatform.start_recording | Start OBS recording |
| obs.py | OBSPlatform.stop_recording | Stop OBS recording |
| obs.py | OBSPlatform.animate_source | Basic animation for OBS source |

## OBS Actions
| Module | Function | Description |
|--------|----------|-------------|
| obs_actions.py | OBSActionSequence | Class for managing sequences of OBS actions |
| obs_actions.py | OBSActionSequence.add_action | Add action to sequence |
| obs_actions.py | OBSActionSequence.execute | Execute entire action sequence |
| obs_actions.py | OBSAction | Base class for actions |
| obs_actions.py | SceneChangeAction | Action to change scene |
| obs_actions.py | SourceVisibilityAction | Action to show/hide source |
| obs_actions.py | DelayAction | Action to introduce delay |
| obs_actions.py | SourceAnimationAction | Action to animate source |
| obs_actions.py | AudioMuteAction | Action to mute/unmute audio |
| obs_actions.py | TextSourceUpdateAction | Action to update text source |
| obs_actions.py | FilterToggleAction | Action to toggle filter |
| obs_actions.py | execute_action_sequence | Helper to execute action sequence |

## Event Adapters
| Module | Function | Description |
|--------|----------|-------------|
| events.py | convert_twitch_message | Convert twitchio message to app event |
| events.py | convert_twitch_bits | Convert twitchio bits event to app event |
| events.py | convert_twitch_subscription | Convert twitchio subscription to app event |
| events.py | convert_twitch_reward | Convert twitchio reward to app event |
| events.py | convert_twitch_follow | Convert twitchio follow to app event |
| events.py | convert_obs_scene_changed | Convert OBS scene changed to app event |
| events.py | convert_obs_stream_status | Convert OBS stream status to app event |
| events.py | convert_obs_source_visibility | Convert OBS source visibility to app event |
| events.py | register_platform_event_handlers | Register event converters with platforms |

## Platform Integration
| Module | Function | Description |
|--------|----------|-------------|
| integration.py | initialise_twitch | Initialise Twitch platform from config |
| integration.py | initialise_obs | Initialise OBS platform from config |
| integration.py | register_twitch_command_handlers | Register app commands with Twitch |
| integration.py | register_reward_handlers | Register channel point reward handlers |
| integration.py | register_bits_handlers | Register bits event handlers |
| integration.py | register_subscription_handlers | Register subscription event handlers |
| integration.py | register_obs_handlers | Register OBS event handlers |
| integration.py | connect_platforms | Connect to all enabled platforms |
| integration.py | shutdown_platforms | Disconnect from all platforms |