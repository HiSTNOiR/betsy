"""
Permissions utility functions for the Twitch bot.
"""
import logging
from enum import Enum, auto
from typing import Dict, List, Set, Optional, Any, Union

from bot.core.errors import PermissionError

# Set up logger
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """Enum representing user roles with hierarchical permissions."""
    VIEWER = 0
    SUBSCRIBER = 100
    VIP = 200
    MODERATOR = 300
    BROADCASTER = 400
    BOT_ADMIN = 500

    @classmethod
    def from_string(cls, role_str: str) -> 'UserRole':
        """
        Convert a string to a UserRole enum.
        
        Args:
            role_str: Role string to convert
        
        Returns:
            UserRole enum value
        
        Raises:
            ValueError: If role_str is not a valid role
        """
        role_map = {
            'viewer': cls.VIEWER,
            'subscriber': cls.SUBSCRIBER,
            'vip': cls.VIP,
            'moderator': cls.MODERATOR,
            'broadcaster': cls.BROADCASTER,
            'bot_admin': cls.BOT_ADMIN
        }
        
        role_str = role_str.lower()
        if role_str not in role_map:
            valid_roles = ', '.join(role_map.keys())
            raise ValueError(f"Invalid role: {role_str}. Valid roles are: {valid_roles}")
        
        return role_map[role_str]
    
    def __str__(self) -> str:
        """
        Convert UserRole enum to string.
        
        Returns:
            String representation of role
        """
        return self.name.lower()

class Permission:
    """Class for handling user permissions."""
    
    def __init__(self, min_role: UserRole = UserRole.VIEWER, 
                allowed_users: Optional[Set[str]] = None,
                denied_users: Optional[Set[str]] = None):
        """
        Initialise permission.
        
        Args:
            min_role: Minimum role required (default: VIEWER)
            allowed_users: Set of specifically allowed users (default: None)
            denied_users: Set of specifically denied users (default: None)
        """
        self.min_role = min_role
        self.allowed_users = allowed_users or set()
        self.denied_users = denied_users or set()
    
    def check(self, user_id: str, user_role: Union[UserRole, str]) -> bool:
        """
        Check if a user has permission.
        
        Args:
            user_id: User ID to check
            user_role: User's role
        
        Returns:
            True if user has permission, False otherwise
        """
        # Convert string role to enum if needed
        if isinstance(user_role, str):
            try:
                user_role = UserRole.from_string(user_role)
            except ValueError:
                logger.warning(f"Invalid role string: {user_role}")
                return False
        
        # Check specifically denied users first
        if user_id in self.denied_users:
            return False
        
        # Check specifically allowed users
        if user_id in self.allowed_users:
            return True
        
        # Check role hierarchy
        return user_role.value >= self.min_role.value
    
    def add_allowed_user(self, user_id: str) -> None:
        """
        Add a user to the allowed users set.
        
        Args:
            user_id: User ID to add
        """
        self.allowed_users.add(user_id)
        # Remove from denied users if present
        self.denied_users.discard(user_id)
    
    def add_denied_user(self, user_id: str) -> None:
        """
        Add a user to the denied users set.
        
        Args:
            user_id: User ID to add
        """
        self.denied_users.add(user_id)
        # Remove from allowed users if present
        self.allowed_users.discard(user_id)
    
    def remove_user(self, user_id: str) -> None:
        """
        Remove a user from both allowed and denied sets.
        
        Args:
            user_id: User ID to remove
        """
        self.allowed_users.discard(user_id)
        self.denied_users.discard(user_id)

