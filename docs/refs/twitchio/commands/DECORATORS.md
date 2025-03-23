# DECORATORS

## commands.command

`@ twitchio.ext.commands.command(name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None, **kwargs: Any) → Any`

    This function is a decorator.

    A decorator which turns a coroutine into a Command which can be used in Component’s or added to a Bot.

    Commands are powerful tools which enable bots to process messages and convert the content into mangeable arguments and Context which is parsed to the wrapped callback coroutine.

    Commands also benefit to such things as guard()’s and the before and after hooks on both, Component and Bot.

    Command callbacks should take in at minimum one parameter, which is Context and is always passed.

    Parameters

            name (str | None) – An optional custom name to use for this command. If this is None or not passed, the coroutine function name will be used instead.

            aliases (list[str] | None) – An optional list of aliases to use for this command.

            extras (dict) – A dict of any data which is stored on this command object. Can be used anywhere you have access to the command object, E.g. in a before or after hook.

            guards_after_parsing (bool) – An optional bool, indicating whether to run guards after argument parsing has completed. Defaults to False, which means guards will be checked before command arguments are parsed and available.

            cooldowns_before_guards (bool) – An optional bool, indicating whether to run cooldown guards after all other guards succeed. Defaults to False, which means cooldowns will be checked after all guards have successfully completed.

            bypass_global_guards (bool) – An optional bool, indicating whether the command should bypass the Bot.global_guard(). Defaults to False.

    Raises

            ValueError – The callback being wrapped is already a command.

            TypeError – The callback must be a coroutine function.

## commands.group

`@ twitchio.ext.commands.group(name: str | None = None, aliases: list[str] | None = None, extras: dict[Any, Any] | None = None, **kwargs: Any) → Any`

    This function is a decorator.

    A decorator which turns a coroutine into a Group which can be used in Component’s or added to a Bot.

    Group commands act as parents to other commands (sub-commands).

    See: command() for more information on commands.

    Group commands are a powerful way of grouping similar sub-commands into a more user friendly interface.

    Group callbacks should take in at minimum one parameter, which is Context and is always passed.

    Parameters

            name (str | None) – An optional custom name to use for this group. If this is None or not passed, the coroutine function name will be used instead.

            aliases (list[str] | None) – An optional list of aliases to use for this group.

            extras (dict) – A dict of any data which is stored on this command object. Can be used anywhere you have access to the command object, E.g. in a before or after hook.

            invoke_fallback (bool) – An optional bool which tells the parent to be invoked as a fallback when no sub-command can be found. Defaults to False.

            apply_cooldowns (bool) – An optional bool indicating whether the cooldowns on this group are checked before invoking any sub commands. Defaults to True.

            apply_guards (bool) – An optional bool indicating whether the guards on this group should be ran before invoking any sub commands. Defaults to True.

## commands.cooldown

`@ twitchio.ext.commands.cooldown(*, base: BaseCooldown, rate: int, per: float, key: Callable[[Any], Hashable] | Callable[[Any], Coroutine[Any, Any, Hashable]] | BucketType, **kwargs: Any)`

    This function is a decorator.

    A decorator which adds a Cooldown to a Command.

    The parameters of this decorator may change depending on the class passed to the base parameter. The parameters needed for the default built-in classes are listed instead.

    When a command is on cooldown or ratelimited, the CommandOnCooldown exception is raised and propagated to all error handlers.

    Parameters

            base (BaseCooldown) –

            Optional base class to use to construct the cooldown. By default this is the Cooldown class, which implements a Token Bucket Algorithm. Another option is the GCRACooldown class which implements the Generic Cell Rate Algorithm, which can be thought of as similar to a continuous state leaky-bucket algorithm, but instead of updating internal state, calculates a Theoretical Arrival Time (TAT), making it more performant, and dissallowing short bursts of requests. However before choosing a class, consider reading more information on the differences between the Token Bucket and GCRA.

            A custom class which inherits from BaseCooldown could also be used. All keyword-arguments passed to this decorator, minus base and key will also be passed to the constructor of the cooldown base class.

            Useful if you would like to implement your own ratelimiting algorithm.

            key (Callable[[Any], Hashable] | Callable[[Any], Coroutine[Any, Any, Hashable]] | BucketType) –

            A regular or coroutine function, or BucketType which must return a typing.Hashable used to determine the keys for the cooldown.

            The BucketType implements some default strategies. If your function returns None the cooldown will be bypassed. See below for some examples. By default the key is chatter.

            rate (int) – An int indicating how many times a command should be allowed per x amount of time. Note the relevance and effects of both rate and per change slightly between algorithms.

            per (float | datetime.timedelta) –

            A float or datetime.timedelta indicating the length of the time (as seconds) a cooldown window is open.

            E.g. if rate is 2 and per is 60.0, using the default Cooldown class, you will only be able to send two commands per 60 seconds, with the window starting when you send the first command.
