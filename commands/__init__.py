import os
import importlib
import inspect
import sys
from pathlib import Path
from typing import List, Type

from commands.base import BaseCommand
from commands.registry import command_registry
from core.logging import get_logger

logger = get_logger("commands")


def discover_commands() -> None:
    commands_dir = Path(__file__).parent

    # Skip special files
    skip_files = {"__init__.py", "base.py", "registry.py"}

    for entry in commands_dir.iterdir():
        if entry.is_file() and entry.suffix == ".py" and entry.name not in skip_files:
            try:
                module_name = f"commands.{entry.stem}"
                module = importlib.import_module(module_name)

                # Find command classes in the module
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                        command_registry.register_command(obj)
            except Exception as e:
                logger.error(f"Error loading commands from {entry.name}: {e}")


# Auto-discover commands when module is imported
discover_commands()
