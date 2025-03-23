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