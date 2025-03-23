"""
Tests for the permissions utility module.
"""
import unittest
from bot.utils.permissions import UserRole, Permission, PermissionManager
from bot.core.errors import PermissionError

class TestUserRole(unittest.TestCase):
    """Tests for the UserRole enum."""
    
    def test_role_hierarchy(self):
        """Test role hierarchy ordering."""
        # Check relative ordering
        self.assertLess(UserRole.VIEWER.value, UserRole.SUBSCRIBER.value)
        self.assertLess(UserRole.SUBSCRIBER.value, UserRole.VIP.value)
        self.assertLess(UserRole.VIP.value, UserRole.MODERATOR.value)
        self.assertLess(UserRole.MODERATOR.value, UserRole.BROADCASTER.value)
        self.assertLess(UserRole.BROADCASTER.value, UserRole.BOT_ADMIN.value)
    
    def test_from_string(self):
        """Test conversion from string to UserRole."""
        # Valid role strings
        self.assertEqual(UserRole.from_string("viewer"), UserRole.VIEWER)
        self.assertEqual(UserRole.from_string("subscriber"), UserRole.SUBSCRIBER)
        self.assertEqual(UserRole.from_string("vip"), UserRole.VIP)
        self.assertEqual(UserRole.from_string("moderator"), UserRole.MODERATOR)
        self.assertEqual(UserRole.from_string("broadcaster"), UserRole.BROADCASTER)
        self.assertEqual(UserRole.from_string("bot_admin"), UserRole.BOT_ADMIN)
        
        # Case insensitive
        self.assertEqual(UserRole.from_string("VIEWER"), UserRole.VIEWER)
        self.assertEqual(UserRole.from_string("Subscriber"), UserRole.SUBSCRIBER)
        
        # Invalid role string
        with self.assertRaises(ValueError):
            UserRole.from_string("invalid_role")
    
    def test_str_conversion(self):
        """Test conversion from UserRole to string."""
        self.assertEqual(str(UserRole.VIEWER), "viewer")
        self.assertEqual(str(UserRole.SUBSCRIBER), "subscriber")
        self.assertEqual(str(UserRole.VIP), "vip")
        self.assertEqual(str(UserRole.MODERATOR), "moderator")
        self.assertEqual(str(UserRole.BROADCASTER), "broadcaster")
        self.assertEqual(str(UserRole.BOT_ADMIN), "bot_admin")

class TestPermission(unittest.TestCase):
    """Tests for the Permission class."""
    
    def test_init(self):
        """Test initialisation."""
        # Default values
        permission = Permission()
        self.assertEqual(permission.min_role, UserRole.VIEWER)
        self.assertEqual(permission.allowed_users, set())
        self.assertEqual(permission.denied_users, set())
        
        # Custom values
        permission = Permission(
            min_role=UserRole.MODERATOR,
            allowed_users={"user1", "user2"},
            denied_users={"user3", "user4"}
        )
        self.assertEqual(permission.min_role, UserRole.MODERATOR)
        self.assertEqual(permission.allowed_users, {"user1", "user2"})
        self.assertEqual(permission.denied_users, {"user3", "user4"})
    
    def test_check_permission(self):
        """Test permission checking."""
        # Setup
        permission = Permission(
            min_role=UserRole.MODERATOR,
            allowed_users={"allowed_viewer"},
            denied_users={"denied_moderator"}
        )
        
        # Specifically allowed users (bypass role check)
        self.assertTrue(permission.check("allowed_viewer", UserRole.VIEWER))
        
        # Specifically denied users (override role check)
        self.assertFalse(permission.check("denied_moderator", UserRole.MODERATOR))
        
        # Role hierarchy
        self.assertFalse(permission.check("regular_viewer", UserRole.VIEWER))
        self.assertFalse(permission.check("subscriber", UserRole.SUBSCRIBER))
        self.assertFalse(permission.check("vip", UserRole.VIP))
        self.assertTrue(permission.check("moderator", UserRole.MODERATOR))
        self.assertTrue(permission.check("broadcaster", UserRole.BROADCASTER))
        self.assertTrue(permission.check("bot_admin", UserRole.BOT_ADMIN))
        
        # String role conversion
        self.assertFalse(permission.check("regular_viewer", "viewer"))
        self.assertTrue(permission.check("moderator", "moderator"))
        
        # Invalid role string
        self.assertFalse(permission.check("user", "invalid_role"))
    
    def test_add_allowed_user(self):
        """Test adding an allowed user."""
        permission = Permission(min_role=UserRole.MODERATOR)
        
        # Add allowed user
        permission.add_allowed_user("viewer")
        self.assertTrue(permission.check("viewer", UserRole.VIEWER))
        
        # Adding an allowed user should remove them from denied users
        permission.add_denied_user("user")
        self.assertFalse(permission.check("user", UserRole.VIEWER))
        permission.add_allowed_user("user")
        self.assertTrue(permission.check("user", UserRole.VIEWER))
        self.assertNotIn("user", permission.denied_users)
    
    def test_add_denied_user(self):
        """Test adding a denied user."""
        permission = Permission(min_role=UserRole.VIEWER)
        
        # Add denied user
        permission.add_denied_user("viewer")
        self.assertFalse(permission.check("viewer", UserRole.VIEWER))
        
        # Adding a denied user should remove them from allowed users
        permission.add_allowed_user("user")
        self.assertTrue(permission.check("user", UserRole.VIEWER))
        permission.add_denied_user("user")
        self.assertFalse(permission.check("user", UserRole.VIEWER))
        self.assertNotIn("user", permission.allowed_users)
    
    def test_remove_user(self):
        """Test removing a user from both allowed and denied sets."""
        permission = Permission(
            min_role=UserRole.MODERATOR,
            allowed_users={"allowed_user"},
            denied_users={"denied_user"}
        )
        
        # Remove allowed user
        permission.remove_user("allowed_user")
        self.assertNotIn("allowed_user", permission.allowed_users)
        
        # Remove denied user
        permission.remove_user("denied_user")
        self.assertNotIn("denied_user", permission.denied_users)
        
        # Remove non-existent user (should not raise an exception)
        permission.remove_user("non_existent_user")

