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

    # Register the tool with the server
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available MCP tools."""
        return [search_cards_tool]

    # Register the tool call handler
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle MCP tool calls."""
        if name == "search_cards":
            return await search_cards_handler(api_client, arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
