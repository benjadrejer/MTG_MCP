"""Tests for get_card_details MCP tool handler."""

import pytest
from unittest.mock import AsyncMock, Mock
from mcp.types import TextContent

from mtg_mcp_server.tools.handlers import get_card_details_handler
from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.exceptions import (
    MTGAPIError,
    MTGAPINotFoundError,
    MTGValidationError,
)


@pytest.fixture
def mock_api_client():
    """Create a mock MTG API client."""
    client = Mock()
    client.get_card = AsyncMock()
    return client


@pytest.fixture
def sample_card():
    """Create sample card data for testing."""
    return Card(
        id="12345",
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
    )


@pytest.fixture
def sample_creature_card():
    """Create sample creature card data for testing."""
    return Card(
        id="67890",
        name="Serra Angel",
        mana_cost="{3}{W}{W}",
        cmc=5,
        colors=["White"],
        color_identity=["W"],
        type="Creature — Angel",
        supertypes=[],
        types=["Creature"],
        subtypes=["Angel"],
        text="Flying, vigilance",
        power="4",
        toughness="4",
        loyalty=None,
        set_name="Alpha",
        set_code="LEA",
        rarity="Uncommon",
        image_url="https://example.com/serra_angel.jpg",
    )


@pytest.fixture
def sample_planeswalker_card():
    """Create sample planeswalker card data for testing."""
    return Card(
        id="11111",
        name="Jace, the Mind Sculptor",
        mana_cost="{2}{U}{U}",
        cmc=4,
        colors=["Blue"],
        color_identity=["U"],
        type="Legendary Planeswalker — Jace",
        supertypes=["Legendary"],
        types=["Planeswalker"],
        subtypes=["Jace"],
        text="+2: Look at the top card of target player's library...",
        power=None,
        toughness=None,
        loyalty="3",
        set_name="Worldwake",
        set_code="WWK",
        rarity="Mythic Rare",
        image_url="https://example.com/jace.jpg",
    )


@pytest.mark.asyncio
async def test_get_card_details_success(mock_api_client, sample_card):
    """Test successful card details retrieval."""
    mock_api_client.get_card.return_value = sample_card

    arguments = {"card_id": "12345"}
    result = await get_card_details_handler(mock_api_client, arguments)

    assert len(result) == 1
    assert isinstance(result[0], TextContent)
    content = result[0].text

    assert "Lightning Bolt" in content
    assert "Mana Cost: {R}" in content
    assert "Type: Instant" in content
    assert "Lightning Bolt deals 3 damage to any target." in content
    assert "Set: Alpha (LEA)" in content
    assert "Rarity: Common" in content

    mock_api_client.get_card.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_card_details_creature(mock_api_client, sample_creature_card):
    """Test card details retrieval for a creature card."""
    mock_api_client.get_card.return_value = sample_creature_card

    arguments = {"card_id": "67890"}
    result = await get_card_details_handler(mock_api_client, arguments)

    assert len(result) == 1
    content = result[0].text

    assert "Serra Angel" in content
    assert "Power/Toughness: 4/4" in content
    assert "Flying, vigilance" in content
    assert "Creature — Angel" in content


@pytest.mark.asyncio
async def test_get_card_details_planeswalker(mock_api_client, sample_planeswalker_card):
    """Test card details retrieval for a planeswalker card."""
    mock_api_client.get_card.return_value = sample_planeswalker_card

    arguments = {"card_id": "11111"}
    result = await get_card_details_handler(mock_api_client, arguments)

    assert len(result) == 1
    content = result[0].text

    assert "Jace, the Mind Sculptor" in content
    assert "Loyalty: 3" in content
    assert "Legendary Planeswalker — Jace" in content
    assert "Mythic Rare" in content


