# MTG MCP Server

A Model Context Protocol (MCP) server that provides tools to interact with the Magic the Gathering API.

## Features

- Search for MTG cards by name with partial matching
- Filter cards by various attributes (color, type, mana cost, etc.)
- Retrieve detailed card information
- Get information about MTG sets
- Discover random cards

## Installation

### Development Setup

1. Create and activate a virtual environment:

```bash
python -m venv mtg-mcp-env
source mtg-mcp-env/bin/activate  # On Windows: mtg-mcp-env\Scripts\activate
```

2. Install the package in development mode:

```bash
pip install -e ".[dev]"
```

## Usage

### As an MCP Server

The server can be used with any MCP-compatible client. Add the following to your MCP client configuration:

```json
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "mtg-mcp-server",
      "args": []
    }
  }
}
```

### Available Tools

- `search_cards`: Search for cards by name
- `get_card_details`: Get detailed information for a specific card
- `filter_cards`: Filter cards by attributes
- `get_sets`: Retrieve MTG set information
- `get_random_cards`: Get random cards for discovery

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black mtg_mcp_server tests
isort mtg_mcp_server tests
```

### Type Checking

```bash
mypy mtg_mcp_server
```

## License

MIT License
