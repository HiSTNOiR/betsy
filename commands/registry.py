import os
import importlib
import inspect
from typing import Dict, List, Type, Any

from commands.base import BaseCommand
from core.logging import get_logger
from event_bus.bus import event_bus

logger = get_logger("command_registry")


class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, BaseCommand] = {}
        self.command_aliases: Dict[str, str] = {}

    def register_command(self, command_class_or_instance):
        try:
            # If it's a class, instantiate it
            if isinstance(command_class_or_instance, type):
                command_instance = command_class_or_instance()
            else:
                command_instance = command_class_or_instance

            name = command_instance.name.lower()

            if not name:
                logger.warning(
                    f"Command {command_class_or_instance.__class__.__name__} has no name specified, skipping")
                return

            self.commands[name] = command_instance
            logger.info(f"Registered command: {name}")

            # Register aliases
            for alias in command_instance.aliases:
                alias = alias.lower()
                if alias in self.command_aliases or alias in self.commands:
                    logger.warning(
                        f"Command alias '{alias}' conflicts with existing command, skipping")
                    continue
                self.command_aliases[alias] = name
                logger.info(
                    f"Registered alias '{alias}' for command '{name}'")
        except Exception as e:
            logger.error(
                f"Error registering command {command_class_or_instance}: {e}")
            import traceback
            traceback.print_exc()

    def get_command(self, name: str) -> BaseCommand:
        name = name.lower()
        if name in self.command_aliases:
            name = self.command_aliases[name]
        return self.commands.get(name)

    def has_command(self, name: str) -> bool:
        name = name.lower()
        return name in self.commands or name in self.command_aliases

    def get_all_commands(self) -> Dict[str, BaseCommand]:
        return self.commands.copy()

    def handle_command(self, data: Dict[str, Any]) -> None:
        command_name = data.get("command", "").lower()
        if not command_name:
            return

        command = self.get_command(command_name)
        if not command:
            return

        command.execute(data)


# Create singleton instance
command_registry = CommandRegistry()
