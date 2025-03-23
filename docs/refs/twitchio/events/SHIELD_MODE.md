# SHIELD MODE

| Type              | Subscription                                                  | Event                     | Payload         |
| ----------------- | ------------------------------------------------------------- | ------------------------- | --------------- |
| Shield Mode Begin | [ShieldModeBeginSubscription()](#shieldmodebeginsubscription) | event_shield_mode_begin() | ShieldModeBegin |
| Shield Mode End   | [ShieldModeEndSubscription()](#shieldmodeendsubscription)     | event_shield_mode_end()   | ShieldModeEnd   |

## ShieldModeBeginSubscription()

`class twitchio.eventsub.ShieldModeBeginSubscription(**condition: Unpack[Condition])`

    The channel.shield_mode.begin subscription type sends a notification when the broadcaster activates Shield Mode.

    This event informs the subscriber that the broadcaster’s moderation settings were changed based on the broadcaster’s Shield Mode configuration settings.

    Important

    Requires the moderator:read:shield_mode or moderator:manage:shield_mode scope.

        If you use webhooks, the moderator must have granted your app (client ID) one of the above permissions prior to your app subscribing to this subscription type.

        If you use WebSockets, the moderator’s ID must match the user ID in the user access token.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            moderator_user_id (str | PartialUser) – The ID, or PartialUser, of a moderator for the the broadcaster you are subscribing to. This could also be the broadcaster.

    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.

## ShieldModeEndSubscription()

`class twitchio.eventsub.ShieldModeEndSubscription(**condition: Unpack[Condition])`

    The channel.shield_mode.end subscription type sends a notification when the broadcaster deactivates Shield Mode.

    This event informs the subscriber that the broadcaster’s moderation settings were changed back to the broadcaster’s previous moderation settings.

    Important

    Requires the moderator:read:shield_mode or moderator:manage:shield_mode scope.

        If you use webhooks, the moderator must have granted your app (client ID) one of the above permissions prior to your app subscribing to this subscription type.

        If you use WebSockets, the moderator’s ID must match the user ID in the user access token.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            moderator_user_id (str | PartialUser) – The ID, or PartialUser, of a moderator for the the broadcaster you are subscribing to. This could also be the broadcaster.

    Raises

        ValueError – The parameter “broadcaster_user_id” must be passed.