@pytest.mark.asyncio
async def test_get_card_details_missing_card_id():
    """Test card details retrieval without card_id parameter."""
    mock_api_client = Mock()

    arguments = {}

    with pytest.raises(ValueError, match="card_id parameter is required"):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_empty_card_id():
    """Test card details retrieval with empty card_id parameter."""
    mock_api_client = Mock()

    arguments = {"card_id": ""}

    with pytest.raises(ValueError, match="card_id parameter cannot be empty"):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_whitespace_card_id():
    """Test card details retrieval with whitespace-only card_id parameter."""
    mock_api_client = Mock()

    arguments = {"card_id": "   "}

    with pytest.raises(ValueError, match="card_id parameter cannot be empty"):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_not_found(mock_api_client):
    """Test card details retrieval when card is not found."""
    mock_api_client.get_card.side_effect = MTGAPINotFoundError("Card not found")

    arguments = {"card_id": "nonexistent"}

    with pytest.raises(MTGAPINotFoundError):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_api_error(mock_api_client):
    """Test card details retrieval when API returns an error."""
    mock_api_client.get_card.side_effect = MTGAPIError("API Error", 500)

    arguments = {"card_id": "12345"}

    with pytest.raises(MTGAPIError):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_validation_error(mock_api_client):
    """Test card details retrieval when validation fails."""
    mock_api_client.get_card.side_effect = MTGValidationError("Invalid card ID format")

    arguments = {"card_id": "invalid-id"}

    with pytest.raises(MTGValidationError):
        await get_card_details_handler(mock_api_client, arguments)


@pytest.mark.asyncio
async def test_get_card_details_formatting_complete(mock_api_client, sample_card):
    """Test that get_card_details formats all available information correctly."""
    # Create a card with all possible fields populated
    complete_card = Card(
        id="12345",
        name="Lightning Bolt",
        mana_cost="{R}",
        cmc=1,
        colors=["Red"],
        color_identity=["R"],
        type="Instant",
        supertypes=["Legendary"],
        types=["Instant"],
        subtypes=["Bolt"],
        text="Lightning Bolt deals 3 damage to any target.",
        power=None,
        toughness=None,
        loyalty=None,
        set_name="Alpha",
        set_code="LEA",
        rarity="Common",
        image_url="https://example.com/lightning_bolt.jpg",
    )

    mock_api_client.get_card.return_value = complete_card

    arguments = {"card_id": "12345"}
    result = await get_card_details_handler(mock_api_client, arguments)

    content = result[0].text

    # Check that all fields are included
    assert "**Lightning Bolt**" in content
    assert "ID: 12345" in content
    assert "Mana Cost: {R}" in content
    assert "Converted Mana Cost: 1" in content
    assert "Colors: Red" in content
    assert "Color Identity: R" in content
    assert "Type: Instant" in content
    assert "Supertypes: Legendary" in content
    assert "Types: Instant" in content
    assert "Subtypes: Bolt" in content
    assert "Text: Lightning Bolt deals 3 damage to any target." in content
    assert "Set: Alpha (LEA)" in content
    assert "Rarity: Common" in content
    assert "Image URL: https://example.com/lightning_bolt.jpg" in content


@pytest.mark.asyncio
async def test_get_card_details_minimal_card(mock_api_client):
    """Test card details formatting with minimal card information."""
    minimal_card = Card(
        id="minimal",
        name="Basic Card",
        mana_cost=None,
        cmc=None,
        colors=[],
        color_identity=[],
        type="",
        supertypes=[],
        types=[],
        subtypes=[],
        text=None,
        power=None,
        toughness=None,
        loyalty=None,
        set_name=None,
        set_code=None,
        rarity=None,
        image_url=None,
    )

    mock_api_client.get_card.return_value = minimal_card

    arguments = {"card_id": "minimal"}
    result = await get_card_details_handler(mock_api_client, arguments)

    content = result[0].text

    # Check that only available fields are shown
    assert "**Basic Card**" in content
    assert "ID: minimal" in content
    assert "Mana Cost:" not in content  # Should not show empty mana cost
    assert "Text:" not in content  # Should not show empty text
    assert "Set:" not in content  # Should not show empty set info
