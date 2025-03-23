# COMMANDS.COOLDOWNS

## commands.BaseCooldown

`class twitchio.ext.commands.BaseCooldown`

    Base class used to implement your own cooldown algorithm for use with cooldown().

    Some built-in cooldown algorithms already exist:

        Cooldown - (Token Bucket Algorithm)

        GCRACooldown - (Generic Cell Rate Algorithm)

    Note

    Every base method must be implemented in this base class.

    abstract reset() → None

        Base method which should be implemented to reset the cooldown.

    abstract update(*args: Any, **kwargs: Any) → float | None

        Base method which should be implemented to update the cooldown/ratelimit.

        This is where your algorithm logic should be contained.

        Important

        This method should always return a float or None. If None is returned by this method, the cooldown will be considered bypassed.

        Returns

                float – The time needed to wait before you are off cooldown.

                None – Bypasses the cooldown.

    abstract copy() → Self

        Base method which should be implemented to return a copy of this class in it’s original state.

    abstract is_ratelimited(*args: Any, **kwargs: Any) → bool

        Base method which should be implemented which returns a bool indicating whether the cooldown is ratelimited.

        Returns

            A bool indicating whether this cooldown is currently ratelimited.
        Return type

            bool

    abstract is_dead(*args: Any, **kwargs: Any) → bool

        Base method which should be implemented to indicate whether the cooldown should be considered stale and allowed to be removed from the bucket: cooldown mapping.

        Returns

            A bool indicating whether this cooldown is stale/old.
        Return type

            bool

## commands.Cooldown

`class twitchio.ext.commands.Cooldown(*, rate: int, per: float | datetime.timedelta)`

    Default cooldown algorithm for cooldown(), which implements a Token Bucket Algorithm.

    See: cooldown() for more documentation.

## commands.BucketType

`class twitchio.ext.commands.BucketType`

    Enum representing default implementations for the key argument in cooldown().

    default

        The cooldown will be considered a global cooldown shared across every channel and user.

    user

        The cooldown will apply per user, accross all channels.

    channel

        The cooldown will apply to every user/chatter in the channel.

    chatter

        The cooldown will apply per user, per channel.
