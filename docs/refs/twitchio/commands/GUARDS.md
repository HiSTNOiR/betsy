# COMMANDS.GUARDS

`twitchio.ext.commands.guard(predicate: collections.abc.Callable[[...], bool] | collections.abc.Callable[[...], collections.abc.Coroutine[Any, Any, bool]]) → Any`

    A function which takes in a predicate as a either a standard function or coroutine function which should return either True or False, and adds it to your Command as a guard.

    The predicate function should take in one parameter, commands.Context, the context used in command invocation.

    If the predicate function returns False, the chatter will not be able to invoke the command and an error will be raised. If the predicate function returns True the chatter will be able to invoke the command, assuming all the other guards also pass their predicate checks.

    Guards can also raise custom exceptions, however your exception should inherit from GuardFailure which will allow your exception to propagate successfully to error handlers.

    Any number of guards can be used on a Command and all must pass for the command to be successfully invoked.

    All guards are executed in the specific order displayed below:

        Global Guard: commands.Bot.global_guard()

        Component Guards: commands.Component.guard()

        Command Specific Guards: The command specific guards, E.g. by using this or other guard decorators on a command.

    Note

    Guards are checked and ran after all command arguments have been parsed and converted, but before any before_invoke hooks are ran.

    It is easy to create simple decorator guards for your commands, see the examples below.

    Some built-in helper guards have been premade, and are listed below:

        is_staff()

        is_broadcaster()

        is_moderator()

        is_vip()

        is_elevated() <-- broadcaster, moderator OR vip status>

    Raises

        GuardFailure – The guard predicate returned False and prevented the chatter from using the command.
