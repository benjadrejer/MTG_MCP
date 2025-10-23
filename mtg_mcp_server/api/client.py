"""MTG API client for interacting with the Magic the Gathering API."""

import asyncio
import logging
from typing import List, Optional, Dict, Any

import httpx
from asyncio_throttle import Throttler

from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.set import Set
from mtg_mcp_server.models.exceptions import (
    MTGAPIError,
    MTGAPIConnectionError,
    MTGAPITimeoutError,
    MTGAPIRateLimitError,
    MTGAPINotFoundError,
    MTGAPIServerError,
)
from mtg_mcp_server.utils.data_converters import convert_card_data, convert_set_data
from mtg_mcp_server.utils.validators import (
    validate_card_name,
    validate_card_id,
    validate_search_limit,
    validate_filter_limit,
    validate_random_count,
)
from mtg_mcp_server.utils.param_processors import (
    build_search_params,
    build_filter_params,
    build_random_params,
)

logger = logging.getLogger(__name__)


class MTGAPIClient:
    """MTG API client for interacting with the Magic the Gathering API."""

    def __init__(self, base_url: str = "https://api.magicthegathering.io/v1"):
        """Initialize the MTG API client."""
        self.base_url = base_url
        self.timeout = 30.0
        self._session: Optional[httpx.AsyncClient] = None
        self._throttler = Throttler(rate_limit=10, period=1.0)  # 10 requests per second

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session."""
        if self._session is None:
            self._session = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={"User-Agent": "MTG-MCP-Server/1.0"},
            )
        return self._session

    async def _make_request(
        self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to MTG API with error handling and retry logic."""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()

        logger.debug(f"Making {method} request to {url} with params: {params}")

        # Rate limiting
        async with self._throttler:
            for attempt in range(3):  # Retry up to 3 times
                try:
                    response = await session.request(method, url, params=params)

                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 404:
                        raise MTGAPINotFoundError("Resource not found")
                    elif response.status_code == 429:
                        raise MTGAPIRateLimitError(
                            "Rate limit exceeded, please try again later"
                        )
                    elif response.status_code >= 500:
                        if attempt < 2:  # Retry on server errors
                            await asyncio.sleep(2**attempt)  # Exponential backoff
                            continue
                        raise MTGAPIServerError(
                            "MTG API service unavailable", response.status_code
                        )
                    else:
                        raise MTGAPIError(
                            f"API request failed: {response.status_code}",
                            response.status_code,
                        )

                except httpx.TimeoutException:
                    raise MTGAPITimeoutError("MTG API request timed out")
                except httpx.ConnectError:
                    raise MTGAPIConnectionError("Unable to connect to MTG API")
                except (
                    MTGAPINotFoundError,
                    MTGAPIRateLimitError,
                    MTGAPITimeoutError,
                    MTGAPIConnectionError,
                    MTGAPIServerError,
                ):
                    # Don't retry these errors
                    raise
                except Exception as e:
                    if attempt < 2:
                        await asyncio.sleep(2**attempt)
                        continue
                    raise MTGAPIError(f"Unexpected error: {str(e)}")

    async def search_cards(self, name: str, limit: int = 10) -> List[Card]:
        """Search for cards by name with partial matching."""
        validate_card_name(name)
        validate_search_limit(limit)

        params = build_search_params(name, limit)
        response = await self._make_request("GET", "/cards", params)

        cards = []
        for card_data in response.get("cards", []):
            cards.append(convert_card_data(card_data))

        return cards

    async def get_card(self, card_id: str) -> Card:
        """Get a specific card by ID."""
        validate_card_id(card_id)

        response = await self._make_request("GET", f"/cards/{card_id}")
        card_data = response.get("card")

        if not card_data:
            raise MTGAPINotFoundError(f"Card with ID {card_id} not found")

        return convert_card_data(card_data)

    async def filter_cards(self, **filters) -> List[Card]:
        """Filter cards by various attributes."""
        limit = filters.pop("limit", 20)
        validate_filter_limit(limit)

        params = build_filter_params(filters, limit)
        response = await self._make_request("GET", "/cards", params)

        cards = []
        for card_data in response.get("cards", []):
            cards.append(convert_card_data(card_data))

        return cards

    async def get_sets(self, set_code: Optional[str] = None) -> List[Set]:
        """Get MTG sets, optionally filtered by set code."""
        if set_code:
            response = await self._make_request("GET", f"/sets/{set_code}")
            set_data = response.get("set")

            if not set_data:
                raise MTGAPINotFoundError(f"Set with code {set_code} not found")

            return [convert_set_data(set_data)]
        else:
            response = await self._make_request("GET", "/sets")

            sets = []
            for set_data in response.get("sets", []):
                sets.append(convert_set_data(set_data))

            return sets

    async def get_random_cards(self, count: int = 1) -> List[Card]:
        """Get random MTG cards for discovery."""
        validate_random_count(count)

        params = build_random_params(count)
        response = await self._make_request("GET", "/cards", params)

        cards = []
        for card_data in response.get("cards", []):
            cards.append(convert_card_data(card_data))

        return cards

    async def close(self):
        """Close the HTTP session."""
        if self._session:
            await self._session.aclose()
            self._session = None
