# SUBSCRIPTION

| Type                         | Subscription                                                                  | Event                        | Payload                    |
| ---------------------------- | ----------------------------------------------------------------------------- | ---------------------------- | -------------------------- |
| Channel Subscribe            | [ChannelSubscribeSubscription()](#channelsubscribesubscription)               | event_subscription()         | ChannelSubscribe           |
| Channel Subscription End     | [ChannelSubscriptionEndSubscription()](#channelsubscriptionendsubscription)   | event_subscription_end()     | ChannelSubscriptionEnd     |
| Channel Subscription Gift    | [ChannelSubscriptionGiftSubscription()](#channelsubscriptiongiftsubscription) | event_subscription_gift()    | ChannelSubscriptionGift    |
| Channel Subscription Message | [ChannelSubscribeMessageSubscription()](#channelsubscribemessagesubscription) | event_subscription_message() | ChannelSubscriptionMessage |

## ChannelSubscribeSubscription()

`class twitchio.eventsub.ChannelSubscribeSubscription(**condition: Unpack[Condition])`

    The channel.subscribe subscription type sends a notification when a specified channel receives a subscriber. This does not include resubscribes.

    Important

    Must have channel:read:subscriptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelSubscriptionEndSubscription()

`class twitchio.eventsub.ChannelSubscriptionEndSubscription(**condition: Unpack[Condition])`

    The channel.subscription.end subscription type sends a notification when a subscription to the specified channel expires.

    Important

    Must have channel:read:subscriptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelSubscriptionGiftSubscription()

`class twitchio.eventsub.ChannelSubscriptionEndSubscription(**condition: Unpack[Condition])`

    The channel.subscription.end subscription type sends a notification when a subscription to the specified channel expires.

    Important

    Must have channel:read:subscriptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelSubscribeMessageSubscription()

`class twitchio.eventsub.ChannelSubscribeMessageSubscription(**condition: Unpack[Condition])`

    The channel.subscription.message subscription type sends a notification when a user sends a resubscription chat message in a specific channel.

    Important

    Must have channel:read:subscriptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
