# REMOVE

-   [remove_moderator](#remove_moderator)
-   [remove_vip](#remove_vip)

## remove_moderator

`async remove_moderator(user: str | int | twitchio.user.PartialUser) → None`

    This function is a coroutine.

    Removes a moderator to the broadcaster’s chat room.

    The broadcaster may remove a maximum of 10 moderators within a 10-second window.

    Note

    Requires a user access token that includes the channel:manage:moderators scope. The user ID in the access token must match the broadcaster’s ID.

    Parameters

        user (str | int | PartialUser) – The ID of the user to remove as a moderator in the broadcaster’s chat room.

## remove_vip

`async remove_vip(user: str | int | twitchio.user.PartialUser) → None`

    This function is a coroutine.

    Removes a VIP to the broadcaster’s chat room.

    The broadcaster may remove a maximum of 10 VIPs within a 10-second window.

    Note

    Requires a user access token that includes the channel:manage:vips scope. The user ID in the access token must match the broadcaster’s ID.

    Parameters

        user (str | int | PartialUser) – The ID, or PartialUser, of the user to remove as a VIP in the broadcaster’s chat room.
