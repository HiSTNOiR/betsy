from typing import Dict, Any, Set

from core.logging import get_logger

logger = get_logger("user_permissions")


def get_user_permissions(user_data: Dict[str, Any]) -> Set[str]:
    permissions = set()

    if not user_data:
        return permissions

    badges = user_data.get("badges", {})

    # Check for bot_admin (will be stored in DB rather than badges)
    if user_data.get("is_bot_admin", False):
        permissions.add("bot_admin")

    if badges:
        if "broadcaster" in badges:
            permissions.add("broadcaster")
        if "moderator" in badges:
            permissions.add("moderator")
        if "vip" in badges:
            permissions.add("vip")
        if "subscriber" in badges:
            permissions.add("subscriber")

    if not permissions:
        permissions.add("viewer")

    return permissions


def get_highest_permission_level(user_data: Dict[str, Any]) -> str:
    if not user_data:
        return "viewer"

    # Check for bot_admin first (highest permission)
    if user_data.get("is_bot_admin", False):
        return "bot_admin"

    badges = user_data.get("badges", {})

    if badges:
        if "broadcaster" in badges:
            return "broadcaster"
        elif "moderator" in badges:
            return "moderator"
        elif "vip" in badges:
            return "vip"
        elif "subscriber" in badges:
            return "subscriber"

    return "viewer"


def has_permission(user_data: Dict[str, Any], required_permission: str) -> bool:
    permissions = get_user_permissions(user_data)

    if required_permission == "viewer":
        return True
    elif required_permission == "subscriber" and any(p in permissions for p in ["subscriber", "moderator", "broadcaster", "bot_admin"]):
        return True
    elif required_permission == "vip" and any(p in permissions for p in ["vip", "moderator", "broadcaster", "bot_admin"]):
        return True
    elif required_permission == "moderator" and any(p in permissions for p in ["moderator", "broadcaster", "bot_admin"]):
        return True
    elif required_permission == "broadcaster" and any(p in permissions for p in ["broadcaster", "bot_admin"]):
        return True
    elif required_permission == "bot_admin" and "bot_admin" in permissions:
        return True

    return False
