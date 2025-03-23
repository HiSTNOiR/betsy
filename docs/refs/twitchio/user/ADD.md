# ADD

-   [add_moderator](#add_moderator)
-   [add_vip](#add_vip)

## add_moderator

`async add_moderator(user: str | int | twitchio.user.PartialUser) → None`

    This function is a coroutine.

    Adds a moderator to the broadcaster’s chat room.

    The broadcaster may add a maximum of 10 moderators within a 10-second window.

    Note

    Requires a user access token that includes the channel:manage:moderators scope.

    Parameters

        user (str | int | PartialUser) – The ID of the user to add as a moderator in the broadcaster’s chat room.

## add_vip

`async add_vip(user: str | int | twitchio.user.PartialUser) → None`

    This function is a coroutine.

    Adds a VIP to the broadcaster’s chat room.

    The broadcaster may add a maximum of 10 VIPs within a 10-second window.

    Note

    Requires a user access token that includes the channel:manage:vips scope. The user ID in the access token must match the broadcaster’s ID.

    Parameters

        user (str | int) – The ID, or PartialUser, of the user to add as a VIP in the broadcaster’s chat room.
