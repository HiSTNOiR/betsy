import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from core.errors import (
    BetsyError, ConfigError, ValidationError, 
    handle_error, register_error_callback, ErrorSeverity
)

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.callback_called = False
        self.callback_error = None
        
    def test_basic_error(self):
        error = BetsyError("Test error message")
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.error_code, "E000")
        self.assertEqual(error.severity, ErrorSeverity.ERROR)
        
    def test_config_error(self):
        error = ConfigError("Missing configuration", {"key": "TEST_KEY"})
        self.assertEqual(error.message, "Missing configuration")
        self.assertEqual(error.details["key"], "TEST_KEY")
        self.assertEqual(error.error_code, "E001")
        self.assertEqual(error.severity, ErrorSeverity.CRITICAL)
        
    def test_validation_error(self):
        error = ValidationError("Invalid data", {"field": "username", "reason": "too short"})
        self.assertEqual(error.severity, ErrorSeverity.WARNING)
        
    def error_callback(self, error, context):
        self.callback_called = True
        self.callback_error = error
        
    def test_error_callback(self):
        register_error_callback(BetsyError, self.error_callback)
        handle_error(ValidationError("Invalid input"))
        self.assertTrue(self.callback_called)
        self.assertIsInstance(self.callback_error, ValidationError)
        
    def test_standard_exception_conversion(self):
        register_error_callback(BetsyError, self.error_callback)
        handle_error(ValueError("This is a standard exception"))
        self.assertTrue(self.callback_called)
        self.assertIsInstance(self.callback_error, BetsyError)
        self.assertIn("Uncategorised error", self.callback_error.message)
        self.assertEqual(self.callback_error.details["original_error_type"], "ValueError")

if __name__ == "__main__":
    unittest.main()