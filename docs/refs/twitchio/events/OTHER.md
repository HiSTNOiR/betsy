# OTHER EVENTS

| Type             | Subscription                                                  | Event                   | Payload       |
| ---------------- | ------------------------------------------------------------- | ----------------------- | ------------- |
| Channel Update   | [ChannelUpdateSubscription()](#channelupdatesubscription)     | event_channel_update()  | ChannelUpdate |
| Channel Follow   | [ChannelFollowSubscription()](#channelfollowsubscription)     | event_follow()          | ChannelFollow |
| Channel Raid     | [ChannelRaidSubscription()](#channelraidsubscription)         | event_raid()            | ChannelRaid   |
| Channel Ban      | [ChannelBanSubscription()](#channelbansubscription)           | event_ban()             | ChannelBan    |
| Channel Unban    | [ChannelUnbanSubscription()](#channelunbansubscription)       | event_unban()           | ChannelUnban  |
| Stream Online    | [StreamOnlineSubscription()](#streamonlinesubscription)       | event_stream_online()   | StreamOnline  |
| Stream Offline   | [StreamOfflineSubscription()](#streamofflinesubscription)     | event_stream_offline()  | StreamOffline |
| Whisper Received | [WhisperReceivedSubscription()](#whisperreceivedsubscription) | event_message_whisper() | Whisper       |

## ChannelUpdateSubscription()

`class twitchio.eventsub.ChannelUpdateSubscription(**condition: Unpack[Condition])`

    The channel.update subscription type sends notifications when a broadcaster updates the category, title, content classification labels, or broadcast language for their channel.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelFollowSubscription()

`class twitchio.eventsub.ChannelFollowSubscription(**condition: Unpack[Condition])`

    The channel.follow subscription type sends a notification when a specified channel receives a follow.

    Important

    Must have moderator:read:followers scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            moderator_user_id (str | PartialUser) – The ID, or PartialUser, of a moderator for the the broadcaster you are subscribing to. This could also be the broadcaster.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “moderator_user_id” must be passed.

## ChannelRaidSubscription()

`class twitchio.eventsub.ChannelRaidSubscription(**condition: Unpack[Condition])`

    The channel.raid subscription type sends a notification when a broadcaster raids another broadcaster’s channel.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            to_broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to. This listens to the raid events to a specific broadcaster.

            from_broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to. This listens to the raid events from a specific broadcaster.

    Raises

        ValueError – The parameter “to_broadcaster_user_id” must be passed.

## ChannelBanSubscription()

`class twitchio.eventsub.ChannelBanSubscription(**condition: Unpack[Condition])`

    The channel.ban subscription type sends a notification when a viewer is timed out or banned from the specified channel.

    Important

    Must have channel:moderate scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelUnbanSubscription()

`class twitchio.eventsub.ChannelUnbanSubscription(**condition: Unpack[Condition])`

    The channel.unban subscription type sends a notification when a viewer is unbanned from the specified channel.

    Important

    Must have channel:moderate scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## StreamOnlineSubscription()

`class twitchio.eventsub.StreamOnlineSubscription(**condition: Unpack[Condition])`

    The stream.online subscription type sends a notification when the specified broadcaster starts a stream.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## StreamOfflineSubscription()

`class twitchio.eventsub.StreamOfflineSubscription(**condition: Unpack[Condition])`

    The stream.offline subscription type sends a notification when the specified broadcaster stops a stream.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## WhisperReceivedSubscription()

`class twitchio.eventsub.WhisperReceivedSubscription(**condition: Unpack[Condition])`

    The user.whisper.message subscription type sends a notification when a user receives a whisper.

    Important

    Must have oauth scope user:read:whispers or user:manage:whispers.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        user_id (str | PartialUser) – The ID, or PartialUser, of the user receiving the whispers you wish to subscribe to.
    Raises

        ValueError – The parameter “user_id” must be passed.
