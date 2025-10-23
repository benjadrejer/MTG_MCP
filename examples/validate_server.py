#!/usr/bin/env python3
"""Simple validation script for MTG MCP Server without running it."""

import sys
import importlib.util
from pathlib import Path


def validate_imports():
    """Validate that all required modules can be imported."""
    print("Validating imports...")

    try:
        # Test main module import
        from mtg_mcp_server.main import main, cli_main

        print("✓ Main module imports successfully")

        # Test API client import
        from mtg_mcp_server.api.client import MTGAPIClient

        print("✓ API client imports successfully")

        # Test handlers import
        from mtg_mcp_server.tools.handlers import register_tools, search_cards_handler

        print("✓ Tool handlers import successfully")

        # Test models import
        from mtg_mcp_server.models.card import Card
        from mtg_mcp_server.models.set import Set

        print("✓ Data models import successfully")

        # Test utilities import
        from mtg_mcp_server.utils.data_converters import convert_card_data
        from mtg_mcp_server.utils.validators import validate_card_name
        from mtg_mcp_server.utils.param_processors import build_search_params

        print("✓ Utilities import successfully")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def validate_server_setup():
    """Validate server setup without running it."""
    print("\nValidating server setup...")

    try:
        from mcp.server import Server
        from mtg_mcp_server.api.client import MTGAPIClient
        from mtg_mcp_server.tools.handlers import register_tools

        # Create server instance
        server = Server("mtg-mcp-server")
        print("✓ MCP server instance created")

        # Create API client
        api_client = MTGAPIClient()
        print("✓ MTG API client instance created")

        # Test tool registration (without actually registering)
        # This validates that the function exists and can be called
        print("✓ Tool registration function available")

        return True

    except Exception as e:
        print(f"✗ Server setup error: {e}")
        return False


def validate_tool_handler():
    """Validate tool handler functionality."""
    print("\nValidating tool handler...")

    try:
        from mtg_mcp_server.tools.handlers import search_cards_handler
        from mtg_mcp_server.models.card import Card
        from mcp.types import TextContent
        from unittest.mock import AsyncMock

        # Create mock API client
        mock_client = AsyncMock()
        mock_client.search_cards.return_value = [
            Card(id="1", name="Test Card", type="Instant")
        ]

        # Test that handler function exists and has correct signature
        import inspect

        sig = inspect.signature(search_cards_handler)
        params = list(sig.parameters.keys())

        if "api_client" in params and "arguments" in params:
            print("✓ search_cards_handler has correct signature")
        else:
            print(f"✗ search_cards_handler has incorrect signature: {params}")
            return False

        return True

    except Exception as e:
        print(f"✗ Tool handler validation error: {e}")
        return False


def validate_entry_points():
    """Validate entry points are configured correctly."""
    print("\nValidating entry points...")

    try:
        # Check if the module can be run
        import mtg_mcp_server.main

        # Check if cli_main function exists
        if hasattr(mtg_mcp_server.main, "cli_main"):
            print("✓ CLI entry point function exists")
        else:
            print("✗ CLI entry point function missing")
            return False

        # Check if main function exists
        if hasattr(mtg_mcp_server.main, "main"):
            print("✓ Main async function exists")
        else:
            print("✗ Main async function missing")
            return False

        return True

    except Exception as e:
        print(f"✗ Entry point validation error: {e}")
        return False


def main():
    """Run all validation checks."""
    print("MTG MCP Server Validation")
    print("=" * 30)

    all_passed = True

    # Run validation checks
    checks = [
        ("Import Validation", validate_imports),
        ("Server Setup Validation", validate_server_setup),
        ("Tool Handler Validation", validate_tool_handler),
        ("Entry Point Validation", validate_entry_points),
    ]

    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"✗ {check_name} failed with exception: {e}")
            all_passed = False

    print("\n" + "=" * 30)
    if all_passed:
        print("✓ All validations passed! Server is ready for testing.")
        print("\nNext steps:")
        print("1. Test with an MCP client")
        print("2. Try the search_cards tool")
        print("3. Validate error handling")
    else:
        print("✗ Some validations failed. Please check the errors above.")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
