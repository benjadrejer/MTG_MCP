"""MCP tool handlers for MTG API functionality."""

from typing import List, Dict, Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from mtg_mcp_server.api.client import MTGAPIClient
from mtg_mcp_server.models.card import Card


async def search_cards_handler(
    api_client: MTGAPIClient, arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle search_cards MCP tool requests.

    Args:
        api_client: MTG API client instance
        arguments: Tool arguments containing name and optional limit

    Returns:
        List containing a single TextContent with formatted search results

    Raises:
        ValueError: If required parameters are missing or invalid
        MTGValidationError: If API client validation fails
        MTGAPIError: If API request fails
    """
    # Validate required parameters
    if "name" not in arguments:
        raise ValueError("name parameter is required")

    name = arguments["name"]
    if not name or not name.strip():
        raise ValueError("name parameter cannot be empty")

    # Validate optional limit parameter
    limit = arguments.get("limit", 10)
    if not isinstance(limit, int):
        raise ValueError("limit parameter must be an integer")

    # Search for cards using the API client
    cards = await api_client.search_cards(name, limit)

    # Format the results
    if not cards:
        content = f"No cards found matching '{name}'"
        return [TextContent(type="text", text=content)]

    # Build formatted response
    result_lines = [f"Found {len(cards)} cards matching '{name}':\n"]

    for i, card in enumerate(cards, 1):
        result_lines.append(f"{i}. **{card.name}**")

        # Add mana cost if available
        if card.mana_cost:
            result_lines.append(f"   Mana Cost: {card.mana_cost}")

        # Add type
        if card.type:
            result_lines.append(f"   Type: {card.type}")

        # Add power/toughness for creatures
        if card.power is not None and card.toughness is not None:
            result_lines.append(f"   Power/Toughness: {card.power}/{card.toughness}")

        # Add loyalty for planeswalkers
        if card.loyalty is not None:
            result_lines.append(f"   Loyalty: {card.loyalty}")

        # Add text if available
        if card.text:
            result_lines.append(f"   Text: {card.text}")

        # Add set information
        if card.set_name:
            set_info = card.set_name
            if card.set_code:
                set_info += f" ({card.set_code})"
            result_lines.append(f"   Set: {set_info}")

        # Add rarity
        if card.rarity:
            result_lines.append(f"   Rarity: {card.rarity}")

        result_lines.append("")  # Empty line between cards

    content = "\n".join(result_lines).strip()
    return [TextContent(type="text", text=content)]


async def filter_cards_handler(
    api_client: MTGAPIClient, arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle filter_cards MCP tool requests.

    Args:
        api_client: MTG API client instance
        arguments: Tool arguments containing filter criteria and optional limit

    Returns:
        List containing a single TextContent with formatted filter results

    Raises:
        ValueError: If parameters are invalid
        MTGValidationError: If API client validation fails
        MTGAPIError: If API request fails
    """
    # Validate optional limit parameter
    limit = arguments.get("limit", 20)
    if not isinstance(limit, int):
        raise ValueError("limit parameter must be an integer")

    # Extract filter parameters (remove limit from filters)
    filters = {k: v for k, v in arguments.items() if k != "limit"}

    # Filter cards using the API client
    cards = await api_client.filter_cards(limit=limit, **filters)

    # Format the results
    if not cards:
        content = "No cards found matching the specified filters"
        return [TextContent(type="text", text=content)]

    # Build formatted response
    result_lines = [f"Found {len(cards)} cards matching the specified filters:\n"]

    for i, card in enumerate(cards, 1):
        result_lines.append(f"{i}. **{card.name}**")

        # Add mana cost if available
        if card.mana_cost:
            result_lines.append(f"   Mana Cost: {card.mana_cost}")

        # Add type
        if card.type:
            result_lines.append(f"   Type: {card.type}")

        # Add colors if available
        if card.colors:
            result_lines.append(f"   Colors: {', '.join(card.colors)}")

        # Add power/toughness for creatures
        if card.power is not None and card.toughness is not None:
            result_lines.append(f"   Power/Toughness: {card.power}/{card.toughness}")

        # Add loyalty for planeswalkers
        if card.loyalty is not None:
            result_lines.append(f"   Loyalty: {card.loyalty}")

        # Add text if available
        if card.text:
            result_lines.append(f"   Text: {card.text}")

        # Add set information
        if card.set_name:
            set_info = card.set_name
            if card.set_code:
                set_info += f" ({card.set_code})"
            result_lines.append(f"   Set: {set_info}")

        # Add rarity
        if card.rarity:
            result_lines.append(f"   Rarity: {card.rarity}")

        result_lines.append("")  # Empty line between cards

    content = "\n".join(result_lines).strip()
    return [TextContent(type="text", text=content)]


async def get_card_details_handler(
    api_client: MTGAPIClient, arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle get_card_details MCP tool requests.

    Args:
        api_client: MTG API client instance
        arguments: Tool arguments containing card_id

    Returns:
        List containing a single TextContent with detailed card information

    Raises:
        ValueError: If required parameters are missing or invalid
        MTGValidationError: If API client validation fails
        MTGAPIError: If API request fails
        MTGAPINotFoundError: If card is not found
    """
    # Validate required parameters
    if "card_id" not in arguments:
        raise ValueError("card_id parameter is required")

    card_id = arguments["card_id"]
    if not card_id or not card_id.strip():
        raise ValueError("card_id parameter cannot be empty")

    # Get card details using the API client
    card = await api_client.get_card(card_id)

    # Build detailed formatted response
    result_lines = [f"**{card.name}**\n"]

    # Add ID
    result_lines.append(f"ID: {card.id}")

    # Add mana cost if available
    if card.mana_cost:
        result_lines.append(f"Mana Cost: {card.mana_cost}")

    # Add converted mana cost if available
    if card.cmc is not None:
        result_lines.append(f"Converted Mana Cost: {card.cmc}")

    # Add colors if available
    if card.colors:
        result_lines.append(f"Colors: {', '.join(card.colors)}")

    # Add color identity if available
    if card.color_identity:
        result_lines.append(f"Color Identity: {', '.join(card.color_identity)}")

    # Add type
    if card.type:
        result_lines.append(f"Type: {card.type}")

    # Add supertypes if available
    if card.supertypes:
        result_lines.append(f"Supertypes: {', '.join(card.supertypes)}")

    # Add types if available
    if card.types:
        result_lines.append(f"Types: {', '.join(card.types)}")

    # Add subtypes if available
    if card.subtypes:
        result_lines.append(f"Subtypes: {', '.join(card.subtypes)}")

    # Add power/toughness for creatures
    if card.power is not None and card.toughness is not None:
        result_lines.append(f"Power/Toughness: {card.power}/{card.toughness}")

    # Add loyalty for planeswalkers
    if card.loyalty is not None:
        result_lines.append(f"Loyalty: {card.loyalty}")

    # Add text if available
    if card.text:
        result_lines.append(f"Text: {card.text}")

    # Add set information
    if card.set_name:
        set_info = card.set_name
        if card.set_code:
            set_info += f" ({card.set_code})"
        result_lines.append(f"Set: {set_info}")

    # Add rarity
    if card.rarity:
        result_lines.append(f"Rarity: {card.rarity}")

    # Add image URL if available
    if card.image_url:
        result_lines.append(f"Image URL: {card.image_url}")

    content = "\n".join(result_lines)
    return [TextContent(type="text", text=content)]


def register_tools(server: Server, api_client: MTGAPIClient) -> None:
    """Register all MCP tools with the server.

    Args:
        server: MCP server instance
        api_client: MTG API client instance
    """
    # Define the search_cards tool
    search_cards_tool = Tool(
        name="search_cards",
        description="Search for Magic the Gathering cards by name with partial matching support",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Card name or partial name to search for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 10, max: 50)",
                    "minimum": 1,
                    "maximum": 50,
                    "default": 10,
                },
            },
            "required": ["name"],
        },
    )

    # Define the filter_cards tool
    filter_cards_tool = Tool(
        name="filter_cards",
        description="Filter Magic the Gathering cards by various attributes like color, type, mana cost, etc.",
        inputSchema={
            "type": "object",
            "properties": {
                "colors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of color identifiers (Red, Blue, Green, White, Black)",
                },
                "type": {
                    "type": "string",
                    "description": "Card type (creature, instant, sorcery, etc.)",
                },
                "cmc": {
                    "type": "integer",
                    "description": "Converted mana cost",
                    "minimum": 0,
                },
                "set": {
                    "type": "string",
                    "description": "Set code (e.g., LEA, M10, etc.)",
                },
                "rarity": {
                    "type": "string",
                    "description": "Card rarity (Common, Uncommon, Rare, Mythic Rare)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 20, max: 100)",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 20,
                },
            },
            "required": [],
        },
    )

    # Define the get_card_details tool
    get_card_details_tool = Tool(
        name="get_card_details",
        description="Get detailed information for a specific Magic the Gathering card by ID",
        inputSchema={
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "MTG API card ID",
                },
            },
            "required": ["card_id"],
        },
    )

    # Register the tools with the server
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available MCP tools."""
        return [search_cards_tool, filter_cards_tool, get_card_details_tool]

    # Register the tool call handler
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle MCP tool calls."""
        if name == "search_cards":
            return await search_cards_handler(api_client, arguments)
        elif name == "filter_cards":
            return await filter_cards_handler(api_client, arguments)
        elif name == "get_card_details":
            return await get_card_details_handler(api_client, arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
