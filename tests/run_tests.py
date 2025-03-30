#!/usr/bin/env python3
"""
Test runner for the bot.

This script runs tests for the bot with specified options.
"""

import argparse
import logging
import os
import sys
import time
import unittest
import warnings
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr


# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def suppress_logging():
    """Suppress all logging output."""
    # Set the root logger to CRITICAL+1 level (higher than any defined level)
    logging.getLogger().setLevel(logging.CRITICAL + 1)

    # Replace all existing handlers with null handlers
    for logger_name in [''] + list(logging.root.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(logging.NullHandler())
        logger.propagate = False


def suppress_warnings():
    """Suppress warnings during test execution."""
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


def run_tests(pattern=None, failfast=False, quiet=False):
    """
    Run tests matching the specified pattern.

    Args:
        pattern (str): Test pattern to match.
        failfast (bool): Whether to stop on first failure.
        quiet (bool): Whether to suppress logging output.

    Returns:
        bool: True if all tests passed, False otherwise.
    """
    if quiet:
        suppress_logging()
        suppress_warnings()

    # Discover and run tests
    loader = unittest.TestLoader()

    # Get the test directory
    start_dir = os.path.join(project_root, 'tests')

    if pattern:
        suite = loader.discover(start_dir, pattern=f"*{pattern}*.py")
    else:
        suite = loader.discover(start_dir)

    # Prepare output capturing if quiet mode is enabled
    if quiet:
        # Capture all output during test execution
        captured_output = StringIO()
        captured_error = StringIO()

        start_time = time.time()
        with redirect_stdout(captured_output), redirect_stderr(captured_error):
            # Create and run the test runner
            runner = unittest.TextTestRunner(
                failfast=failfast, verbosity=1, stream=StringIO())
            result = runner.run(suite)
        elapsed_time = time.time() - start_time

        # Only print the final result
        test_count = result.testsRun
        if result.wasSuccessful():
            print(f"\nRan {test_count} tests in {elapsed_time:.3f}s\n\nOK")
        else:
            # Print failures and errors to stderr
            sys.stderr.write("\nFAILURES:\n")
            for test, error_msg in result.failures:
                sys.stderr.write(f"{test}\n{error_msg}\n")
            for test, error_msg in result.errors:
                sys.stderr.write(f"{test}\n{error_msg}\n")
            sys.stderr.write(
                f"\nRan {test_count} tests in {elapsed_time:.3f}s\n\nFAILED\n")
    else:
        # Run without capturing output
        runner = unittest.TextTestRunner(failfast=failfast, verbosity=1)
        result = runner.run(suite)

    return result.wasSuccessful()


def main():
    """Main function for the test runner."""
    parser = argparse.ArgumentParser(description='Run tests for the bot')
    parser.add_argument(
        '-p', '--pattern',
        help='Pattern to match test files (e.g. "config" for test_config.py)'
    )
    parser.add_argument(
        '-f', '--failfast',
        action='store_true',
        help='Stop on first failure'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all output except test results'
    )

    args = parser.parse_args()
    success = run_tests(args.pattern, args.failfast, args.quiet)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
