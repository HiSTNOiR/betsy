# OTHER

-   [create_stream_marker](#create_stream_marker)
-   [send_message](#send_message)
-   [update_chat_settings](#update_chat_settings)
-   [update_shield_mode_status](#update_shield_mode_status)

## create_stream_marker

`async create_stream_marker(*, token_for: str | PartialUser, description: str | None = None) → StreamMarker`

    This function is a coroutine.

    Adds a marker to a live stream.

    A marker is an arbitrary point in a live stream that the broadcaster or editor wants to mark, so they can return to that spot later to create video highlights.

    Important

    You may not add markers:

        If the stream is not live

        If the stream has not enabled video on demand (VOD)

        If the stream is a premiere (a live, first-viewing event that combines uploaded videos with live chat)

        If the stream is a rerun of a past broadcast, including past premieres.

    Note

    Requires a user access token that includes the channel:manage:broadcast scope.

    Parameters

            token_for (str | PartialUser) – This must be the user ID, or PartialUser, of the broadcaster or one of the broadcaster’s editors.

            description (str | None) – A short description of the marker to help the user remember why they marked the location. The maximum length of the description is 140 characters.

    Returns

        Represents a StreamMarker
    Return type

        StreamMarker
    Raises

        ValueError – The maximum length of the description is 140 characters.

## send_message

`async send_message(*, sender: str | int | PartialUser, message: str, token_for: str | PartialUser | None = None, reply_to_message_id: str | None = None) → SentMessage`

    This function is a coroutine.

    Send a message to the broadcaster’s chat room.

    Important

    Requires an app access token or user access token that includes the user:write:chat scope. User access token is generally recommended.

    If app access token used, then additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status. This means creating a user token for the “bot” account with the above scopes associated to the correct Client ID. This token does not need to be used.

    Tip

    Chat messages can also include emoticons. To include emoticons, use the name of the emote.

    The names are case sensitive. Don’t include colons around the name e.g., :bleedPurple:

    If Twitch recognises the name, Twitch converts the name to the emote before writing the chat message to the chat room.

    Parameters

            sender (str | int | PartialUser) – The ID, or PartialUser, of the user sending the message. This ID must match the user ID in the user access token.

            message (str) – The message to send. The message is limited to a maximum of 500 characters. Chat messages can also include emoticons. To include emoticons, use the name of the emote. The names are case sensitive. Don’t include colons around the name e.g., :bleedPurple:. If Twitch recognises the name, Twitch converts the name to the emote before writing the chat message to the chat room

            token_for (str | PartialUser | None) – User access token that includes the user:write:chat scope. You can use an app access token which additionally requires user:bot scope from chatting user, and either channel:bot scope from broadcaster or moderator status.

            reply_to_message_id (str | None) – The ID of the chat message being replied to.

    Returns

        An object containing the response from Twitch regarding the sent message.
    Return type

        SentMessage
            `class twitchio.SentMessage(data: SendChatMessageResponseData)`
            Represents the settings of a broadcaster’s chat settings.
            id (str)
                The ID for the message that was sent.
            sent (bool)
                Whether the message passed all checks and was sent.
            dropped_code (str | None)
                Code for why the message was dropped.
            dropped_message (str | None)
                Message for why the message was dropped.

    Raises

        ValueError – The message is limited to a maximum of 500 characters.

## update_chat_settings

`async update_chat_settings(moderator: str | int | PartialUser, emote_mode: bool | None = None, follower_mode: bool | None = None, follower_mode_duration: int | None = None, slow_mode: bool | None = None, slow_mode_wait_time: int | None = None, subscriber_mode: bool | None = None, unique_chat_mode: bool | None = None, non_moderator_chat_delay: bool | None = None, non_moderator_chat_delay_duration: Literal[2, 4, 6] | None = None) → ChatSettings`

    This function is a coroutine.

    Update the user’s chat settings.

    Note

        To set the slow_mode_wait_time or follower_mode_duration field to its default value, set the corresponding slow_mode or follower_mode field to True (and don’t include the slow_mode_wait_time or follower_mode_duration field).

        To set the slow_mode_wait_time, follower_mode_duration, or non_moderator_chat_delay_duration field’s value, you must set the corresponding slow_mode, follower_mode, or non_moderator_chat_delay field to True.

        To remove the slow_mode_wait_time, follower_mode_duration, or non_moderator_chat_delay_duration field’s value, set the corresponding slow_mode, follower_mode, or non_moderator_chat_delay field to False (and don’t include the slow_mode_wait_time, follower_mode_duration, or non_moderator_chat_delay_duration field).

    Note

    Requires a user access token that includes the moderator:manage:chat_settings scope.

    Parameters

            moderator (str | int | PartialUser) – The ID, or PartialUser, of a user that has permission to moderate the broadcaster’s chat room, or the broadcaster’s ID if they’re making the update. This ID must match the user ID in the user access token.

            emote_mode (bool | None) – A Boolean value that determines whether chat messages must contain only emotes.

            follower_mode (bool | None) – A Boolean value that determines whether the broadcaster restricts the chat room to followers only.

            follower_mode_duration (int | None) – The length of time, in minutes, that users must follow the broadcaster before being able to participate in the chat room. Set only if follower_mode is True. Possible values are: 0 (no restriction) through 129600 (3 months).

            slow_mode (bool | None) – A Boolean value that determines whether the broadcaster limits how often users in the chat room are allowed to send messages. Set to True if the broadcaster applies a wait period between messages; otherwise, False.

            slow_mode_wait_time (int | None) – The amount of time, in seconds, that users must wait between sending messages. Set only if slow_mode is True. Possible values are: 3 (3 second delay) through 120 (2 minute delay). The default is 30 seconds.

            subscriber_mode (bool | None) – A Boolean value that determines whether only users that subscribe to the broadcaster’s channel may talk in the chat room. Set to True if the broadcaster restricts the chat room to subscribers only; otherwise, False.

            unique_chat_mode (bool | None) – A Boolean value that determines whether the broadcaster requires users to post only unique messages in the chat room. Set to True if the broadcaster allows only unique messages; otherwise, False.

            non_moderator_chat_delay (bool | None) – A Boolean value that determines whether the broadcaster adds a short delay before chat messages appear in the chat room. This gives chat moderators and bots a chance to remove them before viewers can see the message. Set to True if the broadcaster applies a delay; otherwise, False.

            non_moderator_chat_delay_duration (Literal[2, 4, 6] | None) – The amount of time, in seconds, that messages are delayed before appearing in chat. Set only if non_moderator_chat_delay is True. Possible values in seconds: 2 (recommended), 4 and 6.

    Returns

        The newly applied chat settings.
    Return type

        ChatSettings
    Raises

            ValueError – follower_mode_duration must be below 129600

            ValueError – slow_mode_wait_time must be between 3 and 120

## update_shield_mode_status

`async update_shield_mode_status(*, moderator: str | int | PartialUser, active: bool) → ShieldModeStatus`

    This function is a coroutine.

    Activates or deactivates the broadcaster’s Shield Mode.

    Note

    Requires a user access token that includes the moderator:manage:shield_mode scope.

    Parameters

            moderator (str | int | PartialUser) – The ID, or PartialUser, of the broadcaster or a user that is one of the broadcaster’s moderators. This ID must match the user ID in the access token.

            active (bool) – A Boolean value that determines whether to activate Shield Mode. Set to True to activate Shield Mode; otherwise, False to deactivate Shield Mode.
