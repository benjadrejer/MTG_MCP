"""Main entry point for the MTG MCP Server."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server

from mtg_mcp_server.api.client import MTGAPIClient
from mtg_mcp_server.tools.handlers import register_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for the MTG MCP Server."""
    logger.info("Starting MTG MCP Server...")

    # Initialize the MCP server
    server = Server("mtg-mcp-server")

    # Initialize the MTG API client
    api_client = MTGAPIClient()

    # Register all MCP tools
    register_tools(server, api_client)

    logger.info("MTG MCP Server initialized successfully")

    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def cli_main() -> None:
    """CLI entry point."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MTG MCP Server stopped by user")
    except Exception as e:
        logger.error(f"MTG MCP Server failed: {e}")
        raise


if __name__ == "__main__":
    cli_main()
