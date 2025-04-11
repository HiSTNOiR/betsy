from typing import Dict, Any, Optional, Tuple, List
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
                    channel, f"@{user.get('name', 'User')}, pfft! You can't do THAT!")
                return

            self.handle(data)
        except Exception as e:
            handle_error(e, {"command": self.name, "data": data})

    def handle(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError("Command must implement handle method")

    def check_permission(self, user: Dict[str, Any]) -> bool:
        if hasattr(self, 'restricted_to_user_id') and self.restricted_to_user_id:
            if user.get('id') != self.restricted_to_user_id:
                return False

        from utils.user_permissions import has_permission
        return has_permission(user, self.permission)

    def send_message(self, channel: str, content: str) -> None:
        self.event_bus.publish("send_twitch_message", {
            "channel": channel,
            "content": content
        })

    def extract_common_data(self, data: Dict[str, Any]) -> Tuple[Dict, str, str]:
        user = data.get("user", {})
        channel = data.get("channel")
        args = data.get("args", "").strip()
        return user, channel, args

    def check_command_exists(self, cmd_name: str, require_both=False) -> Tuple[bool, Optional[Dict]]:
        from commands.registry import command_registry
        from db.database import db

        cmd_exists_in_registry = command_registry.has_command(cmd_name)
        db_command = db.fetchone(
            "SELECT * FROM commands WHERE name = ?", (cmd_name,))

        if require_both:
            return cmd_exists_in_registry and db_command is not None, db_command
        else:
            return cmd_exists_in_registry or db_command is not None, db_command

    def check_command_alias(self, cmd_name: str) -> Tuple[bool, Optional[str]]:
        from commands.registry import command_registry

        if cmd_name in command_registry.command_aliases:
            original_cmd = command_registry.command_aliases[cmd_name]
            return True, original_cmd
        return False, None

    def send_error_response(self, channel: str, user: Dict[str, Any], message: str) -> None:
        self.send_message(channel, f"@{user.get('name', 'User')}, {message}")
