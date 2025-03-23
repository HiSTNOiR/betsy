# CHAT

| Type                             | Subscription                                                              | Event                        | Payload                      |
| -------------------------------- | ------------------------------------------------------------------------- | ---------------------------- | ---------------------------- |
| Channel Chat Clear User Messages | [ChatClearUserMessagesSubscription()](#chatclearusermessagessubscription) | event_chat_clear_user()      | ChannelChatClearUserMessages |
| Channel Chat Message             | [ChatMessageSubscription()](#chatmessagesubscription)                     | event_message()              | ChatMessage                  |
| Channel Chat Message Delete      | [ChatMessageDeleteSubscription()](#chatmessagedeletesubscription)         | event_message_delete()       | ChatMessageDelete            |
| Channel Chat Notification        | [ChatNotificationSubscription()](#chatnotificationsubscription)           | event_chat_notification()    | ChatNotification             |
| Channel Chat Settings Update     | [ChatSettingsUpdateSubscription()](#chatsettingsupdatesubscription)       | event_chat_settings_update() | ChatSettingsUpdate           |

## ChatClearUserMessagesSubscription()

`class twitchio.eventsub.ChatClearUserMessagesSubscription(**condition: Unpack[Condition])`

    The channel.chat.clear_user_messages subscription type sends a notification when a moderator or bot clears all messages for a specific user.

    Important

    Requires user:read:chat scope from chatting user.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            user_id (str | PartialUser) – The ID, or PartialUser, of the chatter reading chat. e.g. Your bot ID.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “user_id” must be passed.

## ChatMessageSubscription()

`class twitchio.eventsub.ChatMessageSubscription(**condition: Unpack[Condition])`

    The channel.chat.message subscription type sends a notification when any user sends a message to a channel’s chat room.

    Important

    Requires user:read:chat scope from chatting user.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            user_id (str | PartialUser) – The ID, or PartialUser, of the chatter reading chat. e.g. Your bot ID.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “user_id” must be passed.

## ChatMessageDeleteSubscription()

`class twitchio.eventsub.ChatMessageDeleteSubscription(**condition: Unpack[Condition])`

    The channel.chat.message_delete subscription type sends a notification when a moderator removes a specific message.

    Important

    Requires user:read:chat scope from chatting user.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            user_id (str | PartialUser) – The ID, or PartialUser, of the chatter reading chat. e.g. Your bot ID.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “user_id” must be passed.

## ChatNotificationSubscription()

`class twitchio.eventsub.ChatNotificationSubscription(**condition: Unpack[Condition])`

    The channel.chat.notification subscription type sends a notification when an event that appears in chat occurs, such as someone subscribing to the channel or a subscription is gifted.

    Important

    Requires user:read:chat scope from chatting user.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            user_id (str | PartialUser) – The ID, or PartialUser, of the chatter reading chat. e.g. Your bot ID.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “user_id” must be passed.

## ChatSettingsUpdateSubscription()

`class twitchio.eventsub.ChatSettingsUpdateSubscription(**condition: Unpack[Condition])`

    The channel.chat_settings.update subscription type sends a notification when a broadcaster’s chat settings are updated.

    Important

    Requires user:read:chat scope from chatting user.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

    One attribute .condition can be accessed from this class, which returns a mapping of the subscription parameters provided.

    Parameters

            broadcaster_user_id (str | PartialUser) – The ID, or PartialUser, of the broadcaster to subscribe to.

            user_id (str | PartialUser) – The ID, or PartialUser, of the chatter reading chat. e.g. Your bot ID.

    Raises

        ValueError – The parameters “broadcaster_user_id” and “user_id” must be passed.
