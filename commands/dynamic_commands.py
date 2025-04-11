from typing import Dict, Any, List, Optional
from datetime import datetime

from commands.base import BaseCommand
from db.database import db


class DynamicCommand(BaseCommand):
    def __init__(self, name: str, response: str, permission: str = "viewer", aliases: Optional[List[str]] = None):
        self.name = name
        self.description = f"Custom command: {name}"
        self.permission = permission
        self.aliases = aliases or []
        self.response_template = response
        self.cooldown = 3  # Default cooldown in seconds
        self.action_sequence_id = None
        self.restricted_to_user_id = None
        super().__init__()

        self.__name__ = f"DynamicCommand_{name}"

    def handle(self, data: Dict[str, Any]) -> None:
        user = data.get("user", {})
        channel = data.get("channel")
        args = data.get("args", "")

        response = self.response_template
        response = response.replace("{user}", user.get("name", "User"))
        response = response.replace("{args}", args)

        self.send_message(channel, response)

        # Trigger any associated action sequence
        if self.action_sequence_id:
            self._trigger_action_sequence(self.action_sequence_id, data)

        try:
            db.execute(
                "UPDATE commands SET total_uses = total_uses + 1 WHERE name = ?", (self.name,))
        except Exception as e:
            self.logger.error(
                f"Error updating usage count for {self.name}: {e}")
