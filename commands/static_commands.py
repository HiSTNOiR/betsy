"""
Commands not in the database
"""

from typing import Dict, Any
from datetime import datetime

from commands.base import BaseCommand
from db.database import db
from commands.dynamic_commands import DynamicCommand


# ! delete meh ================================================================
# TODO ^
class ImpossibleCommand(BaseCommand):
    name = "leet"
    description = "Responds in kind"
    permission = "broadcaster"
    aliases = ["elite", "l33t"]

    def handle(self, data: Dict[str, Any]) -> None:
        user = data.get("user", {})
        channel = data.get("channel")

        self.send_message(
            channel, f"@{user.get('name', 'User')}, you're worthy.")
# ! delete meh ================================================================


class CommandsCommand(BaseCommand):
    name = "commands"
    description = "Shows available commands"
    permission = "viewer"

    def handle(self, data: Dict[str, Any]) -> None:
        from commands.registry import command_registry
        from utils.user_permissions import has_permission

        user = data.get("user", {})
        channel = data.get("channel")

        available_commands = []
        for cmd_name, cmd in command_registry.get_all_commands().items():
            if has_permission(user, cmd.permission):
                available_commands.append(cmd_name)

        available_commands.sort()
        commands_str = ", ".join([f"!{cmd}" for cmd in available_commands])

        message = f"@{user.get('name', 'User')}, available commands: {commands_str}"
        self.send_message(channel, message)


class QuitCommand(BaseCommand):
    name = "quit"
    description = "Shuts down the bot"
    permission = "broadcaster"

    def handle(self, data: Dict[str, Any]) -> None:
        channel = data.get("channel")
        self.send_message(channel, "Shutting down ...ᶠᵘᶜᵏ ʸᵒᵘ ᵛᵉʳʸ ᵐᵘᶜʰ")
        self.event_bus.publish("bot_shutdown")

# TODO add commands: !points !hug !gamble !com+ !com- !com~
