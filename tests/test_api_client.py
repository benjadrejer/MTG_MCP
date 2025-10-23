"""Unit tests for MTG API client."""

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from typing import List

from mtg_mcp_server.api.client import MTGAPIClient
from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.set import Set
from mtg_mcp_server.models.exceptions import (
    MTGAPIError,
    MTGAPIConnectionError,
    MTGAPITimeoutError,
    MTGAPIRateLimitError,
    MTGAPINotFoundError,
    MTGAPIServerError,
    MTGValidationError,
)


class TestMTGAPIClient:
    """Test cases for MTGAPIClient."""

    @pytest.fixture
    def client(self):
        """Create MTGAPIClient instance for testing."""
        return MTGAPIClient()

    @pytest.fixture
    def mock_card_response(self):
        """Mock card API response data."""
        return {
            "cards": [
                {
                    "id": "1",
                    "name": "Lightning Bolt",
                    "manaCost": "{R}",
                    "cmc": 1,
                    "colors": ["Red"],
                    "colorIdentity": ["R"],
                    "type": "Instant",
                    "supertypes": [],
                    "types": ["Instant"],
                    "subtypes": [],
                    "text": "Lightning Bolt deals 3 damage to any target.",
                    "set": "LEA",
                    "setName": "Limited Edition Alpha",
                    "rarity": "Common",
                    "imageUrl": "http://example.com/image.jpg",
                }
            ]
        }

    @pytest.fixture
    def mock_set_response(self):
        """Mock set API response data."""
        return {
            "sets": [
                {
                    "code": "LEA",
                    "name": "Limited Edition Alpha",
                    "type": "Core",
                    "releaseDate": "1993-08-05",
                    "block": "Core Set",
                    "onlineOnly": False,
                    "cardCount": 295,
                }
            ]
        }

    @pytest.mark.asyncio
    async def test_init_default_base_url(self):
        """Test client initialization with default base URL."""
        client = MTGAPIClient()
        assert client.base_url == "https://api.magicthegathering.io/v1"
        assert client.timeout == 30.0
        assert hasattr(client, "_session")

    @pytest.mark.asyncio
    async def test_init_custom_base_url(self):
        """Test client initialization with custom base URL."""
        custom_url = "https://custom.api.com/v1"
        client = MTGAPIClient(base_url=custom_url)
        assert client.base_url == custom_url

    @pytest.mark.asyncio
    async def test_search_cards_success(self, client, mock_card_response):
        """Test successful card search."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_card_response

            result = await client.search_cards("Lightning Bolt", limit=10)

            assert len(result) == 1
            assert isinstance(result[0], Card)
            assert result[0].name == "Lightning Bolt"
            assert result[0].mana_cost == "{R}"
            assert result[0].cmc == 1

            mock_request.assert_called_once_with(
                "GET", "/cards", {"name": "Lightning Bolt", "pageSize": 10}
            )

    @pytest.mark.asyncio
    async def test_search_cards_empty_name_raises_validation_error(self, client):
        """Test that empty name raises validation error."""
        with pytest.raises(MTGValidationError, match="Card name cannot be empty"):
            await client.search_cards("")

    @pytest.mark.asyncio
    async def test_search_cards_invalid_limit_raises_validation_error(self, client):
        """Test that invalid limit raises validation error."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            await client.search_cards("Lightning Bolt", limit=0)

        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            await client.search_cards("Lightning Bolt", limit=51)

    @pytest.mark.asyncio
    async def test_get_card_success(self, client, mock_card_response):
        """Test successful card retrieval by ID."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {"card": mock_card_response["cards"][0]}

            result = await client.get_card("1")

            assert isinstance(result, Card)
            assert result.id == "1"
            assert result.name == "Lightning Bolt"

            mock_request.assert_called_once_with("GET", "/cards/1")

    @pytest.mark.asyncio
    async def test_get_card_empty_id_raises_validation_error(self, client):
        """Test that empty card ID raises validation error."""
        with pytest.raises(MTGValidationError, match="Card ID cannot be empty"):
            await client.get_card("")

    @pytest.mark.asyncio
    async def test_filter_cards_success(self, client, mock_card_response):
        """Test successful card filtering."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_card_response

            result = await client.filter_cards(colors=["Red"], type="Instant", limit=20)

            assert len(result) == 1
            assert isinstance(result[0], Card)

            mock_request.assert_called_once_with(
                "GET",
                "/cards",
                {"pageSize": 20, "colors": "Red", "type": "Instant"},
            )

    @pytest.mark.asyncio
    async def test_filter_cards_invalid_limit_raises_validation_error(self, client):
        """Test that invalid filter limit raises validation error."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 100"):
            await client.filter_cards(limit=0)

        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 100"):
            await client.filter_cards(limit=101)

    @pytest.mark.asyncio
    async def test_get_sets_all_success(self, client, mock_set_response):
        """Test successful retrieval of all sets."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_set_response

            result = await client.get_sets()

            assert len(result) == 1
            assert isinstance(result[0], Set)
            assert result[0].code == "LEA"
            assert result[0].name == "Limited Edition Alpha"

            mock_request.assert_called_once_with("GET", "/sets")

    @pytest.mark.asyncio
    async def test_get_sets_by_code_success(self, client, mock_set_response):
        """Test successful retrieval of specific set by code."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = {"set": mock_set_response["sets"][0]}

            result = await client.get_sets(set_code="LEA")

            assert len(result) == 1
            assert isinstance(result[0], Set)
            assert result[0].code == "LEA"

            mock_request.assert_called_once_with("GET", "/sets/LEA")

    @pytest.mark.asyncio
    async def test_get_random_cards_success(self, client, mock_card_response):
        """Test successful random card retrieval."""
        with patch.object(
            client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_card_response

            result = await client.get_random_cards(count=1)

            assert len(result) == 1
            assert isinstance(result[0], Card)

            mock_request.assert_called_once_with(
                "GET", "/cards", {"random": "true", "pageSize": 1}
            )

    @pytest.mark.asyncio
    async def test_get_random_cards_invalid_count_raises_validation_error(self, client):
        """Test that invalid count raises validation error."""
        with pytest.raises(MTGValidationError, match="Count must be between 1 and 10"):
            await client.get_random_cards(count=0)

        with pytest.raises(MTGValidationError, match="Count must be between 1 and 10"):
            await client.get_random_cards(count=11)

    @pytest.mark.asyncio
    async def test_make_request_timeout_error(self, client):
        """Test timeout error handling."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.TimeoutException("Request timed out")

            with pytest.raises(MTGAPITimeoutError, match="MTG API request timed out"):
                await client._make_request("GET", "/cards")

    @pytest.mark.asyncio
    async def test_make_request_connection_error(self, client):
        """Test connection error handling."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")

            with pytest.raises(
                MTGAPIConnectionError, match="Unable to connect to MTG API"
            ):
                await client._make_request("GET", "/cards")

    @pytest.mark.asyncio
    async def test_make_request_404_error(self, client):
        """Test 404 error handling."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_request.return_value = mock_response

            with pytest.raises(MTGAPINotFoundError, match="Resource not found"):
                await client._make_request("GET", "/cards/invalid")

    @pytest.mark.asyncio
    async def test_make_request_429_error(self, client):
        """Test rate limit error handling."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_response.text = "Rate limit exceeded"
            mock_request.return_value = mock_response

            with pytest.raises(
                MTGAPIRateLimitError,
                match="Rate limit exceeded, please try again later",
            ):
                await client._make_request("GET", "/cards")

    @pytest.mark.asyncio
    async def test_make_request_500_error(self, client):
        """Test server error handling."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_request.return_value = mock_response

            with pytest.raises(MTGAPIServerError, match="MTG API service unavailable"):
                await client._make_request("GET", "/cards")

    @pytest.mark.asyncio
    async def test_make_request_retry_logic(self, client):
        """Test retry logic for transient failures."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            # First call fails with 500, second succeeds
            mock_response_fail = MagicMock()
            mock_response_fail.status_code = 500
            mock_response_fail.text = "Server Error"

            mock_response_success = MagicMock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = {"cards": []}

            mock_request.side_effect = [mock_response_fail, mock_response_success]

            result = await client._make_request("GET", "/cards")

            assert result == {"cards": []}
            assert mock_request.call_count == 2

    # Note: Data conversion tests moved to test_data_converters.py
    # These methods are now utility functions, not client methods
