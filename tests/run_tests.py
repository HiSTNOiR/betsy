#!/usr/bin/env python
"""
Test runner for the bot.

This script discovers and runs all tests for the bot.
"""

import unittest
import sys
import os
import argparse
import logging
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Return the parent directory (project root)
    return os.path.dirname(script_dir)


def run_tests(test_path=None, verbose=False, failfast=False):
    """
    Discover and run tests.

    Args:
        test_path (str): Optional path to a specific test file or directory.
        verbose (bool): Whether to produce verbose output.
        failfast (bool): Whether to stop at the first failure.

    Returns:
        bool: True if all tests passed, False otherwise.
    """
    # Add the project root to the Python path
    project_root = get_project_root()
    sys.path.insert(0, project_root)

    # Disable certain logs during tests to avoid clutter
    logging.disable(logging.WARNING)

    # Create test loader
    loader = unittest.TestLoader()

    # Discover tests
    if test_path:
        # Load specific test file or directory
        if os.path.isfile(test_path):
            suite = loader.loadTestsFromName(test_path)
        else:
            suite = loader.discover(test_path)
    else:
        # Load all tests
        suite = loader.discover(os.path.join(project_root, "tests"))

    # Create test runner
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        failfast=failfast
    )

    # Run tests
    result = runner.run(suite)

    # Re-enable all logging levels
    logging.disable(logging.NOTSET)

    # Return True if all tests passed
    return result.wasSuccessful()


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run bot tests")
    parser.add_argument(
        "test_path",
        nargs="?",
        help="Path to a specific test file or directory"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Produce verbose output"
    )
    parser.add_argument(
        "-f", "--failfast",
        action="store_true",
        help="Stop at the first failure"
    )
    args = parser.parse_args()

    # Run tests
    success = run_tests(args.test_path, args.verbose, args.failfast)

    # Exit with appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
