# CHANNEL POINTS

| Type                                            | Subscription                                                                      | Event                            | Payload                    |
| ----------------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------- | -------------------------- |
| Channel Points Automatic Reward Redemption      | [ChannelPointsAutoRedeemSubscription()](#channelpointsautoredeemsubscription)     | event_automatic_redemption_add() | ChannelPointsAutoRedeemAdd |
| Channel Points Custom Reward Update             | [ChannelPointsRewardUpdateSubscription()](#channelpointsrewardupdatesubscription) | event_custom_reward_update()     | ChannelPointsRewardUpdate  |
| Channel Points Custom Reward Add                | [ChannelPointsRewardAddSubscription()](#channelpointsrewardaddsubscription)       | event_custom_reward_add()        | ChannelPointsRewardAdd     |
| Channel Points Custom Reward Remove             | [ChannelPointsRewardRemoveSubscription()](#channelpointsrewardremovesubscription) | event_custom_reward_remove()     | ChannelPointsRewardRemove  |
| Channel Points Custom **Reward Redemption** Add | [ChannelPointsRedeemAddSubscription()](#channelpointsredeemaddsubscription)       | event_custom_redemption_add()    | ChannelPointsRedemptionAdd |

## ChannelPointsAutoRedeemSubscription()

`class twitchio.eventsub.ChannelPointsAutoRedeemSubscription(**condition: Unpack[Condition])`

    The channel.channel_points_automatic_reward_redemption.add subscription type sends a notification when a viewer has redeemed an automatic channel points reward on the specified channel.

    Important

    Must have channel:read:redemptions or channel:manage:redemptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelPointsRewardAddSubscription()

`class twitchio.eventsub.ChannelPointsRewardAddSubscription(**condition: Unpack[Condition])`

    The channel.channel_points_custom_reward.add subscription type sends a notification when a custom channel points reward has been created for the specified channel.

    Important

    Must have channel:read:redemptions or channel:manage:redemptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

        broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.
    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelPointsRewardUpdateSubscription()

`class twitchio.eventsub.ChannelPointsRewardUpdateSubscription(**condition: Unpack[Condition])`

    The channel.channel_points_custom_reward.update subscription type sends a notification when a custom channel points reward has been updated for the specified channel.

    Important

    Must have channel:read:redemptions or channel:manage:redemptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            reward_id (str) – Optional to only get notifications for a specific reward.

    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelPointsRewardRemoveSubscription()

`class twitchio.eventsub.ChannelPointsRewardRemoveSubscription(**condition: Unpack[Condition])`

    The channel.channel_points_custom_reward.remove subscription type sends a notification when a custom channel points reward has been removed from the specified channel.

    Important

    Must have channel:read:redemptions or channel:manage:redemptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            reward_id (str) – Optional to only get notifications for a specific reward.

    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ChannelPointsRedeemAddSubscription()

`class twitchio.eventsub.ChannelPointsRedeemAddSubscription(**condition: Unpack[Condition])`

    The channel.channel_points_custom_reward_redemption.add subscription type sends a notification when a viewer has redeemed a custom channel points reward on the specified channel.

    Important

    Must have channel:read:redemptions or channel:manage:redemptions scope.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            reward_id (str) – Optional to only get notifications for a specific reward.

    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