class PermissionManager:
    """Manager for handling command and feature permissions."""
    
    def __init__(self):
        """Initialise permission manager."""
        self.command_permissions: Dict[str, Permission] = {}
        self.feature_permissions: Dict[str, Permission] = {}
        self.default_command_permission = Permission(UserRole.VIEWER)
        self.default_feature_permission = Permission(UserRole.VIEWER)
        self.broadcaster_id: Optional[str] = None
        self.bot_admin_ids: Set[str] = set()
    
    def set_broadcaster(self, broadcaster_id: str) -> None:
        """
        Set the broadcaster ID.
        
        Args:
            broadcaster_id: Broadcaster's user ID
        """
        self.broadcaster_id = broadcaster_id
        logger.info(f"Broadcaster ID set to {broadcaster_id}")
    
    def add_bot_admin(self, user_id: str) -> None:
        """
        Add a bot admin user ID.
        
        Args:
            user_id: User ID to add as bot admin
        """
        self.bot_admin_ids.add(user_id)
        logger.info(f"Added bot admin: {user_id}")
    
    def set_command_permission(self, command: str, permission: Permission) -> None:
        """
        Set permission for a command.
        
        Args:
            command: Command name
            permission: Permission object
        """
        self.command_permissions[command.lower()] = permission
    
    def set_feature_permission(self, feature: str, permission: Permission) -> None:
        """
        Set permission for a feature.
        
        Args:
            feature: Feature name
            permission: Permission object
        """
        self.feature_permissions[feature.lower()] = permission
    
    def get_effective_role(self, user_id: str, user_badges: Dict[str, str]) -> UserRole:
        """
        Get effective role for a user based on their badges.
        
        Args:
            user_id: User ID
            user_badges: Dictionary of user badges
        
        Returns:
            User's effective role
        """
        # Check if user is bot admin
        if user_id in self.bot_admin_ids:
            return UserRole.BOT_ADMIN
        
        # Check if user is broadcaster
        if user_id == self.broadcaster_id:
            return UserRole.BROADCASTER
        
        # Check badges
        if user_badges:
            if 'moderator' in user_badges:
                return UserRole.MODERATOR
            if 'vip' in user_badges:
                return UserRole.VIP
            if 'subscriber' in user_badges:
                return UserRole.SUBSCRIBER
        
        # Default to viewer
        return UserRole.VIEWER
    
    def check_command_permission(self, command: str, user_id: str, 
                               user_role: Union[UserRole, str]) -> bool:
        """
        Check if a user has permission to use a command.
        
        Args:
            command: Command name
            user_id: User ID
            user_role: User's role
        
        Returns:
            True if user has permission, False otherwise
        """
        # Get permission for command, or use default
        permission = self.command_permissions.get(
            command.lower(), self.default_command_permission
        )
        
        return permission.check(user_id, user_role)
    
    def check_feature_permission(self, feature: str, user_id: str, 
                               user_role: Union[UserRole, str]) -> bool:
        """
        Check if a user has permission to use a feature.
        
        Args:
            feature: Feature name
            user_id: User ID
            user_role: User's role
        
        Returns:
            True if user has permission, False otherwise
        """
        # Get permission for feature, or use default
        permission = self.feature_permissions.get(
            feature.lower(), self.default_feature_permission
        )
        
        return permission.check(user_id, user_role)
    
    def require_command_permission(self, command: str, user_id: str, 
                                 user_role: Union[UserRole, str]) -> None:
        """
        Require permission for a command, raising an error if not allowed.
        
        Args:
            command: Command name
            user_id: User ID
            user_role: User's role
        
        Raises:
            PermissionError: If user doesn't have permission
        """
        if not self.check_command_permission(command, user_id, user_role):
            if isinstance(user_role, UserRole):
                role_str = str(user_role)
            else:
                role_str = user_role
                
            logger.warning(f"Permission denied for user {user_id} ({role_str}) to use command: {command}")
            raise PermissionError(f"You don't have permission to use this command.")
    
    def require_feature_permission(self, feature: str, user_id: str, 
                                 user_role: Union[UserRole, str]) -> None:
        """
        Require permission for a feature, raising an error if not allowed.
        
        Args:
            feature: Feature name
            user_id: User ID
            user_role: User's role
        
        Raises:
            PermissionError: If user doesn't have permission
        """
        if not self.check_feature_permission(feature, user_id, user_role):
            if isinstance(user_role, UserRole):
                role_str = str(user_role)
            else:
                role_str = user_role
                
            logger.warning(f"Permission denied for user {user_id} ({role_str}) to use feature: {feature}")
            raise PermissionError(f"You don't have permission to use this feature.")