class TestPermissionManager(unittest.TestCase):
    """Tests for the PermissionManager class."""
    
    def setUp(self):
        """Set up for each test."""
        self.manager = PermissionManager()
        self.manager.set_broadcaster("broadcaster_id")
        self.manager.add_bot_admin("bot_admin_id")
    
    def test_get_effective_role(self):
        """Test effective role calculation."""
        # Bot admin
        self.assertEqual(
            self.manager.get_effective_role("bot_admin_id", {}),
            UserRole.BOT_ADMIN
        )
        
        # Broadcaster
        self.assertEqual(
            self.manager.get_effective_role("broadcaster_id", {}),
            UserRole.BROADCASTER
        )
        
        # Moderator
        self.assertEqual(
            self.manager.get_effective_role("moderator_id", {"moderator": "1"}),
            UserRole.MODERATOR
        )
        
        # VIP
        self.assertEqual(
            self.manager.get_effective_role("vip_id", {"vip": "1"}),
            UserRole.VIP
        )
        
        # Subscriber
        self.assertEqual(
            self.manager.get_effective_role("subscriber_id", {"subscriber": "1"}),
            UserRole.SUBSCRIBER
        )
        
        # Viewer
        self.assertEqual(
            self.manager.get_effective_role("viewer_id", {}),
            UserRole.VIEWER
        )
    
    def test_command_permissions(self):
        """Test command permissions."""
        # Set permission for a command
        permission = Permission(min_role=UserRole.MODERATOR)
        self.manager.set_command_permission("test_command", permission)
        
        # Check permission
        self.assertTrue(self.manager.check_command_permission(
            "test_command", "moderator_id", UserRole.MODERATOR
        ))
        self.assertFalse(self.manager.check_command_permission(
            "test_command", "viewer_id", UserRole.VIEWER
        ))
        
        # Default permission (viewer)
        self.assertTrue(self.manager.check_command_permission(
            "unknown_command", "viewer_id", UserRole.VIEWER
        ))
    
    def test_feature_permissions(self):
        """Test feature permissions."""
        # Set permission for a feature
        permission = Permission(min_role=UserRole.SUBSCRIBER)
        self.manager.set_feature_permission("test_feature", permission)
        
        # Check permission
        self.assertTrue(self.manager.check_feature_permission(
            "test_feature", "subscriber_id", UserRole.SUBSCRIBER
        ))
        self.assertFalse(self.manager.check_feature_permission(
            "test_feature", "viewer_id", UserRole.VIEWER
        ))
        
        # Default permission (viewer)
        self.assertTrue(self.manager.check_feature_permission(
            "unknown_feature", "viewer_id", UserRole.VIEWER
        ))
    
    def test_require_command_permission(self):
        """Test requiring command permission."""
        # Set permission for a command
        permission = Permission(min_role=UserRole.MODERATOR)
        self.manager.set_command_permission("test_command", permission)
        
        # Has permission (should not raise an exception)
        self.manager.require_command_permission(
            "test_command", "moderator_id", UserRole.MODERATOR
        )
        
        # Does not have permission (should raise an exception)
        with self.assertRaises(PermissionError):
            self.manager.require_command_permission(
                "test_command", "viewer_id", UserRole.VIEWER
            )
    
    def test_require_feature_permission(self):
        """Test requiring feature permission."""
        # Set permission for a feature
        permission = Permission(min_role=UserRole.SUBSCRIBER)
        self.manager.set_feature_permission("test_feature", permission)
        
        # Has permission (should not raise an exception)
        self.manager.require_feature_permission(
            "test_feature", "subscriber_id", UserRole.SUBSCRIBER
        )
        
        # Does not have permission (should raise an exception)
        with self.assertRaises(PermissionError):
            self.manager.require_feature_permission(
                "test_feature", "viewer_id", UserRole.VIEWER
            )

if __name__ == '__main__':
    unittest.main()