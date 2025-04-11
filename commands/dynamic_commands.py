from typing import Dict, Any, List, Optional
from datetime import datetime

from commands.base import BaseCommand
from db.database import db


class DynamicCommand(BaseCommand):
    def __init__(self, name=None, response="", permission="viewer", aliases=None):
        super().__init__()

        self.name = name or ""
        self.description = f"Custom command: {self.name}"
        self.permission = permission
        self.aliases = aliases or []
        self.response_template = response
        self.cooldown = 3
        self.action_sequence_id = None
        self.restricted_to_user_id = None

        self.__name__ = f"DynamicCommand_{self.name}"

    def handle(self, data: Dict[str, Any]) -> None:
        if not self.name:
            self.logger.warning(
                "Attempted to use a dynamic command with no name")
            return

        user = data.get("user", {})
        channel = data.get("channel")
        args = data.get("args", "")

        response = self.response_template
        response = response.replace("{user}", user.get("name", "User"))
        # TODO for !hug, this needs to check if the user is in chatters
        response = response.replace("{args}", args)

        self.send_message(channel, response)

        if self.action_sequence_id:
            self._trigger_action_sequence(self.action_sequence_id, data)

        try:
            db.execute(
                "UPDATE commands SET total_uses = total_uses + 1 WHERE name = ?", (self.name,))
        except Exception as e:
            self.logger.error(
                f"Error updating usage count for {self.name}: {e}")
