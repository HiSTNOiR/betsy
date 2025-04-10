# EXCEPTIONS

## Exception Hierarchy

[CommandError](#commanderror)
┣ ComponentLoadError
┣ CommandInvokeError
┃ ┗ CommandHookError
┣ [CommandNotFound](#commandnotfound)
┣ [CommandExistsError](#commandexistserror)
┣ PrefixError
┣ [InputError](#inputerror)
┃ ┣ ArgumentError
┃ ┃ ┣ ConversionError
┃ ┃ ┃ ┗ BadArgument
┃ ┃ ┣ MissingRequiredArgument
┃ ┃ ┣ UnexpectedQuoteError
┃ ┃ ┣ InvalidEndOfQuotedStringError
┃ ┃ ┗ ExpectedClosingQuoteError
┗ [GuardFailure](#guardfailure)
┃ ┗ [CommandOnCooldown](#commandoncooldown)

ModuleError
┣ ModuleLoadFailure
┣ ModuleAlreadyLoadedError
┣ ModuleNotLoadedError
┗ NoEntryPointError

## CommandError

`exception twitchio.ext.commands.CommandError`

    Base exception for command related errors.

    All commands.ext related exceptions inherit from this class.

## CommandNotFound

`exception twitchio.ext.commands.CommandNotFound`

    Exception raised when a message is processed with a valid prefix and no Command could be found.

## CommandExistsError

`exception twitchio.ext.commands.CommandExistsError`

    Exception raised when you try to add a command or alias to a command that is already registered on the Bot.

## InputError

`exception twitchio.ext.commands.InputError`

    Base exception for errors raised while parsing the input for command invocation. All ArgumentError and child exception inherit from this class.

## GuardFailure

`exception twitchio.ext.commands.GuardFailure(msg: str | None = None, *, guard: Any | None = None)`

    Exception raised when a guard() fails or blocks a command from executing.

    This exception should be subclassed when raising a custom exception for a guard().

## CommandOnCooldown

`exception twitchio.ext.commands.CommandOnCooldown(msg: str | None = None, *, cooldown: BaseCooldown, remaining: float)`

    Exception raised when a command is invoked while on cooldown/ratelimited.

    cooldown

        The specific cooldown instance used that raised this error.

        Type

            BaseCooldown

    remaining

        The time remaining for the cooldown as a float of seconds.

        Type

            float
