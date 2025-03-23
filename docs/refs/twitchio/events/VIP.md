# VIP

| Type               | Subscription                                                    | Event              | Payload          |
| ------------------ | --------------------------------------------------------------- | ------------------ | ---------------- |
| Channel VIP Add    | [ChannelVIPAddSubscription()](#channelvipaddsubscription)       | event_vip_add()    | ChannelVIPAdd    |
| Channel VIP Remove | [ChannelVIPRemoveSubscription()](#channelvipremovesubscription) | event_vip_remove() | ChannelVIPRemove |

## ChannelVIPAddSubscription()

`class twitchio.eventsub.ChannelVIPAddSubscription(**condition: Unpack[Condition])`

    The channel.vip.add subscription type sends a notification when a VIP is added to the channel.

    Important

    Must have channel:read:vips or channel:manage:vips scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelVIPRemoveSubscription()

`class twitchio.eventsub.ChannelVIPRemoveSubscription(**condition: Unpack[Condition])`

    The channel.vip.remove subscription type sends a notification when a VIP is removed from the channel.

    Important

    Must have channel:read:vips or channel:manage:vips scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
