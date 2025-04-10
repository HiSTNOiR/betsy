# USER

-   [timeout_user](#timeout_user)
-   [unban_user](#unban_user)
-   [user](#user)

## timeout_user

`async timeout_user(*, moderator: str | int | PartialUser | None, user: str | PartialUser | None, duration: int, reason: str | None = None) → Timeout`

    This function is a coroutine.

    Timeout the provided user from the channel tied with this PartialUser.

    Note

    Requires a user access token that includes the moderator:manage:banned_users scope.

    Parameters

            moderator (str | PartialUser | None) –

            An optional ID of or the PartialUser object of the moderator issuing this action. You must have a token stored with the moderator:manage:banned_users scope for this moderator.

            If None, the ID of this PartialUser will be used.

            user (str | PartialUser) – The ID of, or the PartialUser of the user to ban.

            reason (str | None) – An optional reason this chatter is being banned. If provided the length of the reason must not be more than 500 characters long. Defaults to None.

            duration (int) –

            The duration of the timeout in seconds. The minimum duration is 1 second and the maximum is 1_209_600 seconds (2 weeks).

            To end the chatters timeout early, set this field to 1, or use the unban_user() endpoint.

            The default is 600 which is ten minutes.

    Returns

        The Timeout object.
            `class twitchio.Timeout(data: BanUserResponseData, *, http: HTTPClient)`
            Represents a Timeout.
            broadcaster
                The broadcaster whose chat room the user was timed out from chatting in.
            user
                The user timed out.
            moderator
                The moderator who put the user in timeout.
            end_time
                Datetime of when the timeout will end.
            created_at
                Datetime of when the user was timed out.

## unban_user

`async unban_user(*, moderator: str | int | twitchio.user.PartialUser, user_id: str | int | twitchio.user.PartialUser) → None`

    This function is a coroutine.

    Unban a user from the broadcaster’s channel.

    Note

    Requires a user access token that includes the moderator:manage:banned_users scope.

    Parameters

            moderator (str | int | PartialUser) – The ID of the broadcaster or a user that has permission to moderate the broadcaster’s chat room. This ID must match the user ID in the user access token.

            user_id (str | int | PartialUser) – The ID, or PartialUser, of the user to ban or put in a timeout.

## user

``
async user() → User

    This function is a coroutine.

    Fetch the full User information for the PartialUser.

    Returns

        User object.
    Return type

        User
            `class twitchio.User(data: UsersResponseData, *, http: HTTPClient)`
            Represents a User.
            This class inherits from PartialUser and contains additional information about the user.
            id (str)
                The user’s ID.
            name (str | None)
                The user’s name. In most cases, this is provided. There are however, rare cases where it is not.
            display_name (str)
                The display name of the user.
            type (Literal[“admin”, “global_mod”, “staff”, “”])
                The type of the user. Possible values are:
                    admin - Twitch administrator
                    global_mod
                    staff - Twitch staff
                    empty string - Normal user
            broadcaster_type (Literal[“affiliate”, “partner”, “”])
                The broadcaster type of the user. Possible values are:
                    affiliate
                    partner
                    empty string - Normal user
            description (str)
                Description of the user.
            profile_image (Asset)
                Profile image as an asset.
            offline_image (Asset | None)
                Offline image as an asset, otherwise None if broadcaster as not set one.
            email (str | None)
                The user’s verified email address. The object includes this field only if the user access token includes the user:read:email scope.
            created_at (datetime.datetime)
                When the user was created.
