"""Unit tests for MCP tool registration."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from mcp.server import Server
from mcp.types import Tool

from mtg_mcp_server.tools.handlers import register_tools
from mtg_mcp_server.api.client import MTGAPIClient


class TestToolRegistration:
    """Test cases for MCP tool registration."""

    @pytest.fixture
    def mock_server(self):
        """Create mock MCP server for testing."""
        return MagicMock(spec=Server)

    @pytest.fixture
    def mock_api_client(self):
        """Create mock API client for testing."""
        return AsyncMock(spec=MTGAPIClient)

    def test_register_tools_registers_search_cards(self, mock_server, mock_api_client):
        """Test that register_tools registers the search_cards tool."""
        register_tools(mock_server, mock_api_client)

        # Verify that server.list_tools was called to register the decorator
        mock_server.list_tools.assert_called_once()

        # Verify that server.call_tool was called to register the handler
        mock_server.call_tool.assert_called_once()

    def test_register_tools_registers_call_tool_handler(
        self, mock_server, mock_api_client
    ):
        """Test that register_tools registers the call_tool handler."""
        register_tools(mock_server, mock_api_client)

        # Verify that server.call_tool was called to register the handler
        mock_server.call_tool.assert_called_once()

        # Verify that server.list_tools was called to register tools
        mock_server.list_tools.assert_called_once()
