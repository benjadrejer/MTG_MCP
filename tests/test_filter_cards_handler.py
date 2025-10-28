"""Tests for filter_cards MCP tool handler."""

import pytest
from unittest.mock import AsyncMock, Mock
from mcp.types import TextContent

from mtg_mcp_server.tools.handlers import filter_cards_handler
from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.exceptions import MTGAPIError, MTGValidationError


@pytest.fixture
def mock_api_client():
    """Create a mock MTG API client."""
    client = Mock()
    client.filter_cards = AsyncMock()
    return client


@pytest.fixture
def sample_cards():
    """Create sample card data for testing."""
    return [
        Card(
            id="1",
            name="Lightning Bolt",
            mana_cost="{R}",
            cmc=1,
            colors=["Red"],
            color_identity=["R"],
            type="Instant",
            supertypes=[],
            types=["Instant"],
            subtypes=[],
            text="Lightning Bolt deals 3 damage to any target.",
            power=None,
            toughness=None,
            loyalty=None,
            set_name="Alpha",
            set_code="LEA",
            rarity="Common",
            image_url="https://example.com/lightning_bolt.jpg",
        ),
        Card(
            id="2",
            name="Counterspell",
            mana_cost="{U}{U}",
            cmc=2,
            colors=["Blue"],
            color_identity=["U"],
            type="Instant",
            supertypes=[],
            types=["Instant"],
            subtypes=[],
            text="Counter target spell.",
            power=None,
            toughness=None,
            loyalty=None,
            set_name="Alpha",
            set_code="LEA",
            rarity="Uncommon",
            image_url="https://example.com/counterspell.jpg",
        ),
    ]


@pytest.mark.asyncio
async def test_filter_cards_by_color(mock_api_client, sample_cards):
    """Test filtering cards by color."""
    mock_api_client.filter_cards.return_value = [sample_cards[0]]  # Lightning Bolt

    arguments = {"colors": ["Red"]}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Lightning Bolt" in result[0].text
    assert "Red" in result[0].text
    mock_api_client.filter_cards.assert_called_once_with(colors=["Red"], limit=20)


@pytest.mark.asyncio
async def test_filter_cards_by_type(mock_api_client, sample_cards):
    """Test filtering cards by type."""
    mock_api_client.filter_cards.return_value = sample_cards  # Both instants

    arguments = {"type": "Instant"}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Lightning Bolt" in result[0].text
    assert "Counterspell" in result[0].text
    mock_api_client.filter_cards.assert_called_once_with(type="Instant", limit=20)


@pytest.mark.asyncio
async def test_filter_cards_by_multiple_attributes(mock_api_client, sample_cards):
    """Test filtering cards by multiple attributes."""
    mock_api_client.filter_cards.return_value = [sample_cards[0]]

    arguments = {"colors": ["Red"], "type": "Instant", "cmc": 1, "limit": 10}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Lightning Bolt" in result[0].text
    mock_api_client.filter_cards.assert_called_once_with(
        colors=["Red"], type="Instant", cmc=1, limit=10
    )


@pytest.mark.asyncio
async def test_filter_cards_with_custom_limit(mock_api_client, sample_cards):
    """Test filtering cards with custom limit."""
    mock_api_client.filter_cards.return_value = sample_cards

    arguments = {"colors": ["Blue"], "limit": 5}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    mock_api_client.filter_cards.assert_called_once_with(colors=["Blue"], limit=5)


@pytest.mark.asyncio
async def test_filter_cards_no_results(mock_api_client):
    """Test filtering cards with no results."""
    mock_api_client.filter_cards.return_value = []

    arguments = {"colors": ["Green"]}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "No cards found matching the specified filters" in result[0].text


@pytest.mark.asyncio
async def test_filter_cards_invalid_limit():
    """Test filtering cards with invalid limit parameter."""
    mock_api_client = Mock()

    arguments = {"colors": ["Red"], "limit": "invalid"}

    with pytest.raises(ValueError, match="limit parameter must be an integer"):
        await filter_cards_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_filter_cards_api_error(mock_api_client):
    """Test filtering cards when API returns an error."""
    mock_api_client.filter_cards.side_effect = MTGAPIError("API Error", 500)

    arguments = {"colors": ["Red"]}

    with pytest.raises(MTGAPIError):
        await filter_cards_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_filter_cards_validation_error(mock_api_client):
    """Test filtering cards when validation fails."""
    mock_api_client.filter_cards.side_effect = MTGValidationError("Invalid color")

    arguments = {"colors": ["InvalidColor"]}

    with pytest.raises(MTGValidationError):
        await filter_cards_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_filter_cards_empty_filters(mock_api_client, sample_cards):
    """Test filtering cards with empty filter arguments."""
    mock_api_client.filter_cards.return_value = sample_cards

    arguments = {}
    result = await filter_cards_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    assert "Lightning Bolt" in result[0].text
    assert "Counterspell" in result[0].text
    mock_api_client.filter_cards.assert_called_once_with(limit=20)


@pytest.mark.asyncio
async def test_filter_cards_formatting(mock_api_client, sample_cards):
    """Test that filter_cards formats results correctly."""
    mock_api_client.filter_cards.return_value = [sample_cards[0]]

    arguments = {"colors": ["Red"]}
    result = await filter_cards_handler(mock_api_client, arguments)

    content = result[0].text
    assert "Found 1 cards matching the specified filters" in content
    assert "**Lightning Bolt**" in content
    assert "Mana Cost: {R}" in content
    assert "Type: Instant" in content
    assert "Text: Lightning Bolt deals 3 damage to any target." in content
    assert "Set: Alpha (LEA)" in content
    assert "Rarity: Common" in content
