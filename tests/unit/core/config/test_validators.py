"""
Unit tests for bot.core.config.validators module.

This module tests the configuration validation functions.
"""

import os
import unittest
import tempfile
from enum import Enum
from typing import Any
from unittest import TestCase

# Import the module under test
from bot.core.config.config import ConfigValidationError
from bot.core.config.validators import (
    validate_required,
    validate_pattern,
    validate_in_list,
    validate_range,
    validate_url,
    validate_path_exists,
    validate_port,
    validate_type,
    validate_enum,
    apply_validator,
    validate_config
)

# Suppress print output during tests
unittest.main.__defaults__ = (None, True, [], False)


class TestValidators(TestCase):
    """Test cases for configuration validation functions."""

    def test_validate_required(self):
        """Test validate_required function."""
        # Test None
        self.assertFalse(validate_required(None))

        # Test empty string
        self.assertFalse(validate_required(""))
        self.assertFalse(validate_required("   "))

        # Test empty collections
        self.assertFalse(validate_required([]))
        self.assertFalse(validate_required({}))
        self.assertFalse(validate_required(set()))
        self.assertFalse(validate_required(tuple()))

        # Test non-empty values
        self.assertTrue(validate_required("non-empty"))
        self.assertTrue(validate_required(42))
        self.assertTrue(validate_required([1, 2, 3]))
        self.assertTrue(validate_required({"key": "value"}))
        self.assertTrue(validate_required(set([1, 2, 3])))

    def test_validate_pattern(self):
        """Test validate_pattern function."""
        # Create validator for email-like pattern
        email_validator = validate_pattern(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        # Test valid email patterns
        valid_emails = [
            "user@example.com",
            "user.name@example.co.uk",
            "user123@example-site.com"
        ]
        for email in valid_emails:
            self.assertTrue(email_validator(email), f"Failed for {email}")

        # Test invalid email patterns
        invalid_emails = [
            "invalid_email",
            "user@.com",
            "@example.com",
            "user@example",
            123  # Non-string input
        ]
        for email in invalid_emails:
            self.assertFalse(email_validator(email),
                             f"Unexpectedly passed for {email}")

    def test_validate_in_list(self):
        """Test validate_in_list function."""
        # Create validator for a list of valid colours
        colour_validator = validate_in_list(["red", "green", "blue"])

        # Test valid colours
        valid_colours = ["red", "green", "blue"]
        for colour in valid_colours:
            self.assertTrue(colour_validator(colour), f"Failed for {colour}")

        # Test invalid colours
        invalid_colours = ["yellow", "purple", 123, None]
        for colour in invalid_colours:
            self.assertFalse(colour_validator(colour),
                             f"Unexpectedly passed for {colour}")

    def test_validate_range(self):
        """Test validate_range function."""
        # Test validator with both min and max
        range_validator_full = validate_range(min_value=0, max_value=100)

        # Test within range
        valid_values = [0, 50, 100, 0.5, 99.9]
        for value in valid_values:
            self.assertTrue(range_validator_full(value), f"Failed for {value}")

        # Test outside range
        invalid_values = [-1, 101, 100.1, None, "string"]
        for value in invalid_values:
            self.assertFalse(range_validator_full(value),
                             f"Unexpectedly passed for {value}")

        # Test validator with only min
        range_validator_min = validate_range(min_value=10)
        self.assertTrue(range_validator_min(10))
        self.assertTrue(range_validator_min(100))
        self.assertFalse(range_validator_min(9))

        # Test validator with only max
        range_validator_max = validate_range(max_value=100)
        self.assertTrue(range_validator_max(0))
        self.assertTrue(range_validator_max(100))
        self.assertFalse(range_validator_max(101))

    def test_validate_url(self):
        """Test validate_url function."""
        # Test valid URLs
        valid_urls = [
            "http://example.com",
            "https://www.example.co.uk",
            "ftp://files.example.org",
            "ws://localhost:8080",
            "wss://secure.example.com"
        ]
        for url in valid_urls:
            self.assertTrue(validate_url(url), f"Failed for {url}")

        # Test invalid URLs
        invalid_urls = [
            "not_a_url",
            "example.com",
            123,
            None,
            "file:///path/to/file"
        ]
        for url in invalid_urls:
            self.assertFalse(validate_url(
                url), f"Unexpectedly passed for {url}")

    def test_validate_path_exists(self):
        """Test validate_path_exists function."""
        # Create a temporary directory and file for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "test_file.txt")
            with open(temp_file, 'w') as f:
                f.write("test content")

            # Test valid paths
            valid_paths = [temp_dir, temp_file]
            for path in valid_paths:
                self.assertTrue(validate_path_exists(
                    path), f"Failed for {path}")

        # Test invalid paths
        invalid_paths = [
            "/path/to/non/existent/file",
            123,
            None,
            ""
        ]
        for path in invalid_paths:
            self.assertFalse(validate_path_exists(
                path), f"Unexpectedly passed for {path}")

    def test_validate_port(self):
        """Test validate_port function."""
        # Test valid ports
        valid_ports = [1, 80, 443, 8080, 65535, "8000", "22"]
        for port in valid_ports:
            self.assertTrue(validate_port(port), f"Failed for {port}")

        # Test invalid ports
        invalid_ports = [
            0,  # Below minimum
            65536,  # Above maximum
            -1,
            "not_a_port",
            None,
            "65536"
        ]
        for port in invalid_ports:
            self.assertFalse(validate_port(
                port), f"Unexpectedly passed for {port}")

    def test_validate_type(self):
        """Test validate_type function."""
        # Create type validators
        int_validator = validate_type(int)
        str_validator = validate_type(str)
        list_validator = validate_type(list)

        # Test valid type checks
        valid_type_values = [
            (int_validator, 42),
            (str_validator, "hello"),
            (list_validator, [1, 2, 3])
        ]
        for validator, value in valid_type_values:
            self.assertTrue(validator(value), f"Failed for {value}")

        # Test invalid type checks
        invalid_type_values = [
            (int_validator, "not an int"),
            (str_validator, 123),
            (list_validator, {"not": "a list"})
        ]
        for validator, value in invalid_type_values:
            self.assertFalse(validator(value),
                             f"Unexpectedly passed for {value}")

    def test_validate_enum(self):
        """Test validate_enum function."""
        # Create a test enum
        class TestEnum(Enum):
            FIRST = 1
            SECOND = 2
            THIRD = 3

        # Create enum validator
        enum_validator = validate_enum(TestEnum)

        # Test valid enum values
        valid_enum_values = [
            1, 2, 3,  # Numeric values
            TestEnum.FIRST, TestEnum.SECOND, TestEnum.THIRD,  # Enum instances
            "FIRST", "SECOND", "THIRD",  # Enum names
            "1", "2", "3"  # String representations of numeric values
        ]
        for value in valid_enum_values:
            self.assertTrue(enum_validator(value), f"Failed for {value}")

        # Test invalid enum values
        invalid_enum_values = [
            4,
            "FOURTH",
            None,
            "another_value",
            "5",
            0
        ]
        for value in invalid_enum_values:
            self.assertFalse(enum_validator(value),
                             f"Unexpectedly passed for {value}")

    def test_apply_validator(self):
        """Test apply_validator function."""
        # Test successful validation
        result = apply_validator("test_key", 42, lambda x: 0 <= x <= 100)
        self.assertEqual(result, 42)

        # Test validation failure
        with self.assertRaises(ConfigValidationError):
            apply_validator("test_key", 200, lambda x: 0 <= x <= 100)

        # Test with custom error message
        with self.assertRaises(ConfigValidationError) as cm:
            apply_validator("test_key", 200, lambda x: 0 <=
                            x <= 100, "Custom error")

        self.assertIn("Custom error", str(cm.exception))

    def test_validate_config(self):
        """Test validate_config function."""
        # Define test configuration and validators
        config_dict = {
            "age": 30,
            "name": "John Doe",
            "email": "john@example.com"
        }

        validators = {
            "age": [(validate_range(0, 120), "Invalid age")],
            "name": [(validate_required, "Name is required")],
            "email": [
                (validate_required, "Email is required"),
                (validate_pattern(r'^[^@]+@[^@]+\.[^@]+$'),
                 "Invalid email format")
            ]
        }

        # Test successful validation
        validated_config = validate_config(config_dict, validators)
        self.assertEqual(validated_config, config_dict)

        # Test validation failure
        invalid_configs = [
            # Invalid age
            {**config_dict, "age": 200},
            # Missing name
            {**config_dict, "name": ""},
            # Invalid email
            {**config_dict, "email": "invalid_email"}
        ]

        for invalid_config in invalid_configs:
            with self.assertRaises(ConfigValidationError):
                validate_config(invalid_config, validators)


if __name__ == "__main__":
    unittest.main()
