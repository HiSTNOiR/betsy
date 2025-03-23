# FETCH

-   [fetch_channel_info](#fetch_channel_info)
-   [fetch_chat_settings](#fetch_chat_settings)
-   [fetch_chatters](#fetch_chatters)
-   [fetch_shield_mode_status](#fetch_shield_mode_status)

## fetch_channel_info

`async fetch_channel_info(*, token_for: str | PartialUser | None = None) → ChannelInfo`

    This function is a coroutine.

    Retrieve channel information for this user.

    Parameters

        token_for (str | PartialUser | None) – An optional user token to use instead of the default app token.
    Returns

        ChannelInfo object representing the channel information.
    Return type

        ChannelInfo
            `class twitchio.ChannelInfo(data: ChannelInformationResponseData, *, http: HTTPClient)`
                Represents a channel’s current information
                user
                    The user whose channel information was requested.
                game_id
                    Current game ID being played on the channel.
                game_name
                    Name of the game being played on the channel.
                title
                    Title of the stream.
                language
                    Language of the channel.
                delay
                    Stream delay in seconds. This defaults to 0 if the broadcaster_id does not match the user access token.
                tags
                    The tags applied to the channel.
                classification_labels
                    The CCLs applied to the channel.
                is_branded_content
                    Boolean flag indicating if the channel has branded content.

## fetch_chat_settings

`async fetch_chat_settings(*, moderator: str | int | PartialUser | None = None, token_for: str | PartialUser | None = None) → ChatSettings`

    This function is a coroutine.

    Fetches the broadcaster’s chat settings.

    Note

    If you wish to view non_moderator_chat_delay and non_moderator_chat_delay_duration then you will need to provide a moderator, which can be either the broadcaster’s or a moderators’. The token must include the moderator:read:chat_settings scope. the toke

    Parameters

            moderator (str | int | PartialUser | None) – The ID, or PartialUser, of the broadcaster or one of the broadcaster’s moderators. This field is only required if you want to include the non_moderator_chat_delay and non_moderator_chat_delay_duration settings in the response. If you specify this field, this ID must match the user ID in the user access token.

            token_for (str | PartialUser | None) – If you need the response to contain non_moderator_chat_delay and non_moderator_chat_delay_duration then you will provide a token for the user in moderator. The required scope is moderator:read:chat_settings. Otherwise it is an optional user token to use instead of the default app token.

    Returns

        ChatSettings object of the broadcaster’s chat settings.
    Return type

        ChatSettings
            `class twitchio.ChatSettings(data: ChatSettingsResponseData, *, http: HTTPClient)`
            Represents the settings of a broadcaster’s chat settings.
            broadcaster
                The PartialUser object of the broadcaster, this will only contain the ID.
            moderator
                The PartialUser object of the moderator, this will only contain the ID.
            slow_mode
                A Boolean value that determines whether the broadcaster limits how often users in the chat room are allowed to send messages.
            slow_mode_wait_time
                The amount of time, in seconds, that users must wait between sending messages. Is None if slow_mode is False.
            follower_mode
                A Boolean value that determines whether the broadcaster restricts the chat room to followers only. Is True if the broadcaster restricts the chat room to followers only; otherwise, False.
            follower_mode_duration
                The length of time, in minutes, that users must follow the broadcaster before being able to participate in the chat room. Is None if follower_mode is False.
            subscriber_mode
                A Boolean value that determines whether only users that subscribe to the broadcaster’s channel may talk in the chat room.
            emote_mode
                A Boolean value that determines whether chat messages must contain only emotes. Is True if chat messages may contain only emotes; otherwise, False.
            unique_chat_mode
                A Boolean value that determines whether the broadcaster requires users to post only unique messages in the chat room. Is True if the broadcaster requires unique messages only; otherwise, False.
            non_moderator_chat_delay
                A Boolean value that determines whether the broadcaster adds a short delay before chat messages appear in the chat room. This gives chat moderators and bots a chance to remove them before viewers can see the message. See the non_moderator_chat_delay_duration field for the length of the delay.
            non_moderator_chat_delay_duration
                The amount of time, in seconds, that messages are delayed before appearing in chat. Is None if non_moderator_chat_delay is False.

## fetch_chatters

`async fetch_chatters(*, moderator: str | int | PartialUser, first: int = 100, max_results: int | None = None) → Chatters`

    This function is a coroutine.

    Fetches users that are connected to the broadcaster’s chat session.

    Note

    Requires user access token that includes the moderator:read:chatters scope.

    Parameters

            moderator (str | int | PartialUser) – The ID, or PartialUser, of the broadcaster or one of the broadcaster’s moderators. This ID must match the user ID in the user access token.

            first (int | None) – The maximum number of items to return per page in the response. The minimum page size is 1 item per page and the maximum is 1,000. The default is 100.

            max_results (int | None) – Maximum number of total results to return. When this is set to None (default), then everything found is returned.

    Returns

        A Chatters object containing the information of a broadcaster’s connected chatters.
    Return type

        Chatters
            `class twitchio.Chatters(iterator: HTTPAsyncIterator[PartialUser], data: ChattersResponse)`
            Represents a channel’s chatters.
            Returns
                users (HTTPAsyncIterator[PartialUser]) – The PartialUser object of the chatter.
                total (int) – The the total number of users that are connected to the chat room. This may vary as you iterate through pages.

## fetch_shield_mode_status

`async fetch_shield_mode_status(*, moderator: str | int | PartialUser) → ShieldModeStatus`

    This function is a coroutine.

    Fetches the broadcaster’s Shield Mode activation status.

    Note

    Requires a user access token that includes the moderator:read:shield_mode or moderator:manage:shield_mode scope.

    Parameters

        moderator (str | int | PartialUser) – The ID, or PartialUser, of the broadcaster or a user that is one of the broadcaster’s moderators. This ID must match the user ID in the access token.
