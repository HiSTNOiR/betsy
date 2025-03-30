#!/usr/bin/env python
"""
Test runner for the bot application.

This script runs the application's test suite with customizable options.
"""

import argparse
import os
import sys
import unittest
import warnings

# Add the parent directory to the path so we can import bot modules
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Run tests for the bot application.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Run tests in verbose mode')
    parser.add_argument('-f', '--failfast', action='store_true',
                        help='Stop on first failure')
    parser.add_argument('-p', '--pattern', default='test_*.py',
                        help='Pattern to match test files (default: test_*.py)')
    parser.add_argument('-s', '--start-dir', default='tests',
                        help='Directory to start discovery (default: tests)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Run tests in quiet mode (minimal output)')
    return parser.parse_args()


def main():
    """Run the test suite."""
    # Parse command line arguments
    args = parse_args()

    # Filter out ResourceWarning to avoid file closure warnings from unittest
    warnings.filterwarnings('ignore', category=ResourceWarning)

    # Filter out RuntimeWarning for coroutines to avoid noise from async tests
    warnings.filterwarnings('ignore', category=RuntimeWarning,
                            message="coroutine '.*' was never awaited")

    # Create a test suite
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover(
        args.start_dir,
        pattern=args.pattern
    )

    # Configure the test runner
    verbosity = 2 if args.verbose else 0 if args.quiet else 1

    # Custom test runner that suppresses stdout/stderr during tests
    class QuietTestRunner(unittest.TextTestRunner):
        def run(self, test):
            """Run the test suite with suppressed output."""
            # Redirect stdout and stderr during test execution
            if args.quiet:
                old_stdout, old_stderr = sys.stdout, sys.stderr
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')

            try:
                result = super().run(test)
            finally:
                # Restore stdout and stderr
                if args.quiet:
                    sys.stdout.close()
                    sys.stderr.close()
                    sys.stdout, sys.stderr = old_stdout, old_stderr

            return result

    # Run the tests
    test_runner = QuietTestRunner(verbosity=verbosity, failfast=args.failfast)
    test_result = test_runner.run(test_suite)

    # Return non-zero exit code if tests failed
    sys.exit(not test_result.wasSuccessful())


if __name__ == '__main__':
    main()
