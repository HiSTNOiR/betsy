#!/usr/bin/env python3
"""
Enhanced import verification script for the bot packages.

This script automatically discovers all packages in the project and verifies that
all exported components can be properly imported. It helps catch issues with
__init__.py files, such as missing exports or circular imports.

Usage:
    python scripts/verify_imports.py [--package package_name]
"""

import argparse
import ast
import importlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any

# Add the project root to the Python path if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


def parse_init_file(file_path: str) -> List[str]:
    """
    Parse an __init__.py file to extract the __all__ list.

    Args:
        file_path (str): Path to the __init__.py file.

    Returns:
        List[str]: List of exported names from __all__.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == '__all__':
                        if isinstance(node.value, ast.List):
                            return [
                                elt.s for elt in node.value.elts
                                if isinstance(elt, ast.Str)
                            ]

        # If __all__ is not defined, return an empty list
        return []

    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return []


def find_all_packages() -> Dict[str, List[str]]:
    """
    Find all packages in the project and their exported names.

    Returns:
        Dict[str, List[str]]: Dictionary mapping package paths to lists of exported names.
    """
    packages = {}

    # Start from the bot directory
    bot_dir = os.path.join(project_root, 'bot')

    # Walk through the directory structure
    for root, dirs, files in os.walk(bot_dir):
        if '__init__.py' in files:
            # Calculate the package path
            rel_path = os.path.relpath(root, project_root)
            package_path = rel_path.replace(os.sep, '.')

            # Parse the __init__.py file
            init_path = os.path.join(root, '__init__.py')
            exports = parse_init_file(init_path)

            # Store the package and its exports
            packages[package_path] = exports

    return packages


def check_imports(module_path: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a module can be imported.

    Args:
        module_path (str): Dot-notation path to the module to import.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        module = importlib.import_module(module_path)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def check_attribute(module_path: str, attribute: str) -> Tuple[bool, Optional[str]]:
    """
    Check if an attribute can be accessed from a module.

    Args:
        module_path (str): Dot-notation path to the module.
        attribute (str): Attribute to access.

    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        module = importlib.import_module(module_path)
        getattr(module, attribute)
        return True, None
    except ImportError as e:
        return False, f"Import error: {str(e)}"
    except AttributeError as e:
        return False, f"Attribute error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def verify_package(package_path: str, attributes: List[str]) -> List[Tuple[str, bool, Optional[str]]]:
    """
    Verify that all attributes can be imported from a package.

    Args:
        package_path (str): Dot-notation path to the package.
        attributes (List[str]): List of attributes to check.

    Returns:
        List[Tuple[str, bool, Optional[str]]]: List of (attribute, success, error_message)
    """
    results = []

    # First check if the package itself can be imported
    package_success, package_error = check_imports(package_path)
    results.append((package_path, package_success, package_error))

    if not package_success:
        # If the package can't be imported, don't check attributes
        return results

    # Check each attribute
    for attr in attributes:
        attr_success, attr_error = check_attribute(package_path, attr)
        results.append((f"{package_path}.{attr}", attr_success, attr_error))

    return results


def display_results(results: List[Tuple[str, bool, Optional[str]]]) -> bool:
    """
    Display verification results.

    Args:
        results (List[Tuple[str, bool, Optional[str]]]): List of (item, success, error_message)

    Returns:
        bool: True if all checks passed, False otherwise.
    """
    success_count = 0
    failure_count = 0

    for item, success, error in results:
        if success:
            print(f"✅ {item}")
            success_count += 1
        else:
            print(f"❌ {item}: {error}")
            failure_count += 1

    print(f"\nResults: {success_count} successful, {failure_count} failed")
    return failure_count == 0


def main() -> int:
    """
    Main function that verifies imports for all packages.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Verify imports for bot packages")
    parser.add_argument('--package', type=str,
                        help='Verify only a specific package')
    args = parser.parse_args()

    print("Discovering packages and their exports...\n")

    packages = find_all_packages()

    if args.package:
        # Filter packages by the specified package
        filtered_packages = {
            k: v for k, v in packages.items()
            if k == args.package or k.startswith(args.package + '.')
        }
        if not filtered_packages:
            print(f"No packages found matching '{args.package}'")
            return 1
        packages = filtered_packages

    print(f"Found {len(packages)} packages to verify\n")

    all_results = []

    for package_path, exports in sorted(packages.items()):
        print(f"Verifying package: {package_path}")
        if not exports:
            print(f"  No exports defined in __all__ for {package_path}")
            # Just verify that the package itself can be imported
            results = verify_package(package_path, [])
        else:
            print(f"  Found {len(exports)} exports to verify")
            results = verify_package(package_path, exports)

        all_results.extend(results)
        print()

    print("\nSummary of import verification:")
    all_success = display_results(all_results)

    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
