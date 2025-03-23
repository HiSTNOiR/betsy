# #!/usr/bin/env python
# """
# Test runner for the Twitch bot.
# """
# import unittest
# import sys
# import os

# # Add parent directory to path to allow imports
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Import test modules
# from tests.test_config import TestConfig
# from tests.test_validation import TestValidation
# from tests.test_formatting import TestFormatting
# from tests.test_parsing import TestParsing
# from tests.test_sanitisation import TestSanitisation
# from tests.test_security import TestSecurity
# from tests.test_time_utils import TestTimeUtils
# from tests.test_random_utils import TestRandomUtils
# from tests.test_permissions import TestUserRole, TestPermission, TestPermissionManager
# from tests.test_throttling import TestPrioritisedItem, TestTokenBucket, TestRateLimiter, TestMessageQueue, TestPerUserRateLimiter, TestCommandThrottler
# from tests.test_cooldown import TestCooldown, TestCooldownManager
# from tests.test_queue import TestPriorityItem, TestPriorityMessageQueue, TestCommandQueue, TestDuelQueue

# def run_tests():
#     """Run all tests."""
#     # Create test suite
#     test_suite = unittest.TestSuite()
    
#     # Add test cases
#     test_suite.addTest(unittest.makeSuite(TestConfig))
#     test_suite.addTest(unittest.makeSuite(TestValidation))
#     test_suite.addTest(unittest.makeSuite(TestFormatting))
#     test_suite.addTest(unittest.makeSuite(TestParsing))
#     test_suite.addTest(unittest.makeSuite(TestSanitisation))
#     test_suite.addTest(unittest.makeSuite(TestSecurity))
#     test_suite.addTest(unittest.makeSuite(TestTimeUtils))
#     test_suite.addTest(unittest.makeSuite(TestRandomUtils))
#     test_suite.addTest(unittest.makeSuite(TestUserRole))
#     test_suite.addTest(unittest.makeSuite(TestPermission))
#     test_suite.addTest(unittest.makeSuite(TestPermissionManager))
#     test_suite.addTest(unittest.makeSuite(TestPrioritisedItem))
#     test_suite.addTest(unittest.makeSuite(TestTokenBucket))
#     test_suite.addTest(unittest.makeSuite(TestRateLimiter))
#     test_suite.addTest(unittest.makeSuite(TestMessageQueue))
#     test_suite.addTest(unittest.makeSuite(TestPerUserRateLimiter))
#     test_suite.addTest(unittest.makeSuite(TestCommandThrottler))
#     test_suite.addTest(unittest.makeSuite(TestCooldown))
#     test_suite.addTest(unittest.makeSuite(TestCooldownManager))
#     test_suite.addTest(unittest.makeSuite(TestPriorityItem))
#     test_suite.addTest(unittest.makeSuite(TestPriorityMessageQueue))
#     test_suite.addTest(unittest.makeSuite(TestCommandQueue))
#     test_suite.addTest(unittest.makeSuite(TestDuelQueue))
    
#     # Run tests
#     test_runner = unittest.TextTestRunner(verbosity=2)
#     result = test_runner.run(test_suite)
    
#     # Return success/failure
#     return result.wasSuccessful()

# if __name__ == '__main__':
#     success = run_tests()
#     sys.exit(0 if success else 1)

#!/usr/bin/env python
"""
Test runner for the Twitch bot.
"""
import unittest
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def run_tests():
    """Run all tests."""
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    test_suite = test_loader.discover(start_dir, pattern="test_*.py")
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)