from typing import Dict, Any, Optional, List
from utils.user_permissions import has_permission
from event_bus.bus import event_bus
from core.logging import get_logger
from core.errors import handle_error

logger = get_logger("commands")


class BaseCommand:
    name = ""
    description = ""
    permission = "viewer"
    aliases: List[str] = []

    def __init__(self):
        self.event_bus = event_bus
        self.logger = get_logger(f"cmd.{self.name}")

    def execute(self, data: Dict[str, Any]) -> None:
        try:
            user = data.get("user", {})
            channel = data.get("channel")

            if not self.check_permission(user):
                self.send_message(
                    channel, f"@{user.get('name', 'User')}, you don't have permission to use this command.")
                return

            self.handle(data)
        except Exception as e:
            handle_error(e, {"command": self.name, "data": data})

    def handle(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("Command must implement handle method")

    def check_permission(self, user: Dict[str, Any]) -> bool:
        from utils.user_permissions import has_permission
        return has_permission(user, self.permission)

    def send_message(self, channel: str, content: str) -> None:
        self.event_bus.publish("send_twitch_message", {
            "channel": channel,
            "content": content
        })
