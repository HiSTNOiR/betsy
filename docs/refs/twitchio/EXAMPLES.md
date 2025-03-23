# EXAMPLES

## Decorators

### Add Command

```py
# When added to a Bot or used in a component you can invoke this command with your prefix, E.g:
# !hi or !howdy

@commands.command(name="hi", aliases=["hello", "howdy"])
async def hi_command(ctx: commands.Context) -> None:
    ...
```

TODO: I'd like to make this hook into the DB, where all !commands are stored, allowing mods to add commands via Twitch chat or wherever.

-   something like `@commands.command(name=name, aliases=[alias1, alias2])`

### Command Groups

```py
# When added to a Bot or used in a component you can invoke this group and sub-commands with your prefix, E.g:
# !socials
# !socials discord OR !socials twitch
# When invoke_fallback is True, the parent command will be invoked if a sub-command cannot be found...

@commands.group(name="socials", invoke_fallback=True)
async def socials_group(ctx: commands.Context) -> None:
    await ctx.send("https://discord.gg/RAKc3HF, https://twitch.tv/chillymosh, ...")

@socials_group.command(name="discord", aliases=["disco"])
async def socials_discord(ctx: commands.Context) -> None:
    await ctx.send("https://discord.gg/RAKc3HF")

@socials_group.command(name="twitch")
async def socials_twitch(ctx: commands.Context) -> None:
    await ctx.send("https://twitch.tv/chillymosh")
```

### Cooldowns

```py
# Using the default Cooldown to allow the command to be run twice by an individual chatter, every 10 seconds.

@commands.command()
@commands.cooldown(rate=2, per=10, key=commands.BucketType.chatter)
async def hello(ctx: commands.Context) -> None:
    ...
```

```py
# Using a custom key to bypass cooldowns for certain users.

def bypass_cool(ctx: commands.Context) -> typing.Hashable | None:
    # Returning None will bypass the cooldown

    if ctx.chatter.name.startswith("cool"):
        return None

    # For everyone else, return and call the default chatter strategy
    # This strategy returns a tuple of (channel/broadcaster.id, chatter.id) to use as the unique key
    return commands.BucketType.chatter(ctx)

@commands.command()
@commands.cooldown(rate=2, per=10, key=bypass_cool)
async def hello(ctx: commands.Context) -> None:
    ...
```

```py
# Using a custom function to implement dynamic keys.

async def custom_key(ctx: commands.Context) -> typing.Hashable | None:
    # As an example, get some user info from a database with the chatter...
    # This is just to showcase a use for an async version of a custom key...
    ...

    # Example column in database...
    if row["should_bypass_cooldown"]:
        return None

    # Note: Returning chatter.id is equivalent to commands.BucketType.user NOT commands.BucketType.chatter
    # which uses the channel ID and User ID together as the key...
    return ctx.chatter.id

@commands.command()
@commands.cooldown(rate=1, per=300, key=custom_key)
async def hello(ctx: commands.Context) -> None:
    ...
```

---

## Guards

### Command Guard

```py
def is_cool():
    def predicate(ctx: commands.Context) -> bool:
        return ctx.chatter.name.startswith("cool")

    return commands.guard(predicate)

@is_cool()
@commands.command()
async def cool(self, ctx: commands.Context) -> None:
    await ctx.reply("You are cool...!")
```

```py
# This command can be run by anyone with broadcaster, moderator OR VIP status...
# Other guards are: is_staff(), is_broadcaster(), is_moderator(), is_vip()

@commands.is_elevated()
@commands.command()
async def test(self, ctx: commands.Context) -> None:
    await ctx.reply("You are allowed to use this command!")
```
