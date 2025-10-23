"""Unit tests for search_cards MCP tool handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.types import Tool, TextContent

from mtg_mcp_server.tools.handlers import search_cards_handler
from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.exceptions import MTGValidationError, MTGAPIError


class TestSearchCardsHandler:
    """Test cases for search_cards MCP tool handler."""

    @pytest.fixture
    def mock_api_client(self):
        """Create mock API client for testing."""
        return AsyncMock()

    @pytest.fixture
    def sample_cards(self):
        """Sample card data for testing."""
        return [
            Card(
                id="1",
                name="Lightning Bolt",
                mana_cost="{R}",
                cmc=1,
                colors=["Red"],
                color_identity=["R"],
                type="Instant",
                types=["Instant"],
                text="Lightning Bolt deals 3 damage to any target.",
                set_name="Limited Edition Alpha",
                set_code="LEA",
                rarity="Common",
            ),
            Card(
                id="2",
                name="Lightning Strike",
                mana_cost="{1}{R}",
                cmc=2,
                colors=["Red"],
                color_identity=["R"],
                type="Instant",
                types=["Instant"],
                text="Lightning Strike deals 3 damage to any target.",
                set_name="Magic 2014",
                set_code="M14",
                rarity="Common",
            ),
        ]

    @pytest.mark.asyncio
    async def test_search_cards_success_single_result(
        self, mock_api_client, sample_cards
    ):
        """Test successful card search with single result."""
        mock_api_client.search_cards.return_value = [sample_cards[0]]

        arguments = {"name": "Lightning Bolt"}
        result = await search_cards_handler(mock_api_client, arguments)

        assert len(result) == 1
        assert isinstance(result[0], TextContent)

        content = result[0].text
        assert "Lightning Bolt" in content
        assert "Instant" in content
        assert "{R}" in content
        assert "Lightning Bolt deals 3 damage to any target." in content
        assert "Limited Edition Alpha" in content
        assert "Common" in content

        mock_api_client.search_cards.assert_called_once_with("Lightning Bolt", 10)

    @pytest.mark.asyncio
    async def test_search_cards_success_multiple_results(
        self, mock_api_client, sample_cards
    ):
        """Test successful card search with multiple results."""
        mock_api_client.search_cards.return_value = sample_cards

        arguments = {"name": "Lightning"}
        result = await search_cards_handler(mock_api_client, arguments)

        assert len(result) == 1
        assert isinstance(result[0], TextContent)

        content = result[0].text
        assert "Lightning Bolt" in content
        assert "Lightning Strike" in content
        assert "Found 2 cards matching" in content

        mock_api_client.search_cards.assert_called_once_with("Lightning", 10)

    @pytest.mark.asyncio
    async def test_search_cards_with_custom_limit(self, mock_api_client, sample_cards):
        """Test card search with custom limit parameter."""
        mock_api_client.search_cards.return_value = sample_cards

        arguments = {"name": "Lightning", "limit": 5}
        result = await search_cards_handler(mock_api_client, arguments)

        assert len(result) == 1
        mock_api_client.search_cards.assert_called_once_with("Lightning", 5)

    @pytest.mark.asyncio
    async def test_search_cards_empty_results(self, mock_api_client):
        """Test card search with no results."""
        mock_api_client.search_cards.return_value = []

        arguments = {"name": "NonexistentCard"}
        result = await search_cards_handler(mock_api_client, arguments)

        assert len(result) == 1
        assert isinstance(result[0], TextContent)

        content = result[0].text
        assert "No cards found matching" in content
        assert "NonexistentCard" in content

        mock_api_client.search_cards.assert_called_once_with("NonexistentCard", 10)

    @pytest.mark.asyncio
    async def test_search_cards_missing_name_parameter(self, mock_api_client):
        """Test card search with missing name parameter."""
        arguments = {}

        with pytest.raises(ValueError, match="name parameter is required"):
            await search_cards_handler(mock_api_client, arguments)

        mock_api_client.search_cards.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_cards_empty_name_parameter(self, mock_api_client):
        """Test card search with empty name parameter."""
        arguments = {"name": ""}

        with pytest.raises(ValueError, match="name parameter cannot be empty"):
            await search_cards_handler(mock_api_client, arguments)

        mock_api_client.search_cards.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_cards_invalid_limit_parameter(self, mock_api_client):
        """Test card search with invalid limit parameter."""
        arguments = {"name": "Lightning", "limit": "invalid"}

        with pytest.raises(ValueError, match="limit parameter must be an integer"):
            await search_cards_handler(mock_api_client, arguments)

        mock_api_client.search_cards.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_cards_validation_error_from_api(self, mock_api_client):
        """Test card search when API client raises validation error."""
        mock_api_client.search_cards.side_effect = MTGValidationError("Invalid limit")

        arguments = {"name": "Lightning", "limit": 100}

        with pytest.raises(MTGValidationError):
            await search_cards_handler(mock_api_client, arguments)

    @pytest.mark.asyncio
    async def test_search_cards_api_error_from_client(self, mock_api_client):
        """Test card search when API client raises API error."""
        mock_api_client.search_cards.side_effect = MTGAPIError("API unavailable")

        arguments = {"name": "Lightning"}

        with pytest.raises(MTGAPIError):
            await search_cards_handler(mock_api_client, arguments)

    @pytest.mark.asyncio
    async def test_search_cards_formats_card_with_power_toughness(
        self, mock_api_client
    ):
        """Test card search formats creature cards with power/toughness."""
        creature_card = Card(
            id="3",
            name="Lightning Elemental",
            mana_cost="{3}{R}",
            cmc=4,
            colors=["Red"],
            color_identity=["R"],
            type="Creature — Elemental",
            types=["Creature"],
            subtypes=["Elemental"],
            text="Haste",
            power="4",
            toughness="1",
            set_name="Core Set 2020",
            set_code="M20",
            rarity="Common",
        )

        mock_api_client.search_cards.return_value = [creature_card]

        arguments = {"name": "Lightning Elemental"}
        result = await search_cards_handler(mock_api_client, arguments)

        content = result[0].text
        assert "Lightning Elemental" in content
        assert "Creature — Elemental" in content
        assert "4/1" in content
        assert "Haste" in content

    @pytest.mark.asyncio
    async def test_search_cards_formats_planeswalker_with_loyalty(
        self, mock_api_client
    ):
        """Test card search formats planeswalker cards with loyalty."""
        planeswalker_card = Card(
            id="4",
            name="Jace, the Mind Sculptor",
            mana_cost="{2}{U}{U}",
            cmc=4,
            colors=["Blue"],
            color_identity=["U"],
            type="Legendary Planeswalker — Jace",
            types=["Planeswalker"],
            subtypes=["Jace"],
            text="+2: Look at the top card of target player's library.",
            loyalty="3",
            set_name="Worldwake",
            set_code="WWK",
            rarity="Mythic Rare",
        )

        mock_api_client.search_cards.return_value = [planeswalker_card]

        arguments = {"name": "Jace"}
        result = await search_cards_handler(mock_api_client, arguments)

        content = result[0].text
        assert "Jace, the Mind Sculptor" in content
        assert "Legendary Planeswalker — Jace" in content
        assert "Loyalty: 3" in content

    @pytest.mark.asyncio
    async def test_search_cards_handles_missing_optional_fields(self, mock_api_client):
        """Test card search handles cards with missing optional fields."""
        minimal_card = Card(id="5", name="Test Card", type="Instant")

        mock_api_client.search_cards.return_value = [minimal_card]

        arguments = {"name": "Test Card"}
        result = await search_cards_handler(mock_api_client, arguments)

        content = result[0].text
        assert "Test Card" in content
        assert "Instant" in content
        # Should not crash with missing fields

    @pytest.mark.asyncio
    async def test_search_cards_default_limit_is_10(
        self, mock_api_client, sample_cards
    ):
        """Test that default limit is 10 when not specified."""
        mock_api_client.search_cards.return_value = sample_cards

        arguments = {"name": "Lightning"}
        await search_cards_handler(mock_api_client, arguments)

        mock_api_client.search_cards.assert_called_once_with("Lightning", 10)

    @pytest.mark.asyncio
    async def test_search_cards_result_count_in_summary(
        self, mock_api_client, sample_cards
    ):
        """Test that result summary includes correct count."""
        mock_api_client.search_cards.return_value = sample_cards

        arguments = {"name": "Lightning"}
        result = await search_cards_handler(mock_api_client, arguments)

        content = result[0].text
        assert "Found 2 cards matching" in content
