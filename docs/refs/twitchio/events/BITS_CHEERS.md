# BITS AND CHEERS

| Type             | Subscription                                                | Event            | Payload        |
| ---------------- | ----------------------------------------------------------- | ---------------- | -------------- |
| Channel Bits Use | [ChannelBitsUseSubscription()](#channelbitsusesubscription) | event_bits_use() | ChannelBitsUse |
| Channel Cheer    | [ChannelCheerSubscription()](#channelcheersubscription)     | event_cheer()    | ChannelCheer   |

## ChannelBitsUseSubscription()

`class twitchio.eventsub.ChannelBitsUseSubscription(**condition: Unpack[Condition])`

    The channel.bits.use subscription type sends a notification whenever Bits are used on a channel.

    This event is designed to be an all-purpose event for when Bits are used in a channel and might be updated in the future as more Twitch features use Bits.

    Currently, this event will be sent when a user:

        Cheers in a channel

        Uses a Power-up

                Will not emit when a streamer uses a Power-up for free in their own channel.

    Important

    Requires a user access token that includes the bits:read scope. This must be the broadcaster’s token.

    Bits transactions via Twitch Extensions are not included in this subscription type.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameters “broadcaster_user_id” must be passed.

## ChannelCheerSubscription()

`class twitchio.eventsub.ChannelCheerSubscription(**condition: Unpack[Condition])`

    The channel.cheer subscription type sends a notification when a user cheers on the specified channel.

    Important

    Must have bits:read scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
