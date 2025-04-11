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
    skip_files = {"__init__.py", "base.py",
                  "registry.py", "dynamic_commands.py"}

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


def load_dynamic_commands():
    from db.database import db
    from commands.dynamic_commands import DynamicCommand

    try:
        rows = db.fetchall("SELECT * FROM commands WHERE response IS NOT NULL")

        for row in rows:
            try:
                if not row or 'name' not in row:
                    continue

                name = row['name']
                response = row['response'] if row['response'] else ""

                aliases = []
                if row.get('alias_1'):
                    aliases.append(row['alias_1'])
                if row.get('alias_2'):
                    aliases.append(row['alias_2'])

                # Create the dynamic command directly as an instance
                dynamic_cmd = DynamicCommand(
                    name=name,
                    response=response,
                    permission=row.get('permission_level', 'viewer'),
                    aliases=aliases
                )

                # Set additional properties
                dynamic_cmd.cooldown = row.get('cooldown_seconds', 3)
                dynamic_cmd.action_sequence_id = row.get('action_sequence_id')
                dynamic_cmd.restricted_to_user_id = row.get(
                    'restricted_to_user_id')

                logger.debug(f"Created dynamic command: {dynamic_cmd.name}")
                command_registry.register_command(dynamic_cmd)

            except Exception as e:
                logger.error(
                    f"Error loading dynamic command {row.get('name', 'unknown')}: {e}")

    except Exception as e:
        logger.error(f"Error loading dynamic commands: {e}")

    except Exception as e:
        logger.error(f"Error loading dynamic commands: {e}")


# Discover static commands
discover_commands()
# Load dynamic commands
load_dynamic_commands()
