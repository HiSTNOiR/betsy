"""
Commands stored in the database
"""

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

        try:
            db.execute(
                "UPDATE commands SET total_uses = total_uses + 1 WHERE name = ?", (self.name,))
        except Exception as e:
            self.logger.error(
                f"Error updating usage count for {self.name}: {e}")

    def update_response(self, new_response: str) -> None:
        self.response_template = new_response

    def update_permission(self, new_permission: str) -> None:
        self.permission = new_permission
