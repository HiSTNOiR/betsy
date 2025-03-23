# MODERATOR

| Type                     | Subscription                                                                | Event                    | Payload                |
| ------------------------ | --------------------------------------------------------------------------- | ------------------------ | ---------------------- |
| Channel Moderator Add    | [ChannelModeratorAddSubscription()](#channelmoderatoraddsubscription)       | event_moderator_add()    | ChannelModeratorAdd    |
| Channel Moderator Remove | [ChannelModeratorRemoveSubscription()](#channelmoderatorremovesubscription) | event_moderator_remove() | ChannelModeratorRemove |

## ChannelModeratorAddSubscription()

`class twitchio.eventsub.ChannelModeratorAddSubscription(**condition: Unpack[Condition])`

    The channel.moderator.add subscription type sends a notification when a user is given moderator privileges on a specified channel.

    Important

    Must have moderation:read scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelModeratorRemoveSubscription()

`class twitchio.eventsub.ChannelModeratorRemoveSubscription(**condition: Unpack[Condition])`

    The channel.moderator.remove subscription type sends a notification when a user has moderator privileges removed on a specified channel.

    Important

    Must have moderation:read scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
