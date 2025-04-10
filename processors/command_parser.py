from typing import Dict, Any, Optional

from utils.user_service import enrich_user_data
from core.errors import handle_error
from commands.registry import command_registry
from processors.base import BaseProcessor


class CommandParser(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.prefix = "!"

    def set_prefix(self, prefix):
        self.prefix = prefix

    def parse_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            content = message_data.get("content", "")

            # Check if the message starts with the command prefix
            if not content or not content.startswith(self.prefix):
                return None

            # Split into command and arguments
            parts = content[len(self.prefix):].strip().split(" ", 1)
            command_name = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Check if the command exists
            if not command_registry.has_command(command_name):
                return None

            # Return the command data
            return {
                "command": command_name,
                "args": args,
                "user": message_data.get("author", {}),
                "channel": message_data.get("channel"),
                "message_id": message_data.get("id"),
                "raw_message": message_data
            }
        except Exception as e:
            handle_error(e, {"message_data": message_data})
            return None

    def _validate(self, data: Dict[str, Any]) -> None:
        if not data:
            raise ValueError("Command data cannot be None or empty")
        if "command" not in data:
            raise ValueError(
                "Missing required 'command' field in command data")

    def _process(self, command_data: Dict[str, Any]) -> None:
        # Ensure user data is enriched with stuff from db (like the bot_admin rank)
        if "user" in command_data:
            command_data["user"] = enrich_user_data(command_data["user"])

        command_registry.handle_command(command_data)

    # Public method that leverages the base class processing
    def process_command(self, command_data: Dict[str, Any]) -> None:
        self.process(command_data)


# Singleton instance
command_parser = CommandParser()
