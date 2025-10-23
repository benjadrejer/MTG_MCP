#!/usr/bin/env python3
"""Test script to validate MTG MCP Server functionality."""

import asyncio
import json
import logging
from typing import Any, Dict

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_search_cards():
    """Test the search_cards tool functionality."""
    logger.info("Testing search_cards tool...")

    # Start the MCP server process
    async with stdio_client(
        command="python", args=["-m", "mtg_mcp_server.main"], env={"PYTHONPATH": "."}
    ) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            logger.info(
                f"Available tools: {[tool.name for tool in tools_result.tools]}"
            )

            # Verify search_cards tool is available
            search_tool = None
            for tool in tools_result.tools:
                if tool.name == "search_cards":
                    search_tool = tool
                    break

            if not search_tool:
                logger.error("search_cards tool not found!")
                return False

            logger.info(f"Found search_cards tool: {search_tool.description}")

            # Test search_cards with a simple query
            try:
                result = await session.call_tool(
                    "search_cards", {"name": "Lightning Bolt", "limit": 3}
                )

                logger.info("Search results:")
                for content in result.content:
                    if hasattr(content, "text"):
                        logger.info(content.text)

                return True

            except Exception as e:
                logger.error(f"Error calling search_cards: {e}")
                return False


async def test_error_handling():
    """Test error handling in the MCP server."""
    logger.info("Testing error handling...")

    async with stdio_client(
        command="python", args=["-m", "mtg_mcp_server.main"], env={"PYTHONPATH": "."}
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test with missing required parameter
            try:
                result = await session.call_tool("search_cards", {})
                logger.error("Expected error for missing parameter, but got result")
                return False
            except Exception as e:
                logger.info(f"Correctly caught error for missing parameter: {e}")

            # Test with empty name parameter
            try:
                result = await session.call_tool("search_cards", {"name": ""})
                logger.error("Expected error for empty name, but got result")
                return False
            except Exception as e:
                logger.info(f"Correctly caught error for empty name: {e}")

            # Test with invalid tool name
            try:
                result = await session.call_tool("nonexistent_tool", {"name": "test"})
                logger.error("Expected error for invalid tool, but got result")
                return False
            except Exception as e:
                logger.info(f"Correctly caught error for invalid tool: {e}")

            return True


async def main():
    """Run all MCP server tests."""
    logger.info("Starting MTG MCP Server validation tests...")

    try:
        # Test basic functionality
        search_success = await test_search_cards()
        if not search_success:
            logger.error("Search cards test failed!")
            return False

        # Test error handling
        error_success = await test_error_handling()
        if not error_success:
            logger.error("Error handling test failed!")
            return False

        logger.info("All tests passed! MTG MCP Server is working correctly.")
        return True

    except Exception as e:
        logger.error(f"Test suite failed with error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
