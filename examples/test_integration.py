#!/usr/bin/env python3
"""Integration test for MTG MCP Server functionality."""

import asyncio
import json
import logging
import sys
from unittest.mock import AsyncMock, patch

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def test_search_cards_handler():
    """Test the search_cards handler directly."""
    logger.info("Testing search_cards handler directly...")

    try:
        from mtg_mcp_server.tools.handlers import search_cards_handler
        from mtg_mcp_server.models.card import Card
        from mcp.types import TextContent

        # Create mock API client with sample data
        mock_client = AsyncMock()
        sample_card = Card(
            id="1",
            name="Lightning Bolt",
            mana_cost="{R}",
            cmc=1,
            colors=["Red"],
            type="Instant",
            text="Lightning Bolt deals 3 damage to any target.",
            set_name="Limited Edition Alpha",
            set_code="LEA",
            rarity="Common",
        )
        mock_client.search_cards.return_value = [sample_card]

        # Test successful search
        arguments = {"name": "Lightning Bolt", "limit": 5}
        result = await search_cards_handler(mock_client, arguments)

        # Validate result
        assert len(result) == 1, f"Expected 1 result, got {len(result)}"
        assert isinstance(
            result[0], TextContent
        ), f"Expected TextContent, got {type(result[0])}"

        content = result[0].text
        assert "Lightning Bolt" in content, "Card name not in result"
        assert "Instant" in content, "Card type not in result"
        assert "{R}" in content, "Mana cost not in result"

        logger.info("✓ search_cards handler test passed")

        # Test empty results
        mock_client.search_cards.return_value = []
        result = await search_cards_handler(mock_client, {"name": "NonexistentCard"})

        assert len(result) == 1, "Expected 1 result for empty search"
        assert "No cards found" in result[0].text, "Empty result message not found"

        logger.info("✓ Empty results test passed")

        # Test error handling
        try:
            await search_cards_handler(mock_client, {})  # Missing name parameter
            logger.error("✗ Expected ValueError for missing name parameter")
            return False
        except ValueError as e:
            if "name parameter is required" in str(e):
                logger.info("✓ Error handling test passed")
            else:
                logger.error(f"✗ Unexpected error message: {e}")
                return False

        return True

    except Exception as e:
        logger.error(f"✗ Handler test failed: {e}")
        return False


async def test_tool_registration():
    """Test tool registration functionality."""
    logger.info("Testing tool registration...")

    try:
        from mcp.server import Server
        from mtg_mcp_server.api.client import MTGAPIClient
        from mtg_mcp_server.tools.handlers import register_tools
        from unittest.mock import MagicMock

        # Create mock server
        mock_server = MagicMock(spec=Server)
        api_client = MTGAPIClient()

        # Test registration
        register_tools(mock_server, api_client)

        # Verify decorators were called
        assert mock_server.list_tools.called, "list_tools decorator not called"
        assert mock_server.call_tool.called, "call_tool decorator not called"

        logger.info("✓ Tool registration test passed")
        return True

    except Exception as e:
        logger.error(f"✗ Tool registration test failed: {e}")
        return False


async def test_api_client_integration():
    """Test API client integration with mocked responses."""
    logger.info("Testing API client integration...")

    try:
        from mtg_mcp_server.api.client import MTGAPIClient
        from mtg_mcp_server.models.card import Card
        import httpx
        from unittest.mock import patch, AsyncMock

        # Create API client
        client = MTGAPIClient()

        # Mock HTTP response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cards": [
                {
                    "id": "1",
                    "name": "Lightning Bolt",
                    "manaCost": "{R}",
                    "cmc": 1,
                    "colors": ["Red"],
                    "type": "Instant",
                    "text": "Lightning Bolt deals 3 damage to any target.",
                }
            ]
        }

        # Test search_cards method
        with patch.object(
            client, "_make_request", return_value=mock_response.json.return_value
        ):
            cards = await client.search_cards("Lightning Bolt", 5)

            assert len(cards) == 1, f"Expected 1 card, got {len(cards)}"
            assert isinstance(
                cards[0], Card
            ), f"Expected Card object, got {type(cards[0])}"
            assert (
                cards[0].name == "Lightning Bolt"
            ), f"Expected 'Lightning Bolt', got '{cards[0].name}'"

        logger.info("✓ API client integration test passed")
        return True

    except Exception as e:
        logger.error(f"✗ API client integration test failed: {e}")
        return False


async def test_end_to_end_flow():
    """Test the complete flow from tool call to API response."""
    logger.info("Testing end-to-end flow...")

    try:
        from mtg_mcp_server.tools.handlers import search_cards_handler
        from mtg_mcp_server.api.client import MTGAPIClient
        from unittest.mock import patch, AsyncMock

        # Create real API client
        api_client = MTGAPIClient()

        # Mock the HTTP request to return sample data
        mock_response_data = {
            "cards": [
                {
                    "id": "1",
                    "name": "Lightning Bolt",
                    "manaCost": "{R}",
                    "cmc": 1,
                    "colors": ["Red"],
                    "colorIdentity": ["R"],
                    "type": "Instant",
                    "types": ["Instant"],
                    "text": "Lightning Bolt deals 3 damage to any target.",
                    "set": "LEA",
                    "setName": "Limited Edition Alpha",
                    "rarity": "Common",
                }
            ]
        }

        # Test the complete flow
        with patch.object(api_client, "_make_request", return_value=mock_response_data):
            result = await search_cards_handler(api_client, {"name": "Lightning Bolt"})

            assert len(result) == 1, "Expected 1 result"
            content = result[0].text

            # Verify all expected information is present
            expected_parts = [
                "Lightning Bolt",
                "Mana Cost: {R}",
                "Type: Instant",
                "Text: Lightning Bolt deals 3 damage to any target.",
                "Set: Limited Edition Alpha (LEA)",
                "Rarity: Common",
            ]

            for part in expected_parts:
                assert part in content, f"Missing expected part: {part}"

        logger.info("✓ End-to-end flow test passed")
        return True

    except Exception as e:
        logger.error(f"✗ End-to-end flow test failed: {e}")
        return False


async def main():
    """Run all integration tests."""
    logger.info("Starting MTG MCP Server Integration Tests")
    logger.info("=" * 50)

    tests = [
        ("Search Cards Handler", test_search_cards_handler),
        ("Tool Registration", test_tool_registration),
        ("API Client Integration", test_api_client_integration),
        ("End-to-End Flow", test_end_to_end_flow),
    ]

    all_passed = True

    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            if not await test_func():
                all_passed = False
        except Exception as e:
            logger.error(f"✗ {test_name} failed with exception: {e}")
            all_passed = False

    logger.info("\n" + "=" * 50)
    if all_passed:
        logger.info("✓ All integration tests passed!")
        logger.info("\nThe MTG MCP Server is ready for use with:")
        logger.info("- search_cards tool fully functional")
        logger.info("- Proper error handling")
        logger.info("- MCP protocol compliance")
        logger.info("\nYou can now test it with an MCP client!")
    else:
        logger.error("✗ Some integration tests failed.")

    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
